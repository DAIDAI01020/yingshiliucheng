---
name: image-generation-controller
description: Orchestrate logged Banana generation and review-board creation for film visual workflows. Use when the user explicitly chooses Banana and wants one command to run preflight or generation, save images/prompts/logs, and build a side-by-side image review board.
---

# Image Generation Controller

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

## Fast Banana Default

When the user says `出图`, `用 Banana 出`, `继续出`, `重出`, or `给我图就行`, and the current context already identifies the shots/prompts, enter fast execution mode:

1. Do not restate a long plan.
2. Use Banana unless the user explicitly names another generator.
3. Use `prompt-mode compact`.
4. Keep `image_size: 2K`.
5. Generate only the requested shots or failed shots.
6. Build the review board.
7. Return image previews/paths and one short QC sentence.

If prompts are not ready, ask for or generate the minimal missing prompt first.

## Script Usage

From this skill folder:

```powershell
node .\scripts\run-image-generation.mjs --tool banana --input H:\yingshi\input.json --dry-run
node .\scripts\run-image-generation.mjs --tool banana --input H:\yingshi\input.json
node .\scripts\run-image-generation.mjs --job H:\yingshi\projects\project\generation-jobs\job.json
node .\scripts\run-image-generation.mjs --job H:\yingshi\projects\project\generation-jobs\job.json --dry-run
node .\scripts\run-image-generation.mjs --tool banana --input H:\yingshi\input.json --prompt-mode compact
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
- Banana defaults to `2K` and `prompt-mode compact` when compact prompts are available.
- Do not call real APIs in dry-run mode.
- Do not store or print API keys.
- If the required API key is missing in real-generation mode, stop before calling the generator.
- Always build a review board after the generator creates `generation-log.json`, including dry-run tasks.
- When using `--job` with `projectRoot`, always update `project-manifest.json` and `asset-index.json`.
- If generation partly fails, still build the review board from the log and report failed shots.
- For prompt-only requests, do not use this skill. Use prompt director skills instead.

