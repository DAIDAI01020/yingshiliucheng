import { spawnSync } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";

const CONFIRMED = new Set(["approved", "direct_test", "confirmed"]);
const GENERATORS = new Set([
  "text2image", "image2image", "image_upscale", "text2video", "image2video",
  "frames2video", "multiframe2video", "multimodal2video",
]);

function parseArgs(argv) {
  const [command = "doctor", ...rest] = argv.slice(2);
  const args = { command };
  for (let index = 0; index < rest.length; index += 1) {
    const arg = rest[index];
    if (!arg.startsWith("--")) throw new Error(`Unknown argument: ${arg}`);
    const key = arg.slice(2).replace(/-([a-z])/g, (_, char) => char.toUpperCase());
    const next = rest[index + 1];
    if (!next || next.startsWith("--")) args[key] = true;
    else {
      args[key] = next;
      index += 1;
    }
  }
  return args;
}

function runCli(cli, commandArgs, { allowFailure = false } = {}) {
  const result = spawnSync(cli, commandArgs, {
    cwd: process.cwd(),
    env: process.env,
    encoding: "utf8",
    maxBuffer: 1024 * 1024 * 30,
    shell: false,
  });
  if (result.error) throw new Error(`Dreamina CLI unavailable: ${result.error.message}`);
  const stdout = result.stdout?.trim() || "";
  const stderr = result.stderr?.trim() || "";
  if (result.status !== 0 && !allowFailure) {
    throw new Error([stderr, stdout].filter(Boolean).join("\n") || `Dreamina CLI exited ${result.status}`);
  }
  return { status: result.status, stdout, stderr, combined: [stdout, stderr].filter(Boolean).join("\n") };
}

function parseLastJson(text) {
  const lines = String(text || "").split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  for (let index = lines.length - 1; index >= 0; index -= 1) {
    try {
      return JSON.parse(lines.slice(index).join("\n"));
    } catch {
      // Keep scanning for the start of a trailing JSON object.
    }
  }
  return {};
}

function findValue(object, wanted) {
  if (!object || typeof object !== "object") return undefined;
  for (const [key, value] of Object.entries(object)) {
    if (wanted.includes(key.toLowerCase())) return value;
    const nested = findValue(value, wanted);
    if (nested !== undefined) return nested;
  }
  return undefined;
}

function parseResult(text) {
  const json = parseLastJson(text);
  const match = (name) => new RegExp(`${name}\\s*[=:]\\s*([^\\s,]+)`, "i").exec(text)?.[1] || "";
  const submitId = findValue(json, ["submit_id", "submitid", "task_id", "taskid"]) || match("submit_id|task_id");
  const status = String(findValue(json, ["gen_status", "status", "task_status"]) || match("gen_status|task_status|status") || "unknown").toLowerCase();
  const failReason = findValue(json, ["fail_reason", "error", "message"]) || "";
  const availableCredit = findValue(json, ["available_credits", "available_credit", "credits", "credit", "balance", "inspiration_value"]);
  const paths = [];
  function collect(value, key = "") {
    if (typeof value === "string" && /(path|file|download)/i.test(key)) paths.push(value);
    else if (Array.isArray(value)) value.forEach((item) => collect(item, key));
    else if (value && typeof value === "object") Object.entries(value).forEach(([childKey, child]) => collect(child, childKey));
  }
  collect(json);
  return {
    raw_json: json,
    submit_id: String(submitId || ""),
    gen_status: status,
    fail_reason: String(failReason || ""),
    available_credits: Number.isFinite(Number(availableCredit)) ? Number(availableCredit) : null,
    output_paths: [...new Set(paths)],
  };
}

function helpOptions(helpText) {
  return new Set([...String(helpText || "").matchAll(/--([a-zA-Z0-9][a-zA-Z0-9_-]*)/g)].map((match) => match[1]));
}

function optionName(options, candidates, requiredLabel = "") {
  const match = candidates.find((candidate) => options.has(candidate));
  if (!match && requiredLabel) throw new Error(`Dreamina live help has no supported option for ${requiredLabel}.`);
  return match || "";
}

function pushOption(target, options, candidates, value, requiredLabel = "") {
  if (value === undefined || value === null || value === "") return;
  const name = optionName(options, candidates, requiredLabel);
  if (name) target.push(`--${name}=${value}`);
}

async function buildGeneratorArgs(args, helpText) {
  const options = helpOptions(helpText);
  const commandArgs = [];
  const prompt = args.promptFile ? await fs.readFile(path.resolve(args.promptFile), "utf8") : args.prompt;
  pushOption(commandArgs, options, ["prompt", "text"], prompt, "prompt");
  pushOption(commandArgs, options, ["negative_prompt", "negative-prompt", "negative"], args.negativePrompt);
  pushOption(commandArgs, options, ["image", "image_file", "image-file", "image_path", "image-path", "image_url", "image-url"], args.imageFile || args.imageUrl, args.subcommand === "image2video" ? "image reference" : "");
  pushOption(commandArgs, options, ["first_frame", "first-frame", "first_image", "first-image"], args.firstFrame);
  pushOption(commandArgs, options, ["last_frame", "last-frame", "end_frame", "end-frame", "last_image", "last-image"], args.lastFrame);
  pushOption(commandArgs, options, ["duration"], args.duration);
  pushOption(commandArgs, options, ["ratio", "aspect_ratio", "aspect-ratio"], args.ratio);
  pushOption(commandArgs, options, ["resolution", "size"], args.resolution);
  pushOption(commandArgs, options, ["model", "model_version", "model-version"], args.model);
  pushOption(commandArgs, options, ["session"], args.session);
  pushOption(commandArgs, options, ["poll"], args.poll);
  pushOption(commandArgs, options, ["download_dir", "download-dir", "output_dir", "output-dir"], args.outputDir);
  if (args.extraArgsFile) {
    const extra = JSON.parse(await fs.readFile(path.resolve(args.extraArgsFile), "utf8"));
    if (!Array.isArray(extra) || extra.some((item) => typeof item !== "string")) {
      throw new Error("--extra-args-file must contain a JSON array of strings.");
    }
    commandArgs.push(...extra);
  }
  return commandArgs;
}

async function main() {
  const args = parseArgs(process.argv);
  const cli = args.cliScript ? process.execPath : String(args.cli || process.env.DREAMINA_CLI_PATH || "dreamina");
  const cliPrefix = args.cliScript ? [path.resolve(String(args.cliScript))] : [];
  const invoke = (commandArgs, options) => runCli(cli, [...cliPrefix, ...commandArgs], options);

  if (args.command === "doctor") {
    const help = invoke(["-h"]);
    console.log(JSON.stringify({ available: true, cli, help_checked: true, help_excerpt: help.stdout.slice(0, 2000) }, null, 2));
    return;
  }

  if (args.command === "credit") {
    const help = invoke(["user_credit", "-h"]);
    const result = invoke(["user_credit"]);
    console.log(JSON.stringify({ cli, command: "user_credit", help_checked: Boolean(help.combined), result: parseResult(result.combined), raw: result.stdout }, null, 2));
    return;
  }

  if (args.command === "recover") {
    if (!args.submitId) throw new Error("recover requires --submit-id.");
    const help = invoke(["query_result", "-h"]);
    const options = helpOptions(help.combined);
    const commandArgs = [];
    pushOption(commandArgs, options, ["submit_id", "submit-id"], args.submitId, "submit_id");
    pushOption(commandArgs, options, ["download_dir", "download-dir", "output_dir", "output-dir"], args.outputDir);
    const result = invoke(["query_result", ...commandArgs], { allowFailure: true });
    const parsed = parseResult(result.combined);
    console.log(JSON.stringify({ cli, command: "query_result", help_checked: true, exit_code: result.status, ...parsed }, null, 2));
    if (result.status !== 0 || parsed.gen_status === "fail") process.exitCode = 2;
    return;
  }

  if (args.command !== "execute") throw new Error("Command must be doctor, credit, execute, or recover.");
  const subcommand = String(args.subcommand || "");
  if (!GENERATORS.has(subcommand)) throw new Error(`Unsupported Dreamina generation command: ${subcommand || "missing"}`);
  if (!CONFIRMED.has(String(args.generationConfirmation || "").toLowerCase())) {
    throw new Error("Dreamina paid submission requires --generation-confirmation approved/direct_test/confirmed.");
  }
  const help = invoke([subcommand, "-h"]);
  const commandArgs = await buildGeneratorArgs({ ...args, subcommand }, help.combined);
  const result = invoke([subcommand, ...commandArgs], { allowFailure: true });
  const parsed = parseResult(result.combined);
  const accepted = Boolean(parsed.submit_id) && ["querying", "success"].includes(parsed.gen_status);
  console.log(JSON.stringify({
    cli,
    command: subcommand,
    help_checked: true,
    exit_code: result.status,
    accepted,
    ...parsed,
  }, null, 2));
  if (result.status !== 0 || parsed.gen_status === "fail" || !accepted) process.exitCode = 2;
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
