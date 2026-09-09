---
name: banana-image-generator
description: Generate and save Banana Pro / Nano Banana 2 images through OpenRouter for film and screen visual projects. Use when the user explicitly asks to directly generate Banana images, batch-generate Banana Pro images, regenerate selected storyboard shots, or turn Banana/Jimeng prompts into saved image files. Reads OPENROUTER_API_KEY from the local environment and never stores secrets.
---

# Banana Image Generator

## Core rule

Use this skill only when the user explicitly asks to generate images with Banana Pro / Nano Banana 2 / OpenRouter, such as `用Banana出图`, `Banana直接生成`, `批量生成Banana图片`, `重出S03`, or `把这些Banana提示词生成图片`.

Do not use it when the user only asks for prompts. For prompt writing, use `$frame-vision-director` and, when available, `$banana-pro`.

This skill calls OpenRouter's Chat Completions endpoint for `google/gemini-3.1-flash-image-preview` and saves returned images locally. It does not store API keys in files, logs, skill docs, GitHub, or output records.

## Independent Tool Boundary

This is the only user-facing Banana execution skill. It owns Banana API preflight, paid-run confirmation, idempotency, direct generation, batch generation, per-shot continuation after failures, saved images, saved prompts, generation logs, and managed project-state ingest.

Do not use this skill for `image`, `image-2`, `ChatGPT Image`, `内置 image`, or `内置 imagegen`. Those requests belong to `$builtin-imagegen-director` and the built-in imagegen tool. Never silently fall back from Banana to built-in imagegen, and never describe a built-in image result as Banana.

`$image-generation-controller` is only a legacy internal compatibility wrapper. New Banana requests route directly to this skill; it is not a separate user-facing image-generation route.

## Requirements

- `OPENROUTER_API_KEY` must exist in the local environment for real generation.
- Optional `BANANA_MODEL` can override the default model.
- Default model: `google/gemini-3.1-flash-image-preview`.
- Default output folder: `H:\yingshi\outputs\banana-images\{projectName}\{timestamp}\`.
- Images are saved in `images\`.
- Full prompts are saved in `prompts\`.
- Logs are saved in `logs\generation-log.json`.
- Default aspect ratio: `16:9`.
- Default image size: `2K`.
- Default Banana prompt mode: `quality`, which uses the full per-shot prompt for the API request.
- Use `compact` mode only when the user explicitly asks for speed, low token use, or `省 token`; compact mode keeps `2K` but uses `compactPrompt` / `bananaCompactPrompt` when available.
- Output files use versioned names, such as `S01_banana_v01.png`, `S01_banana_v02.png`.

## Input JSON

Prepare a JSON file and run the script with `--input`.

```json
{
  "projectName": "项目名",
  "model": "google/gemini-3.1-flash-image-preview",
  "aspect_ratio": "16:9",
  "image_size": "2K",
  "shots": [
    {
      "shot": "S01",
      "prompt": "Banana完整可复制提示词...",
      "compactPrompt": "Banana 2K省token执行提示词...",
      "negativePrompt": "负面要求...",
      "ratio": "16:9",
      "references": [
        {
          "role": "product reference",
          "path": "H:\\yingshi\\refs\\product.png"
        }
      ]
    }
  ]
}
```

Accepted shot number fields: `shot`, `shotNumber`, `镜号`.

Accepted prompt fields: `prompt`, `bananaPrompt`, `Banana完整可复制提示词`, `Banana/即梦完整可复制提示词`.

Accepted compact prompt fields: `compactPrompt`, `bananaCompactPrompt`, `Banana 2K省token提示词`, `省token提示词`.

Accepted negative prompt fields: `negativePrompt`, `negative`, `负面提示词`, `Banana/即梦负面提示词`.

Reference images can use:

- `url`: public HTTPS image URL or data URL
- `path`: local image path, converted to a data URL by the script
- `role`: how Banana should use the image, such as product reference, character reference, scene reference, or composition reference

## Script usage

From the skill folder:

```powershell
node .\scripts\generate-banana-images.mjs --input H:\yingshi\some-input.json --dry-run
node .\scripts\generate-banana-images.mjs --input H:\yingshi\some-input.json
node .\scripts\generate-banana-images.mjs --input H:\yingshi\some-input.json --prompt-mode compact
node .\scripts\generate-banana-images.mjs --input H:\yingshi\some-input.json --prompt-mode quality
node .\scripts\generate-banana-images.mjs --input H:\project\generation-jobs\banana.json --project-root H:\project --generation-confirmation approved
node .\scripts\generate-banana-images.mjs --input H:\project\generation-jobs\banana.json --project-root H:\project --generation-confirmation approved --resume
```

Use `--dry-run` before real generation to validate input, output paths, request settings, reference files, and whether `OPENROUTER_API_KEY` is present. Dry run does not call the API.

## Output

The script creates:

- image files in `images\`, named by shot and version, such as `images\S01_banana_v01.png`
- full prompt files in `prompts\`, such as `prompts\S01_banana_v01_prompt.txt` and `prompts\S01_banana_v01_prompt.json`
- `logs\generation-log.json`

After generation, report:

| 镜号 | 版本 | 工具 | 状态 | 图片路径 | 模型 | 比例 | 图片尺寸 | 失败原因 | 重出建议 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

If any shot fails, keep generating the rest and record the error in `generation-log.json`.

Return an overall execution result in addition to the per-shot table:

```text
banana_execution_result
status: completed / partial / failed / preflight_failed
failure_type: none / missing_api_key / invalid_input / missing_reference / api_rejected / network_or_service / empty_image_response / save_error / unknown
attempted_shots:
completed_shots:
failed_shots:
retry_allowed:
next_action:
```

Never auto-resubmit a paid Banana request. Retry only failed shots after explicit `--resume`; reuse successful outputs and block duplicate running/succeeded jobs with the same idempotency key. Missing keys, invalid input, missing references, API rejection, and save-path errors must be fixed before resuming. Use `--force-new-run` only after the user explicitly asks for a genuinely new paid attempt. Never report success unless an image file was actually saved.

The log uses shared fields with OpenAI generation: shot, version, tool, model, promptSummary, fullPrompt, negativePrompt, finalPrompt, promptPath, promptJsonPath, filePath, status, error, and retrySuggestion.
`outputDir` is the task root. `imageDir` points to `images\`. `promptDir` points to `prompts\`. `logDir` points to `logs\`.

For Banana 2K token-saving generation, `fullPrompt` is the actual compact request prompt. If a longer source prompt exists, it is saved as `sourcePrompt` in the log and prompt JSON. This saves request tokens without lowering `image_size`.

For story-driven storyboard batches, short-drama keyframes, TVC narrative shots, or any request where the user asks for detailed per-shot style/camera data, use `quality` mode by default. Do not let compact mode remove per-shot unified style DNA, camera system, focal length, aperture/depth, lighting, composition, continuity, material texture, ratio, or negative controls.

## Workflow

1. If the user has no Banana prompt yet, first use `$frame-vision-director` and `$banana-pro`.
2. Convert selected shots into the input JSON shape.
3. Run the script with `--dry-run`.
4. Before real generation, require `generation_confirmation`, compute the prompt/reference idempotency key, compare available credit and estimated cost when both are known, and check `generation-run-ledger.jsonl`.
5. If dry run and safety preflight pass, run real generation. Preserve successful shots; a failed batch resumes only its failed shot IDs.
6. For a managed `projectRoot`, ingest the generation log into `$project-state-manager`.
7. Return saved image paths, ledger/reuse state, and the generation table.

## Guardrails

- Never ask for or print the plaintext API key.
- Never write the API key into JSON input, logs, skill files, repo files, or final answers.
- Do not call the API unless the user explicitly asked for real Banana image generation.
- Do not submit a paid request without `generation_confirmation: approved / direct_test / confirmed`.
- Do not auto-retry a paid submission; polling/download retries are not generation retries.
- Use `2K` for normal storyboard/keyframe drafts. Do not reduce to `1K` for token saving unless the user explicitly asks.
- Prefer full detailed Banana prompts for storyboards and narrative keyframes unless the user explicitly asks for compact execution. Each shot prompt must be self-contained and include subject, composition, camera, lens, aperture/depth, light, material, continuity anchors, ratio, and core negatives.
- Compact Banana prompts may remove proposal explanations and client-facing rationale, but they must not remove the per-shot camera, light, material, continuity, ratio, or negative-control details needed for execution.
- Keep generation records by shot number so revisions can target a single shot.
- Never call built-in imagegen as a Banana fallback. If Banana execution fails, return the Banana failure reason and remain on the Banana route until the user explicitly changes tools.
