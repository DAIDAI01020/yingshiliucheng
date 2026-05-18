import fs from "node:fs/promises";
import path from "node:path";

const DEFAULT_PROJECTS_DIR = "H:\\yingshi\\projects";

function parseArgs(argv) {
  const [command, ...rest] = argv.slice(2);
  if (!command) throw new Error("Missing command: init, create-job, ingest, or find-asset.");
  const args = { command };
  for (let i = 0; i < rest.length; i += 1) {
    const arg = rest[i];
    if (!arg.startsWith("--")) throw new Error(`Unknown argument: ${arg}`);
    const key = arg.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = rest[i + 1];
    if (!next || next.startsWith("--")) args[key] = true;
    else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
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

async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function readJson(filePath, fallback) {
  if (!(await exists(filePath))) return fallback;
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

async function writeJson(filePath, data) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function projectPaths(projectRoot) {
  return {
    projectRoot,
    manifestPath: path.join(projectRoot, "project-manifest.json"),
    assetIndexPath: path.join(projectRoot, "asset-index.json"),
    jobsDir: path.join(projectRoot, "generation-jobs"),
    generationRunsDir: path.join(projectRoot, "generation-runs"),
    reviewDir: path.join(projectRoot, "review"),
    revisionLogsDir: path.join(projectRoot, "revision-logs"),
  };
}

async function ensureProject({ projectName, projectRoot }) {
  const name = projectName || path.basename(projectRoot || "");
  const root = projectRoot || path.join(DEFAULT_PROJECTS_DIR, safeName(name));
  const paths = projectPaths(path.resolve(root));
  const now = new Date().toISOString();

  await fs.mkdir(paths.jobsDir, { recursive: true });
  await fs.mkdir(paths.generationRunsDir, { recursive: true });
  await fs.mkdir(paths.reviewDir, { recursive: true });
  await fs.mkdir(paths.revisionLogsDir, { recursive: true });

  const manifest = await readJson(paths.manifestPath, {
    schemaVersion: 1,
    projectName: name,
    projectSlug: safeName(name),
    projectRoot: paths.projectRoot,
    createdAt: now,
    updatedAt: now,
    current: {},
    stages: {},
    generationRuns: [],
  });
  manifest.projectName ||= name;
  manifest.projectRoot = paths.projectRoot;
  manifest.updatedAt = now;
  await writeJson(paths.manifestPath, manifest);

  const assetIndex = await readJson(paths.assetIndexPath, {
    schemaVersion: 1,
    projectName: manifest.projectName,
    projectRoot: paths.projectRoot,
    createdAt: now,
    updatedAt: now,
    assets: [],
  });
  assetIndex.projectName ||= manifest.projectName;
  assetIndex.projectRoot = paths.projectRoot;
  assetIndex.updatedAt = now;
  await writeJson(paths.assetIndexPath, assetIndex);

  return { ...paths, manifest, assetIndex };
}

function normalizeTool(tool) {
  const value = String(tool || "").toLowerCase();
  if (!["banana", "openai"].includes(value)) throw new Error("Tool must be banana or openai.");
  return value;
}

function normalizeMode(mode) {
  const value = String(mode || "dry-run").toLowerCase();
  if (["dry-run", "dryrun", "check"].includes(value)) return "dry-run";
  if (["real", "real-generation", "generate"].includes(value)) return "real-generation";
  throw new Error("Mode must be dry-run or real-generation.");
}

async function createJob(args) {
  if (!args.projectRoot) throw new Error("create-job requires --project-root.");
  if (!args.input) throw new Error("create-job requires --input.");
  const state = await ensureProject({ projectRoot: args.projectRoot });
  const input = await readJson(path.resolve(args.input), null);
  const tool = normalizeTool(args.tool || input.tool);
  const mode = normalizeMode(args.mode || input.mode);
  const job = {
    schemaVersion: 1,
    projectName: input.projectName || state.manifest.projectName,
    projectRoot: state.projectRoot,
    tool,
    mode,
    outputDir: args.outputDir || input.outputDir || "",
    model: input.model || "",
    aspect_ratio: input.aspect_ratio || input.aspectRatio || input.ratio || "16:9",
    image_size: input.image_size || input.imageSize || "",
    size: input.size || "",
    quality: input.quality || "",
    output_format: input.output_format || input.outputFormat || "",
    createdAt: new Date().toISOString(),
    sourceInput: path.resolve(args.input),
    shots: input.shots || [],
  };
  if (!Array.isArray(job.shots) || job.shots.length === 0) throw new Error("Input JSON must include a non-empty shots array.");
  const jobName = safeName(args.jobName || `${timestamp()}_${tool}_generation-job`, "generation-job");
  const jobPath = path.join(state.jobsDir, `${jobName}.json`);
  await writeJson(jobPath, job);

  state.manifest.current.latestGenerationJob = jobPath;
  state.manifest.updatedAt = new Date().toISOString();
  await writeJson(state.manifestPath, state.manifest);

  return { projectRoot: state.projectRoot, jobPath, job };
}

function firstImagePath(entry) {
  return entry.filePath || entry.filePaths?.[0]?.path || entry.filePaths?.[0] || null;
}

function runIdFromOutputDir(outputDir) {
  return safeName(path.basename(outputDir || `run_${timestamp()}`), `run_${timestamp()}`);
}

async function ingestGeneration({ projectRoot, generationLog, reviewBoard, generationJob }) {
  if (!projectRoot) throw new Error("ingest requires --project-root.");
  if (!generationLog) throw new Error("ingest requires --generation-log.");
  const state = await ensureProject({ projectRoot });
  const logPath = path.resolve(generationLog);
  const log = await readJson(logPath, null);
  const reviewPath = reviewBoard ? path.resolve(reviewBoard) : "";
  const now = new Date().toISOString();
  const runId = runIdFromOutputDir(log.outputDir);
  const shots = log.shots || [];
  const failedCount = shots.filter((shot) => shot.status === "failed").length;

  const existing = state.assetIndex.assets || [];
  for (const entry of shots) {
    const shot = entry.shot || "SHOT";
    const tool = entry.tool || log.tool || "unknown";
    const version = entry.version || "v01";
    const handle = `${shot}_${tool}_${version}`;
    const imagePath = firstImagePath(entry);
    const asset = {
      assetId: `${handle}_${runId}`,
      handle,
      shot,
      version,
      type: "image",
      tool,
      model: entry.model || log.model || "",
      filePath: imagePath,
      promptPath: entry.promptPath || "",
      promptJsonPath: entry.promptJsonPath || "",
      generationLog: logPath,
      reviewBoard: reviewPath,
      generationJob: generationJob ? path.resolve(generationJob) : "",
      outputDir: log.outputDir || "",
      assetState: entry.status === "failed" ? "待重出" : "候选",
      status: entry.status || "",
      error: entry.error || null,
      retrySuggestion: entry.retrySuggestion || null,
      createdAt: now,
      updatedAt: now,
    };
    const index = existing.findIndex((item) => item.assetId === asset.assetId);
    if (index >= 0) existing[index] = { ...existing[index], ...asset };
    else existing.push(asset);
  }

  state.assetIndex.assets = existing;
  state.assetIndex.updatedAt = now;
  await writeJson(state.assetIndexPath, state.assetIndex);

  state.manifest.current.latestGenerationLog = logPath;
  state.manifest.current.latestReviewBoard = reviewPath;
  if (generationJob) state.manifest.current.latestGenerationJob = path.resolve(generationJob);
  state.manifest.stages.imageGeneration = failedCount ? "部分失败" : (log.dryRun ? "dry-run通过" : "已出图");
  state.manifest.generationRuns ||= [];
  state.manifest.generationRuns.push({
    runId,
    tool: log.tool || "",
    mode: log.dryRun ? "dry-run" : "real-generation",
    outputDir: log.outputDir || "",
    generationLog: logPath,
    reviewBoard: reviewPath,
    generationJob: generationJob ? path.resolve(generationJob) : "",
    status: failedCount ? "部分失败" : "完成",
    shotCount: shots.length,
    failedCount,
    createdAt: now,
  });
  state.manifest.updatedAt = now;
  await writeJson(state.manifestPath, state.manifest);

  return {
    projectRoot: state.projectRoot,
    manifestPath: state.manifestPath,
    assetIndexPath: state.assetIndexPath,
    ingestedCount: shots.length,
    failedCount,
  };
}

async function findAsset(args) {
  if (!args.projectRoot) throw new Error("find-asset requires --project-root.");
  if (!args.handle) throw new Error("find-asset requires --handle.");
  const state = await ensureProject({ projectRoot: args.projectRoot });
  const matches = (state.assetIndex.assets || [])
    .filter((asset) => asset.handle === args.handle || asset.assetId === args.handle)
    .sort((a, b) => String(b.updatedAt || b.createdAt || "").localeCompare(String(a.updatedAt || a.createdAt || "")));
  return { projectRoot: state.projectRoot, handle: args.handle, count: matches.length, assets: matches };
}

async function main() {
  const args = parseArgs(process.argv);
  let result;
  if (args.command === "init") {
    if (!args.projectName && !args.projectRoot) throw new Error("init requires --project-name or --project-root.");
    result = await ensureProject({ projectName: args.projectName, projectRoot: args.projectRoot });
    result = {
      projectRoot: result.projectRoot,
      manifestPath: result.manifestPath,
      assetIndexPath: result.assetIndexPath,
      jobsDir: result.jobsDir,
      generationRunsDir: result.generationRunsDir,
      reviewDir: result.reviewDir,
      revisionLogsDir: result.revisionLogsDir,
    };
  } else if (args.command === "create-job") {
    result = await createJob(args);
  } else if (args.command === "ingest") {
    result = await ingestGeneration({
      projectRoot: args.projectRoot,
      generationLog: args.generationLog,
      reviewBoard: args.reviewBoard,
      generationJob: args.generationJob,
    });
  } else if (args.command === "find-asset") {
    result = await findAsset(args);
  } else {
    throw new Error(`Unknown command: ${args.command}`);
  }
  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
