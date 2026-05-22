---
name: image-review-board
description: Build a visual image review board for generated film keyframes from Banana, built-in imagegen saved outputs, Midjourney, or other local image runs. Use when the user wants to see generation results with prompts and images side by side, compare images, pick usable frames, review output, or modify one image prompt by shot/version.
---

# Image Review Board

## Core Role

Create a review board where every generated image is paired with its exact prompt.

The goal is selection and revision: the user should be able to see the picture, read the prompt that made it, and say which shot/version to change.

Use this after generated images are saved locally, or when the user provides:

- A task folder containing `logs/generation-log.json`.
- A direct path to `generation-log.json`.
- A list of image paths plus prompt paths.

## Output

Generate:

```text
review/
  review-board.md
```

The Markdown must use absolute image paths so Codex can render the images.

## Review Board Structure

For each image:

```markdown
## S01 / banana / v01

| 提示词 | 图片 |
| --- | --- |
| 完整提示词、负面词、实际请求提示词 | ![S01](/absolute/path/to/image.png) |

**修改入口**：改 `S01_banana_v01`
**提示词文件**：/absolute/path/to/prompt.txt
**提示词JSON**：/absolute/path/to/prompt.json
**QC结论**：待质检 / 可用 / 可小修 / 建议重出 / 提示词需重写

**修改建议**
- 保留：
- 问题：
- 建议：
- 重出版本：S01_banana_v02
```

## Rules

- Do not rewrite prompts while building the board.
- If a prompt file exists, use it as the source of truth.
- If a prompt file is missing, fall back to `fullPrompt`, `negativePrompt`, and `finalPrompt` in `generation-log.json`.
- If an image is missing, still show the prompt and mark image as `图片缺失`.
- Keep one board per generation task folder.
- Use the shot/version/tool id as the modification handle, such as `S01_banana_v01`.
- In managed projects, the caller should write the board path back to `asset-index.json` through `$project-state-manager`.

