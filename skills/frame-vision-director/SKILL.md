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
| 顶级摄影锚点 | 必须继承 `$reference-visual-library/references/shared-elite-cinematography.md` 选定的一个摄影或导演视觉锚点 |
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

Mandatory cinematography rule:

```text
Formal project prompts must include the selected top-tier cinematography anchor as executable language.
Do not write only "电影感" or only a reference name.
Convert the anchor into camera system, lens, lighting, color, material, and composition inside every copyable prompt.
```

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

## Fielded Storyboard Source Rule

When the source already uses production-friendly fields such as `Visual Baseline`, `Continuity Lock`, `Shot Size`, `Camera Lens`, `Content`, `Composition`, and `Image Style Prompt`, use that structure instead of rewriting the project from scratch.

Treat the storyboard as two layers:

- Master layer: visual baseline, style lock, continuity lock, era/material rules, character/prop rules, text/logo controls.
- Shot layer: shot id, shot size, camera position, focal length, content, action/state, composition, local lighting, local material details, local negative controls.

Final image prompts should not copy the full master layer verbatim into every shot. Compress the master layer into concrete executable style language, then combine it with the current shot fields:

```text
current visible frame + subject/space/action + shot size/camera/lens/composition + shot continuity locks + compact style lock + targeted negatives + ratio
```

This improves accuracy because the model receives one dominant image goal with explicit spatial and continuity anchors. It also improves speed because repeated style essays and irrelevant scene text are removed before generation.

Never turn a fielded storyboard into a generic keyword prompt. Preserve exact prop shapes, material states, period rules, character relations, and foreground/midground/background layout when those fields are present.

## TVC Single-Shot Image Prompt Handoff

Use this when the source contains `tvc_segment_storyboard_lock` / `tvc_shot_prompt_handoff` and the user asks for 每个小分镜提示词, 单独小分镜出图, 逐镜出图提示词, or individual image frames after a TVC story board.

Default this route to `quick_test`. Do not require formal project state, mother-library packet, full platform audit, or QC unless the user explicitly says 正式批量, 客户交付, 入项目状态, or QC.

Treat these upstream fields as the visual authority:

```text
tvc_segment_storyboard_lock
tvc_shot_prompt_handoff
recommended_board_type / board_type
jimeng_direct_reference_board
character_lock
costume_lock
prop_lock
product_or_brand_lock
scene_lock
style_lock_compact
key_beats
```

Do not redesign characters, props, products, brand exposure, set layout, costume, or style. Convert the approved beat into a clearer single still frame.

For each S/A shot, output one `tvc_shot_image_prompt_packet`:

```text
tvc_shot_image_prompt_packet
segment_name:
shot_id:
source_key_beat:
shot_function:
prompt_priority:
character_lock:
costume_lock:
prop_lock:
product_or_brand_lock:
scene_lock:
composition_and_staging:
camera_and_lens:
lighting_and_material:
style_lock_compact:
continuity_from_board:
copyable_image_prompt:
negative_prompt:
ratio:
handoff_to_video:
jimeng_usage_note:
```

If `jimeng_direct_reference_board: true`, the single-shot image prompt should create a clean first-frame or keyframe candidate for Jimeng/Seedance. The prompt must not include storyboard sheet borders, frame numbers, arrows, readable captions, note areas, layout labels, or tiny text unless the user explicitly asks for a board image.

Every `copyable_image_prompt` must remain self-contained: visible frame, subject/action, scene, product/prop lock, camera/lens/composition, light/material/color, compact style lock, ratio, and negative controls all inside the prompt. Never use 同上, 延续上条, or 参考前面.

### TVC Single-Shot Standard Output

When replying to the user with TVC per-shot image prompts, use this compact structure. Do not bury the copyable prompt inside long analysis.

```text
## TVC逐镜 image 提示词
模式: quick_test / formal_managed
继承来源: segment_name + board_type + upstream_source
用途: image首帧 / 单独关键帧 / 即梦或Seedance视频参考

### S01｜shot_function
画面目标:
锁定项: 人物 / 服装 / 道具 / 产品或品牌 / 场景 / 风格
Image提示词:
负面项:
后续视频用途:
```

Output full prompts for S/A shots first. For B/C shots, provide a short note unless the user asks for every shot.

`Image提示词` must be one copyable paragraph, not a keyword list. It should include:

```text
可见画面 + 人物/产品/道具动作 + 前中后景关系 + 景别/机位/焦段 + 光线/色彩/材质 + 风格锁 + 比例 + 禁止项
```

If exact readable logo, slogan, subtitles, handwritten notes, or product text is required, mark it as 后期叠加 or 只锁定位置/色块/版式关系. Do not ask the image model to generate dense readable text unless the user explicitly requires it.

For Jimeng/Seedance first-frame use, add a short `后续视频用途` line that states what the video model should inherit: character, product, scene, light, camera angle, and action start state. It must also state what not to inherit if the source came from a board: frame borders, numbers, labels, arrows, note areas, and tiny text.

## No Template Prompt Rule

Final copyable prompts must not look like generic AI prompt templates.

Hard reject these patterns:

```text
生成一张 9:16 原生竖屏 4K live-action cinematic documentary still...
live-action cinematic documentary still
电影感，高级感，真实感，纪录片感
Oscar-level / Nolan style / Fincher style as plain name-dropping
镜头7 | MS | 50mm f/2.8 as the main style description
```

Why: these phrases are labels, not visual direction. They do not tell the model what to render, how to light it, or how to compose it.

Required replacement:

```text
先写可见画面：谁在什么地点做什么，前景/中景/背景是什么。
再写摄影锚点转译：例如“长焦压缩派出所询问室空间，实用荧光灯从头顶压下，门框和桌面形成前景遮挡”。
再写具体技术：摄影系统、焦段、景别、光线、色彩、材质、景深、比例。
最后写负面词。
```

For Chinese execution platforms and Banana/Banana Pro, final prompts should be primarily Chinese. Keep English only for camera/model names, lens names, or unavoidable platform terms.

## Visual Helpfulness / Director Contribution Rule

Every final image prompt must be useful to the picture. Each kept phrase must control one of:

```text
visible subject, object shape, costume, prop, scene, or spatial layout
foreground / midground / background / composition / camera position / lens / depth
light source, light direction, exposure, color boundary, or material texture
reference image role or do-not-inherit boundary
mother-library mechanism translated into light, lens, space, composition, material, or performance
AI risk control that protects the frame from text/logo/face/hand/style drift
```

If a phrase cannot answer "what visible part of the image will be more accurate, more stable, or more cinematic?", delete it or translate it.

For formal work, preserve `director_contribution_packet`:

```text
style-reference / reference-visual-library: mother_library_application_packet and cinematography anchor
scene-style-map-director: scene function, light, lens tendency, material, performance state
shot-language-auditor: shot function, coverage role, edit motivation, screen direction when applicable
character/product continuity: identity, costume, prop/product structure, forbidden drift
frame-vision-director: self-contained platform-ready image prompt
```

The final image prompt should not show long director explanation, but it must retain the visible controls contributed by each relevant director.

Bad final prompt:

```text
生成一张 9:16 原生竖屏 4K live-action cinematic documentary still。派出所询问室，黄岚坐在桌前，50mm f/2.8。
```

Good final prompt:

```text
镜头7，派出所询问室中景。黄岚坐在旧木桌前，身体微微前倾，桌面边缘和一盏冷白台灯压在前景，身后是灰绿色墙面和模糊的白板。整体采用程序化悬疑片的克制调度，并转译 Roger Deakins 式动机光摄影：头顶荧光灯和桌面台灯作为真实光源，低饱和冷灰绿调，长焦轻微压缩空间，人物被桌面和门框压迫但表情清楚。ARRI Alexa 35 影像质感，50mm，f/2.8，中景平视，浅景深，真实皮肤、旧木桌、纸张、墙面漆皮细节，9:16。禁止可读文字、警徽特写、字幕、水印、logo、塑料皮肤、HDR锐化、廉价AI电视剧感。
```

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
| 画面有效性 | 每个保留词都能改善或保护可见画面、构图、光线、材质、连续性或风险控制 |
| 导演贡献 | 母库、场戏、镜头语言、角色/产品连续性的贡献被保留或压缩为可见机制 |

## Generation Gate Rule

Image prompts are execution briefs, not style exploration notes.

Before handing a formal project prompt to Banana, Banana Pro, built-in imagegen, Midjourney, or Jimeng Image, the shot must pass:

```text
已有 project-style-lock
镜头功能明确
景别/机位/构图明确
摄影系统/焦段/光圈或景深明确
光线/色彩/材质明确
参考图角色明确（如有参考图）
负面词明确
已准备交给 prompt-platform-auditor
```

If any gate item is missing, do not generate. Complete the director/prompt layer first.

Do not rely on multiple generations to find the style. Generation can test execution quality; it cannot replace reference matching, scene style mapping, shot-language logic, or style lock.

Hard pass rule:

```text
Final image prompts cannot pass if any of these are missing:
景别、机位、构图、摄影机/影像系统、镜头焦段、光圈或景深、光线来源和方向、色彩/调色、材质质感、比例、负面词。
```

If incomplete,补齐后再交给生成工具。

## Mandatory Camera Detail Rule

Every final copyable image prompt must explicitly describe:

| Field | Required detail |
| --- | --- |
| 景别 | ECU / CU / MCU / MS / WS / EWS, or Chinese equivalent such as 特写、中近景、中景、全景、大全景 |
| 机位 | 平视、低机位、高机位、俯视、仰视、肩后、贴地、门缝/玻璃后等 |
| 构图 | 前景/中景/背景关系，主体位置，遮挡物或负空间 |
| 摄影机/影像系统 | ARRI Alexa 35, Alexa Mini LF, Sony Venice 2, RED, Blackmagic URSA Cine, or equivalent visual language |
| 镜头焦段 | 24mm / 35mm / 50mm / 65mm / 85mm / 100mm macro etc. |
| 光圈/景深 | f/1.4, f/2, f/2.8, deep focus, shallow depth, macro depth, or equivalent |
| 光线 | source, direction, softness, contrast, practical light / window light / backlight / fluorescent etc. |
| 色彩 | low saturation, cold gray-green, warm tungsten, industrial blue-gray, restrained contrast etc. |
| 材质 | skin, fabric, paper, metal, glass, wood, concrete, dust, rain, screen glow etc. |
| 风格机制 | top-tier cinematography anchor translated into visible language, not plain name-dropping |

Do not output only:

```text
MS | 50mm f/2.8
```

Output:

```text
中景平视，50mm，f/2.8浅景深，ARRI Alexa 35影像质感，长焦轻微压缩询问室空间，桌面和门框形成前景遮挡。
```

## Process

1. Use storyboard, style bible, visual direction, and reference images as source.
2. If reference images are provided in a formal project, inherit `$reference-image-style-matcher` results before writing prompts.
3. For formal projects, inherit the project/scene reference decision from `$style-reference-director`.
4. If the user provides a script, storyboard, shot list, or multiple scene references, inherit the scene style map from `$scene-style-map-director` before writing shot prompts.
5. For formal projects with an approved route, inherit `$project-style-lock`; do not re-invent style wording.
6. Create or inherit the unified visual style package before writing shot prompts.
7. Treat each prompt like a cinematographer's image brief, not a generic illustration prompt.
8. Expand the project style lock, the reference-image matcher result, and this scene's local visual strategy inside every copyable prompt.
9. When a shot has a reference image, use it only as a local constraint.
10. Do not let a single-shot reference override the unified film style.
11. For S-priority key shots, provide A/B/C style routes only if the user is still choosing the overall style.
12. Once a route is chosen, all prompts must follow that selected style.
13. For B/C-priority shots, give fewer prompts or recommend no image generation.
14. For Banana execution, also provide `compactPrompt` when the user asks for fast/token-saving generation.
15. Before sending prompts to a generation tool, pass them to `$prompt-platform-auditor` for platform-specific approval or rewrite. The auditor must preserve the intended visual effect, not merely shorten the prompt.

## No Lazy Handoff Rule

`$frame-vision-director` writes image prompts from approved upstream decisions. It does not replace upstream directors.

Do not use this skill to:

```text
choose project reference style instead of style-reference-director
reverse-match reference images instead of reference-image-style-matcher
divide scene styles instead of scene-style-map-director
fix shot sequence logic instead of shot-language-auditor
invent project-style-lock or style bible
repair missing poster_type / core_hook / layout_safe_area instead of poster-director
```

If formal image prompts lack required upstream outputs, do not write final copyable prompts. Output `待补上游项` and route back to the owning skill.

Required upstream outputs for formal prompts:

```text
style-reference decision
reference-image match when images are used
scene-style-map for multi-scene work
shot-language result for dramatic/short-drama multi-shot work
project-style-lock
prompt-platform-auditor target platform before execution
```

## Project Style Lock Rule

For formal projects, final prompts must use the current `$project-style-lock`.

Do not rewrite the core visual DNA differently each time. Only vary scene-specific items:

```text
地点、时间、光源方向、景别、焦段、前景遮挡、情绪强度、关键道具、空间关系
```

The project style lock must appear inside every copyable prompt through a stable `master_style_sentence` or its platform-safe compact version.

If no style lock exists and the user is asking for formal project prompts, create or request one through `$style-bible-director` / `$project-style-lock` before final prompt output.

## Reference Image Matcher Inheritance

When `$reference-image-style-matcher` is available, every final prompt using a reference image must include:

```text
参考图只控制什么
母库匹配后的风格机制
顶级摄影锚点转译
不能继承什么
```

Do not write only:

```text
参考这张图风格
按参考图
类似参考图
```

## Mother-Library Translation Inheritance

For formal short-drama, story, commercial, promo, TVC, event, or LED projects, every final prompt must inherit the mother-library translation from `$style-reference-director` or `$reference-image-style-matcher`.

The prompt may mention a reference family only after it has been converted into visible execution language. Every copyable prompt must contain:

```text
mother_library_application_packet 的当前场戏/镜头应用规则
光线方向
空间压迫/开放关系
焦段心理效果
构图调度
材质触感
人物表演状态
AI风险控制
```

These are not optional style notes. They are part of the final prompt. If they are missing, the prompt is not final and must be rewritten before generation.

If a formal prompt lacks `mother_library_application_packet` or an equivalent scene-specific mother-library application rule, route back to `$style-reference-director` / `$scene-style-map-director` / `$project-style-lock`. Do not fill the gap with generic "cinematic" wording.

Bad:

```text
现实主义悬疑短剧风格，低饱和，电影感，高级感。
```

Good:

```text
采用母库中现实主义悬疑短剧的克制调度机制：冷白顶灯从人物上方压下，门框和桌沿制造前景遮挡，65mm长焦轻微压缩问询室空间，低饱和灰绿墙面与旧木桌形成潮湿压迫感，人物表演收住情绪、眼神躲闪但脸部清晰，避免网剧滤镜和夸张表演。
```

## Tool Adaptation

| 工具 | 提示词处理 |
| --- | --- |
| 内置 imagegen | 正式出图主工具之一。中文自然语言为主，少量英文摄影术语只用于 camera/lens/lighting/material，适合单张效果、局部替换、保持原图和自然语言控制 |
| Banana / Banana Pro | 正式出图主工具之一。中文画面指令 + English camera/lens/lighting/material keywords + 中文负面词，适合批量关键帧、省 token、多参考图和稳定执行 |
| 即梦 | 不作为默认出图工具；只在用户明确要求即梦图片时提供平台化提示。正式项目优先用内置 imagegen 或 Banana/Banana Pro 出图，即梦主要用于图生视频 |
| Midjourney | 转成 MJ prompt body + 参数后缀，如 `--ar 16:9 --v 7 --raw` |

## Language Strategy Hard Rule / 语言策略硬规则

Final prompt language must match the execution platform.

- 内置 imagegen / ChatGPT Image: use Chinese natural-language visual instructions first. Keep English only for necessary camera, lens, lighting, material, or model terms. This is best for single images, natural edits, local replacement, and preserving the original image.
- Banana / Banana Pro: use Chinese visible-frame instructions + English camera/lens/lighting/material keywords + Chinese negative prompt. Keep the prompt compact but dense; put the strongest visible image target first.
- Jimeng / Seedance video handoff: do not write image-generation style paragraphs here. Video text should be Chinese, short, motion-clear, and only control action/motion/environment/end frame.

For formal image work, every copyable prompt must include the full style and cinematography mechanism inside itself:

```text
visible frame + shot function + shot size/camera position/composition + camera/lens/depth + mother-library translation + local light/color/material + performance state + anti-AI realism + ratio + negatives
```

Do not allow final prompts that only say:

```text
电影感、高级感、真实感、低饱和、同上、统一风格、参考母库风格
```

Anti-AI realism is mandatory for image prompts:

```text
保留真实摄影的不完美：真实皮肤纹理、轻微瑕疵、衣料褶皱、生活痕迹、环境灰尘、旧物磨损、自然暗部颗粒、明确现实光源、真实景深和原有光比；不过度锐化、不磨皮、不做假HDR、不做平台模板感。
```

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

| 镜号 | 优先级 | 工具 | 出图门槛 | 参考图说明 | 完整可复制提示词 | compactPrompt/Banana 2K省token提示词 | 负面提示词 | 比例 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

`出图门槛` values:

```text
通过 / 待补风格锁 / 待补镜头语言 / 待补参考图角色 / 待补导演贡献 / 待补画面有效性 / 待平台审核
```

For formal managed batches, preserve these packet fields beside the copyable prompt or in the handoff:

```text
director_contribution_packet
visual_helpfulness_check
mother_library_application_packet
```

Do not leave camera, lens, or lighting only in separate columns. They must appear inside `完整可复制提示词`.

Do not write `风格同上`. Every prompt must be self-contained.

## Copyable Prompt Formula

```text
[镜头内容] + [参考图约束] + [统一主风格] + [摄影系统] + [镜头/焦段] + [景别/机位] + [光线方案] + [色彩/调色] + [材质/质感] + [景深/颗粒/锐度] + [构图规则] + [画面情绪] + [比例] + [清晰度/品质要求]
```

For formal projects, the copyable prompt formula must also include a mother-library translation mechanism:

```text
母库应用规则：本镜头继承母库的哪个场戏功能机制，例如审讯压迫、证据反转、产品清晰、工业尺度、仪式揭示或情绪崩塌。
母库转译机制：光线方向 + 空间关系 + 焦段心理效果 + 构图调度 + 材质触感 + 人物表演状态 + AI风险控制
```

## Fixed Copyable Prompt Schema

Use this fixed order for formal project image prompts:

```text
1. 可见画面目标：谁在什么地点做什么，前景/中景/背景是什么。
2. 镜头功能：这张图承担建立空间、人物压力、物证、反应、反转或情绪收束中的哪一种。
3. 景别/机位/构图：必须写清主体位置、遮挡、负空间或空间层次。
4. 摄影系统/焦段/景深：必须写清相机视觉系统、焦段、光圈或景深。
5. 项目风格锁：嵌入固定 master_style_sentence，不重新发明风格。
6. 母库应用规则：写清该镜头继承哪个母库场戏功能机制。
7. 母库转译机制：转成光线、空间、焦段、构图、材质、表演和AI风险。
8. 本场局部变化：只写本场光线、色彩、材质、情绪强度。
9. 参考图角色：只继承指定内容，并写不继承项。
10. 比例/质量。
11. 负面词。
```

Do not output prompt paragraphs in a different order unless the target platform specifically requires it.

Schema correction:

```text
The fixed order must include a dedicated mother-library translation step before ratio/quality:
母库应用规则：写清本镜头继承母库的哪个场戏功能机制。
母库转译机制：写清该镜头继承的母库视觉机制，并转成光线、空间、焦段、构图、材质、表演和AI风险。不能只写电影名、导演名或“高级电影感”。
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
- Does every prompt include the selected top-tier cinematography anchor as executable camera/light/composition language?
- Does every prompt include camera system and lens/focal length inside the copyable prompt?
- Does every prompt include lighting and color inside the copyable prompt?
- Does every prompt repeat the detailed style package instead of saying `同上`?
- Is each reference image role explicit?
- Does the reference image preserve the unified film style rather than changing the whole group?
- Are only shot-specific details changing?
- Are negative prompts easy to copy?

## Tool-Specific Prompt Profiles

Do not use one identical prompt for all image tools. Keep the same visual direction, but rewrite the execution language for the selected tool.

If the target tool is known, the final copyable prompt must be the platform-audited execution version, not the director draft.

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

Built-in imagegen anti-AI style insert:

```text
保留真实摄影的不完美：人物皮肤有自然纹理和轻微瑕疵，衣料有褶皱和重量，空间有合理生活痕迹和灰尘，暗部不过度提亮，光源来自真实窗光/台灯/荧光灯/手机屏幕，画面不过度锐化、不磨皮、不做假HDR。
```

For built-in imagegen edits or replacement tasks, state what must stay unchanged before describing the change. Do not give it a new full-frame style unless the user wants the whole image repainted.

### Banana / Banana Pro

Use when the user says `Banana`, `Banana Pro`, `重出`, `继续出`, `省 token`.

Prompt style:

- Strong single-scene description.
- One core subject and one clear visual goal per image.
- Detailed material, lighting, lens, and composition are useful.
- Negative prompt should be explicit and copyable.
- Provide `compactPrompt` when speed/token saving matters.
- Banana/Banana Pro prompts should be compact but dense: visible frame first, then camera/composition/light/material, then concise anti-AI negatives.
- For Banana Pro or multi-reference work, assign each reference image a narrow role: face, costume, pose, lighting, composition, material, or background.
- To avoid AI look, include tactile imperfections and exposure discipline inside the positive prompt, then put plastic/beauty/HDR/fake-depth failures in the negative prompt.

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

Banana anti-AI compact insert:

```text
真实摄影质感，保留皮肤细纹、自然暗部颗粒、衣料褶皱、旧物磨损、环境灰尘和真实景深，光线来自明确现实光源，暗部不过度提亮，画面不过度锐化。
负面词：塑料皮肤、美颜磨皮、AI模特脸、假景深、HDR锐化、过度补光、平台模板感、网剧柔光、背景融化、五官漂移、文字乱码、logo、水印。
```

### Jimeng / 即梦 Image

Use only when the user explicitly asks for 即梦图片. Do not use Jimeng Image as the default formal image-generation route. For formal short-drama, promo, TVC, and brand-film keyframes, prefer built-in imagegen or Banana/Banana Pro, then use Jimeng primarily for image-to-video.

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
