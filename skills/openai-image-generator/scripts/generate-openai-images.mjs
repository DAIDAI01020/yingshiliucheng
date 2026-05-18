import fs from "node:fs/promises";
import path from "node:path";

const API_URL = "https://api.openai.com/v1/images/generations";
const DEFAULT_BASE_DIR = "H:\\yingshi\\outputs\\openai-images";
const VALID_SIZES = new Set(["1024x1024", "1024x1536", "1536x1024"]);
const VALID_QUALITIES = new Set(["low", "medium", "high"]);
const VALID_FORMATS = new Set(["png", "webp", "jpeg"]);

function parseArgs(argv) {
  const args = { dryRun: false };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--dry-run") args.dryRun = true;
    else if (arg === "--input") args.input = argv[++i];
    else if (arg === "--output-dir") args.outputDir = argv[++i];
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (!args.input) throw new Error("Missing --input path.");
  return args;
}

function safeName(value, fallback = "project") {
  return String(value || fallback)
    .trim()
    .replace(/[<>:"/\\|?*\u0000-\u001f]/g, "_")
    .replace(/\s+/g, "_")
    .slice(0, 80) || fallback;
}

function timestamp() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}_${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
}

function inferSize(shot, fallbackSize) {
  const explicit = shot.size || shot["尺寸"] || fallbackSize;
  if (explicit && VALID_SIZES.has(explicit)) return explicit;
  const ratio = String(shot.ratio || shot["比例"] || "").toLowerCase();
  if (ratio.includes("9:16") || ratio.includes("竖")) return "1024x1536";
  if (ratio.includes("1:1") || ratio.includes("方")) return "1024x1024";
  if (ratio.includes("16:9") || ratio.includes("2.35") || ratio.includes("横")) return "1536x1024";
  return VALID_SIZES.has(fallbackSize) ? fallbackSize : "1536x1024";
}

function promptSummary(text) {
  return String(text || "").replace(/\s+/g, " ").slice(0, 120);
}

function versionLabel(version) {
  return `v${String(version).padStart(2, "0")}`;
}

async function nextVersion(outputDir, shot, tool, ext) {
  let version = 1;
  while (true) {
    const filePath = path.join(outputDir, `${shot}_${tool}_${versionLabel(version)}.${ext}`);
    try {
      await fs.access(filePath);
      version += 1;
    } catch {
      return { version, filePath };
    }
  }
}

async function writePromptFiles({ promptDir, shot, tool, version, model, prompt, negativePrompt, finalPrompt, requestSettings }) {
  const baseName = `${shot}_${tool}_${version}_prompt`;
  const promptPath = path.join(promptDir, `${baseName}.txt`);
  const promptJsonPath = path.join(promptDir, `${baseName}.json`);
  const txt = [
    `镜号: ${shot}`,
    `版本: ${version}`,
    `工具: ${tool}`,
    `模型: ${model}`,
    "",
    "完整提示词:",
    prompt,
    "",
    "负面提示词:",
    negativePrompt || "",
    "",
    "实际请求提示词:",
    finalPrompt,
    "",
  ].join("\n");
  const json = {
    shot,
    version,
    tool,
    model,
    prompt,
    negativePrompt,
    finalPrompt,
    requestSettings,
  };
  await fs.writeFile(promptPath, txt, "utf8");
  await fs.writeFile(promptJsonPath, JSON.stringify(json, null, 2), "utf8");
  return { promptPath, promptJsonPath };
}

function normalizeShot(raw, defaults) {
  const shot = raw.shot || raw.shotNumber || raw["镜号"];
  const prompt = raw.prompt || raw.openaiPrompt || raw["OpenAI完整可复制提示词"];
  const negativePrompt = raw.negativePrompt || raw.negative || raw["OpenAI负面要求"] || "";
  if (!shot) throw new Error("Shot is missing a shot number.");
  if (!prompt) throw new Error(`Shot ${shot} is missing prompt.`);

  const quality = raw.quality || raw["质量"] || defaults.quality || "medium";
  const outputFormat = raw.output_format || raw.outputFormat || raw["输出格式"] || defaults.output_format || "png";
  if (!VALID_QUALITIES.has(quality)) throw new Error(`Shot ${shot} has invalid quality: ${quality}`);
  if (!VALID_FORMATS.has(outputFormat)) throw new Error(`Shot ${shot} has invalid output format: ${outputFormat}`);

  return {
    shot: safeName(shot, "shot"),
    prompt,
    negativePrompt,
    finalPrompt: negativePrompt ? `${prompt}\n\n负面要求：${negativePrompt}` : prompt,
    size: inferSize(raw, defaults.size),
    quality,
    output_format: outputFormat,
  };
}

async function readInput(inputPath) {
  const rawText = await fs.readFile(inputPath, "utf8");
  const data = JSON.parse(rawText);
  if (!Array.isArray(data.shots) || data.shots.length === 0) {
    throw new Error("Input JSON must include a non-empty shots array.");
  }
  return data;
}

async function generateImage({ apiKey, model, shot, filePath }) {
  const body = {
    model,
    prompt: shot.finalPrompt,
    size: shot.size,
    quality: shot.quality,
    output_format: shot.output_format,
  };

  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  const json = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = json?.error?.message || `${response.status} ${response.statusText}`;
    throw new Error(message);
  }

  const image = json?.data?.[0];
  if (!image?.b64_json) throw new Error("API response did not include data[0].b64_json.");
  await fs.writeFile(filePath, Buffer.from(image.b64_json, "base64"));
  return {
    revisedPrompt: image.revised_prompt || null,
    usage: json.usage || null,
  };
}

function buildPreflight({ projectName, model, outputDir, shots, hasApiKey }) {
  return {
    tool: "openai",
    projectName,
    model,
    outputDir,
    mode: "dry-run检查",
    hasApiKey,
    shotCount: shots.length,
    checks: shots.map((shot) => ({
      shot: shot.shot,
      size: shot.size,
      quality: shot.quality,
      promptLength: shot.finalPrompt.length,
      risk: shot.finalPrompt.length < 40 ? "提示词偏短，建议补充主体、构图、光线和风格" : "待生成检查",
    })),
  };
}

async function main() {
  const args = parseArgs(process.argv);
  const input = await readInput(args.input);
  const model = input.model || process.env.OPENAI_IMAGE_MODEL || "gpt-image-1.5";
  const projectName = safeName(input.projectName || input["项目名"], "openai-image-project");
  const outputDir = args.outputDir || input.outputDir || path.join(DEFAULT_BASE_DIR, projectName, timestamp());
  const imageDir = path.join(outputDir, "images");
  const promptDir = path.join(outputDir, "prompts");
  const logDir = path.join(outputDir, "logs");
  const shots = input.shots.map((shot) => normalizeShot(shot, input));
  const hasApiKey = Boolean(process.env.OPENAI_API_KEY);

  const log = {
    projectName,
    tool: "openai",
    model,
    outputDir,
    imageDir,
    promptDir,
    logDir,
    dryRun: args.dryRun,
    hasApiKey,
    createdAt: new Date().toISOString(),
    preflight: buildPreflight({ projectName, model, outputDir, shots, hasApiKey }),
    shots: [],
  };

  await fs.mkdir(imageDir, { recursive: true });
  await fs.mkdir(promptDir, { recursive: true });
  await fs.mkdir(logDir, { recursive: true });

  for (const shot of shots) {
    const ext = shot.output_format === "jpeg" ? "jpg" : shot.output_format;
    const { version, filePath } = await nextVersion(imageDir, shot.shot, "openai", ext);
    const versionText = versionLabel(version);
    const requestSettings = {
      size: shot.size,
      quality: shot.quality,
      output_format: shot.output_format,
    };
    const { promptPath, promptJsonPath } = await writePromptFiles({
      promptDir,
      shot: shot.shot,
      tool: "openai",
      version: versionText,
      model,
      prompt: shot.prompt,
      negativePrompt: shot.negativePrompt,
      finalPrompt: shot.finalPrompt,
      requestSettings,
    });
    const entry = {
      shot: shot.shot,
      version: versionText,
      tool: "openai",
      status: args.dryRun ? "dry-run" : "pending",
      model,
      size: shot.size,
      quality: shot.quality,
      output_format: shot.output_format,
      promptSummary: promptSummary(shot.prompt),
      fullPrompt: shot.prompt,
      negativePrompt: shot.negativePrompt,
      finalPrompt: shot.finalPrompt,
      promptPath,
      promptJsonPath,
      filePath,
      error: null,
      retrySuggestion: null,
    };

    if (!args.dryRun) {
      if (!hasApiKey) throw new Error("OPENAI_API_KEY is missing. Set it in the local environment before real generation.");
      try {
        const result = await generateImage({ apiKey: process.env.OPENAI_API_KEY, model, shot, filePath });
        entry.status = "success";
        entry.revisedPrompt = result.revisedPrompt;
        entry.usage = result.usage;
      } catch (error) {
        entry.status = "failed";
        entry.error = error.message;
        entry.retrySuggestion = "检查提示词、模型权限、尺寸/质量参数和账号额度后重出该镜头";
      }
    }

    log.shots.push(entry);
    await fs.writeFile(path.join(logDir, "generation-log.json"), JSON.stringify(log, null, 2), "utf8");
  }

  console.log(JSON.stringify(log, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
