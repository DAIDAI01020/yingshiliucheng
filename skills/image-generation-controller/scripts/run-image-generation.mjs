import { spawnSync } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  completeRun,
  computeIdempotencyKey,
  failRun,
  preflightRun,
  startRun,
} from "../../project-state-manager/scripts/generation-run-ledger.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillDir = path.dirname(__dirname);
const skillsRoot = path.dirname(skillDir);

const TOOL_CONFIG = {
  banana: {
    envKey: "OPENROUTER_API_KEY",
    generator: path.join(skillsRoot, "banana-image-generator", "scripts", "generate-banana-images.mjs"),
  },
};

const reviewBuilder = path.join(skillsRoot, "image-review-board", "scripts", "build-review-board.mjs");
const stateManager = path.join(skillsRoot, "project-state-manager", "scripts", "manage-project-state.mjs");

function parseArgs(argv) {
  const args = { dryRun: false };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--tool") args.tool = String(argv[++i] || "").toLowerCase();
    else if (arg === "--input") args.input = argv[++i];
    else if (arg === "--job") args.job = argv[++i];
    else if (arg === "--output-dir") args.outputDir = argv[++i];
    else if (arg === "--prompt-mode") args.promptMode = String(argv[++i] || "").toLowerCase();
    else if (arg === "--dry-run") args.dryRun = true;
    else if (arg === "--generation-confirmation") args.generationConfirmation = String(argv[++i] || "").toLowerCase();
    else if (arg === "--available-credits") args.availableCredits = argv[++i];
    else if (arg === "--estimated-cost") args.estimatedCost = argv[++i];
    else if (arg === "--idempotency-key") args.idempotencyKey = argv[++i];
    else if (arg === "--max-attempts") args.maxAttempts = argv[++i];
    else if (arg === "--resume") args.resume = true;
    else if (arg === "--force-new-run") args.forceNewRun = true;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (!args.input && !args.job) throw new Error("Missing --input or --job path.");
  return args;
}

async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

function runNode(scriptPath, args) {
  const result = spawnSync(process.execPath, [scriptPath, ...args], {
    cwd: path.dirname(scriptPath),
    env: process.env,
    encoding: "utf8",
    maxBuffer: 1024 * 1024 * 50,
  });
  if (result.status !== 0) {
    const detail = [result.stderr, result.stdout].filter(Boolean).join("\n").trim();
    throw new Error(detail || `Command failed: node ${scriptPath}`);
  }
  return result.stdout.trim();
}

async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

function parseJsonOutput(output) {
  const text = output.trim();
  if (!text) throw new Error("Generator returned empty output.");
  try {
    return JSON.parse(text);
  } catch {
    const start = text.indexOf("{");
    const end = text.lastIndexOf("}");
    if (start >= 0 && end > start) return JSON.parse(text.slice(start, end + 1));
    throw new Error("Could not parse generator JSON output.");
  }
}

function timestamp() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}_${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
}

function safeName(value, fallback = "project") {
  return String(value || fallback)
    .trim()
    .replace(/[<>:"/\\|?*\u0000-\u001f]/g, "_")
    .replace(/\s+/g, "_")
    .slice(0, 80) || fallback;
}

async function readLog(outputDir) {
  const logPath = path.join(outputDir, "logs", "generation-log.json");
  if (!(await exists(logPath))) throw new Error(`Missing generation log: ${logPath}`);
  return { logPath, log: JSON.parse(await fs.readFile(logPath, "utf8")) };
}

function normalizeMode(mode, dryRunFlag) {
  if (dryRunFlag) return "dry-run";
  const value = String(mode || "").toLowerCase();
  if (["dry-run", "dryrun", "check"].includes(value)) return "dry-run";
  if (["real", "real-generation", "generate"].includes(value)) return "real-generation";
  return "real-generation";
}

async function resolveJob(args) {
  if (!args.job) {
    const tool = String(args.tool || "").toLowerCase();
    if (!TOOL_CONFIG[tool]) throw new Error("Missing or invalid --tool. Use banana.");
    return {
      tool,
      mode: args.dryRun ? "dry-run" : "real-generation",
      inputPath: path.resolve(args.input),
    outputDir: args.outputDir ? path.resolve(args.outputDir) : "",
      promptMode: args.promptMode || "quality",
      projectRoot: "",
      jobPath: "",
    };
  }

  const jobPath = path.resolve(args.job);
  const job = await readJson(jobPath);
  const tool = String(args.tool || job.tool || "").toLowerCase();
  if (!TOOL_CONFIG[tool]) throw new Error("Missing or invalid tool in --job. Use banana.");
  const mode = normalizeMode(job.mode, args.dryRun);
  const projectRoot = job.projectRoot ? path.resolve(job.projectRoot) : "";
  const outputDir = args.outputDir
    ? path.resolve(args.outputDir)
    : job.outputDir
      ? path.resolve(job.outputDir)
      : projectRoot
        ? path.join(projectRoot, "generation-runs", `${timestamp()}_${tool}`)
        : "";

  return {
    tool,
    mode,
    inputPath: jobPath,
    outputDir,
    promptMode: args.promptMode || job.promptMode || job.bananaPromptMode || "quality",
    projectRoot,
    jobPath,
    projectName: job.projectName || safeName(path.basename(projectRoot || ""), "project"),
  };
}

function shotSummary(entry) {
  return {
    shot: entry.shot,
    version: entry.version,
    tool: entry.tool,
    status: entry.status,
    imagePath: entry.filePath || entry.filePaths?.[0]?.path || entry.filePaths?.[0] || null,
    promptPath: entry.promptPath || null,
    promptJsonPath: entry.promptJsonPath || null,
    error: entry.error || null,
    retrySuggestion: entry.retrySuggestion || null,
  };
}

async function main() {
  const args = parseArgs(process.argv);
  const job = await resolveJob(args);
  const config = TOOL_CONFIG[job.tool];
  const sourceInput = await readJson(job.inputPath);
  const promptFingerprint = computeIdempotencyKey((sourceInput.shots || []).map((shot) => ({
    shot: shot.shot,
    prompt: shot.prompt || shot.fullPrompt || shot.qualityPrompt || "",
    negativePrompt: shot.negativePrompt || shot.negative_prompt || "",
  })));
  const referenceFingerprint = computeIdempotencyKey((sourceInput.shots || []).map((shot) => shot.references || []));
  const safetyPayload = {
    provider: job.tool,
    tool: job.tool,
    asset_or_shot_id: (sourceInput.shots || []).map((shot) => shot.shot).join(","),
    deliverable_profile: sourceInput.deliverable_profile || sourceInput.deliverableProfile || "image",
    execution_mode: job.mode,
    prompt_fingerprint: promptFingerprint,
    reference_fingerprint: referenceFingerprint,
    request: {
      prompt_mode: job.promptMode,
      shot_count: (sourceInput.shots || []).length,
      model: sourceInput.model || "",
      aspect_ratio: sourceInput.aspect_ratio || sourceInput.aspectRatio || sourceInput.ratio || "",
      image_size: sourceInput.image_size || sourceInput.imageSize || "",
    },
  };
  const generationConfirmation = args.generationConfirmation
    || sourceInput.generation_confirmation
    || sourceInput.generationConfirmation
    || "";
  const preflight = await preflightRun({
    projectRoot: job.projectRoot,
    payload: safetyPayload,
    idempotencyKey: args.idempotencyKey || sourceInput.idempotency_key || sourceInput.idempotencyKey || "",
    generationConfirmation,
    estimatedCost: args.estimatedCost ?? sourceInput.estimated_cost ?? sourceInput.estimatedCost,
    availableCredits: args.availableCredits ?? sourceInput.available_credits ?? sourceInput.availableCredits,
    resume: Boolean(args.resume),
    forceNewRun: Boolean(args.forceNewRun),
    maxAttempts: Number(args.maxAttempts || sourceInput.max_attempts || 2),
    paid: job.mode !== "dry-run",
  });
  if (!preflight.allowed) {
    if (preflight.reuse) {
      console.log(JSON.stringify({
        tool: job.tool,
        mode: job.mode,
        reused: true,
        idempotencyKey: preflight.idempotency_key,
        reason: preflight.reason,
        existingRun: preflight.existing,
      }, null, 2));
      return;
    }
    throw new Error(`Generation safety preflight blocked: ${preflight.reason}`);
  }

  if (!(await exists(config.generator))) throw new Error(`Generator script not found: ${config.generator}`);
  if (!(await exists(reviewBuilder))) throw new Error(`Review-board script not found: ${reviewBuilder}`);

  const hasApiKey = Boolean(process.env[config.envKey]);
  if (job.mode !== "dry-run" && !hasApiKey) {
    throw new Error(`${config.envKey} is missing. Set it in the local environment before real ${job.tool} generation.`);
  }

  let executionInputPath = job.inputPath;
  if (args.resume && preflight.resume_items?.length) {
    const failedSet = new Set(preflight.resume_items.map(String));
    const resumeShots = (sourceInput.shots || []).filter((shot) => failedSet.has(String(shot.shot)));
    if (!resumeShots.length) throw new Error("Resume was requested but no failed shots match the current input.");
    const resumeDir = job.outputDir || path.join(job.projectRoot || path.dirname(job.inputPath), "generation-runs", `${timestamp()}_${job.tool}_resume`);
    await fs.mkdir(resumeDir, { recursive: true });
    executionInputPath = path.join(resumeDir, "resume-generation-input.json");
    await fs.writeFile(executionInputPath, `${JSON.stringify({ ...sourceInput, shots: resumeShots }, null, 2)}\n`, "utf8");
    job.outputDir = resumeDir;
  }

  const generatorArgs = ["--input", executionInputPath];
  if (job.outputDir) generatorArgs.push("--output-dir", job.outputDir);
  if (job.promptMode) generatorArgs.push("--prompt-mode", job.promptMode);
  if (job.mode === "dry-run") generatorArgs.push("--dry-run");

  const startedAt = Date.now();
  if (job.mode !== "dry-run") await startRun({ projectRoot: job.projectRoot, preflight, payload: safetyPayload });
  try {
    const generatorOutput = runNode(config.generator, generatorArgs);
    const generated = parseJsonOutput(generatorOutput);
    const outputDir = generated.outputDir;
    if (!outputDir) throw new Error("Generator output did not include outputDir.");

    const { logPath, log } = await readLog(outputDir);
    const elapsedSeconds = Number(((Date.now() - startedAt) / 1000).toFixed(3));
    log.idempotencyKey = preflight.idempotency_key;
    log.elapsedSeconds = elapsedSeconds;
    log.estimatedCost = args.estimatedCost ?? sourceInput.estimated_cost ?? sourceInput.estimatedCost ?? null;
    await fs.writeFile(logPath, `${JSON.stringify(log, null, 2)}\n`, "utf8");
    const reviewOutput = runNode(reviewBuilder, ["--task", outputDir]);
    const review = parseJsonOutput(reviewOutput);
    let projectState = null;
    if (job.projectRoot && await exists(stateManager)) {
      const stateOutput = runNode(stateManager, [
        "ingest",
        "--project-root",
        job.projectRoot,
        "--generation-log",
        logPath,
        "--review-board",
        review.reviewBoard,
        "--generation-job",
        job.jobPath,
      ]);
      projectState = parseJsonOutput(stateOutput);
    }

    const failedShots = (log.shots || []).filter((shot) => shot.status === "failed").map(shotSummary);
    const ledgerEvent = job.mode === "dry-run" ? null : await completeRun({
      projectRoot: job.projectRoot,
      preflight,
      payload: safetyPayload,
      output: { output_dir: outputDir, generation_log: logPath, review_board: review.reviewBoard },
      failedItems: failedShots.map((shot) => shot.shot),
      metrics: { elapsed_seconds: elapsedSeconds, estimated_cost: log.estimatedCost },
    });
    const summary = {
      tool: job.tool,
      mode: job.mode,
      hasApiKey,
      outputDir,
      generationLog: logPath,
      reviewBoard: review.reviewBoard,
      projectRoot: job.projectRoot || null,
      promptMode: job.promptMode || null,
      projectState,
      idempotencyKey: preflight.idempotency_key,
      ledgerEvent,
      resumed: Boolean(args.resume),
      shotCount: (log.shots || []).length,
      failedCount: failedShots.length,
      shots: (log.shots || []).map(shotSummary),
      failedShots,
    };

    console.log(JSON.stringify(summary, null, 2));
  } catch (error) {
    if (job.mode !== "dry-run") {
      await failRun({
        projectRoot: job.projectRoot,
        preflight,
        payload: safetyPayload,
        error: error.message,
        failedItems: preflight.resume_items || [],
        metrics: { elapsed_seconds: Number(((Date.now() - startedAt) / 1000).toFixed(3)) },
      });
    }
    throw error;
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
