---
name: banana-image-generator
description: Generate and save Banana Pro / Nano Banana 2 images through OpenRouter for film and screen visual projects. Use when the user explicitly asks to directly generate Banana images, batch-generate Banana Pro images, regenerate selected storyboard shots, or turn Banana/Jimeng prompts into saved image files. Reads OPENROUTER_API_KEY from the local environment and never stores secrets.
---

# Banana Image Generator

## Core rule

Use this skill only when the user explicitly asks to generate images with Banana Pro / Nano Banana 2 / OpenRouter, such as `用Banana出图`, `Banana直接生成`, `批量生成Banana图片`, `重出S03`, or `把这些Banana提示词生成图片`.

Do not use it when the user only asks for prompts. For prompt writing, use `$frame-vision-director` and, when available, `$banana-pro`.

This skill calls OpenRouter's Chat Completions endpoint for `google/gemini-3.1-flash-image-preview` and saves returned images locally. It does not store API keys in files, logs, skill docs, GitHub, or output records.

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

The log uses shared fields with OpenAI generation: shot, version, tool, model, promptSummary, fullPrompt, negativePrompt, finalPrompt, promptPath, promptJsonPath, filePath, status, error, and retrySuggestion.
`outputDir` is the task root. `imageDir` points to `images\`. `promptDir` points to `prompts\`. `logDir` points to `logs\`.

## Workflow

1. If the user has no Banana prompt yet, first use `$frame-vision-director` and `$banana-pro`.
2. Convert selected shots into the input JSON shape.
3. Run the script with `--dry-run`.
4. If dry run is valid and `OPENROUTER_API_KEY` exists, run real generation.
5. Return saved image paths and generation table.

## Guardrails

- Never ask for or print the plaintext API key.
- Never write the API key into JSON input, logs, skill files, repo files, or final answers.
- Do not call the API unless the user explicitly asked for real Banana image generation.
- Use `2K` for normal storyboard/keyframe drafts unless the user asks for faster drafts or higher resolution.
- Keep generation records by shot number so revisions can target a single shot.
