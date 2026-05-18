---
name: openai-image-generator
description: Generate and save images with the OpenAI Images API for film and screen visual projects. Use when the user explicitly asks to directly generate images, batch-generate OpenAI images, regenerate selected storyboard shots, or turn OpenAI image prompts into saved image files. Reads OPENAI_API_KEY from the local environment and never stores secrets.
---

# OpenAI Image Generator

## Core rule

Use this skill only when the user explicitly asks to generate images with OpenAI, such as `直接出图`, `用OpenAI出图`, `批量生成`, `重出S03`, or `把这些OpenAI提示词生成图片`.

Do not use it when the user only asks for prompts. For prompt writing, use `$openai-image-prompt-director` first.

This skill calls the OpenAI Images API through the bundled Node script and saves image files locally. It does not store API keys in files, logs, skill docs, GitHub, or output records.

## Requirements

- `OPENAI_API_KEY` must exist in the local environment for real generation.
- Optional `OPENAI_IMAGE_MODEL` can override the default model.
- Default model: `gpt-image-1.5`.
- Default output folder: `H:\yingshi\outputs\openai-images\{projectName}\{timestamp}\`.
- Images are saved in `images\`.
- Full prompts are saved in `prompts\`.
- Logs are saved in `logs\generation-log.json`.
- Default quality: `medium`.
- Default output format: `png`.
- Output files use versioned names, such as `S01_openai_v01.png`, `S01_openai_v02.png`.

## Input JSON

Prepare a JSON file and run the script with `--input`.

```json
{
  "projectName": "项目名",
  "model": "gpt-image-1.5",
  "size": "1536x1024",
  "quality": "medium",
  "output_format": "png",
  "shots": [
    {
      "shot": "S01",
      "prompt": "OpenAI完整可复制提示词...",
      "negativePrompt": "OpenAI负面要求...",
      "ratio": "16:9"
    }
  ]
}
```

Accepted shot number fields: `shot`, `shotNumber`, `镜号`.

Accepted prompt fields: `prompt`, `openaiPrompt`, `OpenAI完整可复制提示词`.

Accepted negative prompt fields: `negativePrompt`, `negative`, `OpenAI负面要求`.

Supported sizes: `1024x1024`, `1024x1536`, `1536x1024`.

If `size` is missing, infer from ratio:

- `16:9`, `2.35:1`, `横版`: `1536x1024`
- `9:16`, `竖版`: `1024x1536`
- `1:1`, `方图`: `1024x1024`

## Script usage

From the skill folder:

```powershell
node .\scripts\generate-openai-images.mjs --input H:\yingshi\some-input.json --dry-run
node .\scripts\generate-openai-images.mjs --input H:\yingshi\some-input.json
```

Use `--dry-run` before real generation to validate input, output paths, model, and whether `OPENAI_API_KEY` is present. Dry run does not call the API.

## Output

The script creates:

- image files in `images\`, named by shot and version, such as `images\S01_openai_v01.png`
- full prompt files in `prompts\`, such as `prompts\S01_openai_v01_prompt.txt` and `prompts\S01_openai_v01_prompt.json`
- `logs\generation-log.json`

After generation, report:

| 镜号 | 版本 | 工具 | 状态 | 图片路径 | 模型 | 尺寸 | 质量 | 失败原因 | 重出建议 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

If any shot fails, keep generating the rest and record the error in `generation-log.json`.

The log uses shared fields with Banana generation: shot, version, tool, model, promptSummary, fullPrompt, negativePrompt, finalPrompt, promptPath, promptJsonPath, filePath, status, error, and retrySuggestion.
`outputDir` is the task root. `imageDir` points to `images\`. `promptDir` points to `prompts\`. `logDir` points to `logs\`.

## Workflow

1. If the user has no OpenAI prompt yet, first use `$openai-image-prompt-director`.
2. Convert the selected shots into the input JSON shape.
3. Run the script with `--dry-run`.
4. If dry run is valid and `OPENAI_API_KEY` exists, run real generation.
5. Return the saved image paths and generation table.

## Guardrails

- Never ask for or print the plaintext API key.
- Never write the API key into JSON input, logs, skill files, repo files, or final answers.
- Do not call the API unless the user explicitly asked for real image generation.
- Use low or medium quality for quick tests unless the user asks for high quality.
- For client-facing key frames, keep generation records by shot number so revisions can target a single shot.
