import { spawnSync } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillDir = path.dirname(__dirname);
const skillsRoot = path.dirname(skillDir);
const seedanceRunner = path.join(skillsRoot, "seedance-2-video", "scripts", "seedance_task.mjs");
const stateManager = path.join(skillsRoot, "project-state-manager", "scripts", "manage-project-state.mjs");

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

async function main() {
  const args = parseArgs(process.argv);
  if (String(args.provider || "seedance").toLowerCase() !== "seedance") {
    throw new Error("Only --provider seedance is supported in this lightweight controller.");
  }
  if (!args.promptFile) throw new Error("Missing --prompt-file.");
  if (!args.imageUrl && !args.imageFile) throw new Error("Missing --image-url. Use --image-file only when local relay is intentional.");
  if (args.imageFile && !args.allowImageFile) throw new Error("Local --image-file is disabled by default. Pass --allow-image-file when URL Relay is intentional.");
  if (!process.env.ARK_API_KEY) {
    const userKey = process.env.USERPROFILE ? "" : "";
    throw new Error("ARK_API_KEY is missing. Configure it locally before Seedance generation.");
  }
  if (!(await exists(seedanceRunner))) throw new Error(`Seedance runner not found: ${seedanceRunner}`);

  const projectRoot = args.projectRoot ? path.resolve(args.projectRoot) : "";
  const shot = safeName(args.shot || path.basename(args.promptFile, path.extname(args.promptFile)), "video");
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

  const seedanceOutput = runNode(seedanceRunner, runArgs);
  const runManifest = path.join(outputDir, "run_manifest.json");
  const manifest = await readJson(runManifest);
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

  console.log(JSON.stringify({
    provider: "seedance",
    shot,
    outputDir,
    video: manifest.outputs?.video || "",
    runManifest,
    projectRoot: projectRoot || null,
    projectState,
    seedanceOutput: seedanceOutput.split(/\r?\n/).slice(-4).join("\n"),
  }, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
