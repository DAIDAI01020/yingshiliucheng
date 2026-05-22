---
name: builtin-imagegen-director
description: Use Codex/ChatGPT built-in imagegen for fast film visual concept images, storyboard keyframes, reference exploration, image edits, and quick drafts without external API keys. Use when the user asks for built-in imagegen, 内置出图, 直接生成一张图, 快速出图, concept preview, or wants image generation/editing without Banana, OpenAI API, Midjourney, or project logging.
---

# Built-in Imagegen Director

## Role

Use the built-in `imagegen` capability for fast preview images and edits inside the current conversation.

This skill is not an API wrapper. It does not manage external keys, model selection, generation logs, project folders, or Excel execution records unless another workflow captures the result afterward.

## When to Use

- The user asks for `imagegen`, `内置出图`, `直接生成一张图`, `快速出图`, or `先看个效果`.
- The user wants a quick visual concept, mood frame, style test, poster direction, storyboard keyframe, or image edit.
- The user does not require Banana, Midjourney, OpenAI API, versioned files, prompt logs, or project-state writeback.

Do not use this skill when the user explicitly says Banana, MJ/Midjourney, OpenAI API, Seedance, 可灵, 即梦, or asks for logged project execution.

## Workflow

1. Convert the user's request into a concise image-generation prompt.
2. Preserve the current project's unified style if the request is part of an existing film/visual project.
3. For storyboards, include subject, scene, camera angle, lens feeling, lighting, color, material, mood, aspect ratio, and avoid items.
4. If the user says `直接出图`, call the built-in image generation tool without printing the full prompt first.
5. If the user says `给提示词`, output only the prompt and do not generate.
6. For edits, preserve the user's stated invariants and change only the requested elements.
7. After generation, respond briefly with what was generated. Do not claim a model name because the built-in tool does not expose one.

## Film Prompt Shape

Use this compact shape when preparing built-in imagegen prompts:

```text
Create a cinematic key visual / storyboard frame for [project type].
Subject: [main subject and action].
Scene: [environment and time].
Camera: [shot size, angle, lens feeling, composition].
Lighting/color: [lighting plan and palette].
Texture/style: [film look, materials, finish].
Constraints: [no text/logos/watermarks/unwanted artifacts].
Aspect ratio: [16:9 / 9:16 / 1:1 / other].
```

## Output Behavior

- For real generation requests, keep chat output short and show the generated image result.
- For prompt-only requests, provide a clean copyable prompt.
- For workflow comparisons, describe it as `内置 imagegen 快速预览`, not as OpenAI API, Banana, or Midjourney.
- If the image needs tracked files, version names, review boards, or prompt logs, recommend the existing Banana/OpenAI/Midjourney workflow instead.

## Guardrails

- Do not say the exact model name unless the environment exposes it.
- Do not ask for API keys.
- Do not promise deterministic file paths or project logging from the built-in tool.
- Do not silently switch to external tools.
- Do not print long prompts when the user explicitly wants direct generation.
