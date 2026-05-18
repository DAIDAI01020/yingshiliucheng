import fs from "node:fs/promises";
import path from "node:path";

const API_URL = "https://openrouter.ai/api/v1/chat/completions";
const DEFAULT_MODEL = "google/gemini-3.1-flash-image-preview";
const DEFAULT_BASE_DIR = "H:\\yingshi\\outputs\\banana-images";
const VALID_RATIOS = new Set(["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9", "1:4", "4:1", "1:8", "8:1"]);
const VALID_IMAGE_SIZES = new Set(["0.5K", "1K", "2K", "4K"]);

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

function inferRatio(shot, fallbackRatio) {
  const explicit = shot.aspect_ratio || shot.aspectRatio || shot.ratio || shot["比例"] || fallbackRatio;
  if (explicit && VALID_RATIOS.has(explicit)) return explicit;
  const text = String(explicit || "").toLowerCase();
  if (text.includes("9:16") || text.includes("竖")) return "9:16";
  if (text.includes("1:1") || text.includes("方")) return "1:1";
  if (text.includes("21:9") || text.includes("宽屏")) return "21:9";
  return "16:9";
}

function inferImageSize(shot, fallbackSize) {
  const explicit = shot.image_size || shot.imageSize || shot["图片尺寸"] || fallbackSize;
  return VALID_IMAGE_SIZES.has(explicit) ? explicit : "2K";
}

function mimeFromPath(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === ".jpg" || ext === ".jpeg") return "image/jpeg";
  if (ext === ".webp") return "image/webp";
  if (ext === ".gif") return "image/gif";
  return "image/png";
}

function extensionFromMime(mime, fallback = "png") {
  if (mime === "image/jpeg") return "jpg";
  if (mime === "image/webp") return "webp";
  if (mime === "image/gif") return "gif";
  return fallback;
}

function parseDataUrl(dataUrl) {
  const match = /^data:([^;,]+);base64,(.+)$/i.exec(dataUrl);
  if (!match) return null;
  return { mime: match[1], base64: match[2] };
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
      return { version, filePathBase: filePath.slice(0, -1 * (ext.length + 1)), filePath };
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

async function referenceToImageUrl(reference) {
  if (reference.url) return reference.url;
  if (reference.dataUrl) return reference.dataUrl;
  if (reference.path) {
    const bytes = await fs.readFile(reference.path);
    const mime = mimeFromPath(reference.path);
    return `data:${mime};base64,${bytes.toString("base64")}`;
  }
  throw new Error("Reference image must include url, dataUrl, or path.");
}

async function normalizeReference(reference, index) {
  const role = reference.role || reference["作用"] || `reference image ${index + 1}`;
  const url = await referenceToImageUrl(reference);
  return { role, url };
}

async function normalizeShot(raw, defaults) {
  const shot = raw.shot || raw.shotNumber || raw["镜号"];
  const prompt = raw.prompt || raw.bananaPrompt || raw["Banana完整可复制提示词"] || raw["Banana/即梦完整可复制提示词"];
  const negativePrompt = raw.negativePrompt || raw.negative || raw["负面提示词"] || raw["Banana/即梦负面提示词"] || "";
  if (!shot) throw new Error("Shot is missing a shot number.");
  if (!prompt) throw new Error(`Shot ${shot} is missing prompt.`);

  const references = [];
  for (const [index, reference] of (raw.references || raw["参考图"] || []).entries()) {
    references.push(await normalizeReference(reference, index));
  }

  return {
    shot: safeName(shot, "shot"),
    prompt,
    negativePrompt,
    finalPrompt: negativePrompt ? `${prompt}\n\n负面要求：${negativePrompt}` : prompt,
    aspect_ratio: inferRatio(raw, defaults.aspect_ratio || defaults.aspectRatio || "16:9"),
    image_size: inferImageSize(raw, defaults.image_size || defaults.imageSize || "2K"),
    references,
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

function buildMessageContent(shot) {
  if (!shot.references.length) return shot.finalPrompt;
  const roleText = shot.references.map((reference, index) => `Image ${index + 1}: ${reference.role}`).join("\n");
  const content = [{ type: "text", text: `${roleText}\n\n${shot.finalPrompt}` }];
  for (const reference of shot.references) {
    content.push({ type: "image_url", image_url: { url: reference.url } });
  }
  return content;
}

function extractImageUrls(json) {
  const urls = [];
  const message = json?.choices?.[0]?.message;
  for (const image of message?.images || []) {
    const url = image?.image_url?.url || image?.url;
    if (url) urls.push(url);
  }
  const content = message?.content;
  if (Array.isArray(content)) {
    for (const item of content) {
      const url = item?.image_url?.url || item?.url;
      if (url) urls.push(url);
    }
  }
  return urls;
}

async function saveImageUrl(imageUrl, filePathBase) {
  const data = parseDataUrl(imageUrl);
  if (data) {
    const ext = extensionFromMime(data.mime);
    const filePath = `${filePathBase}.${ext}`;
    await fs.writeFile(filePath, Buffer.from(data.base64, "base64"));
    return filePath;
  }

  const response = await fetch(imageUrl);
  if (!response.ok) throw new Error(`Failed to download image URL: ${response.status} ${response.statusText}`);
  const mime = response.headers.get("content-type")?.split(";")[0] || "image/png";
  const ext = extensionFromMime(mime);
  const filePath = `${filePathBase}.${ext}`;
  await fs.writeFile(filePath, Buffer.from(await response.arrayBuffer()));
  return filePath;
}

async function generateImage({ apiKey, model, shot, imageDir }) {
  const body = {
    model,
    messages: [{ role: "user", content: buildMessageContent(shot) }],
    modalities: ["image", "text"],
    stream: false,
    image_config: {
      aspect_ratio: shot.aspect_ratio,
      image_size: shot.image_size,
    },
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

  const urls = extractImageUrls(json);
  if (!urls.length) throw new Error("API response did not include choices[0].message.images[].image_url.url.");

  const filePaths = [];
  for (const [index, imageUrl] of urls.entries()) {
    const { version, filePathBase } = await nextVersion(imageDir, shot.shot, urls.length > 1 ? `banana_${index + 1}` : "banana", "png");
    filePaths.push({
      version: versionLabel(version),
      path: await saveImageUrl(imageUrl, filePathBase),
    });
  }

  return {
    filePaths,
    responseText: typeof json?.choices?.[0]?.message?.content === "string" ? json.choices[0].message.content : null,
    usage: json.usage || null,
  };
}

function buildPreflight({ projectName, model, outputDir, shots, hasApiKey }) {
  return {
    tool: "banana",
    projectName,
    model,
    outputDir,
    mode: "dry-run检查",
    hasApiKey,
    shotCount: shots.length,
    checks: shots.map((shot) => ({
      shot: shot.shot,
      aspect_ratio: shot.aspect_ratio,
      image_size: shot.image_size,
      referenceCount: shot.references.length,
      promptLength: shot.finalPrompt.length,
      risk: shot.finalPrompt.length < 40 ? "提示词偏短，建议补充主体、构图、光线和风格" : "待生成检查",
    })),
  };
}

async function main() {
  const args = parseArgs(process.argv);
  const input = await readInput(args.input);
  const model = input.model || process.env.BANANA_MODEL || DEFAULT_MODEL;
  const projectName = safeName(input.projectName || input["项目名"], "banana-image-project");
  const outputDir = args.outputDir || input.outputDir || path.join(DEFAULT_BASE_DIR, projectName, timestamp());
  const imageDir = path.join(outputDir, "images");
  const promptDir = path.join(outputDir, "prompts");
  const logDir = path.join(outputDir, "logs");
  const shots = [];
  for (const shot of input.shots) shots.push(await normalizeShot(shot, input));
  const hasApiKey = Boolean(process.env.OPENROUTER_API_KEY);

  const log = {
    projectName,
    tool: "banana",
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
    const { version, filePath } = await nextVersion(imageDir, shot.shot, "banana", "png");
    const versionText = versionLabel(version);
    const requestSettings = {
      aspect_ratio: shot.aspect_ratio,
      image_size: shot.image_size,
      referenceCount: shot.references.length,
    };
    const { promptPath, promptJsonPath } = await writePromptFiles({
      promptDir,
      shot: shot.shot,
      tool: "banana",
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
      tool: "banana",
      status: args.dryRun ? "dry-run" : "pending",
      model,
      aspect_ratio: shot.aspect_ratio,
      image_size: shot.image_size,
      promptSummary: promptSummary(shot.prompt),
      fullPrompt: shot.prompt,
      negativePrompt: shot.negativePrompt,
      finalPrompt: shot.finalPrompt,
      promptPath,
      promptJsonPath,
      referenceCount: shot.references.length,
      filePath,
      filePaths: [],
      error: null,
      retrySuggestion: null,
    };

    if (!args.dryRun) {
      if (!hasApiKey) throw new Error("OPENROUTER_API_KEY is missing. Set it in the local environment before real generation.");
      try {
        const result = await generateImage({ apiKey: process.env.OPENROUTER_API_KEY, model, shot, imageDir });
        entry.status = "success";
        entry.filePaths = result.filePaths;
        entry.filePath = result.filePaths[0]?.path || null;
        if (result.filePaths[0]?.version && result.filePaths[0].version !== entry.version) {
          entry.version = result.filePaths[0].version;
        }
        entry.responseText = result.responseText;
        entry.usage = result.usage;
      } catch (error) {
        entry.status = "failed";
        entry.error = error.message;
        entry.retrySuggestion = "检查提示词、参考图、OpenRouter模型权限和账号额度后重出该镜头";
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
