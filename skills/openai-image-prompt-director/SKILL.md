---
name: openai-image-prompt-director
description: OpenAI image prompt director for film and screen visual projects. Use when turning TVC, brand film, program promo, event opener, LED screen visual, storyboard shots, keyframes, or Banana/Jimeng prompts into OpenAI GPT Image compatible prompts while preserving the same unified cinematic visual style, shot-specific reference constraints, clear subject relationships, spatial layout, text control, and negative requirements.
---

# OpenAI Image Prompt Director

## Core rule: same film style, OpenAI-friendly wording

Use this skill to create copyable prompts for OpenAI image generation models such as GPT Image. It does not call the OpenAI API or generate images directly.

When a group of frames already has a `全片统一风格包`, keep it. Do not invent a new look just because the output tool changes.

OpenAI prompts should be more explicit about:

- 主体关系：who or what is the main subject, secondary subject, background, and empty space.
- 空间结构：foreground, midground, background, stage depth, screen location, product position, and perspective.
- 文字控制：whether text should appear, whether it should be blank, or whether a readable title space is only reserved.
- 参考图约束：what the reference image controls and what it must not control.
- 画面逻辑：what should be visible, what should be avoided, and what must remain consistent across the whole group.

## Fielded Storyboard Rule

When the source is a structured storyboard with fields such as `Visual Baseline`, `Continuity Lock`, `Shot Size`, `Camera Lens`, `Content`, `Composition`, and `Image Style Prompt`, treat those fields as the accuracy contract for image generation.

Do not paste a full storyboard file, a full scene block, or many shot prompts into one OpenAI image request. For each image, extract only:

- Global style lock: camera system, lens family, light logic, color boundary, material texture, realism level, aspect ratio.
- Global continuity locks: character, prop, wardrobe, era, location, text/logo, and forbidden inheritance rules.
- Current shot fields: shot id, shot size, camera position, lens/focal length, content, composition, visible action/state, scene lighting, local material details.
- Current shot risk controls: the 3-8 failures most likely to ruin this exact frame.

Build every final prompt as a compact but self-contained execution brief:

```text
visible frame first + subject/space/action + shot size/camera/lens/composition + local accuracy locks + compressed style lock + targeted negatives + aspect ratio
```

Accuracy is more important than shortness. Preserve the exact visible anchors from the storyboard, especially prop shape, object position, material, era rules, character relation, and foreground/midground/background layout. Shorten by removing repeated style adjectives, explanation, mood essays, and duplicate negatives, not by deleting the locks that keep the frame correct.

For multi-shot batches, keep the master style lock outside as a planning layer, but each copyable OpenAI prompt must still include the condensed style lock needed for that one image. Never use `same as above`, `continue previous style`, or a bare reference name.

## Visual Helpfulness Rule

OpenAI image prompts must be direct visual briefs. Every kept phrase must help the model render or preserve:

```text
subject identity / object shape / costume / product structure
foreground, midground, background, spatial layout, or composition
camera position, lens feeling, shot size, depth of field
light source, light direction, color boundary, material texture
reference-image role and do-not-inherit boundary
text/logo/title-space control
specific negative risk that protects the frame
```

If a phrase only sounds impressive but does not affect visible pixels, remove it or translate it into concrete visual instructions.

For formal work, inherit and preserve:

```text
director_contribution_packet
mother_library_application_packet
visual_helpfulness_check
```

Do not let the OpenAI rewrite discard the mother-library mechanism, scene function, shot-language logic, reference roles, or character/product continuity locks.

## Process

1. Read the storyboard, script, visual style, Banana/Jimeng prompts, or existing `全片统一风格包`.
2. Keep the same camera system, lens family, lighting logic, color grade, material texture, composition rule, mood, and aspect ratio used by `$frame-vision-director`.
3. Rewrite each selected shot into an OpenAI-friendly image prompt with clear visual hierarchy and spatial instructions.
4. Embed the full detailed style package inside every `OpenAI完整可复制提示词`. Do not write `同上`.
5. If a shot has a reference image, bind it only to that shot and state exactly what it controls: pose, silhouette, composition, spatial relation, material, color detail, expression, or object form.
6. If the reference image conflicts with the unified style, keep the unified film style and extract only the useful local feature.
7. For shots with logo, UI, signage, on-screen text, product labels, or title cards, specify whether text should be absent, left blank, represented as clean placeholder blocks, or rendered as exact user-provided text.
8. For LED or large-screen visuals, describe the screen ratio, center-safe area, distant viewing clarity, and stage relation.
9. Keep negative requirements concrete and tool-friendly.

## Output

Use this table by default:

| 镜号 | 优先级 | OpenAI用途 | 参考图说明 | OpenAI完整可复制提示词 | OpenAI负面要求 | 比例 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |

If working beside Banana/Jimeng prompts, output a comparison table:

| 镜号 | 优先级 | Banana/即梦提示词摘要 | OpenAI完整可复制提示词 | OpenAI负面要求 | 参考图说明 | 比例 |
| --- | --- | --- | --- | --- | --- | --- |

## Copyable prompt formula

`[镜头内容和主体关系] + [空间层次和构图位置] + [单镜头参考图约束, if any] + [文字/Logo/UI控制] + [详细统一主风格] + [摄影系统和镜头焦段] + [景别/机位] + [光线方案] + [色彩/调色] + [材质/质感] + [景深/颗粒/锐度] + [画面比例] + [清晰度/品质要求]`

Example:

`画面主体是一位产品经理站在极简科技发布会舞台右侧，人物为中景，左侧保留大面积干净留白和抽象产品轮廓光，前景是低反射黑色舞台地面，中景为人物与产品光影，背景为深灰色无文字LED屏；画面不出现真实品牌Logo，不生成可读文字，只保留可放标题的干净空间；全片统一为极简科技发布会电影质感，使用ARRI Alexa Mini LF影像风格，Zeiss Supreme Prime 35mm镜头感，浅景深，精准冷白轮廓光与柔和顶侧光，黑白灰空间搭配少量蓝色科技高光，玻璃与金属材质干净克制，高级商业广告调色，构图中心稳定、边缘留白充足，画面可信、克制、现代，16:9，超清细节，电影级光影。`

Reference-image example:

`镜头3参考图仅用于人物站姿、手部拿产品的姿态和画面左右构图关系，不采用参考图的暖黄色调、不照搬参考图背景；画面主体是一位产品经理站在极简科技发布会舞台右侧，手持产品，人物为中景，左侧保留抽象产品轮廓光和标题留白，背景为深灰色无文字LED屏；整体仍保持全片统一的极简科技发布会电影质感，使用ARRI Alexa Mini LF影像风格，Zeiss Supreme Prime 35mm镜头感，浅景深，精准冷白轮廓光与柔和顶侧光，黑白灰空间搭配少量蓝色科技高光，玻璃与金属细节克制，高级商业广告调色，画面干净、可信、现代，16:9，超清细节，电影级光影。`

Negative requirements example:

`不要生成乱码文字、错误Logo、品牌商标、杂乱UI、廉价舞台、畸形手部、脸部变形、主体比例错误、过度锐化、过曝、低清晰度、塑料感过重、错误水印、假电影边框、无关道具、风格漂移。`

## OpenAI-specific guidance

- Prefer complete sentences over keyword stacks when the image involves people, stage space, product placement, text areas, or complex composition.
- State `no readable text` when text is not needed. If text is needed, provide exact text and keep it short.
- State `clean blank area for later typography` when the design needs title space but AI should not write text.
- For product shots, describe form, material, scale, position, reflections, and what must stay accurate.
- For people shots, describe pose, gaze, wardrobe category, expression, and body framing. Avoid complex hand actions unless necessary.
- For LED stage visuals, avoid tiny details at the edge; emphasize center-safe composition and strong silhouette readability.
- For TV/program promos, describe hierarchy of host, guest, stage, graphics, and broadcast-safe title space.

## Consistency checks

Before final output, check:

- Does every OpenAI prompt preserve the same `全片统一风格包`?
- Does every prompt include camera system, lens/focal length, lighting, color, material, composition, ratio, and quality directly in the copyable prompt?
- Does every prompt avoid `同上`?
- Are subject relationship and spatial layout clearer than the Banana/Jimeng version?
- Are text, logo, UI, and title-space requirements explicit?
- If a shot has a reference image, is the reference constraint written only inside that shot's prompt?
- Are negative requirements specific enough to copy into OpenAI image generation?
