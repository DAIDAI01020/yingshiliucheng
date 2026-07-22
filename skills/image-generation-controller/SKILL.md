---
name: image-generation-controller
description: Legacy internal compatibility wrapper for managed Banana generation jobs and review-board creation. New user-facing Banana requests must route to banana-image-generator; built-in image requests must route to builtin-imagegen-director. Use this wrapper only when an existing managed job explicitly requires the legacy combined generation, review-board, and state-ingest sequence.
---

# Image Generation Controller

This is not a third user-facing image-generation skill. The two user-facing routes are `$banana-image-generator` for Banana and `$builtin-imagegen-director` for built-in imagegen. Keep this wrapper only for legacy managed jobs that require its combined review/state sequence.

## Core Role

This skill is the execution coordinator for logged Banana image generation. It does not replace `$banana-image-generator`, the built-in imagegen route, `$midjourney`, or `$image-review-board`; it calls the Banana generator in a stable sequence so the user does less manual work.

User-facing naming:

- Banana route: Banana / Nano Banana / OpenRouter.
- Built-in latest imagegen route: `image`, `ChatGPT Image`, `image-2`, `内置最新模型出图`; use the built-in `image_gen` tool directly, not this controller.
- Midjourney route: `$midjourney`; keep it independent.

## Required Decision

The user must specify or imply the logged Banana generation route:

- `banana`

If the user says `image / ChatGPT Image / image-2`, do not use this controller; use built-in imagegen directly. If the user says `MJ / Midjourney / Legnext`, use `$midjourney`. If the user only says `出图 / 重出 / 继续出` and the current project already uses Banana, default to Banana fast mode.

## Default Flow

1. Confirm the mode:
   - `dry-run` if the user says `先测一下`, `检查`, `dry-run`, or `出图前检查`.
   - real generation only when the user explicitly asks to generate images.
2. Accept either legacy `--input` or managed `--job`:
   - `--input` keeps the old generator JSON flow.
   - `--job` reads a unified `generation-job.json` from `$project-state-manager`.
3. Check `OPENROUTER_API_KEY`.
4. Call `$banana-image-generator`.
5. Build the review board with `$image-review-board`.
6. If the job has `projectRoot`, write generation results back to `$project-state-manager`.
7. Return the task folder, generation log, review board, image paths, prompt paths, and failed-shot retry suggestions.

For managed real generation, compute an idempotency key from tool, prompt, references, model, size, and shot set. Refuse a duplicate succeeded/in-flight run, require `generation_confirmation`, and write `revision-logs/generation-run-ledger.jsonl`. `--resume` retries only the failed shot IDs from a prior partial run; it never discards successful outputs. Use `--force-new-run` only after an explicit user request for a genuinely new paid attempt.

## No Lazy Execution Rule

This controller executes only. It does not create, complete, repair, or reinterpret prompts.

Real generation may run only when the request has an audited prompt:

```text
prompt-platform-auditor decision is 通过 or 保效精简后通过
final execution prompt is present
target image tool is Banana / Banana Pro for this controller
reference image roles are explicit when references are used
project-style-lock is present for formal project batches
```

For formal or managed work, the input must be a `generation_ready_packet` or a managed job containing the same fields:

```text
generation_ready_packet
target_tool: Banana / Banana Pro
project_root:
shot_or_asset_id:
final_prompt:
negative_or_forbidden:
audit_status: 通过 / 保效精简后通过
audited_prompt_packet:
source_lock:
reference_roles:
first_frame_or_image_refs:
ratio:
output_path_rule:
state_writeback:
```

If any required prompt input is missing, stop and route back:

```text
missing poster/key-art direction -> poster-director
missing keyframe prompt -> frame-vision-director
missing platform approval -> prompt-platform-auditor
missing project state/job data -> project-state-manager
missing generation_ready_packet fields -> project-state-manager / prompt-platform-auditor
```

Do not invent a minimal prompt inside this controller. Do not use generation to discover style.

## Fast Banana Default

When the user says `出图`, `用 Banana 出`, `继续出`, `重出`, or `给我图就行`, and the current context already identifies the shots/prompts, enter fast execution mode:

1. Do not restate a long plan.
2. Use Banana unless the user explicitly names another generator.
3. Use `prompt-mode quality` unless the user explicitly asks for `省 token`, fast testing, or compact execution.
4. Keep `image_size: 2K`.
5. Generate only the requested shots or failed shots.
6. Build the review board.
7. Return image previews/paths and one short QC sentence.

If prompts are not ready, stop and route back to `$frame-vision-director`, `$poster-director`, or `$prompt-platform-auditor`. Do not generate a minimal missing prompt inside this controller.

## Script Usage

From this skill folder:

```powershell
node .\scripts\run-image-generation.mjs --tool banana --input H:\yingshi\input.json --dry-run
node .\scripts\run-image-generation.mjs --tool banana --input H:\yingshi\input.json
node .\scripts\run-image-generation.mjs --job H:\yingshi\projects\project\generation-jobs\job.json
node .\scripts\run-image-generation.mjs --job H:\yingshi\projects\project\generation-jobs\job.json --dry-run
node .\scripts\run-image-generation.mjs --tool banana --input H:\yingshi\input.json --prompt-mode quality
node .\scripts\run-image-generation.mjs --job H:\yingshi\projects\project\generation-jobs\job.json --generation-confirmation approved
node .\scripts\run-image-generation.mjs --job H:\yingshi\projects\project\generation-jobs\job.json --generation-confirmation approved --resume
```

## Output

The controller returns a JSON summary:

```json
{
  "tool": "banana",
  "mode": "dry-run",
  "outputDir": "H:\\yingshi\\outputs\\banana-images\\project\\timestamp",
  "generationLog": "H:\\...\\logs\\generation-log.json",
  "reviewBoard": "H:\\...\\review\\review-board.md",
  "projectRoot": "H:\\yingshi\\projects\\project",
  "shotCount": 1,
  "failedCount": 0,
  "shots": []
}
```

## Rules

- Default concurrency is `1`; do not parallelize API calls in v1.
- Banana defaults to `2K` and `prompt-mode quality`; use compact prompts only when explicitly requested.
- Only run real generation from an audited prompt; dry-run may inspect job shape but must still report missing audit state.
- Do not call real APIs in dry-run mode.
- Do not store or print API keys.
- If the required API key is missing in real-generation mode, stop before calling the generator.
- Always build a review board after the generator creates `generation-log.json`, including dry-run tasks.
- When using `--job` with `projectRoot`, always update `project-manifest.json` and `asset-index.json`.
- If generation partly fails, still build the review board from the log and report failed shots.
- Preserve successful shots and retry only failed items on `--resume`; default to at most two explicitly confirmed attempts.
- When available, compare `available_credits` with `estimated_cost` before submission and stop before a paid request when insufficient.
- Repeated invocation with the same idempotency key must reuse/block the existing result instead of submitting again.
- For prompt-only requests, do not use this skill. Use prompt director skills instead.

