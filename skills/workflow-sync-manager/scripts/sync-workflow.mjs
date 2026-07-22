import { spawnSync } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";

const ALLOWED_PATHS = [".gitignore", "README.md", "WORKFLOW.md", "skills", "sync-logs"];
const BLOCKED_PREFIXES = ["outputs/", "projects/"];
const BLOCKED_SUFFIXES = [".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".mov", ".wav", ".mp3"];
const SECRET_PATTERNS = [
  /sk-[A-Za-z0-9_-]{20,}/,
  /(?:OPENAI|OPENROUTER|ARK|DREAMINA|JIMENG)_(?:API_KEY|TOKEN|COOKIE)\s*[=:]\s*['"]?[^'"\s]+/i,
  /-----BEGIN (?:OPENSSH|RSA|EC|DSA|PRIVATE) KEY-----/,
];

function parseArgs(argv) {
  const [command = "status", ...rest] = argv.slice(2);
  const args = { command, push: false, remote: "origin", branch: "main" };
  for (let i = 0; i < rest.length; i += 1) {
    const arg = rest[i];
    if (arg === "--push") args.push = true;
    else if (arg === "--summary") args.summary = rest[++i];
    else if (arg === "--message") args.message = rest[++i];
    else if (arg === "--remote") args.remote = rest[++i];
    else if (arg === "--branch") args.branch = rest[++i];
    else if (arg === "--paths-file") args.pathsFile = rest[++i];
    else if (arg === "--tag") args.tag = rest[++i];
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (args.tag && !args.push) throw new Error("--tag requires --push so the frozen version is published.");
  return args;
}

function runGit(args, options = {}) {
  const result = spawnSync("git", args, {
    cwd: process.cwd(),
    encoding: "utf8",
    maxBuffer: 1024 * 1024 * 30,
    ...options,
  });
  if (result.status !== 0 && !options.allowFailure) {
    const detail = [result.stderr, result.stdout].filter(Boolean).join("\n").trim();
    throw new Error(detail || `git ${args.join(" ")} failed`);
  }
  return {
    status: result.status,
    stdout: result.stdout.trim(),
    stderr: result.stderr.trim(),
  };
}

function nowStamp() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return {
    date: `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`,
    time: `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`,
  };
}

function normalizePath(filePath) {
  return filePath.trim().replace(/\\/g, "/").replace(/^"\s*/, "").replace(/\s*"$/, "");
}

function parseStatusPorcelain(text) {
  return text
    .split(/\r?\n/)
    .map((line) => line.trimEnd())
    .filter(Boolean)
    .map((line) => normalizePath(line.slice(3).replace(/^.* -> /, "")));
}

function isAllowed(filePath) {
  const p = normalizePath(filePath);
  if (BLOCKED_PREFIXES.some((prefix) => p.startsWith(prefix))) return false;
  if (BLOCKED_SUFFIXES.some((suffix) => p.toLowerCase().endsWith(suffix))) return false;
  return ALLOWED_PATHS.some((allowed) => p === allowed || p.startsWith(`${allowed}/`));
}

async function readPathWhitelist(pathsFile) {
  if (!pathsFile) return null;
  const text = await fs.readFile(path.resolve(pathsFile), "utf8");
  const files = [...new Set(text.split(/\r?\n/)
    .map((line) => normalizePath(line))
    .filter((line) => line && !line.startsWith("#")))];
  if (!files.length) throw new Error("The path whitelist is empty.");
  const disallowed = files.filter((file) => !isAllowed(file));
  if (disallowed.length) throw new Error(`Path whitelist contains disallowed files:\n${disallowed.join("\n")}`);
  return files;
}

async function writeLog({ summary, files, commit = "", pushed = false, remote = "" }) {
  const { date, time } = nowStamp();
  const logDir = path.join(process.cwd(), "sync-logs");
  await fs.mkdir(logDir, { recursive: true });
  const logPath = path.join(logDir, `${date}.md`);
  const lines = [
    `## ${time} ${summary || "Workflow update"}`,
    "",
    `- Commit: ${commit || "pending"}`,
    `- Pushed: ${pushed ? "yes" : "no"}`,
    `- Remote: ${remote || "not pushed"}`,
    "- Changed files:",
    ...(files.length ? files.map((file) => `  - ${file}`) : ["  - none"]),
    "",
  ];
  await fs.appendFile(logPath, `${lines.join("\n")}\n`, "utf8");
  return logPath;
}

function scanStagedDiff() {
  const diff = runGit(["diff", "--cached", "--unified=0"]).stdout;
  const hit = SECRET_PATTERNS.find((pattern) => pattern.test(diff));
  if (hit) throw new Error(`Secret scan failed. Pattern matched: ${hit}`);
}

function stageAllowedFiles(paths) {
  const targets = paths?.length ? paths : ALLOWED_PATHS;
  runGit(["add", "--", ...targets]);
  const staged = parseStatusPorcelain(runGit(["diff", "--cached", "--name-status"]).stdout.replace(/\t/g, "   "));
  const disallowed = staged.filter((file) => !isAllowed(file));
  if (disallowed.length) {
    runGit(["restore", "--staged", "--", ...disallowed], { allowFailure: true });
    throw new Error(`Refusing to stage disallowed files:\n${disallowed.join("\n")}`);
  }
  return staged;
}

function commitIfNeeded(message) {
  const hasStaged = runGit(["diff", "--cached", "--quiet"], { allowFailure: true }).status !== 0;
  if (!hasStaged) return "";
  runGit(["commit", "-m", message || "Update film AI workflow"]);
  return runGit(["rev-parse", "--short", "HEAD"]).stdout;
}

function preparePushTarget(remote, branch) {
  const currentBranch = runGit(["branch", "--show-current"]).stdout;
  if (currentBranch !== branch) {
    throw new Error(`Current branch is ${currentBranch || "detached HEAD"}; refusing to push it as ${branch}.`);
  }
  const remoteCheck = runGit(["remote", "get-url", remote], { allowFailure: true });
  if (remoteCheck.status !== 0) throw new Error(`Git remote does not exist: ${remote}`);
  runGit(["fetch", "--prune", remote, branch]);
  const remoteRef = `refs/remotes/${remote}/${branch}`;
  const exists = runGit(["show-ref", "--verify", "--quiet", remoteRef], { allowFailure: true }).status === 0;
  if (!exists) return;
  const counts = runGit(["rev-list", "--left-right", "--count", `HEAD...${remoteRef}`]).stdout.split(/\s+/).map(Number);
  const behind = counts[1] || 0;
  if (behind > 0) {
    throw new Error(`Remote ${remote}/${branch} contains ${behind} commit(s) not in local HEAD. Integrate them before sync.`);
  }
}

function ensureVersionTag(tag, message) {
  if (!tag) return "";
  if (!/^[A-Za-z0-9][A-Za-z0-9._/-]*$/.test(tag)) throw new Error(`Invalid tag name: ${tag}`);
  const current = runGit(["rev-parse", "HEAD"]).stdout;
  const existing = runGit(["rev-list", "-n", "1", tag], { allowFailure: true });
  if (existing.status === 0) {
    if (existing.stdout !== current) throw new Error(`Tag ${tag} already points to a different commit.`);
    return tag;
  }
  runGit(["tag", "-a", tag, "-m", message || tag]);
  return tag;
}

function pushPublishedVersion(remote, branch, tag) {
  const push = runGit(["push", "-u", remote, branch]);
  if (tag) runGit(["push", remote, `refs/tags/${tag}`]);
  return push.stdout || push.stderr || `${remote}/${branch}`;
}

async function status() {
  return {
    branch: runGit(["branch", "--show-current"]).stdout,
    status: runGit(["status", "--short", "--branch"]).stdout,
    remote: runGit(["remote", "-v"]).stdout,
    latestCommit: runGit(["log", "--oneline", "-1"]).stdout,
  };
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.command === "status") {
    console.log(JSON.stringify(await status(), null, 2));
    return;
  }

  const summary = args.summary || args.message || "Workflow update";
  const whitelist = await readPathWhitelist(args.pathsFile);
  const changedBefore = parseStatusPorcelain(runGit(["status", "--porcelain", "-uall"]).stdout)
    .filter(isAllowed)
    .filter((file) => !whitelist || whitelist.includes(file));

  if (args.command === "log") {
    const logPath = await writeLog({ summary, files: changedBefore });
    console.log(JSON.stringify({ logPath, files: changedBefore }, null, 2));
    return;
  }

  if (args.command !== "sync") throw new Error("Command must be status, log, or sync.");
  if (args.push) preparePushTarget(args.remote, args.branch);

  const firstLogPath = await writeLog({ summary, files: changedBefore });
  const staged = stageAllowedFiles(whitelist ? [...whitelist, normalizePath(path.relative(process.cwd(), firstLogPath))] : null);
  scanStagedDiff();
  const workflowCommit = commitIfNeeded(args.message || summary);
  const finalFiles = staged.length ? staged : changedBefore;
  const finalLogPath = await writeLog({
    summary: `${summary} result`,
    files: finalFiles,
    commit: workflowCommit,
    pushed: args.push,
    remote: args.push ? `${args.remote}/${args.branch}` : "",
  });
  runGit(["add", "--", finalLogPath]);
  scanStagedDiff();
  const logCommit = commitIfNeeded(`Log sync: ${summary}`);
  const finalCommit = runGit(["rev-parse", "--short", "HEAD"]).stdout;
  const tag = ensureVersionTag(args.tag, summary);
  const remoteResult = args.push ? pushPublishedVersion(args.remote, args.branch, tag) : "";

  console.log(JSON.stringify({
    summary,
    firstLogPath,
    finalLogPath,
    workflowCommit,
    logCommit,
    finalCommit,
    tag,
    pushed: args.push,
    remote: remoteResult,
    status: await status(),
  }, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
