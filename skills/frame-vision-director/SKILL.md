---
name: frame-vision-director
description: Cinematic keyframe vision director for Banana and Jimeng. Use when turning TVC, brand film, program promo, event opener, LED screen visual, storyboard shots, or key frames into consistent film-style image prompts. Enforces a unified visual style package across a group of images, handles shot-specific reference images, and embeds camera system, lens, focal length, lighting, color, texture, aspect ratio, and negative prompts directly inside copyable prompts.
---

# Frame Vision Director

## Core rule: one film, one visual system

When generating prompts for a group of storyboard frames, do not change the overall style for every image.

First define a `全片统一风格包`, then reuse it across every prompt:

| 风格项 | 统一设定 |
| --- | --- |
| 主风格 |  |
| 摄影系统 |  |
| 镜头体系 |  |
| 色彩/调色 |  |
| 光线方案 |  |
| 材质/质感 |  |
| 构图规则 |  |
| 景深/颗粒/锐度 |  |
| 画面情绪 |  |
| 风格展开描述 |  |
| 画面比例 |  |
| 统一负面词 |  |

Each shot can vary subject, scene, action, shot size, and composition, but the camera system, lens family, color tone, lighting logic, and texture should remain consistent unless the script intentionally changes chapter or mood.

The `风格展开描述` must be detailed enough to paste into every shot prompt. Do not shorten it to labels like `商业电影感` or `同上`.

## Process

1. Use storyboard and visual style as source.
2. Create the unified visual style package before writing shot prompts.
3. Treat each prompt like a cinematographer's image brief, not a generic illustration prompt.
4. Expand the unified style package inside every copyable prompt. Each prompt must repeat the camera body, lens/focal length, depth of field, lighting plan, color pipeline, texture, composition rule, aspect ratio, and quality requirements.
5. When the user provides reference films or brands, translate them into visual principles. Do not copy exact frames, brand UI, logo layouts, slogans, or protected compositions.
6. When a specific shot has a reference image, use it only as a local constraint for that shot: subject shape, pose, composition relationship, spatial structure, material, color detail, or gesture.
7. Do not let a single-shot reference image override the unified film style. If the reference conflicts with the film style, keep the film style and extract only the useful local feature.
8. For S-priority key shots, provide A/B/C style routes only if the user is still choosing the film's overall style. Once a route is chosen, all shot prompts must follow that chosen route.
9. For B/C-priority shots, give fewer prompts or recommend no image generation.
10. For Banana execution, also provide `Banana 2K省token提示词` or `compactPrompt` when the user asks for fast/token-saving Banana generation. Keep image quality at `2K`; shorten only the request wording.

## Output

Use this table by default:

| 镜号 | 优先级 | 工具 | 参考图说明 | 完整可复制提示词 | 负面提示词 | 比例 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |

Do not leave camera, lens, or lighting only in separate columns. They must appear inside `完整可复制提示词`.
Do not write `风格同上` inside a prompt. Every `完整可复制提示词` must be self-contained.

For Banana token-saving execution, add a separate compact field named `Banana 2K省token提示词` or `compactPrompt`:
- Keep shot subject, composition, camera/lens, lighting, key color/material, ratio, `2K`, and the most important constraints.
- Remove client proposal meaning, repeated explanations, long rationale, and low-risk negative words.
- Never reduce image size below `2K` unless the user explicitly asks.

Optional style exploration table, only before the user chooses a route:

| 方案 | 统一风格包 | 适合原因 |
| --- | --- | --- |
| A 商业电影感 |  |  |
| B 情绪电影感 |  |  |
| C 视觉实验感 |  |  |

After the user chooses A/B/C, generate all shot prompts using the same selected package.

## Copyable prompt formula

`[镜头内容] + [单镜头参考图约束, if any] + [详细统一主风格] + [摄影系统] + [镜头/焦段] + [景别/机位] + [光线方案] + [色彩/调色] + [材质/质感] + [景深/颗粒/锐度] + [构图规则] + [画面情绪] + [画面比例] + [清晰度/品质要求]`

Example:

`一位主持人站在极简科技发布会舞台中央，身后是巨大的抽象产品轮廓光，低机位中景，画面中心构图；全片统一为极简科技发布会电影质感，使用ARRI Alexa Mini LF影像风格，Zeiss Supreme Prime 35mm镜头感，浅景深，精准冷白轮廓光与柔和顶侧光，黑白灰空间搭配少量蓝色科技高光，材质干净、玻璃与金属细节克制，高级商业广告调色，16:9，超清细节，电影级光影。`

Reference-image example:

`镜头3参考图仅用于人物站姿、手部拿产品的关系和画面左右构图参考，不采用参考图的暖黄色调；画面为一位产品经理站在极简科技发布会舞台右侧，左侧留出产品轮廓光与标题空间；整体仍保持全片统一的极简科技发布会电影质感，使用ARRI Alexa Mini LF影像风格，Zeiss Supreme Prime 35mm镜头感，浅景深，精准冷白轮廓光与柔和顶侧光，黑白灰空间搭配少量蓝色科技高光，玻璃与金属细节克制，高级商业广告调色，画面干净、克制、可信，16:9，超清细节，电影级光影。`

Negative prompt example:

`避免文字乱码、低清晰度、主体变形、脸部崩坏、畸形手部、错误logo、杂乱背景、过曝、廉价质感、塑料感过重、无关元素、过度锐化、AI感太强、假电影剧照边框、错误摄影机水印。`

## Cinematic camera guidance

Use camera and lens references as visual language, not fake metadata claims. Choose a consistent package:

- ARRI Alexa 35 + Zeiss Supreme Prime: premium commercial film look, clean product clarity, controlled highlight roll-off.
- ARRI Alexa Mini LF + Cooke S4/i: large-format cinematic depth, warm skin, elegant brand film.
- Sony Venice 2 + Panavision anamorphic: polished modern luxury, wide cinematic scale, smooth low-light.
- RED V-Raptor + Zeiss Supreme Prime: crisp high-resolution, tech/product detail, bold contrast.
- Blackmagic URSA Cine + Cooke Panchro: grounded cinematic realism, human documentary texture.

## Tool guidance

- Banana: favor clear subject hierarchy, clean composition, product/character accuracy, and material detail.
- 即梦: favor cinematic Chinese wording, camera language, lighting, ratio, and clear negative prompts.

## Single-shot reference images

When the user provides or describes reference images for individual shots:

- Bind each reference to a shot number, for example `镜头1参考图A`, `镜头3参考图B`.
- Add a `参考图说明` field for that shot.
- In the copyable prompt, write exactly what the reference controls: pose, silhouette, framing, spatial relation, object design, material, color detail, or expression.
- Also write what the reference should not control if needed, such as `不采用参考图的色调`, `不照搬参考图背景`, or `只参考构图关系`.
- Keep the unified film style dominant.

## Consistency checks

Before final output, check:

- Does every prompt use the same main style?
- Does every prompt include camera system and lens/focal length inside the copyable prompt?
- Does every prompt include lighting and color inside the copyable prompt?
- Does every prompt repeat the detailed style package instead of saying `同上`?
- If a shot has a reference image, is the reference constraint written inside only that shot's prompt?
- Does the reference image preserve the unified film style rather than changing the whole group?
- Are only shot-specific details changing?
- Are negative prompts easy to copy?
