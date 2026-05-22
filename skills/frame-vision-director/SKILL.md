---
name: frame-vision-director
description: Cinematic keyframe vision director for built-in imagegen, Banana, Jimeng, and Midjourney prompt handoff. Use when turning TVC, brand film, program promo, event opener, LED screen visual, storyboard shots, or key frames into consistent film-style image prompts. Enforces a unified visual style package, checks prompt completeness before generation, handles shot-specific reference images, and embeds camera, lens, lighting, color, texture, aspect ratio, and negative prompts directly inside copyable prompts.
---

# Frame Vision Director

## Core Rule: One Film, One Visual System

When generating prompts for a group of storyboard frames, do not change the overall style for every image.

First define a `全片统一风格包`, then reuse it across every prompt.

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
| 参考图使用规则 |  |
| 风格展开描述 |  |
| 画面比例 |  |
| 统一负面词 |  |

Each shot can vary subject, scene, action, shot size, and composition, but the camera system, lens family, color tone, lighting logic, and texture should remain consistent unless the script intentionally changes chapter or mood.

## Style Control: Unified DNA, Shot-Specific Variation

Do not interpret `每个画面给相应风格` as giving every shot a completely different aesthetic.

Correct rule:

```text
全片统一影像 DNA 不变：
摄影系统、镜头家族、真实度、色彩边界、材质质感、颗粒/锐度、人物质感、禁用项。

每个镜头局部变化：
地点、时间、光源方向、景别、构图、前景遮挡、情绪强度、关键道具、空间关系。
```

For a sequence, prompts must feel like frames from the same film or same episode, not a mixed moodboard.

Bad:

```text
镜头1参考 Fincher，镜头2参考 Wong Kar-wai，镜头3参考 Dune，镜头4参考 Apple TVC。
```

Good:

```text
全片主参考：Fincher-style procedural realism + Roger Deakins restrained natural light.
镜头1：雨后警局入口，暖内光和湿地反光。
镜头2：询问室，冷白荧光灯和门框遮挡。
镜头3：证据室，屏幕冷光和长焦压缩。
镜头4：山林闪回，自然灰绿光和手持不安感。
```

Every prompt should inherit the same master style sentence, then add a short shot-specific visual sentence.

Use this internal formula:

```text
Master style lock + Shot-specific scene/lighting/composition + Tool-specific prompt wording + Negative control
```

If the user asks for different scene/location style, vary only what the story naturally changes. Do not change the whole film style unless the user explicitly says to change chapter, genre, era, or visual route.

## Self-Contained Prompt Rule

Every storyboard/keyframe prompt must include the complete style language inside the prompt itself.

Do not put the style only in a separate `统一风格包` and then give short shot prompts underneath. The style package can be shown for planning, but every final copyable prompt must repeat the relevant style details.

Forbidden output:

```text
统一风格：现实主义犯罪电影感，低饱和，ARRI Alexa...
镜头01：警局门口，人物报案。
镜头02：询问室，人物坐在桌前。
```

Required output:

```text
镜头01：警局门口，人物报案，现实主义犯罪电影质感，ARRI Alexa 35影像风格，50mm镜头，低饱和灰蓝色调，雨后湿地反光，冷暖混合自然光，真实皮肤和旧建筑材质...

镜头02：询问室，人物坐在桌前，现实主义犯罪电影质感，ARRI Alexa 35影像风格，85mm长焦压缩，低饱和灰绿色墙面，冷白荧光灯，旧木桌和纸质卷宗材质...
```

Final prompts must never use:

```text
风格同上 / 延续上条 / 同统一风格 / 同前 / 保持一致
```

The user may still receive a `全片统一风格包` for review, but the copyable table must be fully self-contained.

## Prompt Readiness Check

Before real image generation, check whether the prompt contains:

| 检查项 | 要求 |
| --- | --- |
| 主体 | 人物/产品/场景/道具明确 |
| 场景 | 时间、地点、环境明确 |
| 动作/状态 | 静态姿态或关键动作明确 |
| 构图 | 前景/中景/远景、主体位置明确 |
| 机位/景别 | 低机位、高机位、近景、中景、大全景等明确 |
| 摄影系统 | ARRI/Sony/RED/Blackmagic 等影像语言明确 |
| 镜头焦段 | 24mm/35mm/50mm/100mm macro 等明确 |
| 光线 | 主光、逆光、自然光、体积光或棚拍光明确 |
| 色彩 | 调色方向和主色关系明确 |
| 材质 | 关键材质和触感明确 |
| 比例 | 默认 16:9，除非用户另说 |
| 负面词 | 文字/logo/手脸/变形/AI感等风险明确 |
| 参考图角色 | 每张参考图只控制指定特征 |

If incomplete,补齐后再交给生成工具。

## Process

1. Use storyboard, style bible, visual direction, and reference images as source.
2. Create or inherit the unified visual style package before writing shot prompts.
3. Treat each prompt like a cinematographer's image brief, not a generic illustration prompt.
4. Expand the unified style package inside every copyable prompt.
5. When a shot has a reference image, use it only as a local constraint.
6. Do not let a single-shot reference override the unified film style.
7. For S-priority key shots, provide A/B/C style routes only if the user is still choosing the overall style.
8. Once a route is chosen, all prompts must follow that selected style.
9. For B/C-priority shots, give fewer prompts or recommend no image generation.
10. For Banana execution, also provide `compactPrompt` when the user asks for fast/token-saving generation.

## Tool Adaptation

| 工具 | 提示词处理 |
| --- | --- |
| 内置 imagegen | 完整、自然语言、强调主体层级和空间布局，适合快速看效果 |
| Banana | 清晰主体、材质、构图、负面词，提供 `compactPrompt`，默认 2K |
| 即梦 | 中文电影化描述，镜头语言、光线、比例、负面项清晰 |
| Midjourney | 转成 MJ prompt body + 参数后缀，如 `--ar 16:9 --v 7 --raw` |

## Reference Image Roles

For each reference image, specify one or more roles:

| 角色 | 含义 |
| --- | --- |
| 构图参考 | 只参考画面位置、前后景和空间关系 |
| 材质参考 | 只参考表面质感、纹理、反光、年代感 |
| 动作参考 | 只参考姿态、手势、运动瞬间 |
| 人物参考 | 只参考角色身份、脸型、发型、服装等指定内容 |
| 产品/道具参考 | 只参考造型、结构、比例、关键细节 |
| 色调参考 | 只参考色彩氛围，不照搬内容 |
| 风格参考 | 只参考摄影、光线、质感，不复制具体画面 |

Also state what not to inherit when needed, such as `不采用参考图背景`、`不采用参考图色调`、`不复制文字和logo`.

## Output

Use this table by default:

| 镜号 | 优先级 | 工具 | 参考图说明 | 完整可复制提示词 | compactPrompt/Banana 2K省token提示词 | 负面提示词 | 比例 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Do not leave camera, lens, or lighting only in separate columns. They must appear inside `完整可复制提示词`.

Do not write `风格同上`. Every prompt must be self-contained.

## Copyable Prompt Formula

```text
[镜头内容] + [参考图约束] + [统一主风格] + [摄影系统] + [镜头/焦段] + [景别/机位] + [光线方案] + [色彩/调色] + [材质/质感] + [景深/颗粒/锐度] + [构图规则] + [画面情绪] + [比例] + [清晰度/品质要求]
```

## Camera Guidance

Use camera and lens references as visual language:

- ARRI Alexa 35 + Zeiss Supreme Prime: premium commercial film look, clean product clarity, controlled highlight roll-off.
- ARRI Alexa Mini LF + Cooke S4/i: large-format cinematic depth, warm skin, elegant brand film.
- Sony Venice 2 + Panavision anamorphic: polished modern luxury, wide cinematic scale, smooth low-light.
- RED V-Raptor + Zeiss Supreme Prime: crisp high-resolution, tech/product detail, bold contrast.
- Blackmagic URSA Cine + Cooke Panchro: grounded cinematic realism, human documentary texture.

## Consistency Checks

Before final output, check:

- Does every prompt use the same main style?
- Does every prompt include camera system and lens/focal length inside the copyable prompt?
- Does every prompt include lighting and color inside the copyable prompt?
- Does every prompt repeat the detailed style package instead of saying `同上`?
- Is each reference image role explicit?
- Does the reference image preserve the unified film style rather than changing the whole group?
- Are only shot-specific details changing?
- Are negative prompts easy to copy?

## Tool-Specific Prompt Profiles

Do not use one identical prompt for all image tools. Keep the same visual direction, but rewrite the execution language for the selected tool.

### Built-In Imagegen / ChatGPT Image

Use when the user says `内置出图`, `image-2`, `ChatGPT Image`, `直接生成一张`.

Prompt style:

- Natural visual instruction, not parameter-heavy.
- Lead with the exact image content and spatial layout.
- Explain reference image roles clearly if images are attached.
- Use camera/lens/light language only when it helps the image.
- Avoid long negative prompt blocks; fold important exclusions into the instruction.

Best structure:

```text
Create a cinematic still frame of [subject/action] in [scene].
Composition: [foreground/midground/background, camera angle, shot size].
Lighting and color: [source, direction, tone].
Texture and realism: [materials, skin, fabric, environment].
Reference images: [only use X for face/pose/material/etc.].
Avoid: [major risks].
Aspect ratio: [ratio].
```

### Banana / Banana Pro

Use when the user says `Banana`, `Banana Pro`, `重出`, `继续出`, `省 token`.

Prompt style:

- Strong single-scene description.
- One core subject and one clear visual goal per image.
- Detailed material, lighting, lens, and composition are useful.
- Negative prompt should be explicit and copyable.
- Provide `compactPrompt` when speed/token saving matters.

Best structure:

```text
[镜头编号与画面目标]，[主体 + 场景 + 动作]，
[构图/机位/景别]，[摄影系统 + 焦段]，
[光线 + 色彩 + 材质]，
[统一风格 DNA + 质量要求]，[比例]。

负面词：
[文字/logo/手部/脸崩/塑料感/风格漂移/工具特定风险]
```

Banana Pro should receive cleaner cinematic descriptions and fewer conflicting adjectives. If a prompt is long, keep the first 60-90 Chinese characters as the strongest image target.

### Jimeng / 即梦 Image

Use when prompts are prepared for 即梦图片.

Prompt style:

- Chinese, direct, shot-oriented.
- Put subject, action, scene, and lens movement/angle early.
- Avoid excessive English camera jargon unless necessary.
- Negative prompt must strongly control text, logos, hands, faces, and modern/period errors.

Best structure:

```text
[主体]在[场景]中[动作/状态]，
画面为[景别/机位/构图]，
[光线/色彩/材质/氛围]，
[电影摄影风格 + 清晰度 + 比例]。
```

### Midjourney / MJ

Use when the user says `MJ`, `Midjourney`, or `Legnext`.

Prompt style:

- Condensed visual phrases.
- Put the strongest visual nouns first.
- Use style references as principles, not copied names if the user wants commercial-safe output.
- Use parameters at the end.
- Avoid long explanatory sentences.

Best structure:

```text
[subject], [scene], [composition], [lighting], [material texture], [cinematic camera language], [mood], [quality]
--ar 16:9 --style raw --v 7
```

### Prompt Quality Rules For All Tools

- A good image prompt is not a director essay. It is a precise image instruction.
- One image = one dominant subject, one space, one visual intention.
- Put the most important visible content first.
- Put abstract meaning after visible image details, or omit it.
- Reference images must have assigned roles: face, pose, costume, material, scene, composition, or tone.
- Do not ask the model to generate readable long text. Use `short number / simple Chinese mark / blurred unreadable document` when needed.
- Do not stack incompatible styles in one prompt, such as documentary realism + glossy fantasy + cyberpunk + oil painting.
- If a prompt needs more than one paragraph to explain the shot, create a director note plus a shorter tool prompt.

## Local Edit / Person Replacement Prompt Control

When the task is `替换人物`, `换脸`, `换角色`, `只改人物`, `不改变其他`, `保持原图`, or `局部重绘`, do not use the normal full-frame keyframe prompt.

Use an edit prompt with four blocks:

1. `锁定原图`: what must stay unchanged.
2. `替换目标`: exactly which person/object/area changes.
3. `新形象`: what the replacement should look like.
4. `融合规则`: how to match lighting, pose, lens, shadow, grain, and color.

Required copyable prompt shape:

```text
只替换原图中的[目标人物/目标区域]，严格保留原图的背景、构图、机位、镜头透视、光线方向、色调、景深、画面比例、其他人物和所有环境细节。
将目标人物替换为[新人物形象]；人物参考图只用于脸型、发型、年龄气质、服装特征，不参考背景和构图。
新人物必须站在原图同一位置，保持原图姿态和身体朝向，受光、阴影、边缘光、颗粒、清晰度与原图一致，像真实拍摄中同一镜头内的人物替换。
禁止重绘整张图，禁止改变背景，禁止改变其他人物，禁止新增或删除物体，禁止改变镜头角度，禁止改变光线和色调。
```

For Banana/Banana Pro, keep this edit boundary at the very beginning of the prompt. Avoid long cinematic style expansions that may cause the model to remake the whole image.
