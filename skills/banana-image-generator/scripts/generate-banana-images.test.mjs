import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const script = fileURLToPath(new URL("./generate-banana-images.mjs", import.meta.url));

async function fixture(t) {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "banana-output-test-"));
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  const projectRoot = path.join(root, "project");
  await fs.mkdir(projectRoot);
  return { root, projectRoot };
}

async function run(root, input, args = []) {
  const inputPath = path.join(root, "input.json");
  await fs.writeFile(inputPath, JSON.stringify({ projectName: "sample", shots: [{ shot: "S01", prompt: "A red product box on a plain white table, soft light, centered composition." }], ...input }));
  const env = { ...process.env };
  delete env.OPENROUTER_API_KEY;
  delete env.BANANA_MODEL;
  return spawnSync(process.execPath, [script, "--input", inputPath, "--dry-run", ...args], { cwd: root, encoding: "utf8", env });
}

test("standalone output follows the invocation workspace", async (t) => {
  const { root } = await fixture(t);
  const result = await run(root, {});
  assert.equal(result.status, 0, result.stderr);
  const data = JSON.parse(result.stdout);
  assert.ok(data.outputDir.startsWith(path.join(root, "outputs", "banana-images") + path.sep));
  assert.equal(data.status, "dry-run");
});

test("managed default is inside its project and preserves explicit model", async (t) => {
  const { root, projectRoot } = await fixture(t);
  const result = await run(root, { projectRoot, model: "configured-pro-model" });
  assert.equal(result.status, 0, result.stderr);
  const data = JSON.parse(result.stdout);
  assert.ok(data.outputDir.startsWith(path.join(projectRoot, "generation-runs", "banana") + path.sep));
  assert.equal(data.model, "configured-pro-model");
});

test("explicit managed output overrides the default", async (t) => {
  const { root, projectRoot } = await fixture(t);
  const outputDir = path.join(projectRoot, "approved output");
  const result = await run(root, { projectRoot }, ["--output-dir", outputDir]);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(JSON.parse(result.stdout).outputDir, outputDir);
});

test("managed output escaping the project fails before creating output", async (t) => {
  const { root, projectRoot } = await fixture(t);
  const outputDir = path.join(root, "outside");
  const result = await run(root, { projectRoot, outputDir });
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /inside projectRoot/);
  await assert.rejects(fs.access(outputDir), { code: "ENOENT" });
});
