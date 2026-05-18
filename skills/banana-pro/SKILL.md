---
name: banana-pro
description: Prepare Banana Pro / Nano Banana 2 image-generation prompts and OpenRouter request settings for text-to-image, image-to-image, multi-reference image workflows, character sheets, clean scene plates, product or prop design images, and storyboard first frames. Use when Codex is asked to work with Banana Pro, Nano Banana 2, google/gemini-3.1-flash-image-preview, OpenRouter image generation, aspect-ratio/image-size settings, or reusable visual prompt packs.
---

# Banana Pro

## Operating Principle

Prepare production-ready image prompts and request settings for OpenRouter's `google/gemini-3.1-flash-image-preview`, also known as Nano Banana 2 or Banana Pro.

This v1 skill is a workflow and reference skill. Do not submit real API requests or claim images were generated unless the user explicitly asks for generation through another available image tool or a later script-enabled version of this skill.

Use the user's language for generated prompt content. For Chinese briefs, write Chinese prompts and labels unless the user asks otherwise.

## Default Request Settings

Use these defaults unless the user gives different constraints:

```json
{
  "model": "google/gemini-3.1-flash-image-preview",
  "modalities": ["image", "text"],
  "stream": false,
  "image_config": {
    "aspect_ratio": "16:9",
    "image_size": "2K"
  }
}
```

Preserve requested aspect ratio or size when the user specifies them. Prefer `16:9` for storyboard frames, product demos, cinematic shots, UI reference frames, and video first frames. Prefer `1:1` only for icons, product closeups, or square social assets when explicitly appropriate.

## Workflow

1. Clarify only blocking visual intent.
   - If subject, format, or output purpose is missing, ask one concise question.
   - If enough context exists, proceed with reasonable assumptions and state them briefly.
   - Capture: subject, output type, target aspect ratio, image size, style, reference images, continuity constraints, and must-avoid artifacts.

2. Choose the task pattern.
   - Text-to-image: use when no image reference is provided.
   - Image-to-image: use when one reference image should be preserved, edited, restyled, expanded, or used as grounding.
   - Multi-reference: use when character, scene, product, UI, or style references must be combined.
   - Asset generation: use specialized templates for character, scene, product, prop, or storyboard first-frame work.
   - Read `references/prompt-patterns.md` for reusable prompt structures.

3. Produce a compact handoff.
   - Include the OpenRouter model and `image_config`.
   - Provide the final prompt as a clean block, not a long explanation.
   - For image-reference workflows, list each input image role, such as `character reference`, `product reference`, `scene reference`, or `composition reference`.
   - Include a short QA checklist for continuity, aspect ratio, subject fidelity, text legibility, and unwanted extra objects.

4. Add API details only when useful.
   - Read `references/openrouter-direct.md` when the user asks for raw API payloads, SDK shape, response parsing, or OpenRouter-specific request notes.
   - Do not expose API keys or invent secrets.
   - If the user asks to call the API, explain that this v1 skill only prepares prompts/settings unless another tool or script is explicitly available for execution.

## Prompt Standards

Write prompts as direct visual production instructions:

- Lead with the subject and output type.
- Specify composition, camera/framing, lighting, material, environment, and visual style.
- Describe exact continuity anchors for characters, products, logos, colors, proportions, and UI layout.
- Use positive constraints over long negative-prompt lists.
- Avoid random text, watermarks, QR codes, subtitles, logos, or labels unless requested.
- For commercial/product work, preserve brand, structure, color, proportions, and key details.
- For storyboard first frames, include shot scale, subject, action, scene, lighting, composition, and consistency with referenced assets.

## Output Contract

When preparing a Banana Pro handoff, use this shape:

```markdown
## Banana Pro Settings
- model: `google/gemini-3.1-flash-image-preview`
- modalities: `["image", "text"]`
- image_config:
  ```json
  {
    "aspect_ratio": "16:9",
    "image_size": "2K"
  }
  ```

## Prompt
[final prompt]

## Reference Roles
[only when images are provided]

## QA Checklist
[3-5 concise checks]
```

For raw OpenRouter API requests, include a JSON or TypeScript payload using the same model ID and the `image_config` object.

## Resource Guide

- Read `references/prompt-patterns.md` for task-specific prompt templates and examples.
- Read `references/openrouter-direct.md` for OpenRouter payload format, image reference input, response parsing, and source links.
