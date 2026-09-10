import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const script = fileURLToPath(new URL("./sync-workflow.mjs", import.meta.url));
async function fixture(t) {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "workflow-sync-test-"));
  // Only this test-owned, absolute temporary root is removed.
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  const repo = path.join(root, "repo");
  await fs.mkdir(repo);
  const git = (...args) => {
    const result = spawnSync("git", args, { cwd: repo, encoding: "utf8" });
    assert.equal(result.status, 0, result.stderr);
    return result.stdout.trim();
  };
  const write = async (name, value) => {
    const target = path.join(repo, name);
    await fs.mkdir(path.dirname(target), { recursive: true });
    await fs.writeFile(target, value);
  };
  git("init", "-b", "main");
  git("config", "user.name", "Sync Test");
  git("config", "user.email", "sync-test@example.invalid");
  git("config", "commit.gpgsign", "false");
  git("config", "core.hooksPath", path.join(root, "no-hooks"));
  await write("README.md", "initial\n");
  git("add", "README.md");
  git("commit", "-m", "initial");
  const run = (...args) => spawnSync(process.execPath, [script, "sync", ...args], { cwd: repo, encoding: "utf8" });
  const whitelist = async names => {
    const name = path.join(root, "paths.txt");
    await fs.writeFile(name, names.join("\n"));
    return name;
  };
  return { root, repo, git, write, run, whitelist };
}

test("modified first path, Unicode/spaces, and no-op sync", async t => {
  const f = await fixture(t);
  await f.write("README.md", "updated\n");
  await f.write("skills/测试 空间/rules.md", "safe\n");
  let result = f.run();
  assert.equal(result.status, 0, result.stderr);
  const payload = JSON.parse(result.stdout);
  const log = await fs.readFile(payload.firstLogPath, "utf8");
  assert.match(log, /README\.md/);
  assert.match(log, /测试 空间/);
  const head = f.git("rev-parse", "HEAD");
  result = f.run();
  assert.equal(result.status, 0, result.stderr);
  assert.equal(JSON.parse(result.stdout).unchanged, true);
  assert.equal(f.git("rev-parse", "HEAD"), head);
});

test("pre-staged allowed file outside whitelist stays staged and is not committed", async t => {
  const f = await fixture(t);
  await f.write("skills/other.md", "user work\n");
  f.git("add", "skills/other.md");
  await f.write("README.md", "approved\n");
  const before = f.git("diff", "--cached");
  const head = f.git("rev-parse", "HEAD");
  const result = f.run("--paths-file", await f.whitelist(["README.md"]));
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /index preserved/);
  assert.equal(f.git("diff", "--cached"), before);
  assert.equal(f.git("rev-parse", "HEAD"), head);
  await assert.rejects(fs.access(path.join(f.repo, "sync-logs")));
});

test("pre-staged project asset is rejected without unstaging", async t => {
  const f = await fixture(t);
  await f.write("projects/private.txt", "private\n");
  f.git("add", "projects/private.txt");
  const before = f.git("diff", "--cached");
  assert.notEqual(f.run().status, 0);
  assert.equal(f.git("diff", "--cached"), before);
});

test("automatic log cannot carry unreviewed existing log edits", async t => {
  const f = await fixture(t);
  const d = new Date();
  const stamp = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const log = `sync-logs/${stamp}.md`;
  await f.write(log, "unrelated user log\n");
  await f.write("README.md", "approved\n");
  const result = f.run("--paths-file", await f.whitelist(["README.md"]));
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /Existing log edits outside whitelist/);
  assert.equal(await fs.readFile(path.join(f.repo, log), "utf8"), "unrelated user log\n");
  assert.equal(f.git("diff", "--cached"), "");
});

test("sensitive and traversal paths are rejected", async t => {
  const f = await fixture(t);
  for (const name of ["skills/tool/.env", "skills/tool/cookies.json", "skills/../README.md", "skills/key.pem"]) {
    const result = f.run("--paths-file", await f.whitelist([name]));
    assert.notEqual(result.status, 0, name);
    assert.match(result.stderr, /disallowed/);
  }
});

test("concrete secret blocked without echoing value", async t => {
  const f = await fixture(t);
  const secret = ["sk", "x".repeat(36)].join("-");
  await f.write("skills/config.txt", secret);
  const head = f.git("rev-parse", "HEAD");
  const result = f.run();
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /Secret scan failed/);
  assert.equal(result.stderr.includes(secret), false);
  assert.equal(f.git("rev-parse", "HEAD"), head);
});

test("removing an old secret is allowed; environment reference is not a secret", async t => {
  const f = await fixture(t);
  await f.write("skills/config.txt", ["sk", "x".repeat(36)].join("-"));
  f.git("add", "skills/config.txt");
  f.git("commit", "-m", "fixture legacy credential");
  await f.write("skills/config.txt", "OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY\n");
  const result = f.run();
  assert.equal(result.status, 0, result.stderr);
});

test("tracked deletion is committed and logged", async t => {
  const f = await fixture(t);
  await f.write("skills/old.md", "obsolete\n");
  f.git("add", "skills/old.md");
  f.git("commit", "-m", "fixture");
  await fs.unlink(path.join(f.repo, "skills/old.md"));
  const result = f.run();
  assert.equal(result.status, 0, result.stderr);
  assert.match(f.git("show", "--format=", "--name-status", "HEAD"), /D\s+skills\/old.md/);
});

test("staged symlink cannot be published", async t => {
  const f = await fixture(t);
  const blob = f.git("rev-parse", "HEAD:README.md");
  f.git("update-index", "--add", "--cacheinfo", `120000,${blob},skills/link`);
  const result = f.run();
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /symlink\/submodule/);
});

async function remoteFixture(t) {
  const f = await fixture(t);
  const remote = path.join(f.root, "remote.git");
  f.git("init", "--bare", remote);
  f.git("remote", "add", "github", remote);
  f.git("push", "github", "main");
  return { ...f, remote };
}

test("successful push verified and repeat push adds no commit", async t => {
  const f = await remoteFixture(t);
  await f.write("README.md", "publish\n");
  let result = f.run("--push", "--remote", "github");
  assert.equal(result.status, 0, result.stderr);
  const payload = JSON.parse(result.stdout);
  assert.equal(payload.pushed, true);
  const log = await fs.readFile(payload.firstLogPath, "utf8");
  assert.match(log, /Publication: pending/);
  assert.doesNotMatch(log, /Pushed: yes/);
  const head = f.git("rev-parse", "HEAD");
  assert.match(f.git("ls-remote", "github", "refs/heads/main"), new RegExp(`^${head}`));
  result = f.run("--push", "--remote", "github");
  assert.equal(result.status, 0, result.stderr);
  assert.equal(f.git("rev-parse", "HEAD"), head);
});

test("failed push never logs success; push-only recovery reuses commit", async t => {
  const f = await remoteFixture(t);
  f.git("config", "remote.github.pushurl", path.join(f.root, "missing.git"));
  await f.write("README.md", "publish later\n");
  const result = f.run("--push", "--remote", "github");
  assert.notEqual(result.status, 0);
  const logs = await fs.readdir(path.join(f.repo, "sync-logs"));
  const log = await fs.readFile(path.join(f.repo, "sync-logs", logs[0]), "utf8");
  assert.match(log, /Publication: pending/);
  assert.doesNotMatch(log, /Pushed: yes/);
  const head = f.git("rev-parse", "HEAD");
  f.git("config", "--unset", "remote.github.pushurl");
  const recovered = f.run("--push", "--remote", "github");
  assert.equal(recovered.status, 0, recovered.stderr);
  assert.equal(f.git("rev-parse", "HEAD"), head);
});

test("remote-ahead blocks before local commit", async t => {
  const f = await remoteFixture(t);
  // Create a remote-only commit using a second local clone.
  const other = path.join(f.root, "other");
  f.git("clone", "-b", "main", f.remote, other);
  f.git("-C", other, "config", "user.name", "Remote Test");
  f.git("-C", other, "config", "user.email", "remote-test@example.invalid");
  f.git("-C", other, "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-m", "remote change");
  f.git("-C", other, "push", "origin", "main");
  await f.write("README.md", "local change\n");
  const head = f.git("rev-parse", "HEAD");
  const result = f.run("--push", "--remote", "github");
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /not in local HEAD/);
  assert.equal(f.git("rev-parse", "HEAD"), head);
});
