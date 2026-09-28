import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

const DEFAULT_PROJECTS_DIR = "H:\\yingshi\\projects";
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = path.resolve(SCRIPT_DIR, "..");
const SHORT_DRAMA_TEMPLATE_DIR = path.join(SKILL_DIR, "templates", "short-drama");
const SHORT_DRAMA_ROUTES = new Set(["storyboard-execution", "full-development", "quick-test"]);

const SHORT_DRAMA_STATE_FILES = {
  projectIntake: "project-intake.json",
  styleLock: "style-lock.json",
  sceneMap: path.join("references", "scene-map.md"),
  shotAudit: path.join("references", "shot-audit.md"),
  promptAudit: path.join("prompts", "prompt-audit.md"),
  generationReady: path.join("generation-jobs", "generation-ready.json"),
  qcFeedback: path.join("revision-logs", "qc-feedback.md"),
};

function parseArgs(argv) {
  const [command, ...rest] = argv.slice(2);
  if (!command) throw new Error("Missing command: init, create-job, ingest, ingest-video, find-asset, record-observation, summarize-feedback, audit, or check.");
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
    videoRunsDir: path.join(projectRoot, "video-runs"),
    reviewDir: path.join(projectRoot, "review"),
    revisionLogsDir: path.join(projectRoot, "revision-logs"),
    briefsDir: path.join(projectRoot, "briefs"),
    promptsDir: path.join(projectRoot, "prompts"),
    referencesDir: path.join(projectRoot, "references"),
    styleLockPath: path.join(projectRoot, "style-lock.json"),
    observationsPath: path.join(projectRoot, "revision-logs", "generation-observations.jsonl"),
    feedbackSummaryPath: path.join(projectRoot, "revision-logs", "generation-feedback-summary.json"),
    runLedgerPath: path.join(projectRoot, "revision-logs", "generation-run-ledger.jsonl"),
  };
}

function isInsideRoot(root, target) {
  const relative = path.relative(path.resolve(root), path.resolve(target));
  return relative === "" || (!relative.startsWith("..") && !path.isAbsolute(relative));
}

function stableHash(value) {
  return createHash("sha256").update(JSON.stringify(value)).digest("hex");
}

async function readJsonLines(filePath) {
  if (!(await exists(filePath))) return [];
  const text = await fs.readFile(filePath, "utf8");
  return text.split(/\r?\n/).filter(Boolean).map((line, index) => {
    try {
      return JSON.parse(line);
    } catch (error) {
      throw new Error(`Invalid JSONL at ${filePath}:${index + 1}: ${error.message}`);
    }
  });
}

async function appendJsonLine(filePath, data) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.appendFile(filePath, `${JSON.stringify(data)}\n`, "utf8");
}

function upsertRunById(items, run) {
  const existing = Array.isArray(items) ? items : [];
  const index = existing.findIndex((item) => item.runId === run.runId);
  if (index >= 0) existing[index] = { ...existing[index], ...run };
  else existing.push(run);
  return existing;
}

function normalizeShortDramaRoute(route) {
  const value = String(route || "storyboard-execution").toLowerCase();
  if (!SHORT_DRAMA_ROUTES.has(value)) {
    throw new Error("Short-drama route must be storyboard-execution, full-development, or quick-test.");
  }
  return value;
}

function shortDramaStatePaths(projectRoot) {
  return Object.fromEntries(
    Object.entries(SHORT_DRAMA_STATE_FILES).map(([key, relativePath]) => [
      key,
      path.join(projectRoot, relativePath),
    ]),
  );
}

function templateReplacements({ state, route, projectTier }) {
  return {
    "__PROJECT_NAME__": state.manifest.projectName,
    "__PROJECT_SLUG__": state.manifest.projectSlug || safeName(state.manifest.projectName),
    "__PROJECT_ROOT__": state.projectRoot.replace(/\\/g, "\\\\"),
    "__ROUTE__": route,
    "__PROJECT_TIER__": projectTier,
    "__CREATED_AT__": new Date().toISOString(),
  };
}

async function copyTemplateIfMissing({ templateName, targetPath, replacements }) {
  if (await exists(targetPath)) return false;
  const sourcePath = path.join(SHORT_DRAMA_TEMPLATE_DIR, templateName);
  let content = await fs.readFile(sourcePath, "utf8");
  for (const [key, value] of Object.entries(replacements)) {
    content = content.replaceAll(key, value);
  }
  await fs.mkdir(path.dirname(targetPath), { recursive: true });
  await fs.writeFile(targetPath, content, "utf8");
  return true;
}

async function ensureShortDramaWorkflow(state, { route, projectTier }) {
  const normalizedRoute = normalizeShortDramaRoute(route);
  const tier = projectTier || "formal";
  const now = new Date().toISOString();
  const stateFiles = shortDramaStatePaths(state.projectRoot);
  const replacements = templateReplacements({ state, route: normalizedRoute, projectTier: tier });
  const templateMap = [
    ["project-intake-template.json", stateFiles.projectIntake],
    ["style-lock-template.json", stateFiles.styleLock],
    ["scene-map-template.md", stateFiles.sceneMap],
    ["shot-audit-template.md", stateFiles.shotAudit],
    ["prompt-audit-template.md", stateFiles.promptAudit],
    ["generation-ready-template.json", stateFiles.generationReady],
    ["qc-feedback-template.md", stateFiles.qcFeedback],
  ];
  const created = [];
  for (const [templateName, targetPath] of templateMap) {
    if (await copyTemplateIfMissing({ templateName, targetPath, replacements })) {
      created.push(targetPath);
    }
  }

  state.manifest.workflow = {
    ...(state.manifest.workflow || {}),
    type: "short-drama",
    route: normalizedRoute,
    projectTier: tier,
    mainLine: "short_drama_story",
    strongStateGate: tier === "formal",
    defaultPlatformTargets: {
      image: ["built_in_image", "Banana", "Banana Pro"],
      video: ["Jimeng", "Seedance", "Ark", "Kling", "Kling O1", "Kling VIDEO 3.0 Omni"],
    },
    updatedAt: now,
  };
  state.manifest.gates ||= {};
  state.manifest.gates.generation = {
    strongStateGate: tier === "formal",
    required: [
      "project-intake",
      "mother-library-application",
      "style-lock",
      "scene-map",
      "shot-audit",
      "prompt-audit",
      "generation-ready",
    ],
    stateFiles,
    routeBackOrder: [
      "zongkong",
      "style-reference-director",
      "project-style-lock",
      "scene-style-map-director",
      "shot-language-auditor",
      "prompt-platform-auditor",
      "project-state-manager",
    ],
    updatedAt: now,
  };
  state.manifest.current ||= {};
  state.manifest.current.projectIntake = stateFiles.projectIntake;
  state.manifest.current.styleLock = stateFiles.styleLock;
  state.manifest.current.sceneMap = stateFiles.sceneMap;
  state.manifest.current.shotAudit = stateFiles.shotAudit;
  state.manifest.current.promptAudit = stateFiles.promptAudit;
  state.manifest.current.generationReady = stateFiles.generationReady;
  state.manifest.current.qcFeedback = stateFiles.qcFeedback;
  state.manifest.updatedAt = now;
  await writeJson(state.manifestPath, state.manifest);
  return { stateFiles, created };
}

async function ensureProject({ projectName, projectRoot, workflow, route, projectTier }) {
  const name = projectName || path.basename(projectRoot || "");
  const root = projectRoot || path.join(DEFAULT_PROJECTS_DIR, safeName(name));
  const paths = projectPaths(path.resolve(root));
  const now = new Date().toISOString();

  await fs.mkdir(paths.jobsDir, { recursive: true });
  await fs.mkdir(paths.generationRunsDir, { recursive: true });
  await fs.mkdir(paths.videoRunsDir, { recursive: true });
  await fs.mkdir(paths.reviewDir, { recursive: true });
  await fs.mkdir(paths.revisionLogsDir, { recursive: true });
  await fs.mkdir(paths.briefsDir, { recursive: true });
  await fs.mkdir(paths.promptsDir, { recursive: true });
  await fs.mkdir(paths.referencesDir, { recursive: true });

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
    videoRuns: [],
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

  const state = { ...paths, manifest, assetIndex };
  if (workflow === "short-drama") {
    const shortDrama = await ensureShortDramaWorkflow(state, { route, projectTier });
    return { ...state, shortDrama };
  }

  return state;
}

function normalizeTool(tool) {
  const value = String(tool || "").toLowerCase();
  if (value !== "banana") throw new Error("Tool must be banana.");
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
    promptMode: args.promptMode || input.promptMode || input.bananaPromptMode || (tool === "banana" ? "quality" : ""),
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

// Physical evidence is a minimum requirement; decoding and creative QC remain separate.
async function verifiedOutput(filePath, baseDir) {
  if (typeof filePath !== "string" || !filePath || /^https?:\/\//i.test(filePath)) return null;
  const resolved = path.resolve(baseDir, filePath);
  try {
    const info = await fs.stat(resolved);
    return info.isFile() && info.size > 0 ? resolved : null;
  } catch {
    return null;
  }
}

function mergeIngestedAsset(previous, asset) {
  const sameEvidence = previous.filePath && previous.filePath === asset.filePath
    && ["success", "succeeded", "completed"].includes(previous.status) && asset.assetState === "候选";
  return {
    ...previous, ...asset,
    createdAt: previous.createdAt || asset.createdAt,
    assetState: sameEvidence ? previous.assetState || asset.assetState : asset.assetState,
  };
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
  if (!log || !Array.isArray(log.shots)) throw new Error(`Invalid generation log: ${logPath}`);
  const reviewPath = reviewBoard ? path.resolve(reviewBoard) : "";
  const now = new Date().toISOString();
  const runId = runIdFromOutputDir(log.outputDir);
  const shots = log.shots || [];
  let failedCount = 0;
  let successCount = 0;
  let dryRunCount = 0;

  const existing = state.assetIndex.assets || [];
  for (const entry of shots) {
    const shot = entry.shot || "SHOT";
    const tool = entry.tool || log.tool || "unknown";
    const version = entry.version || "v01";
    const handle = `${shot}_${tool}_${version}`;
    const plannedFilePath = firstImagePath(entry);
    const claimedStatus = String(entry.status || "pending").toLowerCase();
    const dryRun = claimedStatus !== "failed" && Boolean(log.dryRun || claimedStatus === "dry-run");
    const claimedSuccess = ["success", "succeeded", "completed"].includes(claimedStatus);
    const imagePath = log.dryRun || dryRun ? null : await verifiedOutput(plannedFilePath, path.dirname(logPath));
    const status = dryRun ? "dry-run" : claimedSuccess && !imagePath ? "output_missing" : claimedStatus;
    const verifiedSuccess = !dryRun && claimedSuccess && Boolean(imagePath);
    if (dryRun) dryRunCount++;
    else if (status === "failed") failedCount++;
    else if (verifiedSuccess) successCount++;
    const asset = {
      assetId: `${handle}_${runId}`,
      handle,
      shot,
      version,
      type: "image",
      tool,
      model: entry.model || log.model || "",
      filePath: imagePath,
      plannedFilePath,
      promptPath: entry.promptPath || "",
      promptJsonPath: entry.promptJsonPath || "",
      generationLog: logPath,
      reviewBoard: reviewPath,
      generationJob: generationJob ? path.resolve(generationJob) : "",
      outputDir: log.outputDir || "",
      assetState: dryRun ? "待执行" : status === "failed" ? "待重出" : verifiedSuccess ? "候选" : "待检查",
      status,
      error: entry.error || null,
      retrySuggestion: entry.retrySuggestion || null,
      idempotencyKey: entry.idempotencyKey || log.idempotencyKey || "",
      usage: entry.usage || null,
      elapsedSeconds: entry.elapsedSeconds ?? log.elapsedSeconds ?? null,
      creditsUsed: entry.creditsUsed ?? log.creditsUsed ?? null,
      estimatedCost: entry.estimatedCost ?? log.estimatedCost ?? null,
      createdAt: now,
      updatedAt: now,
    };
    const index = existing.findIndex((item) => item.assetId === asset.assetId);
    if (index >= 0) existing[index] = mergeIngestedAsset(existing[index], asset);
    else existing.push(asset);
  }

  state.assetIndex.assets = existing;
  state.assetIndex.updatedAt = now;
  await writeJson(state.assetIndexPath, state.assetIndex);

  state.manifest.current.latestGenerationLog = logPath;
  state.manifest.current.latestReviewBoard = reviewPath;
  if (generationJob) state.manifest.current.latestGenerationJob = path.resolve(generationJob);
  const isDryRun = Boolean(log.dryRun || (shots.length > 0 && dryRunCount === shots.length));
  const pendingCount = shots.length - successCount - failedCount - dryRunCount;
  const runStatus = failedCount ? (failedCount === shots.length ? "失败" : "部分失败")
    : isDryRun && shots.length > 0 ? "dry-run通过"
      : pendingCount || dryRunCount || !shots.length ? "待检查" : "完成";
  state.manifest.stages.imageGeneration = runStatus === "完成" ? "已出图" : runStatus;
  state.manifest.generationRuns = upsertRunById(state.manifest.generationRuns, {
    runId,
    tool: log.tool || "",
    mode: isDryRun ? "dry-run" : "real-generation",
    outputDir: log.outputDir || "",
    generationLog: logPath,
    reviewBoard: reviewPath,
    generationJob: generationJob ? path.resolve(generationJob) : "",
    status: runStatus,
    shotCount: shots.length,
    failedCount,
    successCount,
    pendingCount,
    idempotencyKey: log.idempotencyKey || "",
    elapsedSeconds: log.elapsedSeconds ?? null,
    creditsUsed: log.creditsUsed ?? null,
    estimatedCost: log.estimatedCost ?? null,
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

async function ingestVideo({ projectRoot, runManifest, videoJob }) {
  if (!projectRoot) throw new Error("ingest-video requires --project-root.");
  if (!runManifest) throw new Error("ingest-video requires --run-manifest.");
  const state = await ensureProject({ projectRoot });
  const manifestPath = path.resolve(runManifest);
  const run = await readJson(manifestPath, null);
  if (!run) throw new Error(`Could not read run manifest: ${manifestPath}`);
  const now = new Date().toISOString();
  const plannedFilePath = run.outputs?.video || "";
  const videoPath = await verifiedOutput(plannedFilePath, path.dirname(manifestPath)) || "";
  const taskId = run.task?.id || run.taskId || run.externalTaskId || "";
  const runId = runIdFromOutputDir(path.dirname(manifestPath));
  const sourceImages = run.source_images || run.first_frame_or_image_refs || run.references || [];
  const source = sourceImages[0] || {};
  const shot = run.shot || run.shotNumber || source.shot || "VIDEO";
  const version = run.version || "v01";
  const tool = run.provider || run.tool || run.target_tool || run.request?.provider || run.request?.target_tool || "video";
  const toolSlug = safeName(tool, "video").toLowerCase();
  const claimedStatus = String(run.task?.status || run.status || "pending").toLowerCase();
  const claimedSuccess = ["succeeded", "success", "completed"].includes(claimedStatus);
  const status = claimedSuccess ? (videoPath ? "succeeded" : "output_missing") : claimedStatus;
  const assetState = status === "succeeded" ? "候选" : status === "manual_handoff" ? "待执行" : "待检查";
  const handle = `${shot}_${toolSlug}_${version}`;
  const asset = {
    assetId: `${handle}_${runId}`,
    handle,
    shot,
    version,
    type: "video",
    tool,
    model: run.model || run.target_model || run.request?.model || run.request?.target_model || "",
    filePath: videoPath,
    plannedFilePath,
    promptPath: run.prompt?.source || run.promptFile || run.approved_prompt_source || "",
    runManifest: manifestPath,
    videoJob: videoJob ? path.resolve(videoJob) : "",
    outputDir: path.dirname(manifestPath),
    sourceImages,
    referenceRoles: run.reference_roles || run.request?.reference_roles || [],
    audioPolicy: run.audio_policy || run.request?.audio_policy || "",
    musicPolicy: run.music_policy || run.request?.music_policy || "no_music_allow_sfx",
    taskId,
    assetState,
    status,
    idempotencyKey: run.idempotency_key || run.idempotencyKey || "",
    elapsedSeconds: run.metrics?.elapsed_seconds ?? run.elapsed_seconds ?? null,
    creditsUsed: run.metrics?.credits_used ?? run.credits_used ?? null,
    estimatedCost: run.metrics?.estimated_cost ?? run.estimated_cost ?? null,
    createdAt: now,
    updatedAt: now,
  };
  const existing = state.assetIndex.assets || [];
  const index = existing.findIndex((item) => item.assetId === asset.assetId);
  if (index >= 0) existing[index] = mergeIngestedAsset(existing[index], asset);
  else existing.push(asset);
  state.assetIndex.assets = existing;
  state.assetIndex.updatedAt = now;
  await writeJson(state.assetIndexPath, state.assetIndex);

  state.manifest.current.latestVideoRunManifest = manifestPath;
  state.manifest.current.latestVideo = videoPath;
  if (videoJob) state.manifest.current.latestVideoJob = path.resolve(videoJob);
  state.manifest.stages.videoGeneration = status === "succeeded" ? "已生成" : status === "manual_handoff" ? "待执行" : "待检查";
  state.manifest.videoRuns = upsertRunById(state.manifest.videoRuns, {
    runId,
    tool,
    outputDir: path.dirname(manifestPath),
    runManifest: manifestPath,
    videoJob: videoJob ? path.resolve(videoJob) : "",
    video: videoPath,
    taskId,
    status,
    idempotencyKey: run.idempotency_key || run.idempotencyKey || "",
    elapsedSeconds: run.metrics?.elapsed_seconds ?? run.elapsed_seconds ?? null,
    creditsUsed: run.metrics?.credits_used ?? run.credits_used ?? null,
    estimatedCost: run.metrics?.estimated_cost ?? run.estimated_cost ?? null,
    createdAt: now,
  });
  state.manifest.updatedAt = now;
  await writeJson(state.manifestPath, state.manifest);

  return {
    projectRoot: state.projectRoot,
    manifestPath: state.manifestPath,
    assetIndexPath: state.assetIndexPath,
    asset: index >= 0 ? existing[index] : asset,
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

function normalizeObservation(input, projectRoot) {
  const now = new Date().toISOString();
  const observation = {
    schema_version: 1,
    observation_id: input.observation_id || `obs_${stableHash({
      asset_id: input.asset_id,
      source_prompt: input.source_prompt,
      platform: input.platform,
      failure_type: input.failure_type,
      attempted_fix: input.attempted_fix,
      outcome: input.outcome,
      nonce: input.created_at || now,
    }).slice(0, 16)}`,
    project_root: projectRoot,
    asset_id: String(input.asset_id || "").trim(),
    source_prompt: String(input.source_prompt || "").trim(),
    platform: String(input.platform || "").trim().toLowerCase(),
    model: String(input.model || "").trim(),
    deliverable_profile: String(input.deliverable_profile || "").trim(),
    mother_library_route: String(input.mother_library_route || "").trim(),
    shot_type: String(input.shot_type || "").trim(),
    source_authority: String(input.source_authority || "").trim(),
    reference_count: Number(input.reference_count || 0),
    prompt_fingerprint: String(input.prompt_fingerprint || "").trim(),
    settings_fingerprint: String(input.settings_fingerprint || "").trim(),
    style_lock_version: String(input.style_lock_version || "").trim(),
    technical_qc_report: String(input.technical_qc_report || "").trim(),
    qc_score: input.qc_score === null || input.qc_score === undefined || input.qc_score === "" ? null : Number(input.qc_score),
    qc_decision: String(input.qc_decision || "").trim(),
    failure_type: String(input.failure_type || "none").trim().toLowerCase(),
    severity: String(input.severity || "low").trim().toLowerCase(),
    attempted_fix: String(input.attempted_fix || "none").trim(),
    outcome: String(input.outcome || "not_tested").trim().toLowerCase(),
    metrics: {
      elapsed_seconds: input.metrics?.elapsed_seconds ?? input.elapsed_seconds ?? null,
      credits_used: input.metrics?.credits_used ?? input.credits_used ?? null,
      estimated_cost: input.metrics?.estimated_cost ?? input.estimated_cost ?? null,
    },
    notes: String(input.notes || "").trim(),
    created_at: input.created_at || now,
  };
  const missing = ["asset_id", "source_prompt", "platform", "deliverable_profile", "qc_decision", "failure_type", "attempted_fix", "outcome"]
    .filter((key) => !hasUsefulValue(observation[key]));
  if (missing.length) throw new Error(`Observation missing required fields: ${missing.join(", ")}`);
  if (!new Set(["improved", "unchanged", "worse", "not_tested"]).has(observation.outcome)) {
    throw new Error("Observation outcome must be improved, unchanged, worse, or not_tested.");
  }
  return observation;
}

async function recordObservation(args) {
  if (!args.projectRoot) throw new Error("record-observation requires --project-root.");
  if (!args.input) throw new Error("record-observation requires --input.");
  const state = await ensureProject({ projectRoot: args.projectRoot });
  const input = await readJson(path.resolve(args.input), null);
  if (!input) throw new Error(`Could not read observation input: ${args.input}`);
  const observation = normalizeObservation(input.generation_observation || input, state.projectRoot);
  const observations = await readJsonLines(state.observationsPath);
  const existing = observations.find((item) => item.observation_id === observation.observation_id);
  if (!existing) await appendJsonLine(state.observationsPath, observation);

  const asset = (state.assetIndex.assets || []).find((item) => (
    item.assetId === observation.asset_id || item.asset_id === observation.asset_id || item.handle === observation.asset_id
  ));
  if (asset) {
    asset.observationIds ||= [];
    if (!asset.observationIds.includes(observation.observation_id)) asset.observationIds.push(observation.observation_id);
    asset.updatedAt = new Date().toISOString();
    state.assetIndex.updatedAt = asset.updatedAt;
    await writeJson(state.assetIndexPath, state.assetIndex);
  }

  state.manifest.current ||= {};
  state.manifest.current.generationObservations = state.observationsPath;
  state.manifest.updatedAt = new Date().toISOString();
  await writeJson(state.manifestPath, state.manifest);
  return {
    projectRoot: state.projectRoot,
    observationsPath: state.observationsPath,
    recorded: !existing,
    duplicate: Boolean(existing),
    observation: existing || observation,
  };
}

function feedbackGroupKey(observation) {
  return [
    observation.platform || "unknown",
    observation.model || "",
    observation.deliverable_profile || "unknown",
    observation.failure_type || "none",
    observation.attempted_fix || "none",
  ].join("|");
}

function summarizeObservationRows(observations, minimumEvidence) {
  const groups = new Map();
  for (const observation of observations) {
    const key = feedbackGroupKey(observation);
    const group = groups.get(key) || {
      key,
      platform: observation.platform || "unknown",
      model: observation.model || "",
      deliverable_profile: observation.deliverable_profile || "unknown",
      failure_type: observation.failure_type || "none",
      attempted_fix: observation.attempted_fix || "none",
      evidence_count: 0,
      outcomes: { improved: 0, unchanged: 0, worse: 0, not_tested: 0 },
      observation_ids: [],
    };
    group.evidence_count += 1;
    group.outcomes[observation.outcome] = (group.outcomes[observation.outcome] || 0) + 1;
    group.observation_ids.push(observation.observation_id);
    groups.set(key, group);
  }
  const summaries = [...groups.values()].map((group) => {
    const tested = group.outcomes.improved + group.outcomes.unchanged + group.outcomes.worse;
    return {
      ...group,
      improvement_rate: tested ? Number((group.outcomes.improved / tested).toFixed(4)) : 0,
    };
  }).sort((a, b) => b.evidence_count - a.evidence_count || a.key.localeCompare(b.key));
  const promotionProposals = summaries.filter((group) => (
    group.evidence_count >= minimumEvidence
      && group.outcomes.improved >= 2
      && group.improvement_rate >= (2 / 3)
      && group.outcomes.worse === 0
  )).map((group) => ({
    proposal_id: `proposal_${stableHash(group.key).slice(0, 12)}`,
    status: "needs_human_confirmation",
    scope: {
      platform: group.platform,
      model: group.model,
      deliverable_profile: group.deliverable_profile,
      failure_type: group.failure_type,
    },
    proposed_rule: group.attempted_fix,
    evidence_count: group.evidence_count,
    improvement_rate: group.improvement_rate,
    observation_ids: group.observation_ids,
    must_not_auto_modify: ["style-lock.json", "mother_library_application_packet", "global project context"],
  }));
  return { summaries, promotionProposals };
}

async function summarizeFeedback(args) {
  if (!args.projectRoot) throw new Error("summarize-feedback requires --project-root.");
  const paths = projectPaths(path.resolve(args.projectRoot));
  const observations = await readJsonLines(paths.observationsPath);
  const minimumEvidence = Math.max(2, Number(args.minimumEvidence || 3));
  const { summaries, promotionProposals } = summarizeObservationRows(observations, minimumEvidence);
  const performanceMap = new Map();
  for (const observation of observations) {
    const key = [observation.platform || "unknown", observation.model || "", observation.deliverable_profile || "unknown"].join("|");
    const row = performanceMap.get(key) || {
      key,
      platform: observation.platform || "unknown",
      model: observation.model || "",
      deliverable_profile: observation.deliverable_profile || "unknown",
      observations: 0,
      improved: 0,
      worse: 0,
      elapsed_seconds_total: 0,
      credits_used_total: 0,
      estimated_cost_total: 0,
      qc_score_total: 0,
      qc_score_count: 0,
    };
    row.observations += 1;
    if (observation.outcome === "improved") row.improved += 1;
    if (observation.outcome === "worse") row.worse += 1;
    row.elapsed_seconds_total += Number(observation.metrics?.elapsed_seconds || 0);
    row.credits_used_total += Number(observation.metrics?.credits_used || 0);
    row.estimated_cost_total += Number(observation.metrics?.estimated_cost || 0);
    if (Number.isFinite(observation.qc_score)) {
      row.qc_score_total += observation.qc_score;
      row.qc_score_count += 1;
    }
    performanceMap.set(key, row);
  }
  const platformPerformance = [...performanceMap.values()].map((row) => ({
    ...row,
    average_elapsed_seconds: row.observations ? Number((row.elapsed_seconds_total / row.observations).toFixed(3)) : null,
    average_estimated_cost: row.observations ? Number((row.estimated_cost_total / row.observations).toFixed(4)) : null,
    average_qc_score: row.qc_score_count ? Number((row.qc_score_total / row.qc_score_count).toFixed(3)) : null,
  }));
  const result = {
    schema_version: 1,
    project_root: paths.projectRoot,
    generated_at: new Date().toISOString(),
    minimum_evidence: minimumEvidence,
    observation_count: observations.length,
    groups: summaries,
    platform_performance: platformPerformance,
    promotion_proposals: promotionProposals,
  };
  if (!args.checkOnly) {
    await writeJson(paths.feedbackSummaryPath, result);
    const manifest = await readJson(paths.manifestPath, null);
    if (manifest) {
      manifest.current ||= {};
      manifest.current.generationFeedbackSummary = paths.feedbackSummaryPath;
      manifest.updatedAt = new Date().toISOString();
      await writeJson(paths.manifestPath, manifest);
    }
  }
  return { ...result, feedback_summary_path: args.checkOnly ? "" : paths.feedbackSummaryPath };
}

async function auditProject(args) {
  if (!args.projectRoot) throw new Error("audit requires --project-root.");
  const root = path.resolve(args.projectRoot);
  const paths = projectPaths(root);
  const failures = [];
  const warnings = [];
  const manifest = await readJson(paths.manifestPath, null);
  if (!manifest) failures.push("missing project-manifest.json");
  const declaredRoot = manifest?.project_root || manifest?.projectRoot || "";
  if (declaredRoot && path.resolve(declaredRoot).toLowerCase() !== root.toLowerCase()) {
    failures.push(`manifest project root mismatch: ${declaredRoot}`);
  }
  const assetIndex = await readJson(paths.assetIndexPath, null);
  if (!assetIndex) warnings.push("missing asset-index.json");
  else if (!Array.isArray(assetIndex.assets)) failures.push("asset-index.json assets must be an array");

  const registryPointer = manifest?.current?.thread_registry
    || manifest?.current?.threadRegistry
    || manifest?.workflow?.thread_orchestration?.registry
    || "";
  let registry = null;
  let registryPath = "";
  if (registryPointer) {
    registryPath = path.resolve(root, registryPointer);
    if (!isInsideRoot(root, registryPath)) failures.push("thread registry pointer escapes project root");
    else registry = await readJson(registryPath, null);
    if (!registry) failures.push("thread registry pointer is missing or invalid");
  }
  const allowedStatuses = new Set(["queued", "active", "waiting_user", "blocked", "ready_for_review", "accepted", "stale", "archived"]);
  const seenTaskIds = new Set();
  for (const task of registry?.tasks || []) {
    if (!task.task_id || seenTaskIds.has(task.task_id)) failures.push(`duplicate or missing task_id: ${task.task_id || "<empty>"}`);
    seenTaskIds.add(task.task_id);
    if (!allowedStatuses.has(task.status)) failures.push(`${task.task_id}: invalid status ${task.status}`);
    for (const field of ["task_workspace", "task_packet_path", "handoff_path"]) {
      if (!task[field]) continue;
      const target = path.resolve(root, task[field]);
      if (!isInsideRoot(root, target)) failures.push(`${task.task_id}: ${field} escapes project root`);
    }
    const packetPath = task.task_packet_path ? path.resolve(root, task.task_packet_path) : "";
    if (packetPath && !(await exists(packetPath))) warnings.push(`${task.task_id}: missing task packet`);
    const handoffPath = task.handoff_path ? path.resolve(root, task.handoff_path) : "";
    if (["ready_for_review", "accepted", "archived"].includes(task.status) && handoffPath && !(await exists(handoffPath))) {
      failures.push(`${task.task_id}: ${task.status} task missing handoff`);
    }
  }
  return {
    valid: failures.length === 0,
    read_only: true,
    project_root: root,
    project_name: manifest?.project_name || manifest?.projectName || manifest?.project || path.basename(root),
    manifest_path: paths.manifestPath,
    asset_index_path: paths.assetIndexPath,
    thread_registry_path: registryPath,
    task_count: registry?.tasks?.length || 0,
    asset_count: assetIndex?.assets?.length || 0,
    failures,
    warnings,
  };
}

function hasUsefulValue(value) {
  if (Array.isArray(value)) return value.length > 0;
  if (typeof value === "string") return value.trim() !== "" && !value.includes("待填写");
  if (value && typeof value === "object") return Object.keys(value).length > 0;
  return Boolean(value);
}

function normalizePlatformName(value) {
  return String(value || "").trim().toLowerCase();
}

function generationPacketTargets(packet) {
  const sourcePacket = packet?.video_prompt_source_packet || {};
  const auditPacket = packet?.audited_prompt_packet || {};
  const legacyVideoPacket = packet?.video_platform_prompt_packet || {};
  return [
    packet?.target_tool,
    packet?.platform_target,
    packet?.target_platform,
    packet?.target_model,
    sourcePacket.platform_target,
    sourcePacket.target_model,
    auditPacket.platform_target,
    legacyVideoPacket.target_platform,
    legacyVideoPacket.target_model,
  ].map(normalizePlatformName).filter(Boolean);
}

function isVideoGenerationPacket(packet) {
  const names = generationPacketTargets(packet);
  return names.some((name) => (
    name.includes("jimeng")
      || name.includes("即梦")
      || name.includes("seedance")
      || name.includes("ark")
      || name.includes("kling")
      || name.includes("可灵")
  ));
}

function isKlingOmniPacket(packet) {
  const names = generationPacketTargets(packet);
  return names.some((name) => (
    name.includes("o1")
      || name.includes("omni")
      || name.includes("omini")
      || name.includes("video 3.0")
      || name.includes("video_3.0")
  ));
}

function firstUseful(...values) {
  return values.find((value) => hasUsefulValue(value));
}

function generationReadyMissingFields(generationPacket) {
  const missing = [];
  const sourcePacket = generationPacket?.video_prompt_source_packet || {};
  const auditPacket = generationPacket?.audited_prompt_packet || {};
  const legacyVideoPacket = generationPacket?.video_platform_prompt_packet || {};
  const auditStatus = String(generationPacket?.audit_status || "");

  if (!firstUseful(
    generationPacket?.target_tool,
    generationPacket?.platform_target,
    generationPacket?.target_platform,
    sourcePacket.platform_target,
    auditPacket.platform_target,
    legacyVideoPacket.target_platform,
  )) {
    missing.push("target-tool");
  }
  if (!hasUsefulValue(generationPacket?.deliverable_profile)) missing.push("deliverable-profile");
  if (!hasUsefulValue(generationPacket?.final_prompt)) missing.push("final-prompt");
  if (!["通过", "保效精简后通过", "approved", "passed"].includes(auditStatus)) missing.push("audit-status");

  if (isVideoGenerationPacket(generationPacket)) {
    const taskType = firstUseful(generationPacket.task_type, sourcePacket.task_type, legacyVideoPacket.task_type);
    if (!hasUsefulValue(taskType)) missing.push("task-type");
    if (!firstUseful(generationPacket.complexity_mode, sourcePacket.complexity_mode)) missing.push("complexity-mode");
    if (!firstUseful(generationPacket.duration, sourcePacket.duration, legacyVideoPacket.duration)) missing.push("duration");
    if (!firstUseful(generationPacket.ratio, sourcePacket.ratio, legacyVideoPacket.ratio)) missing.push("ratio");
    if (!firstUseful(generationPacket.ending_behavior, sourcePacket.ending_behavior)) missing.push("ending-behavior");

    const taskTypeText = normalizePlatformName(taskType);
    const sourceAuthority = firstUseful(generationPacket.source_authority, sourcePacket.source_authority);
    const isTextOnly = taskTypeText === "t2v"
      || taskTypeText.includes("text")
      || normalizePlatformName(sourceAuthority) === "text_only";
    const hasReference = firstUseful(
      generationPacket.first_frame_or_image_refs,
      generationPacket.first_frame_or_reference,
      generationPacket.reference_roles,
      sourcePacket.first_frame_or_reference,
      sourcePacket.reference_roles,
      legacyVideoPacket.first_frame_or_reference,
      legacyVideoPacket.reference_roles,
    );
    if (!isTextOnly && !hasReference) missing.push("first-frame-or-reference");

    if (isKlingOmniPacket(generationPacket) && !firstUseful(
      generationPacket.kling_omni_reference_role_map,
      sourcePacket.kling_omni_reference_role_map,
      legacyVideoPacket.kling_omni_reference_role_map,
    )) {
      missing.push("kling-omni-reference-role-map");
    }
  }

  const requiresMotherLibrary = generationPacket?.requires_mother_library === true
    || sourcePacket?.requires_mother_library === true;
  if (requiresMotherLibrary && !firstUseful(
    generationPacket?.mother_library_application_packet,
    sourcePacket.mother_library_application_packet,
    legacyVideoPacket.mother_library_application_packet,
  )) {
    missing.push("mother-library-application-packet");
  }

  return missing;
}

async function readTextIfExists(filePath) {
  if (!(await exists(filePath))) return "";
  return fs.readFile(filePath, "utf8");
}

function textHasApprovedStatus(text, allowedStatuses) {
  let fence = null;
  for (const line of text.replace(/^\uFEFF/, "").split(/\r?\n/)) {
    const marker = line.match(/^ {0,3}(`{3,}|~{3,})/);
    if (marker) {
      if (!fence) fence = marker[1];
      else if (marker[1][0] === fence[0] && marker[1].length >= fence.length) fence = null;
      continue;
    }
    if (fence) continue;
    // Only current document metadata counts; examples and historical sections do not.
    if (/^ {0,3}#{2,6}\s/.test(line)) break;
    const match = line.match(/^ {0,3}status:\s*(.+)$/i);
    if (match) return allowedStatuses.includes(match[1].trim().toLowerCase());
  }
  return false;
}

async function checkShortDramaGeneration(paths, manifest) {
  const stateFiles = manifest?.gates?.generation?.stateFiles || shortDramaStatePaths(paths.projectRoot);
  const gates = {};
  const missingFields = [];

  const intake = await readJson(stateFiles.projectIntake, null);
  const intakePacket = intake?.project_intake_packet;
  gates.projectIntake = Boolean(
    intakePacket
      && intakePacket.project_tier === "formal"
      && intakePacket.main_line === "short_drama_story"
      && Array.isArray(intakePacket.missing_fields)
      && intakePacket.missing_fields.length === 0,
  );
  if (!gates.projectIntake) missingFields.push("project-intake");

  const styleLock = await readJson(stateFiles.styleLock, null);
  const stylePacket = styleLock?.style_lock_packet;
  gates.styleLock = Boolean(
    stylePacket?.status === "approved"
      && hasUsefulValue(stylePacket.style_id)
      && hasUsefulValue(stylePacket.master_style_sentence)
      && hasUsefulValue(stylePacket.mother_library_application_packet)
      && hasUsefulValue(stylePacket.upstream_source),
  );
  if (!gates.styleLock) missingFields.push("style-lock");

  const sceneMapText = await readTextIfExists(stateFiles.sceneMap);
  gates.sceneMap = textHasApprovedStatus(sceneMapText, ["approved", "complete"]);
  if (!gates.sceneMap) missingFields.push("scene-map");

  const shotAuditText = await readTextIfExists(stateFiles.shotAudit);
  gates.shotAudit = textHasApprovedStatus(shotAuditText, ["passed", "approved"]);
  if (!gates.shotAudit) missingFields.push("shot-audit");

  const promptAuditText = await readTextIfExists(stateFiles.promptAudit);
  gates.promptAudit = textHasApprovedStatus(promptAuditText, ["通过", "保效精简后通过", "approved", "passed"]);
  if (!gates.promptAudit) missingFields.push("prompt-audit");

  const generationReady = await readJson(stateFiles.generationReady, null);
  const generationPacket = generationReady?.generation_ready_packet;
  const generationReadyMissing = generationPacket ? generationReadyMissingFields(generationPacket) : ["generation-ready-packet"];
  gates.generationReady = generationReadyMissing.length === 0;
  if (!gates.generationReady) missingFields.push("generation-ready");

  const routeMap = {
    "project-intake": "zongkong",
    "style-lock": "project-style-lock",
    "scene-map": "scene-style-map-director",
    "shot-audit": "shot-language-auditor",
    "prompt-audit": "prompt-platform-auditor",
    "generation-ready": "project-state-manager",
  };
  const routeBackTo = missingFields.length ? routeMap[missingFields[0]] : "";
  return {
    ready: missingFields.length === 0,
    missingFields,
    routeBackTo,
    currentState: {
      projectRoot: paths.projectRoot,
      workflow: manifest?.workflow || null,
      stage: "generation",
      gates,
      generationReadyMissingFields: generationReadyMissing,
      stateFiles,
    },
  };
}

async function checkProject(args) {
  if (!args.projectRoot) throw new Error("check requires --project-root.");
  const stage = String(args.stage || "generation").toLowerCase();
  if (stage !== "generation") throw new Error("Only --stage generation is currently supported.");
  const paths = projectPaths(path.resolve(args.projectRoot));
  const manifest = await readJson(paths.manifestPath, null);
  if (manifest?.workflow?.type !== "short-drama") {
    return {
      ready: false,
      missingFields: ["short-drama-workflow"],
      routeBackTo: "project-state-manager",
      currentState: {
        projectRoot: paths.projectRoot,
        workflow: manifest?.workflow || null,
        stage,
        gates: {},
        stateFiles: {},
      },
    };
  }
  return checkShortDramaGeneration(paths, manifest);
}

async function main() {
  const args = parseArgs(process.argv);
  let result;
  if (args.command === "init") {
    if (!args.projectName && !args.projectRoot) throw new Error("init requires --project-name or --project-root.");
    result = await ensureProject({
      projectName: args.projectName,
      projectRoot: args.projectRoot,
      workflow: args.workflow,
      route: args.route,
      projectTier: args.projectTier,
    });
    result = {
      projectRoot: result.projectRoot,
      manifestPath: result.manifestPath,
      assetIndexPath: result.assetIndexPath,
      styleLockPath: result.styleLockPath,
      jobsDir: result.jobsDir,
      generationRunsDir: result.generationRunsDir,
      videoRunsDir: result.videoRunsDir,
      reviewDir: result.reviewDir,
      revisionLogsDir: result.revisionLogsDir,
      briefsDir: result.briefsDir,
      promptsDir: result.promptsDir,
      referencesDir: result.referencesDir,
      shortDrama: result.shortDrama || null,
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
  } else if (args.command === "ingest-video") {
    result = await ingestVideo({
      projectRoot: args.projectRoot,
      runManifest: args.runManifest,
      videoJob: args.videoJob,
    });
  } else if (args.command === "find-asset") {
    result = await findAsset(args);
  } else if (args.command === "record-observation") {
    result = await recordObservation(args);
  } else if (args.command === "summarize-feedback") {
    result = await summarizeFeedback(args);
  } else if (args.command === "audit") {
    result = await auditProject(args);
  } else if (args.command === "check") {
    result = await checkProject(args);
  } else {
    throw new Error(`Unknown command: ${args.command}`);
  }
  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
