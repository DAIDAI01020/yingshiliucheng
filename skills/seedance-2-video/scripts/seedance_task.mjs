#!/usr/bin/env node
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com";
const DEFAULT_MODEL = "doubao-seedance-2-0-260128";
const DEFAULT_RATIO = "9:16";
const DEFAULT_DURATION = 15;
const DEFAULT_RESOLUTION = "720p";
const DEFAULT_SEED = -1;
const DEFAULT_TIMEOUT_SECONDS = 21600;
const DEFAULT_SECRET_FILE = path.join(os.homedir(), ".config", "codex-seedance-2-video", "secrets.json");
const VALID_RATIOS = new Set(["21:9", "16:9", "4:3", "1:1", "3:4", "9:16", "adaptive"]);
const VALID_RESOLUTIONS = new Set(["480p", "720p", "1080p"]);

class SeedanceError extends Error {}

function parseArgs(argv) {
  const args = { imageUrl: [] };
  const rest = argv.slice(2);
  if (rest[0] === "--help" || rest[0] === "-h") return withDefaults({ command: "help", help: true });
  args.command = rest.shift();
  for (let i = 0; i < rest.length; i += 1) {
    const arg = rest[i];
    if (arg === "--image-url") args.imageUrl.push(rest[++i]);
    else if (arg === "--prompt") args.prompt = rest[++i];
    else if (arg === "--prompt-file") args.promptFile = rest[++i];
    else if (arg === "--output-dir") args.outputDir = rest[++i];
    else if (arg === "--task-id") args.taskId = rest[++i];
    else if (arg === "--api-base-url") args.apiBaseUrl = rest[++i];
    else if (arg === "--key-file") args.keyFile = rest[++i];
    else if (arg === "--model") args.model = rest[++i];
    else if (arg === "--ratio") args.ratio = rest[++i];
    else if (arg === "--duration") args.duration = Number(rest[++i]);
    else if (arg === "--resolution") args.resolution = rest[++i];
    else if (arg === "--seed") args.seed = Number(rest[++i]);
    else if (arg === "--video-mode") args.videoMode = rest[++i];
    else if (arg === "--timeout-seconds") args.timeoutSeconds = Number(rest[++i]);
    else if (arg === "--poll-min-seconds") args.pollMinSeconds = Number(rest[++i]);
    else if (arg === "--poll-mid-seconds") args.pollMidSeconds = Number(rest[++i]);
    else if (arg === "--poll-max-seconds") args.pollMaxSeconds = Number(rest[++i]);
    else if (arg === "--output-name") args.outputName = rest[++i];
    else if (arg === "--submit-only") args.submitOnly = true;
    else if (arg === "--watermark") args.watermark = true;
    else if (arg === "--help" || arg === "-h") args.help = true;
    else throw new SeedanceError(`Unknown argument: ${arg}`);
  }
  return withDefaults(args);
}

function withDefaults(args) {
  return {
    ...args,
    apiBaseUrl: (args.apiBaseUrl || process.env.ARK_BASE_URL || DEFAULT_BASE_URL).replace(/\/+$/, ""),
    keyFile: expandHome(args.keyFile || process.env.SEEDANCE_ARK_KEY_FILE || process.env.ARK_KEY_FILE || DEFAULT_SECRET_FILE),
    model: args.model || DEFAULT_MODEL,
    ratio: args.ratio || DEFAULT_RATIO,
    duration: Number.isFinite(args.duration) ? args.duration : DEFAULT_DURATION,
    resolution: args.resolution || DEFAULT_RESOLUTION,
    seed: Number.isFinite(args.seed) ? args.seed : DEFAULT_SEED,
    videoMode: args.videoMode || "reference",
    timeoutSeconds: Number.isFinite(args.timeoutSeconds) ? args.timeoutSeconds : DEFAULT_TIMEOUT_SECONDS,
    pollMinSeconds: Number.isFinite(args.pollMinSeconds) ? args.pollMinSeconds : 15,
    pollMidSeconds: Number.isFinite(args.pollMidSeconds) ? args.pollMidSeconds : 45,
    pollMaxSeconds: Number.isFinite(args.pollMaxSeconds) ? args.pollMaxSeconds : 120,
    outputName: args.outputName || "final.mp4",
  };
}

function help() {
  return `Seedance 2.0 Ark runner

Commands:
  doctor [--image-url URL] [--output-dir DIR]
  dry-run --prompt "text" --image-url URL
  dry-run --prompt-file video_prompt.txt --image-url URL
  run --prompt-file video_prompt.txt --image-url URL --output-dir outputs/seedance-demo
  poll --output-dir outputs/seedance-demo [--task-id TASK_ID]

Common options:
  --ratio 9:16|16:9|1:1|...   Default: 9:16
  --duration 4-15|-1           Default: 15
  --resolution 480p|720p|1080p Default: 720p
  --video-mode reference|firstFrame|firstLastFrame
  --api-base-url URL           Default: ${DEFAULT_BASE_URL}
`;
}

function expandHome(value) {
  if (!value) return value;
  return value.startsWith("~/") || value === "~" ? path.join(os.homedir(), value.slice(2)) : value;
}

function isHttpUrl(value) {
  return typeof value === "string" && /^https?:\/\//i.test(value);
}

function nowIso() {
  return new Date().toISOString();
}

function sha256(value) {
  return crypto.createHash("sha256").update(value, "utf8").digest("hex");
}

function readJson(filePath) {
  if (!filePath || !fs.existsSync(filePath)) return {};
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function writeJson(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function manifestPath(outputDir) {
  return path.join(outputDir, "run_manifest.json");
}

function readApiKey(args) {
  const envKey = String(process.env.ARK_API_KEY || "").trim();
  if (envKey) return { apiKey: envKey, source: "env:ARK_API_KEY" };
  const data = readJson(args.keyFile);
  const fileKey = String(data.ark_api_key || data.ARK_API_KEY || "").trim();
  if (fileKey) return { apiKey: fileKey, source: "local_secret_file" };
  throw new SeedanceError("ARK_API_KEY is not configured. Set ARK_API_KEY or provide a local key file.");
}

function keyState(args) {
  const envKey = String(process.env.ARK_API_KEY || "").trim();
  if (envKey) return { state: `present:${envKey.length}chars`, source: "env:ARK_API_KEY" };
  const data = readJson(args.keyFile);
  const fileKey = String(data.ark_api_key || data.ARK_API_KEY || "").trim();
  if (fileKey) return { state: `present:${fileKey.length}chars`, source: "local_secret_file" };
  return { state: "missing", source: "missing" };
}

function readPrompt(args) {
  if (args.prompt) return { prompt: String(args.prompt).trim(), source: "inline" };
  if (args.promptFile) {
    const filePath = path.resolve(args.promptFile);
    if (!fs.existsSync(filePath)) throw new SeedanceError(`prompt file does not exist: ${filePath}`);
    return { prompt: fs.readFileSync(filePath, "utf8").trim(), source: filePath };
  }
  throw new SeedanceError("Provide --prompt or --prompt-file.");
}

function validateGenerationArgs(args) {
  if (!VALID_RATIOS.has(args.ratio)) throw new SeedanceError(`ratio must be one of ${[...VALID_RATIOS].join(", ")}`);
  if (!VALID_RESOLUTIONS.has(args.resolution)) throw new SeedanceError(`resolution must be one of ${[...VALID_RESOLUTIONS].join(", ")}`);
  if (args.duration !== -1 && (!Number.isInteger(args.duration) || args.duration < 4 || args.duration > 15)) {
    throw new SeedanceError("duration must be -1 or an integer from 4 to 15");
  }
}

function validateImageUrls(urls) {
  const clean = (urls || []).map((url) => String(url || "").trim()).filter(Boolean);
  if (!clean.length) throw new SeedanceError("Provide at least one --image-url.");
  if (clean.length > 9) throw new SeedanceError("Seedance supports at most 9 image URLs.");
  for (const url of clean) {
    if (!isHttpUrl(url)) throw new SeedanceError(`Seedance direct Ark input must be a public http(s) URL, got: ${url}`);
  }
  return clean;
}

function imageContent(imageUrls, videoMode) {
  if (videoMode === "firstFrame") {
    return [{ type: "image_url", image_url: { url: imageUrls[0] }, role: "first_frame" }];
  }
  if (videoMode === "firstLastFrame") {
    if (imageUrls.length < 2) throw new SeedanceError("video-mode firstLastFrame requires at least 2 image URLs.");
    return [
      { type: "image_url", image_url: { url: imageUrls[0] }, role: "first_frame" },
      { type: "image_url", image_url: { url: imageUrls[1] }, role: "last_frame" },
    ];
  }
  return imageUrls.map((url) => ({ type: "image_url", image_url: { url }, role: "reference_image" }));
}

function buildPayload(prompt, imageUrls, args) {
  validateGenerationArgs(args);
  return {
    model: args.model,
    content: [{ type: "text", text: prompt }, ...imageContent(imageUrls, args.videoMode)],
    ratio: args.ratio,
    duration: args.duration,
    resolution: args.resolution,
    watermark: Boolean(args.watermark),
    seed: args.seed,
  };
}

async function httpJson(method, url, apiKey, payload) {
  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json",
      Authorization: `Bearer ${apiKey}`,
      ...(payload ? { "Content-Type": "application/json" } : {}),
    },
    body: payload ? JSON.stringify(payload) : undefined,
  });
  const text = await response.text();
  if (!response.ok) {
    throw new SeedanceError(`${method} ${url} failed: HTTP ${response.status}: ${text.replaceAll(apiKey, "<redacted>").slice(0, 500)}`);
  }
  return text ? JSON.parse(text) : {};
}

function getByPath(obj, pathExpr) {
  let current = obj;
  for (const part of pathExpr.replace(/\[/g, ".").replace(/\]/g, "").split(".")) {
    if (!part) continue;
    if (current == null) return undefined;
    current = Array.isArray(current) && /^\d+$/.test(part) ? current[Number(part)] : current[part];
  }
  return current;
}

function firstString(data, paths) {
  for (const p of paths) {
    const value = getByPath(data, p);
    if (typeof value === "string" && value.trim()) return value.trim();
  }
  return "";
}

function extractTaskId(data) {
  return firstString(data, ["id", "task_id", "data.task_id", "data.id", "data[0].task_id"]);
}

function extractStatus(data) {
  return firstString(data, ["status", "data.status", "data[0].status"]) || "processing";
}

function normalizeStatus(value) {
  const status = String(value || "").toLowerCase();
  if (status.includes("success") || status.includes("complete") || status.includes("succeed")) return "succeeded";
  if (status.includes("fail") || status.includes("error") || status.includes("expired")) return "failed";
  if (status.includes("cancel")) return "canceled";
  if (status.includes("queue") || status.includes("submit") || status.includes("pending") || status.includes("start")) return "queued";
  return "processing";
}

function extractResultUrl(data) {
  return firstString(data, [
    "content.video_url",
    "content.url",
    "content.output_url",
    "video_url",
    "output",
    "output.url",
    "result_url",
    "url",
    "data.content.video_url",
    "data.video_url",
    "data.output",
    "data.result_url",
  ]);
}

function extractError(data) {
  return firstString(data, ["error.message", "error", "message", "data.fail_reason", "fail_reason"]);
}

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function nextPoll(elapsed, args) {
  if (elapsed < 120) return args.pollMinSeconds;
  if (elapsed < 900) return args.pollMidSeconds;
  return args.pollMaxSeconds;
}

async function downloadFile(url, outputPath) {
  const response = await fetch(url);
  if (!response.ok) throw new SeedanceError(`download failed: HTTP ${response.status}`);
  const buffer = Buffer.from(await response.arrayBuffer());
  if (buffer.length < 1024) throw new SeedanceError(`downloaded video is too small (${buffer.length} bytes)`);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, buffer);
}

async function commandDoctor(args) {
  const { state, source } = keyState(args);
  const checks = [];
  const problems = [];
  if (state === "missing") problems.push("ARK_API_KEY is missing.");
  if (args.outputDir) {
    const parent = fs.existsSync(args.outputDir) ? args.outputDir : path.dirname(path.resolve(args.outputDir));
    const ok = fs.existsSync(parent);
    checks.push({ name: "output_dir", path: path.resolve(args.outputDir), ok });
    if (!ok) problems.push(`output directory parent does not exist: ${parent}`);
  }
  for (const url of args.imageUrl || []) {
    checks.push({ name: "image_url", url, ok: isHttpUrl(url), detail: isHttpUrl(url) ? "looks like public URL" : "not http(s)" });
  }
  console.log(JSON.stringify({
    api_base_url: args.apiBaseUrl,
    ARK_API_KEY: state,
    key_source: source,
    key_file: args.keyFile,
    checks,
    ok: problems.length === 0,
    problems,
  }, null, 2));
}

async function commandDryRun(args) {
  const { prompt, source } = readPrompt(args);
  const imageUrls = validateImageUrls(args.imageUrl);
  const payload = buildPayload(prompt, imageUrls, args);
  console.log(JSON.stringify({
    method: "POST",
    url: `${args.apiBaseUrl}/api/v3/contents/generations/tasks`,
    headers: { Authorization: "Bearer <ARK_API_KEY:redacted>", "Content-Type": "application/json" },
    prompt_source: source,
    prompt_sha256: sha256(prompt),
    payload,
  }, null, 2));
}

function writeInitialManifest(outputDir, args, payload, prompt, promptSource, imageUrls, submitResponse, taskId, keySource) {
  writeJson(manifestPath(outputDir), {
    skill: "seedance-2-video",
    provider: "ark",
    api_base_url: args.apiBaseUrl,
    model: payload.model,
    created_at: nowIso(),
    updated_at: nowIso(),
    auth: { key_source: keySource, key_stored_in_manifest: false },
    prompt: { source: promptSource, sha256: sha256(prompt) },
    source_images: imageUrls.map((url, index) => ({ url, role: payload.content[index + 1]?.role })),
    request: {
      model: payload.model,
      ratio: payload.ratio,
      duration: payload.duration,
      resolution: payload.resolution,
      watermark: payload.watermark,
      seed: payload.seed,
      content_count: payload.content.length,
    },
    task: { id: taskId, status: "submitted", submitted_at: nowIso(), submit_response: submitResponse },
  });
}

function updateManifest(outputDir, updates) {
  const filePath = manifestPath(outputDir);
  const current = readJson(filePath);
  const next = { ...current, ...updates, updated_at: nowIso() };
  writeJson(filePath, next);
  return next;
}

async function pollUntilDone(outputDir, args, apiKey, taskId) {
  const started = Date.now();
  while (true) {
    const elapsed = Math.floor((Date.now() - started) / 1000);
    if (elapsed > args.timeoutSeconds) throw new SeedanceError(`Timed out waiting for Seedance task: ${taskId}`);
    const data = await httpJson("GET", `${args.apiBaseUrl}/api/v3/contents/generations/tasks/${encodeURIComponent(taskId)}`, apiKey);
    const rawStatus = extractStatus(data);
    const status = normalizeStatus(rawStatus);
    updateManifest(outputDir, {
      task: { ...(readJson(manifestPath(outputDir)).task || {}), id: taskId, status, raw_status: rawStatus },
      polling: { status, raw_status: rawStatus, elapsed_seconds: elapsed, last_polled_at: nowIso() },
    });
    if (status === "succeeded") {
      const resultUrl = extractResultUrl(data);
      if (!isHttpUrl(resultUrl)) throw new SeedanceError("Ark task succeeded but no result video URL was found.");
      const outputPath = path.join(outputDir, args.outputName);
      await downloadFile(resultUrl, outputPath);
      return updateManifest(outputDir, {
        task: { ...(readJson(manifestPath(outputDir)).task || {}), id: taskId, status: "succeeded", result_url: resultUrl, completed_at: nowIso() },
        outputs: { video: outputPath, video_bytes: fs.statSync(outputPath).size },
      });
    }
    if (status === "failed" || status === "canceled") {
      throw new SeedanceError(extractError(data) || `Ark task ended with status ${rawStatus}`);
    }
    const seconds = nextPoll(elapsed, args);
    console.log(`Seedance task ${taskId}: ${status}, poll again in ${seconds}s`, { flush: true });
    await wait(seconds * 1000);
  }
}

async function commandRun(args) {
  const { prompt, source } = readPrompt(args);
  const imageUrls = validateImageUrls(args.imageUrl);
  if (!args.outputDir) throw new SeedanceError("Provide --output-dir.");
  const outputDir = path.resolve(args.outputDir);
  fs.mkdirSync(outputDir, { recursive: true });
  const payload = buildPayload(prompt, imageUrls, args);
  const { apiKey, source: keySource } = readApiKey(args);
  const submitResponse = await httpJson("POST", `${args.apiBaseUrl}/api/v3/contents/generations/tasks`, apiKey, payload);
  const taskId = extractTaskId(submitResponse);
  if (!taskId) throw new SeedanceError(`Ark submit succeeded but no task id was found: ${JSON.stringify(submitResponse).slice(0, 500)}`);
  writeInitialManifest(outputDir, args, payload, prompt, source, imageUrls, submitResponse, taskId, keySource);
  console.log(`Submitted Seedance task ${taskId}`);
  if (args.submitOnly) return;
  const finalManifest = await pollUntilDone(outputDir, args, apiKey, taskId);
  console.log(JSON.stringify({ ok: true, video: finalManifest.outputs?.video }, null, 2));
}

async function commandPoll(args) {
  const outputDir = path.resolve(args.outputDir || ".");
  const manifest = readJson(manifestPath(outputDir));
  const taskId = args.taskId || manifest.task?.id;
  if (!taskId) throw new SeedanceError("Provide --task-id or an output directory containing run_manifest.json with task.id.");
  const { apiKey } = readApiKey(args);
  const finalManifest = await pollUntilDone(outputDir, args, apiKey, taskId);
  console.log(JSON.stringify({ ok: true, video: finalManifest.outputs?.video }, null, 2));
}

async function main() {
  const args = parseArgs(process.argv);
  if (!args.command || args.help) {
    console.log(help());
    return;
  }
  if (args.command === "doctor") return commandDoctor(args);
  if (args.command === "dry-run") return commandDryRun(args);
  if (args.command === "run") return commandRun(args);
  if (args.command === "poll") return commandPoll(args);
  throw new SeedanceError(`Unknown command: ${args.command}`);
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`ERROR: ${message}`);
  process.exit(1);
});
