import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const DEFAULT_PROJECTS_DIR = "H:\\yingshi\\projects";
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = path.resolve(SCRIPT_DIR, "..");
const SHORT_DRAMA_TEMPLATE_DIR = path.join(SKILL_DIR, "templates", "short-drama");
const SHORT_DRAMA_ROUTES = new Set(["storyboard-execution", "full-development", "quick-test"]);

const SHORT_DRAMA_STATE_FILES = {
  projectIntake: "project-intake.json",
  hookAudit: path.join("references", "hook-audit.md"),
  characterContinuity: path.join("references", "character-continuity.md"),
  styleLock: "style-lock.json",
  sceneMap: path.join("references", "scene-map.md"),
  shotAudit: path.join("references", "shot-audit.md"),
  promptAudit: path.join("prompts", "prompt-audit.md"),
  generationReady: path.join("generation-jobs", "generation-ready.json"),
  qcFeedback: path.join("revision-logs", "qc-feedback.md"),
};

function parseArgs(argv) {
  const [command, ...rest] = argv.slice(2);
  if (!command) throw new Error("Missing command: init, create-job, ingest, ingest-video, find-asset, or check.");
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
    continuityBoardsDir: path.join(projectRoot, "references", "continuity-boards"),
    styleLockPath: path.join(projectRoot, "style-lock.json"),
  };
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
    ["hook-audit-template.md", stateFiles.hookAudit],
    ["character-continuity-template.md", stateFiles.characterContinuity],
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
      "hook-audit",
      "character-continuity",
      "mother-library-application",
      "director-contribution",
      "visual-helpfulness",
      "style-lock",
      "scene-map",
      "shot-audit",
      "prompt-audit",
      "generation-ready",
    ],
    stateFiles,
    routeBackOrder: [
      "zongkong",
      "short-drama-episode-writer",
      "short-drama-character-bible",
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
  state.manifest.current.hookAudit = stateFiles.hookAudit;
  state.manifest.current.characterContinuity = stateFiles.characterContinuity;
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
  await fs.mkdir(paths.continuityBoardsDir, { recursive: true });

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
    promptMode: args.promptMode || input.promptMode || input.bananaPromptMode || (tool === "banana" ? "compact" : ""),
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

async function ingestVideo({ projectRoot, runManifest, videoJob }) {
  if (!projectRoot) throw new Error("ingest-video requires --project-root.");
  if (!runManifest) throw new Error("ingest-video requires --run-manifest.");
  const state = await ensureProject({ projectRoot });
  const manifestPath = path.resolve(runManifest);
  const run = await readJson(manifestPath, null);
  if (!run) throw new Error(`Could not read run manifest: ${manifestPath}`);
  const now = new Date().toISOString();
  const videoPath = run.outputs?.video || "";
  const taskId = run.task?.id || run.taskId || run.externalTaskId || "";
  const runId = runIdFromOutputDir(path.dirname(manifestPath));
  const sourceImages = run.source_images || run.first_frame_or_image_refs || run.references || [];
  const source = sourceImages[0] || {};
  const shot = run.shot || run.shotNumber || source.shot || "VIDEO";
  const version = run.version || "v01";
  const tool = run.provider || run.tool || run.target_tool || run.request?.provider || run.request?.target_tool || "video";
  const toolSlug = safeName(tool, "video").toLowerCase();
  const status = run.task?.status || run.status || (videoPath ? "succeeded" : "manual_handoff");
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
    promptPath: run.prompt?.source || run.promptFile || run.approved_prompt_source || "",
    runManifest: manifestPath,
    videoJob: videoJob ? path.resolve(videoJob) : "",
    outputDir: path.dirname(manifestPath),
    sourceImages,
    referenceRoles: run.reference_roles || run.request?.reference_roles || [],
    audioPolicy: run.audio_policy || run.request?.audio_policy || "",
    taskId,
    assetState,
    status,
    createdAt: now,
    updatedAt: now,
  };
  const existing = state.assetIndex.assets || [];
  const index = existing.findIndex((item) => item.assetId === asset.assetId);
  if (index >= 0) existing[index] = { ...existing[index], ...asset };
  else existing.push(asset);
  state.assetIndex.assets = existing;
  state.assetIndex.updatedAt = now;
  await writeJson(state.assetIndexPath, state.assetIndex);

  state.manifest.current.latestVideoRunManifest = manifestPath;
  state.manifest.current.latestVideo = videoPath;
  if (videoJob) state.manifest.current.latestVideoJob = path.resolve(videoJob);
  state.manifest.stages.videoGeneration = status === "succeeded" ? "已生成" : status === "manual_handoff" ? "待执行" : "待检查";
  state.manifest.videoRuns ||= [];
  state.manifest.videoRuns.push({
    runId,
    tool,
    outputDir: path.dirname(manifestPath),
    runManifest: manifestPath,
    videoJob: videoJob ? path.resolve(videoJob) : "",
    video: videoPath,
    taskId,
    status,
    createdAt: now,
  });
  state.manifest.updatedAt = now;
  await writeJson(state.manifestPath, state.manifest);

  return {
    projectRoot: state.projectRoot,
    manifestPath: state.manifestPath,
    assetIndexPath: state.assetIndexPath,
    asset,
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

function hasUsefulValue(value) {
  if (Array.isArray(value)) return value.some((item) => hasUsefulValue(item));
  if (typeof value === "string") return value.trim() !== "" && !isPlaceholderString(value);
  if (value && typeof value === "object") return Object.values(value).some((item) => hasUsefulValue(item));
  return Boolean(value);
}

function isPlaceholderString(value) {
  const text = String(value || "").trim().toLowerCase();
  if (!text) return true;
  return [
    "__fill__",
    "__project_",
    "tbd",
    "todo",
    "待填",
    "待填写",
    "待补",
    "寰呭",
    "draft only",
  ].some((marker) => text.includes(marker));
}

function textHasPlaceholder(text) {
  return isPlaceholderString(text)
    || /(^|\b)(TBD|TODO|__FILL__)(\b|$)/i.test(text)
    || text.includes("待填")
    || text.includes("待填写")
    || text.includes("待补")
    || text.includes("寰呭");
}

function textHasTerms(text, terms) {
  return terms.every((term) => text.includes(term));
}

function normalizePlatformName(value) {
  return String(value || "").trim().toLowerCase();
}

function generationPacketTargets(packet) {
  const videoPacket = packet?.video_platform_prompt_packet || {};
  return [
    packet?.target_tool,
    packet?.target_platform,
    packet?.target_model,
    videoPacket.target_platform,
    videoPacket.target_model,
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
  const videoPacket = generationPacket?.video_platform_prompt_packet || {};
  const auditStatus = String(generationPacket?.audit_status || "");

  if (!firstUseful(generationPacket?.target_tool, generationPacket?.target_platform, videoPacket.target_platform)) {
    missing.push("target-tool");
  }
  if (!hasUsefulValue(generationPacket?.final_prompt)) missing.push("final-prompt");
  if (!["通过", "保效精简后通过", "approved", "passed"].includes(auditStatus)) missing.push("audit-status");
  if (!hasUsefulValue(generationPacket?.short_drama_hook_packet)) missing.push("short-drama-hook-packet");
  if (!hasUsefulValue(generationPacket?.character_continuity_lock)) missing.push("character-continuity-lock");

  if (isVideoGenerationPacket(generationPacket)) {
    const taskType = firstUseful(generationPacket.task_type, videoPacket.task_type);
    if (!hasUsefulValue(taskType)) missing.push("task-type");
    if (!firstUseful(generationPacket.duration, videoPacket.duration)) missing.push("duration");
    if (!firstUseful(generationPacket.ratio, videoPacket.ratio)) missing.push("ratio");
    if (!firstUseful(generationPacket.audio_policy, videoPacket.audio_policy)) missing.push("audio-policy");

    const taskTypeText = normalizePlatformName(taskType);
    const isTextOnly = taskTypeText === "t2v" || taskTypeText.includes("text");
    const hasReference = firstUseful(
      generationPacket.first_frame_or_image_refs,
      generationPacket.first_frame_or_reference,
      generationPacket.reference_roles,
      videoPacket.first_frame_or_reference,
      videoPacket.reference_roles,
    );
    if (!isTextOnly && !hasReference) missing.push("first-frame-or-reference");

    if (isKlingOmniPacket(generationPacket) && !firstUseful(
      generationPacket.kling_omni_reference_role_map,
      videoPacket.kling_omni_reference_role_map,
    )) {
      missing.push("kling-omni-reference-role-map");
    }
  }

  const requiresSameSceneCoverage = Boolean(
    generationPacket?.requires_same_scene_coverage
      || videoPacket.requires_same_scene_coverage
      || generationPacket?.coverage_type
      || videoPacket.coverage_type,
  );
  if (requiresSameSceneCoverage) {
    if (!firstUseful(generationPacket.scene_continuity_lock, videoPacket.scene_continuity_lock)) {
      missing.push("scene-continuity-lock");
    }
    if (!firstUseful(generationPacket.background_continuity_lock, videoPacket.background_continuity_lock)) {
      missing.push("background-continuity-lock");
    }
    if (!firstUseful(generationPacket.continuity_reference_board, videoPacket.continuity_reference_board)) {
      missing.push("continuity-reference-board");
    }
  }

  if (!firstUseful(
    generationPacket?.mother_library_application_packet,
    videoPacket.mother_library_application_packet,
  )) {
    missing.push("mother-library-application-packet");
  }
  if (!firstUseful(
    generationPacket?.director_contribution_packet,
    videoPacket.director_contribution_packet,
  )) {
    missing.push("director-contribution-packet");
  }
  if (!firstUseful(
    generationPacket?.visual_helpfulness_check,
    videoPacket.visual_helpfulness_check,
  )) {
    missing.push("visual-helpfulness-check");
  }

  return missing;
}

async function readTextIfExists(filePath) {
  if (!(await exists(filePath))) return "";
  return fs.readFile(filePath, "utf8");
}

function textHasApprovedStatus(text, allowedStatuses) {
  return text.split(/\r?\n/).some((line) => {
    const match = line.trim().toLowerCase().match(/^status:\s*(.+)$/);
    return match && allowedStatuses.includes(match[1].trim());
  });
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

  const hookAuditText = await readTextIfExists(stateFiles.hookAudit);
  gates.hookAudit = textHasApprovedStatus(hookAuditText, ["passed", "approved"])
    && !textHasPlaceholder(hookAuditText)
    && textHasTerms(hookAuditText, ["hook_audit_packet", "opening_hook", "audience_question"]);
  if (!gates.hookAudit) missingFields.push("hook-audit");

  const characterContinuityText = await readTextIfExists(stateFiles.characterContinuity);
  gates.characterContinuity = textHasApprovedStatus(characterContinuityText, ["passed", "approved"])
    && !textHasPlaceholder(characterContinuityText)
    && textHasTerms(characterContinuityText, ["character_continuity_packet", "generation_anchor", "director_contribution_packet", "visual_helpfulness_targets", "forbidden_drift"]);
  if (!gates.characterContinuity) missingFields.push("character-continuity");

  const styleLock = await readJson(stateFiles.styleLock, null);
  const stylePacket = styleLock?.style_lock_packet;
  gates.styleLock = Boolean(
    stylePacket?.status === "approved"
      && hasUsefulValue(stylePacket.style_id)
      && hasUsefulValue(stylePacket.master_style_sentence)
      && hasUsefulValue(stylePacket.mother_library_application_packet)
      && hasUsefulValue(stylePacket.director_contribution_packet)
      && hasUsefulValue(stylePacket.visual_helpfulness_targets)
      && hasUsefulValue(stylePacket.short_drama_hook_packet_source)
      && hasUsefulValue(stylePacket.character_continuity_source)
      && hasUsefulValue(stylePacket.upstream_source),
  );
  if (!gates.styleLock) missingFields.push("style-lock");

  const sceneMapText = await readTextIfExists(stateFiles.sceneMap);
  gates.sceneMap = textHasApprovedStatus(sceneMapText, ["approved", "complete"])
    && !textHasPlaceholder(sceneMapText)
    && textHasTerms(sceneMapText, [
      "hook_audit_source",
      "character_continuity_source",
      "mother_library_translation",
      "director_contribution_packet",
      "visual_helpfulness_targets",
      "generation_risk_split",
    ]);
  if (!gates.sceneMap) missingFields.push("scene-map");

  const shotAuditText = await readTextIfExists(stateFiles.shotAudit);
  gates.shotAudit = textHasApprovedStatus(shotAuditText, ["passed", "approved"])
    && !textHasPlaceholder(shotAuditText)
    && textHasTerms(shotAuditText, ["shot_function", "edit_motivation", "director_contribution_packet", "visual_helpfulness_targets", "breath_tail_rule", "handoff_to_prompt"]);
  if (!gates.shotAudit) missingFields.push("shot-audit");

  const promptAuditText = await readTextIfExists(stateFiles.promptAudit);
  gates.promptAudit = textHasApprovedStatus(promptAuditText, ["通过", "保效精简后通过", "approved", "passed"])
    && !textHasPlaceholder(promptAuditText)
    && textHasTerms(promptAuditText, [
      "hook_audit_packet",
      "character_continuity_lock",
      "mother_library_application_packet",
      "director_contribution_packet",
      "visual_helpfulness_check",
      "source_lock",
    ]);
  if (!gates.promptAudit) missingFields.push("prompt-audit");

  const generationReady = await readJson(stateFiles.generationReady, null);
  const generationPacket = generationReady?.generation_ready_packet;
  const generationReadyMissing = generationPacket ? generationReadyMissingFields(generationPacket) : ["generation-ready-packet"];
  gates.generationReady = generationReadyMissing.length === 0;
  if (!gates.generationReady) missingFields.push("generation-ready");

  const routeMap = {
    "project-intake": "zongkong",
    "hook-audit": "short-drama-episode-writer",
    "character-continuity": "short-drama-character-bible",
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
      continuityBoardsDir: result.continuityBoardsDir,
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
