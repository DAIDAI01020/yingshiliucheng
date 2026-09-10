import { spawnSync } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";

const ALLOWED_PATHS = [".gitignore", "README.md", "WORKFLOW.md", "skills", "sync-logs"];
const BLOCKED_PREFIXES = ["outputs/", "projects/"];
const BLOCKED_SUFFIXES = [".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".mov", ".wav", ".mp3"];
const SECRET_PATTERNS = [
  /sk-[A-Za-z0-9_-]{20,}/,
  /(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})/,
  /(?:OPENAI|OPENROUTER|ARK|DREAMINA|JIMENG)_(?:API_KEY|TOKEN|COOKIE)\s*[=:]\s*['"]?[A-Za-z0-9+/_=-]{24,}/i,
  /-----BEGIN (?:(?:OPENSSH|RSA|EC|DSA) )?PRIVATE KEY-----/,
];

function parseArgs(argv) {
  const [command = "status", ...rest] = argv.slice(2);
  const args = { command, push: false, remote: "origin", branch: "main" };
  for (let i = 0; i < rest.length; i += 1) {
    const arg = rest[i];
    if (arg !== "--push" && (!rest[i + 1] || rest[i + 1].startsWith("--"))) throw new Error(`Missing value for ${arg}`);
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
  const { allowFailure, raw, ...spawnOptions } = options;
  const result = spawnSync("git", args, {
    cwd: process.cwd(),
    encoding: "utf8",
    maxBuffer: 1024 * 1024 * 30,
    ...spawnOptions,
  });
  if (result.error) throw result.error;
  if (result.status !== 0 && !allowFailure) {
    // Command output may contain credentials from remote URLs or hooks.
    throw new Error(`git ${args[0]} failed (exit ${result.status}); inspect Git locally for details.`);
  }
  return {
    status: result.status,
    stdout: raw ? result.stdout : result.stdout.trim(),
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

function gitPaths(args) {
  return runGit(args, { raw: true }).stdout.split("\0").filter(Boolean);
}

function stagedPaths() {
  return gitPaths(["diff", "--cached", "--name-only", "--no-renames", "-z"]);
}

function changedPaths() {
  return [...new Set([
    ...stagedPaths(),
    ...gitPaths(["diff", "--name-only", "--no-renames", "-z"]),
    ...gitPaths(["ls-files", "--others", "--exclude-standard", "-z"]),
  ])];
}

function isAllowed(filePath) {
  const p = filePath.replace(/\\/g, "/");
  if (p !== p.trim() || path.isAbsolute(p) || /^[A-Za-z]:/.test(p) || /[\x00-\x1f]/.test(p)) return false;
  const parts = p.split("/");
  if (parts.some(part => !part || part === "." || part === ".." || part.toLowerCase() === ".git")) return false;
  if (parts.some(part => /^(?:\.env(?:\..*)?|id_(?:rsa|ed25519|ecdsa|dsa)(?:\..*)?|credentials(?:\..*)?|cookies?(?:\..*)?|secrets?(?:\..*)?)$/i.test(part))) return false;
  if (/\.(?:pem|key|p12|pfx)$/i.test(p)) return false;
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

async function writeLog({ summary, files, commit = "", remote = "" }) {
  const { date, time } = nowStamp();
  const logDir = path.join(process.cwd(), "sync-logs");
  await fs.mkdir(logDir, { recursive: true });
  const logPath = path.join(logDir, `${date}.md`);
  const lines = [
    `## ${time} ${summary || "Workflow update"}`,
    "",
    `- Commit: ${commit || "pending"}`,
    `- Publication: ${remote ? "pending; verify remote HEAD after push" : "local only"}`,
    `- Remote: ${remote || "not pushed"}`,
    "- Changed files:",
    ...(files.length ? files.map((file) => `  - ${file}`) : ["  - none"]),
    "",
  ];
  await fs.appendFile(logPath, `${lines.join("\n")}\n`, "utf8");
  return logPath;
}

function scanStagedDiff() {
  const files = gitPaths(["diff", "--cached", "--name-only", "--no-renames", "--diff-filter=ACMRT", "-z"]);
  for (const file of files) {
    const entries = gitPaths(["ls-files", "--stage", "-z", "--", `:(literal)${file}`]);
    if (entries.some(entry => /^(?:120000|160000) /.test(entry))) throw new Error(`Refusing symlink/submodule: ${file}`);
    const content = runGit(["show", `:${file}`], { raw: true }).stdout;
    if (SECRET_PATTERNS.some(pattern => pattern.test(content))) throw new Error(`Secret scan failed in ${file}; value withheld.`);
  }
}

function stageAllowedFiles(paths) {
  for (const file of stagedPaths()) {
    const entries = gitPaths(["ls-files", "--stage", "-z", "--", `:(literal)${file}`]);
    if (entries.some(entry => /^(?:120000|160000) /.test(entry))) throw new Error(`Refusing symlink/submodule: ${file}`);
  }
  const unstaged = new Set([
    ...gitPaths(["diff", "--name-only", "--no-renames", "-z"]),
    ...gitPaths(["ls-files", "--others", "--exclude-standard", "-z"]),
  ]);
  const targets = paths.filter(file => unstaged.has(file));
  if (targets.length) runGit(["add", "--", ...targets.map(file => `:(literal)${file}`)]);
  const staged = stagedPaths();
  const disallowed = staged.filter(file => !isAllowed(file) || !paths.includes(file));
  if (disallowed.length) {
    throw new Error(`Refusing to stage disallowed files:\n${disallowed.join("\n")}`);
  }
  return staged;
}

function commitIfNeeded(message) {
  const diffStatus = runGit(["diff", "--cached", "--quiet"], { allowFailure: true }).status;
  if (diffStatus === 0) return "";
  if (diffStatus !== 1) throw new Error("Cannot inspect staged changes; refusing to commit.");
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
  runGit(["push", "-u", remote, branch]);
  if (tag) runGit(["push", remote, `refs/tags/${tag}`]);
  const local = runGit(["rev-parse", "HEAD"]).stdout;
  const published = runGit(["ls-remote", remote, `refs/heads/${branch}`]).stdout.split(/\s+/)[0];
  if (published !== local) throw new Error("Push verification failed: remote branch does not match local HEAD.");
  if (tag) {
    const publishedTag = runGit(["ls-remote", remote, `refs/tags/${tag}`, `refs/tags/${tag}^{}`]).stdout;
    if (!publishedTag.split(/\r?\n/).some(line => line.split(/\s+/)[0] === local)) throw new Error("Push verification failed: tag does not match local HEAD.");
  }
  return `${remote}/${branch}`;
}

async function checkPlainFiles(files) {
  for (const file of files) {
    const parts = file.split("/");
    for (let i = 1; i <= parts.length; i += 1) {
      const current = path.resolve(...parts.slice(0, i));
      const stat = await fs.lstat(current).catch(error => {
        if (error.code === "ENOENT") return null; // Tracked deletion.
        throw error;
      });
      if (stat?.isSymbolicLink()) throw new Error(`Refusing symlink path: ${file}`);
      if (i === parts.length && stat && !stat.isFile()) throw new Error(`Expected an explicit file path: ${file}`);
    }
  }
}

async function status() {
  return {
    branch: runGit(["branch", "--show-current"]).stdout,
    status: runGit(["status", "--short", "--branch"]).stdout,
    remote: runGit(["remote"]).stdout,
    latestCommit: runGit(["log", "--oneline", "-1"]).stdout,
  };
}

async function main() {
  const args = parseArgs(process.argv);
  const root = runGit(["rev-parse", "--show-toplevel"]).stdout;
  if (path.resolve(root).toLowerCase() !== path.resolve(process.cwd()).toLowerCase()) throw new Error("Run from the repository root.");
  if (args.command === "status") {
    console.log(JSON.stringify(await status(), null, 2));
    return;
  }

  const summary = args.summary || args.message || "Workflow update";
  const whitelist = await readPathWhitelist(args.pathsFile);
  const changedBefore = changedPaths()
    .filter(isAllowed)
    .filter((file) => !whitelist || whitelist.includes(file));

  if (args.command === "log") {
    await checkPlainFiles([`sync-logs/${nowStamp().date}.md`]);
    const logPath = await writeLog({ summary, files: changedBefore });
    console.log(JSON.stringify({ logPath, files: changedBefore }, null, 2));
    return;
  }

  if (args.command !== "sync") throw new Error("Command must be status, log, or sync.");
  const outside = stagedPaths().filter(file => !isAllowed(file) || (whitelist && !whitelist.includes(file)));
  if (outside.length) throw new Error(`Pre-staged files outside publication scope; index preserved:\n${outside.join("\n")}`);
  const logRelative = `sync-logs/${nowStamp().date}.md`;
  if (changedBefore.length && changedPaths().includes(logRelative) && !changedBefore.includes(logRelative)) {
    throw new Error("Existing log edits outside whitelist; review and include them explicitly before sync.");
  }
  await checkPlainFiles(changedBefore);
  await checkPlainFiles([logRelative]);
  if (args.push) preparePushTarget(args.remote, args.branch);

  let firstLogPath = "";
  let workflowCommit = "";
  if (changedBefore.length) {
    stageAllowedFiles(changedBefore);
    scanStagedDiff();
    firstLogPath = await writeLog({ summary, files: changedBefore, remote: args.push ? `${args.remote}/${args.branch}` : "" });
    stageAllowedFiles([...new Set([...changedBefore, normalizePath(path.relative(process.cwd(), firstLogPath))])]);
    scanStagedDiff();
    workflowCommit = commitIfNeeded(args.message || summary);
  }
  const finalCommit = runGit(["rev-parse", "--short", "HEAD"]).stdout;
  const tag = ensureVersionTag(args.tag, summary);
  const remoteResult = args.push ? pushPublishedVersion(args.remote, args.branch, tag) : "";

  console.log(JSON.stringify({
    summary,
    firstLogPath,
    finalLogPath: firstLogPath,
    workflowCommit,
    logCommit: "",
    unchanged: !workflowCommit,
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
