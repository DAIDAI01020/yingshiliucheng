import { spawnSync } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  completeRun,
  computeIdempotencyKey,
  failRun,
  latestRun,
  preflightRun,
  startRun,
  submitRun,
} from "../../project-state-manager/scripts/generation-run-ledger.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillDir = path.dirname(__dirname);
const skillsRoot = path.dirname(skillDir);
const seedanceRunner = path.join(skillsRoot, "seedance-2-video", "scripts", "seedance_task.mjs");
const dreaminaRunner = path.join(skillsRoot, "dreamina-cli", "scripts", "dreamina_runner.mjs");
const stateManager = path.join(skillsRoot, "project-state-manager", "scripts", "manage-project-state.mjs");
const DEFAULT_EXTERNAL_AUDIO_POLICY = "不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白。";

function parseArgs(argv) {
  const args = { provider: "seedance", duration: "5", resolution: "720p", videoMode: "firstFrame" };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith("--")) throw new Error(`Unknown argument: ${arg}`);
    const key = arg.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) args[key] = true;
    else {
      args[key] = next;
      i += 1;
    }
  }
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

function timestamp() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}_${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
}

function safeName(value, fallback = "video") {
  return String(value || fallback)
    .trim()
    .replace(/[<>:"/\\|?*\u0000-\u001f]/g, "_")
    .replace(/\s+/g, "_")
    .slice(0, 80) || fallback;
}

function normalizeProvider(value) {
  return String(value || "seedance").trim().toLowerCase();
}

function providerSlug(value) {
  return safeName(String(value || "video").replace(/[\/\\]+/g, "_"), "video").toLowerCase();
}

function isManualVideoProvider(provider) {
  return provider.includes("jimeng-manual")
    || provider.includes("kling")
    || provider.includes("可灵");
}

function isDreaminaLiveProvider(provider) {
  return ["jimeng", "jimeng-cli", "dreamina", "dreamina-cli", "即梦"].includes(provider);
}

function dreaminaSubcommand(args) {
  if (args.dreaminaCommand) return String(args.dreaminaCommand);
  if (args.firstFrame && args.lastFrame) return "frames2video";
  if (args.imageFile || args.imageUrl || args.firstFrame) return "image2video";
  return "text2video";
}

function firstVideoPath(paths = []) {
  return paths.find((filePath) => /\.(mp4|mov|webm|mkv)$/i.test(String(filePath))) || "";
}

function runNode(scriptPath, args, env = process.env) {
  const result = spawnSync(process.execPath, [scriptPath, ...args], {
    cwd: path.dirname(scriptPath),
    env,
    encoding: "utf8",
    maxBuffer: 1024 * 1024 * 50,
  });
  if (result.status !== 0) {
    const detail = [result.stderr, result.stdout].filter(Boolean).join("\n").trim();
    throw new Error(detail || `Command failed: node ${scriptPath}`);
  }
  return result.stdout.trim();
}

function parseJsonFromOutput(output) {
  const text = output.trim();
  const start = text.lastIndexOf("{");
  if (start >= 0) {
    try {
      return JSON.parse(text.slice(start));
    } catch {
      // Fall through.
    }
  }
  return {};
}

async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

async function readText(filePath) {
  return fs.readFile(filePath, "utf8");
}

function parseMaybeJson(value, fallback = value || "") {
  if (!value) return fallback;
  try {
    return JSON.parse(value);
  } catch {
    return fallback;
  }
}

async function maybeReadJsonArg(value) {
  if (!value) return [];
  const resolved = path.resolve(String(value));
  if (await exists(resolved)) {
    return JSON.parse(await fs.readFile(resolved, "utf8"));
  }
  return parseMaybeJson(value, value);
}

async function ingestManualVideoRun({ args, provider, promptText, idempotencyKey, startedAt }) {
  const projectRoot = args.projectRoot ? path.resolve(args.projectRoot) : "";
  const shot = safeName(args.shot || path.basename(args.promptFile, path.extname(args.promptFile)), "video");
  const version = args.version || "v01";
  const slug = providerSlug(provider);
  const outputDir = args.outputDir
    ? path.resolve(args.outputDir)
    : projectRoot
      ? path.join(projectRoot, "video-runs", `${shot}_${timestamp()}_${slug}`)
      : path.join("H:\\yingshi\\outputs", `${slug}-${shot}-${timestamp()}`);

  await fs.mkdir(outputDir, { recursive: true });
  const promptCopyPath = path.join(outputDir, "approved_prompt.txt");
  await fs.writeFile(promptCopyPath, promptText, "utf8");

  const referenceRoles = await maybeReadJsonArg(args.referenceRoles);
  const firstFrameRefs = [];
  if (args.imageUrl) firstFrameRefs.push({ type: "url", url: args.imageUrl });
  if (args.imageFile) firstFrameRefs.push({ type: "file", path: path.resolve(args.imageFile) });
  const outputVideo = args.outputVideo ? path.resolve(args.outputVideo) : "";
  const status = args.status || (outputVideo ? "succeeded" : "manual_handoff");
  const audioPolicy = args.audioPolicy || DEFAULT_EXTERNAL_AUDIO_POLICY;
  const musicPolicy = args.musicPolicy || "no_music_allow_sfx";
  const runManifest = path.join(outputDir, "run_manifest.json");
  const manifest = {
    schemaVersion: 1,
    provider,
    tool: provider,
    target_tool: args.targetTool || provider,
    target_model: args.targetModel || args.model || "",
    prompt_direction: args.promptDirection || "",
    shot,
    version,
    status,
    idempotency_key: idempotencyKey,
    prompt: {
      source: path.resolve(args.promptFile),
      copy: promptCopyPath,
      text: promptText,
    },
    request: {
      provider,
      target_tool: args.targetTool || provider,
      target_model: args.targetModel || args.model || "",
      prompt_direction: args.promptDirection || "",
      task_type: args.taskType || "",
      duration: String(args.duration || ""),
      ratio: args.ratio || "",
      audio_policy: audioPolicy,
      music_policy: musicPolicy,
      reference_roles: referenceRoles,
    },
    source_images: firstFrameRefs,
    first_frame_or_image_refs: firstFrameRefs,
    reference_roles: referenceRoles,
    audio_policy: audioPolicy,
    music_policy: musicPolicy,
    task: {
      id: args.taskId || "",
      status,
    },
    outputs: {
      video: outputVideo,
    },
    metrics: {
      elapsed_seconds: Number(((Date.now() - startedAt) / 1000).toFixed(3)),
      credits_used: args.creditsUsed ? Number(args.creditsUsed) : null,
      estimated_cost: args.estimatedCost ? Number(args.estimatedCost) : null,
    },
    notes: args.notes || "Manual/external video platform handoff. Upload references according to reference_roles before copying the approved prompt.",
    createdAt: new Date().toISOString(),
  };
  await fs.writeFile(runManifest, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");

  let projectState = null;
  if (projectRoot && await exists(stateManager)) {
    const ingestOutput = runNode(stateManager, [
      "ingest-video",
      "--project-root", projectRoot,
      "--run-manifest", runManifest,
      ...(args.videoJob ? ["--video-job", path.resolve(args.videoJob)] : []),
    ]);
    projectState = parseJsonFromOutput(ingestOutput);
  }

  return {
    provider,
    shot,
    outputDir,
    video: outputVideo,
    runManifest,
    promptCopy: promptCopyPath,
    projectRoot: projectRoot || null,
    projectState,
  };
}

async function main() {
  const args = parseArgs(process.argv);
  if (!args.promptFile) throw new Error("Missing --prompt-file.");
  const provider = normalizeProvider(args.provider);
  const promptText = await readText(path.resolve(args.promptFile));
  const projectRoot = args.projectRoot ? path.resolve(args.projectRoot) : "";
  const shot = safeName(args.shot || path.basename(args.promptFile, path.extname(args.promptFile)), "video");
  const liveDreamina = isDreaminaLiveProvider(provider);
  const dreaminaAdapterArgs = [
    ...(args.dreaminaCli ? ["--cli", String(args.dreaminaCli)] : []),
    ...(args.dreaminaCliScript ? ["--cli-script", path.resolve(String(args.dreaminaCliScript))] : []),
  ];
  let dreaminaAvailable = false;
  let dreaminaDoctorError = "";
  let detectedDreaminaCredits = null;
  if (liveDreamina) {
    if (!(await exists(dreaminaRunner))) throw new Error(`Dreamina adapter not found: ${dreaminaRunner}`);
    try {
      runNode(dreaminaRunner, ["doctor", ...dreaminaAdapterArgs]);
      dreaminaAvailable = true;
    } catch (error) {
      dreaminaDoctorError = error.message;
    }
    if (dreaminaAvailable && !args.submitId && !args.skipCreditCheck) {
      try {
        const creditOutput = runNode(dreaminaRunner, ["credit", ...dreaminaAdapterArgs]);
        const creditResult = JSON.parse(creditOutput || "{}");
        detectedDreaminaCredits = creditResult.result?.available_credits ?? null;
      } catch (error) {
        throw new Error(`Dreamina credit check failed; log in or use --skip-credit-check only when explicitly approved: ${error.message}`);
      }
    }
  }
  const promptFingerprint = computeIdempotencyKey(promptText);
  const referenceFingerprint = computeIdempotencyKey({ image_url: args.imageUrl || "", image_file: args.imageFile ? path.resolve(args.imageFile) : "", reference_roles: args.referenceRoles || "" });
  const manualProvider = provider !== "seedance" && !(liveDreamina && dreaminaAvailable);
  const safetyPayload = {
    provider,
    asset_or_shot_id: shot,
    deliverable_profile: args.deliverableProfile || "video_i2v",
    execution_mode: manualProvider ? "external_manual" : "api",
    prompt_fingerprint: promptFingerprint,
    reference_fingerprint: referenceFingerprint,
    request: {
      target_tool: args.targetTool || provider,
      target_model: args.targetModel || args.model || "",
      task_type: args.taskType || "",
      duration: String(args.duration || "5"),
      ratio: args.ratio || "",
      resolution: args.resolution || "720p",
      video_mode: args.videoMode || "firstFrame",
      audio_policy: args.audioPolicy || "",
    },
  };
  if (liveDreamina && dreaminaAvailable && args.submitId) {
    const recoveryStartedAt = Date.now();
    const recoveryKey = args.idempotencyKey || computeIdempotencyKey(safetyPayload);
    const existing = projectRoot ? await latestRun(projectRoot, recoveryKey) : null;
    const recoveryPreflight = { idempotency_key: recoveryKey, attempt: Number(existing?.attempt || 1), existing };
    const recoveryOutputDir = args.outputDir
      ? path.resolve(args.outputDir)
      : projectRoot
        ? path.join(projectRoot, "video-runs", `${shot}_${timestamp()}_jimeng`)
        : path.join("H:\\yingshi\\outputs", `jimeng-${shot}-${timestamp()}`);
    await fs.mkdir(recoveryOutputDir, { recursive: true });
    try {
      const recoveredText = runNode(dreaminaRunner, [
        "recover",
        "--submit-id", String(args.submitId),
        "--output-dir", recoveryOutputDir,
        ...dreaminaAdapterArgs,
      ]);
      const recovered = JSON.parse(recoveredText || "{}");
      const outputVideo = firstVideoPath(recovered.output_paths || []);
      if (recovered.gen_status === "success" && (!outputVideo || !(await exists(outputVideo)))) {
        throw new Error("Dreamina reported success but no downloaded video file was found; preserve submit_id and query again instead of resubmitting.");
      }
      const manifestResult = await ingestManualVideoRun({
        args: {
          ...args,
          outputDir: recoveryOutputDir,
          outputVideo,
          taskId: recovered.submit_id || args.submitId,
          status: recovered.gen_status || "querying",
          notes: "Dreamina CLI recovery/query. No new generation submission was made.",
        },
        provider: "jimeng-cli",
        promptText,
        idempotencyKey: recoveryKey,
        startedAt: recoveryStartedAt,
      });
      const metrics = { elapsed_seconds: Number(((Date.now() - recoveryStartedAt) / 1000).toFixed(3)), estimated_cost: args.estimatedCost ? Number(args.estimatedCost) : null };
      const ledgerEvent = recovered.gen_status === "success"
        ? await completeRun({ projectRoot, preflight: recoveryPreflight, payload: safetyPayload, output: { output_dir: recoveryOutputDir, run_manifest: manifestResult.runManifest, video: outputVideo, submit_id: recovered.submit_id }, metrics })
        : await submitRun({ projectRoot, preflight: recoveryPreflight, payload: safetyPayload, output: { output_dir: recoveryOutputDir, run_manifest: manifestResult.runManifest, submit_id: recovered.submit_id || args.submitId }, metrics });
      console.log(JSON.stringify({ ...manifestResult, dreamina: recovered, recovered: true, reused: true, idempotencyKey: recoveryKey, ledgerEvent }, null, 2));
      return;
    } catch (error) {
      await failRun({ projectRoot, preflight: recoveryPreflight, payload: safetyPayload, error: error.message, metrics: { elapsed_seconds: Number(((Date.now() - recoveryStartedAt) / 1000).toFixed(3)) } });
      throw error;
    }
  }
  const preflight = await preflightRun({
    projectRoot,
    payload: safetyPayload,
    idempotencyKey: args.idempotencyKey || "",
    generationConfirmation: args.generationConfirmation || "",
    estimatedCost: args.estimatedCost,
    availableCredits: args.availableCredits ?? detectedDreaminaCredits,
    resume: Boolean(args.resume),
    forceNewRun: Boolean(args.forceNewRun),
    maxAttempts: Number(args.maxAttempts || 2),
    paid: !manualProvider,
  });
  if (!preflight.allowed) {
    if (preflight.reuse) {
      console.log(JSON.stringify({
        provider,
        shot,
        reused: true,
        idempotencyKey: preflight.idempotency_key,
        reason: preflight.reason,
        existingRun: preflight.existing,
      }, null, 2));
      return;
    }
    throw new Error(`Generation safety preflight blocked: ${preflight.reason}`);
  }
  const startedAt = Date.now();

  if (manualProvider) {
    const handoffProvider = liveDreamina ? "jimeng-manual" : provider;
    if (!isManualVideoProvider(handoffProvider)) {
      throw new Error("Only --provider seedance, jimeng-manual, kling, kling-o1, or kling-omni are supported.");
    }
    const result = await ingestManualVideoRun({
      args: {
        ...args,
        notes: liveDreamina
          ? `Dreamina CLI unavailable; preserved a manual Jimeng handoff. ${dreaminaDoctorError}`
          : args.notes,
      },
      provider: handoffProvider,
      promptText,
      idempotencyKey: preflight.idempotency_key,
      startedAt,
    });
    const ledgerEvent = await completeRun({
      projectRoot,
      preflight,
      payload: safetyPayload,
      output: { output_dir: result.outputDir, run_manifest: result.runManifest, video: result.video },
      metrics: { elapsed_seconds: Number(((Date.now() - startedAt) / 1000).toFixed(3)), estimated_cost: args.estimatedCost ? Number(args.estimatedCost) : null },
      manualHandoff: !result.video,
    });
    result.idempotencyKey = preflight.idempotency_key;
    result.ledgerEvent = ledgerEvent;
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (liveDreamina) {
    const outputDir = args.outputDir
      ? path.resolve(args.outputDir)
      : projectRoot
        ? path.join(projectRoot, "video-runs", `${shot}_${timestamp()}_jimeng`)
        : path.join("H:\\yingshi\\outputs", `jimeng-${shot}-${timestamp()}`);
    await fs.mkdir(outputDir, { recursive: true });
    const command = dreaminaSubcommand(args);
    const negativePrompt = args.negativePromptFile ? await readText(path.resolve(args.negativePromptFile)) : (args.negativePrompt || "");
    const runnerArgs = [
      "execute",
      "--subcommand", command,
      "--prompt-file", path.resolve(args.promptFile),
      "--generation-confirmation", String(args.generationConfirmation || ""),
      "--output-dir", outputDir,
      "--poll", String(args.poll || 30),
      ...(args.imageFile ? ["--image-file", path.resolve(args.imageFile)] : []),
      ...(args.imageUrl ? ["--image-url", String(args.imageUrl)] : []),
      ...(args.firstFrame ? ["--first-frame", path.resolve(args.firstFrame)] : []),
      ...(args.lastFrame ? ["--last-frame", path.resolve(args.lastFrame)] : []),
      ...(negativePrompt ? ["--negative-prompt", negativePrompt] : []),
      ...(args.duration ? ["--duration", String(args.duration)] : []),
      ...(args.ratio ? ["--ratio", String(args.ratio)] : []),
      ...(args.resolution ? ["--resolution", String(args.resolution)] : []),
      ...(args.model ? ["--model", String(args.model)] : []),
      ...(args.session ? ["--session", String(args.session)] : []),
      ...(args.extraArgsFile ? ["--extra-args-file", path.resolve(args.extraArgsFile)] : []),
      ...dreaminaAdapterArgs,
    ];
    const startEvent = await startRun({ projectRoot, preflight, payload: safetyPayload });
    try {
      const dreaminaText = runNode(dreaminaRunner, runnerArgs);
      const dreamina = JSON.parse(dreaminaText || "{}");
      const outputVideo = firstVideoPath(dreamina.output_paths || []);
      if (dreamina.gen_status === "success" && (!outputVideo || !(await exists(outputVideo)))) {
        throw new Error("Dreamina reported success but no downloaded video file was found; preserve submit_id and recover instead of resubmitting.");
      }
      const result = await ingestManualVideoRun({
        args: {
          ...args,
          outputDir,
          outputVideo,
          taskId: dreamina.submit_id,
          status: dreamina.gen_status || "querying",
          notes: "Dreamina CLI live execution. Recover querying tasks by submit_id; do not resubmit.",
        },
        provider: "jimeng-cli",
        promptText,
        idempotencyKey: preflight.idempotency_key,
        startedAt,
      });
      const metrics = {
        elapsed_seconds: Number(((Date.now() - startedAt) / 1000).toFixed(3)),
        credits_used: args.creditsUsed ? Number(args.creditsUsed) : null,
        estimated_cost: args.estimatedCost ? Number(args.estimatedCost) : null,
      };
      const ledgerEvent = dreamina.gen_status === "success"
        ? await completeRun({ projectRoot, preflight, payload: safetyPayload, output: { output_dir: outputDir, run_manifest: result.runManifest, video: outputVideo, submit_id: dreamina.submit_id }, metrics })
        : await submitRun({ projectRoot, preflight, payload: safetyPayload, output: { output_dir: outputDir, run_manifest: result.runManifest, submit_id: dreamina.submit_id }, metrics });
      console.log(JSON.stringify({ ...result, dreamina, idempotencyKey: preflight.idempotency_key, ledgerEvent, startEvent, resumed: Boolean(args.resume) }, null, 2));
      return;
    } catch (error) {
      await failRun({ projectRoot, preflight, payload: safetyPayload, error: error.message, metrics: { elapsed_seconds: Number(((Date.now() - startedAt) / 1000).toFixed(3)) } });
      throw error;
    }
  }

  if (!args.imageUrl && !args.imageFile) throw new Error("Missing --image-url. Use --image-file only when local relay is intentional.");
  if (args.imageFile && !args.allowImageFile) throw new Error("Local --image-file is disabled by default. Pass --allow-image-file when URL Relay is intentional.");
  if (!process.env.ARK_API_KEY) {
    const userKey = process.env.USERPROFILE ? "" : "";
    throw new Error("ARK_API_KEY is missing. Configure it locally before Seedance generation.");
  }
  if (!(await exists(seedanceRunner))) throw new Error(`Seedance runner not found: ${seedanceRunner}`);

  const outputDir = args.outputDir
    ? path.resolve(args.outputDir)
    : projectRoot
      ? path.join(projectRoot, "video-runs", `${shot}_${timestamp()}_seedance`)
      : path.join("H:\\yingshi\\outputs", `seedance-${shot}-${timestamp()}`);

  const runArgs = [
    "run",
    "--prompt-file", path.resolve(args.promptFile),
    "--duration", String(args.duration || 5),
    "--resolution", String(args.resolution || "720p"),
    "--video-mode", String(args.videoMode || "firstFrame"),
    "--output-dir", outputDir,
  ];
  if (args.ratio) runArgs.push("--ratio", String(args.ratio));
  if (args.imageUrl) runArgs.push("--image-url", String(args.imageUrl));
  if (args.imageFile) runArgs.push("--image-file", path.resolve(args.imageFile));

  await startRun({ projectRoot, preflight, payload: safetyPayload });
  try {
    const seedanceOutput = runNode(seedanceRunner, runArgs);
    const runManifest = path.join(outputDir, "run_manifest.json");
    const manifest = await readJson(runManifest);
    const elapsedSeconds = Number(((Date.now() - startedAt) / 1000).toFixed(3));
    manifest.idempotency_key = preflight.idempotency_key;
    manifest.metrics = {
      ...(manifest.metrics || {}),
      elapsed_seconds: elapsedSeconds,
      credits_used: args.creditsUsed ? Number(args.creditsUsed) : null,
      estimated_cost: args.estimatedCost ? Number(args.estimatedCost) : null,
    };
    await fs.writeFile(runManifest, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
    let projectState = null;
    if (projectRoot && await exists(stateManager)) {
      const ingestOutput = runNode(stateManager, [
        "ingest-video",
        "--project-root", projectRoot,
        "--run-manifest", runManifest,
        ...(args.videoJob ? ["--video-job", path.resolve(args.videoJob)] : []),
      ]);
      projectState = parseJsonFromOutput(ingestOutput);
    }
    const ledgerEvent = await completeRun({
      projectRoot,
      preflight,
      payload: safetyPayload,
      output: { output_dir: outputDir, run_manifest: runManifest, video: manifest.outputs?.video || "", task_id: manifest.task?.id || "" },
      metrics: manifest.metrics,
    });

    console.log(JSON.stringify({
      provider: "seedance",
      shot,
      outputDir,
      video: manifest.outputs?.video || "",
      runManifest,
      projectRoot: projectRoot || null,
      projectState,
      idempotencyKey: preflight.idempotency_key,
      ledgerEvent,
      resumed: Boolean(args.resume),
      seedanceOutput: seedanceOutput.split(/\r?\n/).slice(-4).join("\n"),
    }, null, 2));
  } catch (error) {
    await failRun({
      projectRoot,
      preflight,
      payload: safetyPayload,
      error: error.message,
      metrics: { elapsed_seconds: Number(((Date.now() - startedAt) / 1000).toFixed(3)) },
    });
    throw error;
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
