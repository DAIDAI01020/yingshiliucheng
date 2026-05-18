# AI Prompt Guide

## Image prompt structure

Use this order for Banana and 即梦 image prompts. The image prompt should feel like a cinematographer's brief, not only a beautiful illustration prompt:

`主体 + 场景 + 戏剧动作 + 构图 + 景别/机位 + 摄影机型号风格 + 镜头/焦段 + 光线方案 + 色彩/调色 + 材质 + 情绪 + 比例 + 清晰度要求`

## Group consistency rule

For a set of storyboard images, first define one `全片统一风格包`, then keep it consistent across every prompt.

The unified package includes:

- 主风格
- 摄影系统
- 镜头体系
- 色彩/调色
- 光线方案
- 材质/质感
- 构图规则
- 景深/颗粒/锐度
- 画面情绪
- 风格展开描述
- 画面比例
- 统一负面词

Only the shot content should change between prompts: subject, scene, action, shot size, camera angle, and frame-specific composition.

Do not put camera system, focal length, or lighting only in separate table columns. They must be embedded inside the copyable prompt text.
Do not write `风格同上` or rely on the style package table alone. Every prompt must be self-contained and repeat the detailed style package.

## Single-shot reference image rule

If an individual shot has a reference image, use it as a local constraint only.

Reference images can guide:

- 主体造型
- 人物姿态
- 构图关系
- 空间结构
- 材质细节
- 局部色彩
- 表情或动作

Reference images must not override:

- 全片统一主风格
- 摄影系统
- 镜头体系
- 调色方向
- 光线逻辑
- 画面比例

In the copyable prompt, explicitly state the reference-image role, for example:

`镜头3参考图仅用于人物站姿和构图关系，整体仍保持ARRI Alexa Mini LF极简科技发布会电影质感...`

For key storyboard frames, provide three client-facing style options only when choosing the overall film style. Once the user chooses A/B/C, all frame prompts must use the same chosen style package:

| 方案 | 适用 | 视觉方向 |
| --- | --- | --- |
| A 商业电影感 | TVC、品牌片、产品画面 | ARRI Alexa 35 / Alexa Mini LF, clean premium lighting, clear subject hierarchy |
| B 情绪电影感 | 品牌片、节目人物、故事片段 | Sony Venice 2 or Cooke lens warmth, moody light, deeper contrast, atmosphere |
| C 视觉实验感 | 大屏、开场、节目包装、年轻化广告 | RED V-Raptor crisp detail, anamorphic flare, surreal scale, graphic composition |

Adapt these names to the project. Do not force all three if the user has already locked one visual style.

Add a negative prompt:

`避免文字乱码、畸形手部、低清晰度、过曝、脸部崩坏、主体变形、logo错误、杂乱背景、廉价质感`

## Cinematic camera and lens vocabulary

Use camera names as style references to guide image models:

- ARRI Alexa 35: premium TVC, natural highlight roll-off, rich but controlled color, high-end commercial look.
- ARRI Alexa Mini LF: large-format brand film, elegant shallow depth, cinematic scale.
- Sony Venice 2: polished modern commercial, clean night scenes, smooth skin tone, luxury tone.
- RED V-Raptor: crisp high-resolution, tech/product detail, action energy, strong contrast.
- Blackmagic URSA Cine: grounded cinematic realism, documentary texture, less glossy mood.

Lens references:

- Zeiss Supreme Prime: clean, sharp, modern premium.
- Cooke S4/i or Cooke Panchro: warm, gentle, human, emotional.
- Panavision anamorphic: widescreen flare, oval bokeh, epic cinema feeling.
- Angenieux Optimo: broadcast/event/program promo motion energy.
- 100mm macro lens: product material, texture, food, beauty, craft details.

## Video prompt structure

Use this order for 即梦 and 可灵 video prompts:

`首帧画面 + 主体动作 + 镜头运动 + 环境变化 + 光影变化 + 节奏 + 时长 + 比例 + 禁止项`

Avoid vague verbs like "高级起来" or "更震撼". Translate them into camera, light, scale, material, motion, and rhythm.

## Tool notes

- Banana: favor concrete image composition, clean subject hierarchy, and detailed material/light description.
- 即梦 image: favor cinematic Chinese prompts, clear aspect ratio, camera language, and negative prompts.
- 即梦 video: describe first frame, motion path, subject action, and end-state clearly.
- 可灵 video: keep action physically plausible, state camera movement and duration, avoid too many simultaneous changes.

## Banana 2K token-saving execution

When the user wants Banana fast generation or token saving, keep the image request at `2K` and shorten only the prompt sent to the API.

Output both:
- `完整可复制提示词`: full version for review, revision, and client-facing prompt records.
- `Banana 2K省token提示词` / `compactPrompt`: compact execution version for Banana API calls.

The compact prompt must keep:
- subject and action
- composition and camera angle
- camera system, lens/focal length, and lighting
- core color/material/texture rules
- ratio and `2K`
- important negative constraints

The compact prompt should remove:
- proposal explanations
- creative rationale
- repeated style package text
- weak or generic negative words
- anything not needed by the image model to draw the frame

Do not reduce the image size below `2K` unless the user explicitly asks.

## Prompt fields

Each prompt should include:

- 工具：Banana / 即梦 / 可灵
- 参考图说明：only when a shot has a reference image; bind it to the shot number
- 完整可复制提示词：must include style, camera system, lens/focal length, lighting, color, material, composition, ratio, and quality requirements
- 英文补充词：optional, for style terms such as cinematic lighting, product photography, volumetric light
- 负面提示词
- 比例：16:9, 9:16, 1:1, 21:9, 32:9, or custom LED ratio
- 用途：关键视觉、分镜图、产品特写、舞台背景、动态镜头首帧
