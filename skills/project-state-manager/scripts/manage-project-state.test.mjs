import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const script = fileURLToPath(new URL("./manage-project-state.mjs", import.meta.url));
function command(root, ...args) {
  const result = spawnSync(process.execPath, [script, ...args, "--project-root", root], { encoding: "utf8" });
  assert.equal(result.status, 0, result.stderr);
  return JSON.parse(result.stdout);
}
async function write(file, value) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, typeof value === "string" ? value : JSON.stringify(value));
}
async function fixture(t) {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "project-evidence-test-"));
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  command(root, "init", "--workflow", "short-drama", "--route", "storyboard-execution");
  return root;
}
async function state(root) {
  return {
    manifest: JSON.parse(await fs.readFile(path.join(root, "project-manifest.json"), "utf8")),
    index: JSON.parse(await fs.readFile(path.join(root, "asset-index.json"), "utf8")),
  };
}

test("draft status cannot be overridden by an approved example", async (t) => {
  const root = await fixture(t);
  await write(path.join(root, "references", "scene-map.md"), "# Scene\nstatus: draft\n\n```text\nstatus: approved\n```\n");
  assert.equal(command(root, "check").currentState.gates.sceneMap, false);
});
test("historical status cannot stand in for current metadata", async (t) => {
  const root = await fixture(t);
  await write(path.join(root, "references", "scene-map.md"), "# Scene\n\n## History\nstatus: approved\n");
  assert.equal(command(root, "check").currentState.gates.sceneMap, false);
});
test("current approved metadata passes despite later historical draft", async (t) => {
  const root = await fixture(t);
  await write(path.join(root, "references", "scene-map.md"), "# Scene\nstatus: approved\n\n## History\nstatus: draft\n");
  assert.equal(command(root, "check").currentState.gates.sceneMap, true);
});
test("dry-run planned image is retained as a pending record, not generated media", async (t) => {
  const root = await fixture(t);
  const log = path.join(root, "generation-runs", "dry", "generation-log.json");
  await write(log, { dryRun: true, tool: "banana", outputDir: path.dirname(log), shots: [{ shot: "S01", status: "dry-run", filePath: path.join(root, "not-generated.png") }] });
  command(root, "ingest", "--generation-log", log);
  const result = await state(root);
  assert.equal(result.index.assets[0].filePath, null);
  assert.equal(result.index.assets[0].assetState, "待执行");
  assert.equal(result.manifest.stages.imageGeneration, "dry-run通过");
  assert.notEqual(result.manifest.generationRuns[0].status, "完成");
});
test("missing output cannot become a successful image asset", async (t) => {
  const root = await fixture(t);
  const log = path.join(root, "generation-runs", "missing", "generation-log.json");
  await write(log, { tool: "banana", outputDir: path.dirname(log), shots: [{ shot: "S01", status: "success", filePath: path.join(root, "missing.png") }] });
  command(root, "ingest", "--generation-log", log);
  const result = await state(root);
  assert.equal(result.index.assets[0].filePath, null);
  assert.equal(result.index.assets[0].status, "output_missing");
  assert.equal(result.manifest.stages.imageGeneration, "待检查");
});
test("reported video success requires a nonempty file", async (t) => {
  const root = await fixture(t);
  const run = path.join(root, "video-runs", "empty", "run_manifest.json");
  const video = path.join(root, "empty.mp4");
  await write(video, "");
  await write(run, { provider: "fixture", status: "succeeded", outputs: { video } });
  const result = command(root, "ingest-video", "--run-manifest", run);
  assert.equal(result.asset.filePath, "");
  assert.equal(result.asset.status, "output_missing");
  assert.equal((await state(root)).manifest.stages.videoGeneration, "待检查");
});
test("existing image evidence ingests idempotently without changing selection", async (t) => {
  const root = await fixture(t);
  const log = path.join(root, "generation-runs", "real", "generation-log.json");
  const filePath = path.join(path.dirname(log), "S01.png");
  await write(filePath, "nonempty fixture; semantic/media decoding belongs to QC");
  await write(log, { tool: "banana", outputDir: path.dirname(log), shots: [{ shot: "S01", status: "success", filePath }] });
  command(root, "ingest", "--generation-log", log);
  const selected = await state(root);
  selected.index.assets[0].assetState = "入选";
  await write(path.join(root, "asset-index.json"), selected.index);
  command(root, "ingest", "--generation-log", log);
  const result = await state(root);
  assert.equal(result.index.assets.length, 1);
  assert.equal(result.index.assets[0].filePath, filePath);
  assert.equal(result.index.assets[0].assetState, "入选");
  assert.equal(result.manifest.stages.imageGeneration, "已出图");
});

test("fenced and indented status examples are not current approval", async (t) => {
  const root = await fixture(t);
  await write(path.join(root, "references", "scene-map.md"), "# Scene\n~~~text\nstatus: approved\n~~~\n    status: approved\nstatus: draft\n");
  assert.equal(command(root, "check").currentState.gates.sceneMap, false);
});

test("dry-run errors and empty logs cannot claim completion", async (t) => {
  const root = await fixture(t);
  const log = path.join(root, "generation-runs", "failed-dry", "generation-log.json");
  await write(log, { dryRun: true, outputDir: path.dirname(log), shots: [{ status: "failed" }] });
  command(root, "ingest", "--generation-log", log);
  assert.equal((await state(root)).manifest.stages.imageGeneration, "失败");
  await write(log, { dryRun: true, outputDir: path.dirname(log), shots: [] });
  command(root, "ingest", "--generation-log", log);
  assert.equal((await state(root)).manifest.stages.imageGeneration, "待检查");
});

test("relative video outputs need both success status and physical evidence", async (t) => {
  const root = await fixture(t);
  const run = path.join(root, "video-runs", "real", "run_manifest.json");
  const video = path.join(path.dirname(run), "S01.mp4");
  await write(video, "nonempty fixture; media decoding belongs to QC");
  await write(run, { provider: "fixture", status: "pending", outputs: { video: "S01.mp4" } });
  const pending = command(root, "ingest-video", "--run-manifest", run);
  assert.equal(pending.asset.assetState, "待检查");
  await write(run, { provider: "fixture", status: "succeeded", outputs: { video: "S01.mp4" } });
  command(root, "ingest-video", "--run-manifest", run);
  const result = await state(root);
  assert.equal(result.index.assets.length, 1);
  assert.equal(result.index.assets[0].filePath, video);
  assert.equal(result.index.assets[0].assetState, "候选");
  assert.equal(result.manifest.stages.videoGeneration, "已生成");
  result.index.assets[0].assetState = "入选";
  await write(path.join(root, "asset-index.json"), result.index);
  const reingested = command(root, "ingest-video", "--run-manifest", run);
  assert.equal(reingested.asset.assetState, "入选");
  assert.equal(reingested.asset.createdAt, result.index.assets[0].createdAt);
});
