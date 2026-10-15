---
name: banana-pro
description: Prepare Banana Pro request settings and explicit legacy CLI workflows through OpenRouter's google/gemini-3-pro-image-preview for text-to-image, image-to-image, multi-reference image workflows, character sheets, clean scene plates, product or prop design images, and storyboard first frames. Use when Codex is asked to work with Banana Pro, Nano Banana 2, Gemini image generation, OpenRouter image generation, aspect-ratio/image-size settings, reusable visual prompt packs, or the installed banana-pro CLI.
---

# Banana Pro

## Operating Principle

Prepare production-ready image prompts and request settings for OpenRouter's `google/gemini-3-pro-image-preview`, also known here as Banana Pro.

This skill includes CLI wrappers named `banana-pro` and `banana-pro.cmd`. On Windows/Codex, prefer `bin\banana-pro.cmd` because it uses PowerShell and does not require Python. For new generation requests use `$banana-image-generator`, the sole execution owner. Use this bundled CLI only when the user explicitly requests this legacy CLI workflow; naming Banana Pro alone does not select it. Do not claim images were generated unless the CLI or another available image tool actually produced outputs.

Never expose API keys in chat, prompt handoffs, markdown examples, logs, or committed skill files. The CLI reads `OPENROUTER_API_KEY` from the environment or from `~/.config/banana-pro/openrouter.env`.

Use the user's language for generated prompt content. For Chinese briefs, write Chinese prompts and labels unless the user asks otherwise.

For prompt work, the deliverable-specific semantic owner creates image meaning and `$prompt-platform-auditor` compiles it. This skill supplies Banana-specific settings or explicit compatibility support, not a second concept or execution route.

## Default Request Settings

Use these defaults unless the user gives different constraints:

```json
{
  "model": "google/gemini-3-pro-image-preview",
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
   - For commercial KV, product advertising, environment design, or concept posters, also read `references/design-prompt-examples.md`. Its example briefs are demonstrations, not project defaults or approved generation jobs.

3. Produce a compact handoff.
   - For prompts the user will paste into a website or app, deliver the copyable Chinese prompt, recommended aspect ratio, and reference roles when needed. Omit API payloads and model IDs unless requested.
   - For an execution/API handoff, include the selected model and `image_config`. Preserve the chosen Banana variant; the Pro defaults below do not override an explicit Nano Banana 2 target or the execution owner's model selection.
   - Provide the final prompt as a clean block, not a long explanation.
   - For image-reference workflows, list each input image role, such as `character reference`, `product reference`, `scene reference`, or `composition reference`.
   - Check continuity, aspect ratio, subject fidelity, text legibility, and unwanted extra objects internally. Show a short checklist when requested or when it materially helps the handoff.

4. Add API details only when useful.
   - Read `references/openrouter-direct.md` when the user asks for raw API payloads, SDK shape, response parsing, or OpenRouter-specific request notes.
   - Do not expose API keys or invent secrets.
   - Use `banana-pro --dry-run` or `bin\banana-pro.cmd --dry-run` for payload inspection.
   - Use `banana-pro "prompt..." -o /path/to/output` or `bin\banana-pro.cmd "prompt..." -o H:\path\to\output` for real generation only within an explicitly requested legacy CLI workflow.
   - Use `banana-pro --image /path/to/reference.png "prompt..."` or `bin\banana-pro.cmd --image H:\path\reference.png "prompt..."` for image-to-image or multi-reference workflows.

## Prompt Standards

Write prompts as direct visual production instructions:

- Lead with the subject and output type.
- Specify composition, camera/framing, lighting, material, environment, and visual style.
- Select fields by deliverable: graphic KV and illustrated posters need hierarchy, shape, spacing, typography, and medium; photographic products and environments need plausible light, material, perspective, and spatial relationships. Do not force camera brands or cinematic lighting into every design.
- For paired built-in image / Banana prompts, preserve the approved concept, subject, composition, palette, reference roles, and exact text. Change only platform wording and supported settings; never invent a second concept while adapting.
- Describe exact continuity anchors for characters, products, logos, colors, proportions, and UI layout.
- Use positive constraints over long negative-prompt lists.
- Avoid random text, watermarks, QR codes, subtitles, logos, or labels unless requested.
- For commercial/product work, preserve brand, structure, color, proportions, and key details.
- For storyboard first frames, include shot scale, subject, action, scene, lighting, composition, and consistency with referenced assets.
- For narrative/storyboard sequences, every shot prompt must be self-contained. Repeat the unified style DNA, camera system, lens/focal length, aperture or depth of field, shot size, camera height/angle, lighting source/direction/color temperature, local material texture, continuity anchors, aspect ratio, and negative controls inside each individual shot prompt.
- Do not rely on a separate unified style block, `同上`, `延续上条`, `统一风格见上`, or a shared camera table as the only source for a shot. The shared style block may be shown for planning, but the copyable Banana prompt for every shot must stand alone.
- Provide compact Banana prompts only when the user asks for speed, low token use, or `省 token`. Otherwise the full detailed prompt is the execution authority.

## Narrative Storyboard Detail Rule

When preparing Banana Pro prompts for story-driven scenes, short drama, TVC storyboards, branded narrative sequences, or multi-shot first frames, output one full prompt per shot. Each prompt must contain these fields as visible execution language, not only as separate columns:

```text
镜号 / 画幅 / 出图用途
可见画面目标：人物、产品、道具、场景、动作瞬间、前中后景
统一风格 DNA：项目主风格、真实度、色彩边界、材质纪律、禁用项
相机数据：摄影机/影像系统、镜头焦段、光圈或景深、机位高度、角度、景别、运动趋势
光线：主光来源、方向、软硬、色温、反差、环境光
构图：主体位置、前景遮挡、中景关系、背景信息、视觉焦点、留白
连续性：角色脸、发型、服装、道具、背景、轴线/视线方向、参考图角色
质感：真实皮肤、衣料褶皱、旧物磨损、灰尘、雨水、金属/玻璃/木纹等可见材料
负面控制：乱码文字、水印、logo、脸漂、手崩、背景乱变、塑料皮肤、假HDR、廉价AI感
```

Hard rule:

```text
For a multi-shot Banana storyboard batch, no shot may be handed off as "same style as above" or with camera/lens/light only in a shared table. If exact details repeat, repeat them in the shot prompt anyway.
```

## Image Edit / Character Replacement Mode

Use this mode when the user wants to replace a person, face, outfit, product, or prop in an existing image while preserving the rest of the image.

This is a different task from normal text-to-image. Do not write a general cinematic prompt that lets the model reinterpret the whole frame.

### Core Edit Rule

The first sentence must state the edit boundary:

```text
只替换原图中的[指定人物/区域]，严格保留原图的背景、构图、机位、镜头焦段、光线方向、色调、景深、空间关系和画面比例。
```

### Reference Roles

For replacement tasks, always separate references:

| Reference | Role |
| --- | --- |
| 原图 / base image | composition, background, lighting, camera, pose slot, aspect ratio |
| 人物参考 / character reference | only face identity, hairstyle, age, body type, costume if requested |
| 风格参考 / style reference | only film texture or color, never composition unless requested |

Do not let the character reference change the base image background, pose slot, camera angle, or lighting unless the user asks.

### Prompt Formula

```text
只替换原图中的[人物A/前景人物/右侧人物]，严格保留原图背景、构图、机位、光线、色彩、景深、镜头透视和画面比例。
将该人物替换为[新人物形象]，参考人物图只用于脸型、发型、年龄气质和服装特征。
新人物必须自然站在原图同一位置，姿态、身体朝向、受光方向、阴影、边缘光、清晰度和画面颗粒与原图一致。
不要改变其他人物、道具、环境、文字、建筑、天空、地面、镜头焦段和整体风格。
```

### Negative Control

Always include:

```text
禁止改变背景，禁止改变构图，禁止改变镜头角度，禁止改变光线方向，禁止改变色调，禁止改变其他人物，禁止新增人物，禁止删除道具，禁止重绘整张图，禁止过度磨皮，禁止脸部变形，禁止手部畸形，禁止衣服融入背景，禁止AI感，禁止水印和乱码文字。
```

### If First Result Fails

Use targeted retries instead of rewriting the whole prompt:

- Background changed: strengthen `base image is locked; preserve all non-target pixels as much as possible`.
- Face not close enough: strengthen `character reference only controls face identity and hairstyle`.
- Lighting mismatch: add `match original light direction, shadow softness, exposure, and color temperature`.
- Pose changed too much: add `keep the original pose slot and body orientation`.
- Whole image restyled: remove extra style adjectives and keep only preservation + replacement instructions.

## Output Contract

For manual website/app use, provide the final prompt first and only the settings the user needs to select. If no references were supplied, do not invent numbered input images. Do not promise exact product or character fidelity without an appropriate reference.

For an execution/API Banana Pro handoff, use this shape (substitute the selected model/settings when the target is another Banana variant):

````markdown
## Banana Pro Settings
- model: `google/gemini-3-pro-image-preview`
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
````

For raw OpenRouter API requests, include a JSON or TypeScript payload using the same model ID and the `image_config` object.

For local execution, use the installed command:

```bash
banana-pro "Generate a cinematic 16:9 product hero image..." -o ./banana-pro-output
```

On Windows/Codex, use the bundled PowerShell wrapper:

```powershell
H:\yingshi\skills\banana-pro\bin\banana-pro.cmd "Generate a cinematic 16:9 product hero image..." -o H:\yingshi\outputs\banana-pro-output
```

For reference-image execution:

```bash
banana-pro --image ./reference.png "Keep the reference subject identity and generate a 16:9 cinematic frame..." -o ./banana-pro-output
```

For Windows dry-run payload inspection:

```powershell
H:\yingshi\skills\banana-pro\bin\banana-pro.cmd --dry-run "Generate a clean 16:9 storyboard first frame..."
```

## Resource Guide

- Read `references/prompt-patterns.md` for task-specific prompt templates and examples.
- Read `references/design-prompt-examples.md` for original paired image/Banana examples across KV, product advertising, environments, and concept posters, including reference and revision rules.
- Read `references/openrouter-direct.md` for OpenRouter payload format, image reference input, response parsing, and source links.
