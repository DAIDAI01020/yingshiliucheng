import fs from "node:fs/promises";
import path from "node:path";

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--task") args.task = argv[++i];
    else if (arg === "--log") args.log = argv[++i];
    else if (arg === "--output") args.output = argv[++i];
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (!args.task && !args.log) throw new Error("Provide --task folder or --log generation-log.json.");
  return args;
}

function toPosixPath(filePath) {
  return path.resolve(filePath).replace(/\\/g, "/");
}

function imageMarkdownPath(filePath) {
  return toPosixPath(filePath);
}

async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function findLog(taskPath) {
  const direct = path.join(taskPath, "logs", "generation-log.json");
  if (await exists(direct)) return direct;
  const legacy = path.join(taskPath, "generation-log.json");
  if (await exists(legacy)) return legacy;
  throw new Error(`Could not find generation-log.json under ${taskPath}`);
}

async function readTextIfExists(filePath) {
  if (!filePath || !(await exists(filePath))) return "";
  return fs.readFile(filePath, "utf8");
}

function nextVersion(version) {
  const num = Number(String(version || "v01").replace(/^v/i, ""));
  if (!Number.isFinite(num)) return "v02";
  return `v${String(num + 1).padStart(2, "0")}`;
}

function firstImagePath(entry) {
  return entry.filePath || entry.filePaths?.[0]?.path || entry.filePaths?.[0] || "";
}

function inferTool(entry, log, taskDir) {
  if (entry.tool) return entry.tool;
  if (log.tool) return log.tool;

  const haystack = [
    taskDir,
    firstImagePath(entry),
    entry.promptPath,
    entry.promptJsonPath,
    log.outputDir,
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();

  if (haystack.includes("banana")) return "banana";
  if (haystack.includes("openai")) return "openai";
  return "unknown";
}

function inferVersion(entry) {
  if (entry.version) return entry.version;
  const haystack = [firstImagePath(entry), entry.promptPath, entry.promptJsonPath]
    .filter(Boolean)
    .join(" ");
  const match = haystack.match(/(?:^|[_-])(v\d+)(?:[_\-.]|$)/i);
  return match ? match[1].toLowerCase() : "v01";
}

function promptBlock(entry, promptText) {
  if (promptText.trim()) return promptText.trim();
  return [
    "完整提示词:",
    entry.fullPrompt || entry.prompt || "",
    "",
    "负面词:",
    entry.negativePrompt || "",
    "",
    "实际请求提示词:",
    entry.finalPrompt || "",
  ].join("\n").trim();
}

function imageCell(entry) {
  const imagePath = firstImagePath(entry);
  if (!imagePath) return "图片缺失";
  return `![${entry.shot || "shot"}](${imageMarkdownPath(imagePath)})`;
}

function escapeTableCell(text) {
  return String(text || "")
    .replace(/\r?\n/g, "<br>")
    .replace(/\|/g, "\\|");
}

async function buildBoard({ logPath, outputPath }) {
  const log = JSON.parse(await fs.readFile(logPath, "utf8"));
  const taskDir = log.outputDir || path.dirname(path.dirname(logPath));
  const reviewDir = outputPath ? path.dirname(outputPath) : path.join(taskDir, "review");
  const boardPath = outputPath || path.join(reviewDir, "review-board.md");
  await fs.mkdir(reviewDir, { recursive: true });

  const lines = [];
  lines.push(`# 出图审片面板`);
  lines.push("");
  lines.push(`- 项目：${log.projectName || ""}`);
  lines.push(`- 工具：${log.tool || inferTool({}, log, taskDir)}`);
  lines.push(`- 模型：${log.model || ""}`);
  lines.push(`- 任务目录：${toPosixPath(taskDir)}`);
  lines.push(`- 日志：${toPosixPath(logPath)}`);
  lines.push("");
  lines.push(`## 总览`);
  lines.push("");
  lines.push("| 镜号 | 版本 | 工具 | 图片 | 提示词文件 | 修改入口 |");
  lines.push("| --- | --- | --- | --- | --- | --- |");

  for (const entry of log.shots || []) {
    const shot = entry.shot || entry.shotId || "SHOT";
    const tool = inferTool(entry, log, taskDir);
    const version = inferVersion(entry);
    const handle = `${shot}_${tool}_${version}`;
    const promptPath = entry.promptPath || "";
    const imagePath = firstImagePath(entry);
    lines.push(`| ${shot} | ${version} | ${tool} | ${imagePath ? `![${shot}](${imageMarkdownPath(imagePath)})` : "图片缺失"} | ${promptPath ? toPosixPath(promptPath) : "缺失"} | 改 \`${handle}\` |`);
  }

  for (const entry of log.shots || []) {
    const shot = entry.shot || entry.shotId || "SHOT";
    const tool = inferTool(entry, log, taskDir);
    const version = inferVersion(entry);
    const handle = `${shot}_${tool}_${version}`;
    const promptText = await readTextIfExists(entry.promptPath);
    const promptJsonPath = entry.promptJsonPath || "";

    lines.push("");
    lines.push(`## ${shot} / ${tool} / ${version}`);
    lines.push("");
    lines.push("| 提示词 | 图片 |");
    lines.push("| --- | --- |");
    lines.push(`| ${escapeTableCell(promptBlock(entry, promptText))} | ${imageCell(entry)} |`);
    lines.push("");
    lines.push(`**修改入口**：改 \`${handle}\``);
    lines.push("");
    lines.push(`**提示词文件**：${entry.promptPath ? toPosixPath(entry.promptPath) : "缺失"}`);
    lines.push("");
    lines.push(`**提示词JSON**：${promptJsonPath ? toPosixPath(promptJsonPath) : "缺失"}`);
    lines.push("");
    lines.push("**修改建议**");
    lines.push("- 保留：");
    lines.push("- 问题：");
    lines.push("- 建议：");
    lines.push(`- 重出版本：${shot}_${tool}_${nextVersion(version)}`);
  }

  await fs.writeFile(boardPath, lines.join("\n"), "utf8");
  console.log(JSON.stringify({ reviewBoard: boardPath, taskDir, logPath }, null, 2));
}

async function main() {
  const args = parseArgs(process.argv);
  const logPath = args.log ? path.resolve(args.log) : await findLog(path.resolve(args.task));
  await buildBoard({ logPath, outputPath: args.output ? path.resolve(args.output) : null });
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
