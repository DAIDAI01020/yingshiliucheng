# GPT Image 2.5 Prompt Compilation

Apply this reference only when `model_target` is `gpt_image_2_5`, `gpt_image_2_5_flare`, or `gpt_image_2_5_sunburst`, or when a new built-in ChatGPT/Codex image request is explicitly routed to the current Images 2.5 default. A project or prompt pinned to GPT Image 2 or an older model keeps its existing model rules.

## Model Boundary

Use these normalized targets:

```text
gpt_image_2_5 -> ChatGPT/Codex built-in Images 2.5; exact serving submodel is not exposed
gpt_image_2_5_flare -> API-oriented speed/default candidate
gpt_image_2_5_sunburst -> API-oriented premium precision candidate
```

For direct built-in generation, never claim that Flare or Sunburst was selected unless the execution surface explicitly exposes that choice. Keep API parameters outside the copyable visual prompt.

For API-oriented planning, start with Flare for previews, iteration, or throughput. Use Sunburst first for demanding campaign, polished product, dense layout, exact-text, identity-sensitive, or multi-turn edit work where quality is the unmet requirement. Do not switch a user-selected or project-pinned model silently.

## Prompt Shape

Simple generation usually needs one to three clear natural-language sentences. Use labeled sections only when the brief has several independent constraints.

Compile in this order:

```text
intended deliverable and visible result
-> subject, action, and spatial relationships
-> composition, crop, hierarchy, and aspect ratio
-> light, color, material, texture, and visual medium
-> reference roles and what not to inherit
-> exact text, typography, and placement when applicable
-> must-preserve constraints
-> 3-8 targeted exclusions
```

Describe a visible image, not a keyword pile. Use `photorealistic` or `real photograph` explicitly when photographic output is required. Treat camera and lens terms as appearance cues rather than a guarantee of exact optical simulation.

Do not front-load prestige labels, camera-brand stacks, `8K/masterpiece/best quality` filler, or a universal negative block. Keep only controls that change the visible result.

## Generation Modes

### Film, TVC, and storyboard frames

Lead with the exact frozen moment, subject state, setting, and frame function. Then specify blocking, foreground/midground/background relationships, camera position or focal behavior when useful, motivated light, material texture, continuity locks, and aspect ratio.

For people, state body framing, gaze, hand-object interaction, relative scale, and any feet/hands that must be visible. Preserve identity, wardrobe, props, screen direction, and scene geography only when they are approved constraints.

### Product and commercial KV

State the deliverable as a product photograph, campaign key visual, poster base art, or other real use. Lock product geometry, proportions, label/logo policy, material, reflections, focal hierarchy, negative space, and title/logo-safe zones. For complex KV layouts, use short labeled sections such as `画面目标 / 主体 / 构图 / 光线材质 / 版式安全区 / 必须保持 / 禁止项`.

Do not ask one still image to show several sequential actions. Convert the request into one decisive moment or an explicitly requested multi-panel artifact.

### Graphic, typography, and dense layout

Write the prompt as an artifact specification rather than concept art. Name the canvas, hierarchy, real copy/data, spacing, text sizes or emphasis, palette, icon/shape language, and what must remain readable.

For exact text:

```text
- put required copy in quotation marks;
- state how many times it appears;
- specify position, hierarchy, font character, color, and size relationship;
- spell unusual brand words letter by letter when useful;
- request no extra text, unrelated logos, or watermarks;
- inspect spelling and legibility after generation.
```

Use a higher quality setting only when the execution surface exposes it and small text, dense information, multiple fonts, or fine detail remains an unmet requirement. Do not write quality parameters into the visual prompt.

### Transparent assets

Request an isolated subject in the prompt and set transparent background separately on the execution surface. Require clean alpha edges, centered padding, and no solid backdrop, scenery, checkerboard, or watermark. Verify hair, glass, shadows, translucent material, labels, and edge fringing in the returned alpha channel. A drawn checkerboard is not transparency.

### Sketch to image

Treat the sketch as layout, contour, pose, or perspective authority according to its assigned role. State which geometry must remain, then add the intended materials, lighting, environment, and finish. Exclude new elements or text unless requested.

## Reference Roles

Identify every input by order and one narrow purpose:

```text
image 1 -> identity / subject / product / base composition / edit master
image 2 -> wardrobe / prop / style / palette / lighting / background
do_not_inherit -> unwanted person, scene, layout, logo, color, texture, or text
```

Explain how referenced elements combine and where they appear using clear spatial language. A small purposeful reference set is preferable to an undifferentiated pile. Do not infer roles from filenames alone.

## Precision Editing

Start with the delta and preservation boundary:

```text
只修改[目标元素或区域]：[当前状态]变为[目标状态]。
严格保持[人物身份/产品结构/构图/镜位/背景/透视/光线/色调/标签/画质/非目标元素]不变。
让修改后的[元素]与原图的[姿态/几何/阴影/色温/材质/颗粒/边缘]自然融合。
不要添加[未请求的配饰/文字/Logo/物体/风格变化]。
```

Use one meaningful edit per turn when precision matters. Feed the latest accepted result into the next edit, restate critical locks, and inspect each output before continuing. Do not rebuild the full prompt or re-describe an unrelated new style during a local edit.

The model can still drift across repeated edits. Never promise pixel-identical preservation. If a region must remain pixel-identical, make or composite the approved local change outside generation.

## Audit Checks

Before approval, check only the controls relevant to the task:

```text
visible target is stated before style rhetoric
one still contains one coherent moment unless multi-panel is explicit
model_target and task_mode are clear
reference roles and do_not_inherit boundaries are explicit
generation separates visible instructions from execution parameters
edit states one delta and a concrete preservation lock
identity, product geometry, layout, exact text, or alpha is checked when applicable
aspect ratio and placement constraints match the intended use
targeted exclusions do not contradict requested content
```

Return `打回重写` for a missing visible target or preservation boundary. Return `建议拆分` when several incompatible edits, layouts, or moments are packed into one execution. Do not add missing creative decisions at the platform layer.

## Current Capability Guard

Official model documentation is the authority for live model names, sizes, quality values, transparency support, and availability. The current documented GPT Image 2.5 API family supports generation, editing, custom sizes within published limits, and transparent backgrounds; execution surfaces may expose different subsets. Inspect the live surface before promising a parameter or submodel.
