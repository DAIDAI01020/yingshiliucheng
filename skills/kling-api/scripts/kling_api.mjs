import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

const DEFAULT_BASE_URL = "https://api-beijing.klingai.com";
const DEFAULT_KEY_FILE = path.join(os.homedir(), ".config", "codex-kling-api", "secrets.json");

function parseArgs(argv) {
  const [command = "doctor", ...rest] = argv.slice(2);
  const args = { command };
  for (let index = 0; index < rest.length; index += 1) {
    const arg = rest[index];
    if (!arg.startsWith("--")) throw new Error("Unknown positional argument.");
    const key = arg.slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
    const next = rest[index + 1];
    if (!next || next.startsWith("--")) args[key] = true;
    else {
      args[key] = next;
      index += 1;
    }
  }
  return args;
}

function expandUser(value) {
  if (!value) return DEFAULT_KEY_FILE;
  if (value === "~") return os.homedir();
  if (value.startsWith("~/") || value.startsWith("~\\")) return path.join(os.homedir(), value.slice(2));
  return path.resolve(value);
}

function validatedBaseUrl(value) {
  const url = new URL(String(value || process.env.KLING_API_BASE_URL || DEFAULT_BASE_URL));
  const loopback = ["localhost", "127.0.0.1", "::1"].includes(url.hostname);
  if (url.protocol !== "https:" && !(url.protocol === "http:" && loopback)) {
    throw new Error("KLING_API_BASE_URL must use HTTPS; HTTP is allowed only for loopback tests.");
  }
  if (url.username || url.password || url.search || url.hash) throw new Error("KLING_API_BASE_URL must not contain credentials, query, or fragment.");
  return url.toString().replace(/\/$/, "");
}

function validateKey(value) {
  const key = String(value || "").trim();
  if (key.length < 24 || /\s/.test(key)) throw new Error("Invalid Kling API key format.");
  return key;
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8").trim();
}

async function readCredential(keyFile) {
  const envKey = String(process.env.KLING_API_KEY || "").trim();
  if (envKey) return { key: validateKey(envKey), source: "env:KLING_API_KEY" };
  let parsed;
  try {
    parsed = JSON.parse(await fs.readFile(keyFile, "utf8"));
  } catch (error) {
    if (error.code === "ENOENT") throw new Error("KLING_API_KEY is not configured. Run setup-key --key-stdin.");
    throw new Error("Cannot read the private Kling credential file.");
  }
  return { key: validateKey(parsed.kling_api_key || parsed.KLING_API_KEY), source: "private-file" };
}

async function setupKey(args) {
  if (!args.keyStdin) throw new Error("Use setup-key --key-stdin so the key is not placed in command history.");
  const key = validateKey(await readStdin());
  const keyFile = expandUser(args.keyFile);
  await fs.mkdir(path.dirname(keyFile), { recursive: true, mode: 0o700 });
  await fs.writeFile(keyFile, `${JSON.stringify({ kling_api_key: key }, null, 2)}\n`, { encoding: "utf8", mode: 0o600 });
  await fs.chmod(keyFile, 0o600).catch(() => {});
  return { configured: true, source: "private-file", key_file: keyFile, key_state: `present:${key.length}chars` };
}

async function liveCheck({ key, baseUrl, timeoutMs }) {
  const end = Date.now();
  const start = end - 24 * 60 * 60 * 1000;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  let response;
  try {
    response = await fetch(`${baseUrl}/account/costs?start_time=${start}&end_time=${end}`, {
      headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      signal: controller.signal,
    });
  } catch (error) {
    if (error.name === "AbortError") throw new Error("Kling authentication check timed out.");
    throw new Error("Kling authentication check failed at the network layer.");
  } finally {
    clearTimeout(timer);
  }
  let body = {};
  try {
    body = await response.json();
  } catch {
    // Status remains authoritative when the body is not JSON.
  }
  if (!response.ok || (body.code !== undefined && Number(body.code) !== 0)) {
    const apiCode = body.code === undefined ? "unknown" : String(body.code);
    throw new Error(`Kling authentication rejected (HTTP ${response.status}, API code ${apiCode}).`);
  }
  return { authenticated: true, http_status: response.status, api_code: body.code ?? 0, data_returned: body.data !== undefined };
}

async function doctor(args) {
  const keyFile = expandUser(args.keyFile);
  const credential = await readCredential(keyFile);
  const baseUrl = validatedBaseUrl(args.baseUrl);
  const result = {
    configured: true,
    source: credential.source,
    key_state: `present:${credential.key.length}chars`,
    base_url: baseUrl,
    live_check: Boolean(args.live),
  };
  if (args.live) Object.assign(result, await liveCheck({ key: credential.key, baseUrl, timeoutMs: Number(args.timeoutMs || 20000) }));
  return result;
}

async function main() {
  const args = parseArgs(process.argv);
  let result;
  if (args.command === "setup-key") result = await setupKey(args);
  else if (args.command === "doctor") result = await doctor(args);
  else throw new Error("Command must be setup-key or doctor.");
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

main().catch(error => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
