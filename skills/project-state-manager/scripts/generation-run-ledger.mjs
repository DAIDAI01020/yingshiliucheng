import fs from "node:fs/promises";
import path from "node:path";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";


const THIS_FILE = fileURLToPath(import.meta.url);
const CONFIRMED = new Set(["approved", "direct_test", "confirmed"]);
const IN_FLIGHT = new Set(["submitted", "running"]);


function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonical(value[key])]));
  }
  return value;
}


export function computeIdempotencyKey(payload) {
  return createHash("sha256").update(JSON.stringify(canonical(payload))).digest("hex");
}


function ledgerPath(projectRoot) {
  return path.join(path.resolve(projectRoot), "revision-logs", "generation-run-ledger.jsonl");
}


async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}


async function readLedger(projectRoot) {
  const filePath = ledgerPath(projectRoot);
  if (!(await exists(filePath))) return [];
  const text = await fs.readFile(filePath, "utf8");
  return text.split(/\r?\n/).filter(Boolean).map((line, index) => {
    try {
      return JSON.parse(line);
    } catch (error) {
      throw new Error(`Invalid generation ledger JSONL at line ${index + 1}: ${error.message}`);
    }
  });
}


async function appendLedger(projectRoot, event) {
  const filePath = ledgerPath(projectRoot);
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.appendFile(filePath, `${JSON.stringify(event)}\n`, "utf8");
  return filePath;
}


function numeric(value) {
  if (value === null || value === undefined || value === "") return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}


export async function latestRun(projectRoot, idempotencyKey) {
  const events = await readLedger(projectRoot);
  return [...events].reverse().find((event) => event.idempotency_key === idempotencyKey) || null;
}


export async function preflightRun({
  projectRoot,
  payload,
  idempotencyKey = "",
  generationConfirmation = "",
  estimatedCost = null,
  availableCredits = null,
  resume = false,
  forceNewRun = false,
  maxAttempts = 2,
  paid = true,
}) {
  const key = idempotencyKey || computeIdempotencyKey(payload);
  if (paid && !CONFIRMED.has(String(generationConfirmation || "").toLowerCase())) {
    return { allowed: false, idempotency_key: key, reason: "missing_generation_confirmation", existing: null };
  }
  const estimated = numeric(estimatedCost);
  const available = numeric(availableCredits);
  if (estimated !== null && available !== null && available < estimated) {
    return {
      allowed: false,
      idempotency_key: key,
      reason: "insufficient_credits",
      estimated_cost: estimated,
      available_credits: available,
      existing: null,
    };
  }
  if (!projectRoot) {
    return { allowed: true, idempotency_key: key, attempt: 1, ledger_path: "", existing: null };
  }
  const existing = await latestRun(projectRoot, key);
  if (!existing) {
    return { allowed: true, idempotency_key: key, attempt: 1, ledger_path: ledgerPath(projectRoot), existing: null };
  }
  const existingAttempt = Number(existing.attempt || 1);
  if (forceNewRun) {
    return { allowed: true, idempotency_key: key, attempt: existingAttempt + 1, ledger_path: ledgerPath(projectRoot), existing, forced: true };
  }
  if (existing.status === "succeeded" || existing.status === "manual_handoff") {
    return { allowed: false, idempotency_key: key, reason: "reusable_existing_result", reuse: true, existing };
  }
  if (IN_FLIGHT.has(existing.status)) {
    return { allowed: false, idempotency_key: key, reason: "run_already_in_flight", reuse: true, existing };
  }
  if (["failed", "partial"].includes(existing.status)) {
    if (!resume) {
      return { allowed: false, idempotency_key: key, reason: "resume_confirmation_required", existing };
    }
    if (existingAttempt >= Number(maxAttempts || 2)) {
      return { allowed: false, idempotency_key: key, reason: "max_attempts_reached", existing };
    }
    return {
      allowed: true,
      idempotency_key: key,
      attempt: existingAttempt + 1,
      ledger_path: ledgerPath(projectRoot),
      existing,
      resume_items: existing.failed_items || [],
    };
  }
  return { allowed: false, idempotency_key: key, reason: `unsupported_existing_status:${existing.status}`, existing };
}


function baseEvent({ preflight, payload, status, output = {}, failedItems = [], error = "", metrics = {} }) {
  const now = new Date().toISOString();
  return {
    schema_version: 1,
    event_id: `run_${preflight.idempotency_key.slice(0, 12)}_${preflight.attempt || 1}_${Date.now()}`,
    run_id: `run_${preflight.idempotency_key.slice(0, 16)}_a${preflight.attempt || 1}`,
    idempotency_key: preflight.idempotency_key,
    attempt: preflight.attempt || 1,
    status,
    provider: payload.provider || payload.tool || "",
    asset_or_shot_id: payload.asset_or_shot_id || payload.shot || "",
    deliverable_profile: payload.deliverable_profile || "",
    execution_mode: payload.execution_mode || "",
    prompt_fingerprint: payload.prompt_fingerprint || "",
    reference_fingerprint: payload.reference_fingerprint || "",
    request: payload.request || {},
    output,
    failed_items: failedItems,
    error,
    metrics: {
      elapsed_seconds: metrics.elapsed_seconds ?? null,
      credits_used: metrics.credits_used ?? null,
      estimated_cost: metrics.estimated_cost ?? null,
    },
    updated_at: now,
  };
}


export async function startRun({ projectRoot, preflight, payload }) {
  const event = baseEvent({ preflight, payload, status: "running" });
  if (projectRoot) await appendLedger(projectRoot, event);
  return event;
}


export async function submitRun({ projectRoot, preflight, payload, output = {}, metrics = {} }) {
  const event = baseEvent({ preflight, payload, status: "submitted", output, metrics });
  if (projectRoot) await appendLedger(projectRoot, event);
  return event;
}


export async function completeRun({ projectRoot, preflight, payload, output = {}, failedItems = [], metrics = {}, manualHandoff = false }) {
  const status = manualHandoff ? "manual_handoff" : failedItems.length ? "partial" : "succeeded";
  const event = baseEvent({ preflight, payload, status, output, failedItems, metrics });
  if (projectRoot) await appendLedger(projectRoot, event);
  return event;
}


export async function failRun({ projectRoot, preflight, payload, error, failedItems = [], metrics = {} }) {
  const event = baseEvent({ preflight, payload, status: "failed", error: String(error || "unknown failure"), failedItems, metrics });
  if (projectRoot) await appendLedger(projectRoot, event);
  return event;
}


function parseArgs(argv) {
  const [command, ...rest] = argv.slice(2);
  const args = { command };
  for (let index = 0; index < rest.length; index += 1) {
    const arg = rest[index];
    if (!arg.startsWith("--")) throw new Error(`Unknown argument: ${arg}`);
    const key = arg.slice(2).replace(/-([a-z])/g, (_, char) => char.toUpperCase());
    const next = rest[index + 1];
    if (!next || next.startsWith("--")) args[key] = true;
    else {
      args[key] = next;
      index += 1;
    }
  }
  return args;
}


async function cli() {
  const args = parseArgs(process.argv);
  if (!args.command) throw new Error("Missing command: preflight or status.");
  if (!args.projectRoot) throw new Error("--project-root is required.");
  if (args.command === "status") {
    const events = await readLedger(args.projectRoot);
    const latest = args.idempotencyKey ? await latestRun(args.projectRoot, args.idempotencyKey) : events.at(-1) || null;
    console.log(JSON.stringify({ ledger_path: ledgerPath(args.projectRoot), event_count: events.length, latest }, null, 2));
    return;
  }
  if (args.command !== "preflight") throw new Error("Command must be preflight or status.");
  if (!args.input) throw new Error("preflight requires --input JSON.");
  const payload = JSON.parse(await fs.readFile(path.resolve(args.input), "utf8"));
  const result = await preflightRun({
    projectRoot: args.projectRoot,
    payload,
    idempotencyKey: args.idempotencyKey || "",
    generationConfirmation: args.generationConfirmation || "",
    estimatedCost: args.estimatedCost,
    availableCredits: args.availableCredits,
    resume: Boolean(args.resume),
    forceNewRun: Boolean(args.forceNewRun),
    maxAttempts: Number(args.maxAttempts || 2),
    paid: !args.unpaid,
  });
  console.log(JSON.stringify(result, null, 2));
  if (!result.allowed && !result.reuse) process.exitCode = 2;
}


if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(THIS_FILE)) {
  cli().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
