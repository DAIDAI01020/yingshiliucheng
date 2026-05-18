import { spawnSync } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillDir = path.dirname(__dirname);
const skillsRoot = path.dirname(skillDir);

const TOOL_CONFIG = {
  banana: {
    envKey: "OPENROUTER_API_KEY",
    generator: path.join(skillsRoot, "banana-image-generator", "scripts", "generate-banana-images.mjs"),
  },
  openai: {
    envKey: "OPENAI_API_KEY",
    generator: path.join(skillsRoot, "openai-image-generator", "scripts", "generate-openai-images.mjs"),
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
    else if (arg === "--dry-run") args.dryRun = true;
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
    if (!TOOL_CONFIG[tool]) throw new Error("Missing or invalid --tool. Use banana or openai.");
    return {
      tool,
      mode: args.dryRun ? "dry-run" : "real-generation",
      inputPath: path.resolve(args.input),
      outputDir: args.outputDir ? path.resolve(args.outputDir) : "",
      projectRoot: "",
      jobPath: "",
    };
  }

  const jobPath = path.resolve(args.job);
  const job = await readJson(jobPath);
  const tool = String(args.tool || job.tool || "").toLowerCase();
  if (!TOOL_CONFIG[tool]) throw new Error("Missing or invalid tool in --job. Use banana or openai.");
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

  if (!(await exists(config.generator))) throw new Error(`Generator script not found: ${config.generator}`);
  if (!(await exists(reviewBuilder))) throw new Error(`Review-board script not found: ${reviewBuilder}`);

  const hasApiKey = Boolean(process.env[config.envKey]);
  if (job.mode !== "dry-run" && !hasApiKey) {
    throw new Error(`${config.envKey} is missing. Set it in the local environment before real ${job.tool} generation.`);
  }

  const generatorArgs = ["--input", job.inputPath];
  if (job.outputDir) generatorArgs.push("--output-dir", job.outputDir);
  if (job.mode === "dry-run") generatorArgs.push("--dry-run");

  const generatorOutput = runNode(config.generator, generatorArgs);
  const generated = parseJsonOutput(generatorOutput);
  const outputDir = generated.outputDir;
  if (!outputDir) throw new Error("Generator output did not include outputDir.");

  const { logPath, log } = await readLog(outputDir);
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
  const summary = {
    tool: job.tool,
    mode: job.mode,
    hasApiKey,
    outputDir,
    generationLog: logPath,
    reviewBoard: review.reviewBoard,
    projectRoot: job.projectRoot || null,
    projectState,
    shotCount: (log.shots || []).length,
    failedCount: failedShots.length,
    shots: (log.shots || []).map(shotSummary),
    failedShots,
  };

  console.log(JSON.stringify(summary, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
