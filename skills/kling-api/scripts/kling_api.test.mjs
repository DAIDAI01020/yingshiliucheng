import test from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import fs from "node:fs/promises";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const runner = fileURLToPath(new URL("./kling_api.mjs", import.meta.url));

function run(args, { input = "", env = process.env } = {}) {
  return new Promise(resolve => {
    const child = spawn(process.execPath, [runner, ...args], { env });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", chunk => { stdout += chunk; });
    child.stderr.on("data", chunk => { stderr += chunk; });
    child.on("close", status => resolve({ status, stdout, stderr }));
    child.stdin.end(input);
  });
}

test("setup and local doctor redact the credential", async t => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "kling-key-test-"));
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  const keyFile = path.join(root, "secrets.json");
  const secret = `api-key-kling-${"x".repeat(36)}`;
  let result = await run(["setup-key", "--key-stdin", "--key-file", keyFile], { input: secret });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.includes(secret), false);
  result = await run(["doctor", "--key-file", keyFile]);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(JSON.parse(result.stdout).source, "private-file");
  assert.equal(result.stdout.includes(secret), false);
});

test("live doctor sends Bearer auth and returns only redacted state", async t => {
  const secret = `api-key-kling-${"y".repeat(36)}`;
  let authorization = "";
  const server = http.createServer((request, response) => {
    authorization = request.headers.authorization || "";
    response.writeHead(200, { "Content-Type": "application/json" });
    response.end(JSON.stringify({ code: 0, data: { private_account_detail: "not-returned" } }));
  });
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  t.after(() => server.close());
  const port = server.address().port;
  const result = await run(["doctor", "--live", "--base-url", `http://127.0.0.1:${port}`], {
    env: { ...process.env, KLING_API_KEY: secret },
  });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(authorization, `Bearer ${secret}`);
  assert.equal(result.stdout.includes(secret), false);
  assert.equal(result.stdout.includes("private_account_detail"), false);
  assert.equal(JSON.parse(result.stdout).authenticated, true);
});

test("non-loopback HTTP endpoint is rejected", async () => {
  const result = await run(["doctor", "--base-url", "http://example.com"], {
    env: { ...process.env, KLING_API_KEY: `api-key-kling-${"z".repeat(36)}` },
  });
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /must use HTTPS/);
});
