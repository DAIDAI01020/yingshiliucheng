---
name: image-generation-controller
description: Orchestrate Banana/OpenAI image generation and review-board creation for film visual workflows. Use when the user explicitly chooses Banana or OpenAI and wants one command to run preflight or generation, save images/prompts/logs, and build a side-by-side image review board.
---

# Image Generation Controller

## Core role

This skill is the execution coordinator for image generation. It does not replace `$banana-image-generator`, `$openai-image-generator`, or `$image-review-board`; it calls them in a stable sequence so the user does less manual work.

Use it when the user says things like:

- `用 Banana 出图并整理`
- `用 OpenAI 出图并整理`
- `这批镜头帮我跑一下，用 Banana`
- `生成审片结果`
- `先测一下能不能出`

## Required decision

The user must specify the generation tool:

- `banana`
- `openai`

Do not guess the tool. If the tool is not specified, ask the user to choose Banana or OpenAI.

## Default flow

1. Confirm the mode:
   - `dry-run` if the user says `先测一下`, `检查`, `dry-run`, or `出图前检查`.
   - real generation only when the user explicitly asks to generate images.
2. Accept either legacy `--input` or managed `--job`:
   - `--input` keeps the old generator JSON flow.
   - `--job` reads a unified `generation-job.json` from `$project-state-manager`.
3. Check the required environment variable:
   - Banana: `OPENROUTER_API_KEY`
   - OpenAI: `OPENAI_API_KEY`
4. Call the matching generator script:
   - Banana: `$banana-image-generator`
   - OpenAI: `$openai-image-generator`
5. Build the review board with `$image-review-board`.
6. If the job has `projectRoot`, write generation results back to `$project-state-manager`.
7. Return:
   - generation task folder
   - `logs/generation-log.json`
   - `review/review-board.md`
   - image paths
   - prompt TXT/JSON paths
   - failed shots and retry suggestions

## Script usage

From this skill folder:

```powershell
node .\scripts\run-image-generation.mjs --tool banana --input H:\yingshi\input.json --dry-run
node .\scripts\run-image-generation.mjs --tool banana --input H:\yingshi\input.json
node .\scripts\run-image-generation.mjs --tool openai --input H:\yingshi\input.json --dry-run
node .\scripts\run-image-generation.mjs --job H:\yingshi\projects\project\generation-jobs\job.json
node .\scripts\run-image-generation.mjs --job H:\yingshi\projects\project\generation-jobs\job.json --dry-run
```

Optional:

```powershell
node .\scripts\run-image-generation.mjs --tool banana --input H:\yingshi\input.json --output-dir H:\yingshi\outputs\banana-images\project\manual_run
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
  "projectState": {
    "manifestPath": "H:\\...\\project-manifest.json",
    "assetIndexPath": "H:\\...\\asset-index.json"
  },
  "shots": [
    {
      "shot": "S01",
      "version": "v01",
      "status": "dry-run",
      "imagePath": "H:\\...\\images\\S01_banana_v01.png",
      "promptPath": "H:\\...\\prompts\\S01_banana_v01_prompt.txt",
      "promptJsonPath": "H:\\...\\prompts\\S01_banana_v01_prompt.json"
    }
  ]
}
```

## Rules

- Default concurrency is `1`; do not parallelize API calls in v1.
- Do not call real APIs in dry-run mode.
- Do not store or print API keys.
- If the required API key is missing in real-generation mode, stop before calling the generator.
- Always build a review board after the generator creates `generation-log.json`, including dry-run tasks.
- When using `--job` with `projectRoot`, always update `project-manifest.json` and `asset-index.json`.
- If generation partly fails, still build the review board from the log and report failed shots.
- For prompt-only requests, do not use this skill. Use prompt director skills instead.
