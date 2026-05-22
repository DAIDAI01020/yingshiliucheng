#!/usr/bin/env node
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const DEFAULT_BASE_URL = "https://api.legnext.ai";
const SUCCESS_STATUSES = new Set(["success", "succeeded", "completed", "complete", "done"]);
const FAILED_STATUSES = new Set(["failure", "failed", "error", "canceled", "cancelled"]);

function parseArgs(argv) {
  const raw = argv.slice(2);
  if (!raw.length || raw[0] === "--help" || raw[0] === "-h") return { command: "help" };
  const command = ["doctor", "dry-run", "run"].includes(raw[0]) ? raw.shift() : "run";
  const args = { command, promptParts: [] };
  for (let i = 0; i < raw.length; i += 1) {
    const arg = raw[i];
    if (arg === "--prompt") args.prompt = raw[++i];
    else if (arg === "--prompt-file") args.promptFile = raw[++i];
    else if (arg === "--api-key") args.apiKey = raw[++i];
    else if (arg === "--base-url") args.baseUrl = raw[++i];
    else if (arg === "--callback") args.callback = raw[++i];
    else if (arg === "--poll-interval") args.pollInterval = Number(raw[++i]);
    else if (arg === "--timeout") args.timeout = Number(raw[++i]);
    else if (arg === "--download-dir") args.downloadDir = raw[++i];
    else if (arg === "--no-poll") args.noPoll = true;
    else if (arg === "--no-download") args.noDownload = true;
    else if (arg === "--help" || arg === "-h") args.help = true;
    else args.promptParts.push(arg);
  }
  return {
    ...args,
    baseUrl: (args.baseUrl || process.env.LEGNEXT_BASE_URL || DEFAULT_BASE_URL).replace(/\/+$/, ""),
    callback: args.callback || process.env.LEGNEXT_CALLBACK_URL || "",
    pollInterval: Number.isFinite(args.pollInterval) ? args.pollInterval : 3,
    timeout: Number.isFinite(args.timeout) ? args.timeout : 300,
    downloadDir: path.resolve(expandHome(args.downloadDir || process.env.MIDJOURNEY_DOWNLOAD_DIR || path.join(os.homedir(), ".codex", "generated_images", "midjourney"))),
  };
}

function help() {
  return `Midjourney Legnext runner

Commands:
  doctor
  dry-run "prompt --ar 16:9 --v 7"
  run "prompt --ar 16:9 --v 7"

Options:
  --prompt TEXT
  --prompt-file PATH
  --base-url URL          Default: ${DEFAULT_BASE_URL}
  --callback URL          Optional Legnext callback URL
  --download-dir DIR      Default: ~/.codex/generated_images/midjourney
  --no-poll              Submit only
  --no-download          Keep remote URLs only
  --timeout SECONDS      Default: 300
`;
}

function expandHome(value) {
  if (!value) return value;
  if (value === "~") return os.homedir();
  if (value.startsWith("~/") || value.startsWith("~\\")) return path.join(os.homedir(), value.slice(2));
  return value;
}

function apiKey(args) {
  return String(args.apiKey || process.env.LEGNEXT_API_KEY || "").trim();
}

function redact(text, key) {
  return key ? String(text).replaceAll(key, "<redacted>") : String(text);
}

function readPrompt(args) {
  if (args.prompt) return String(args.prompt).trim();
  if (args.promptFile) {
    const filePath = path.resolve(args.promptFile);
    if (!fs.existsSync(filePath)) throw new Error(`prompt file does not exist: ${filePath}`);
    return fs.readFileSync(filePath, "utf8").trim();
  }
  const joined = (args.promptParts || []).join(" ").trim();
  if (joined) return joined;
  throw new Error("prompt is required. Pass a positional prompt, --prompt, or --prompt-file.");
}

async function requestJson(method, url, key, payload) {
  const headers = {
    Accept: "application/json",
    "User-Agent": "codex-midjourney-runner/1.0",
    "x-api-key": key,
  };
  if (payload) headers["Content-Type"] = "application/json";
  const response = await fetch(url, {
    method,
    headers,
    body: payload ? JSON.stringify(payload) : undefined,
  });
  const text = await response.text();
  if (!response.ok) {
    if (response.status === 401 || response.status === 403) throw new Error("Legnext authentication failed. Check LEGNEXT_API_KEY.");
    if (response.status === 402) throw new Error("Legnext account has insufficient balance or plan access.");
    if (response.status === 429) throw new Error("Legnext rate limit hit. Retry later.");
    throw new Error(`HTTP ${response.status} from ${url}: ${redact(text, key).slice(0, 1000)}`);
  }
  return text ? JSON.parse(text) : {};
}

function extractJobId(data) {
  for (const key of ["job_id", "jobId", "id", "result", "taskId"]) {
    if (typeof data?.[key] === "string" && data[key].trim()) return data[key].trim();
  }
  if (data?.data && typeof data.data === "object") return extractJobId(data.data);
  return "";
}

function extractStatus(data) {
  for (const key of ["status", "state"]) {
    if (typeof data?.[key] === "string" && data[key].trim()) return data[key].trim().toLowerCase();
  }
  if (data?.data && typeof data.data === "object") return extractStatus(data.data);
  return "";
}

function collectImageUrls(value, urls = []) {
  if (!value) return urls;
  if (typeof value === "string") {
    if (/^https?:\/\//i.test(value)) urls.push(value);
    return urls;
  }
  if (Array.isArray(value)) {
    for (const item of value) collectImageUrls(item, urls);
    return [...new Set(urls)];
  }
  if (typeof value === "object") {
    const outputImageUrls = value.output?.image_urls;
    if (Array.isArray(outputImageUrls) && outputImageUrls.length) return collectImageUrls(outputImageUrls, urls);
    for (const key of ["imageUrl", "image_url", "url", "uri", "proxy_url", "images", "imageUrls", "output", "outputs", "result", "data"]) {
      collectImageUrls(value[key], urls);
    }
  }
  return [...new Set(urls)];
}

function extractError(data) {
  for (const key of ["failReason", "error", "message", "msg"]) {
    const value = data?.[key];
    if (typeof value === "string" && value.trim()) return value.trim();
    if (value && typeof value === "object") {
      const nested = extractError(value);
      if (nested) return nested;
    }
  }
  if (data?.data && typeof data.data === "object") return extractError(data.data);
  return "";
}

function safeStem(prompt, jobId) {
  const digest = crypto.createHash("sha1").update(prompt, "utf8").digest("hex").slice(0, 10);
  const shortJob = String(jobId || "job").replace(/[^a-z0-9]/gi, "").slice(0, 8) || "job";
  return `midjourney-${shortJob}-${digest}`;
}

async function downloadFile(url, outputPath) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`download failed: HTTP ${response.status}`);
  const buffer = Buffer.from(await response.arrayBuffer());
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, buffer);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function printEvent(label, value) {
  console.log(`${label}: ${JSON.stringify(value)}`);
}

async function doctor(args) {
  const key = apiKey(args);
  console.log(JSON.stringify({
    baseUrl: args.baseUrl,
    LEGNEXT_API_KEY: key ? `present:${key.length}chars` : "missing",
    downloadDir: args.downloadDir,
    ok: Boolean(key),
    problems: key ? [] : ["LEGNEXT_API_KEY is missing."],
  }, null, 2));
}

async function dryRun(args) {
  const prompt = readPrompt(args);
  const key = apiKey(args);
  console.log(JSON.stringify({
    method: "POST",
    url: `${args.baseUrl}/api/v1/diffusion`,
    headers: {
      "x-api-key": key ? "<LEGNEXT_API_KEY:redacted>" : "<missing>",
      "Content-Type": "application/json",
    },
    payload: {
      text: prompt,
      ...(args.callback ? { callback: args.callback } : {}),
    },
  }, null, 2));
}

async function run(args) {
  const key = apiKey(args);
  if (!key) throw new Error("LEGNEXT_API_KEY is required. Set it in the environment before real Midjourney generation.");
  const prompt = readPrompt(args);
  const payload = { text: prompt };
  if (args.callback) payload.callback = args.callback;

  const submitted = await requestJson("POST", `${args.baseUrl}/api/v1/diffusion`, key, payload);
  const jobId = extractJobId(submitted);
  if (!jobId) throw new Error(`Legnext accepted no job id: ${JSON.stringify(submitted)}`);
  printEvent("submitted", { jobId });
  if (args.noPoll) return;

  const deadline = Date.now() + args.timeout * 1000;
  let lastStatus = "";
  while (Date.now() < deadline) {
    const data = await requestJson("GET", `${args.baseUrl}/api/v1/job/${encodeURIComponent(jobId)}`, key);
    const nested = data?.data && typeof data.data === "object" ? data.data : {};
    const status = extractStatus(data);
    const progress = data.progress ?? nested.progress;
    const message = data.message ?? data.msg ?? nested.message ?? nested.msg;
    const statusKey = JSON.stringify({ status, progress, message });
    if (statusKey !== lastStatus) {
      printEvent("status", { status, progress, message });
      lastStatus = statusKey;
    }

    if (SUCCESS_STATUSES.has(status)) {
      const imageUrls = collectImageUrls(data);
      if (!imageUrls.length) throw new Error(`Job ${jobId} succeeded but no image URL was found.`);
      const localPaths = [];
      if (!args.noDownload) {
        const stem = safeStem(prompt, jobId);
        for (let index = 0; index < imageUrls.length; index += 1) {
          const parsed = new URL(imageUrls[index]);
          const ext = path.extname(parsed.pathname) || ".png";
          const outputPath = path.join(args.downloadDir, `${stem}-${index}${ext}`);
          await downloadFile(imageUrls[index], outputPath);
          localPaths.push(outputPath);
        }
      }
      printEvent("completed", { jobId, imageUrls, localPaths, rawStatus: status, prompt });
      return;
    }

    if (FAILED_STATUSES.has(status)) {
      throw new Error(`Midjourney job ${jobId} failed: ${extractError(data) || "unknown error"}`);
    }

    await sleep(args.pollInterval * 1000);
  }
  throw new Error(`Timed out waiting for Midjourney job ${jobId}`);
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.command === "help" || args.help) return console.log(help());
  if (args.command === "doctor") return doctor(args);
  if (args.command === "dry-run") return dryRun(args);
  if (args.command === "run") return run(args);
  throw new Error(`Unknown command: ${args.command}`);
}

main().catch((error) => {
  console.error(`error: ${error instanceof Error ? error.message : String(error)}`);
  process.exit(1);
});
