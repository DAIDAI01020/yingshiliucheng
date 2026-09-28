---
name: image-qc-director
description: Quality-control generated images and video first frames for film and screen visual workflows. Use after built-in imagegen, Banana, Midjourney, or other image generation when the user asks whether generated images are usable, need revision, should be regenerated, or should have prompts rewritten. Checks storyboard alignment, unified visual style, subject accuracy, composition, reference-image usage, text/logo risks, face/hand issues, generation artifacts, and video first-frame motion potential.
---

# Image QC Director

## Core Rule

Use this skill after images have been generated or when the user provides generated image paths/screenshots and asks whether they work.

Judge against:

- Original storyboard or shot intent.
- Prompt.
- Unified style bible.
- Reference image constraints.
- scene_continuity_lock / background_continuity_lock / continuity reference board when present.
- Delivery context.
- Whether the image will be used as a video first frame.

Do not judge only by whether the image looks beautiful.

## Route Authority Boundary

Inherit `deliverable_profile`, `response_mode`, `qc_mode`, route decisions, and project state from `$zongkong` when present.

This skill owns QC diagnosis, failure attribution, and revision routing. It does not choose project tier, change `speed_mode`, rewrite the whole project style, approve missing formal gates, or generate replacement prompts as a substitute for the owning director.

For formal work, locate prompt/style/reference/state inputs before judging when available. If they are missing, output `missing_fields` and `route_back_to`; do not infer managed project state from memory.

## Direct Built-in Image QC

When an image was created through built-in `imagegen` / `直接用 image 出图`, obey `qc_mode`:

```text
none -> do not start an automatic QC pass
light_deferred -> review in a separate turn/workflow after the image result
formal -> run profile-specific QC and write state
```

If the user explicitly asks for review, run QC regardless of the previous `qc_mode`.

For quick direct image generation, output one compact judgment:

```text
direct_image_qc
decision: 可用 / 可小修 / 定向重出 / 提示词需重写 / 前置导演判断错误
reason:
main_risk:
next_action:
```

Check against the preflight intent, prompt, inherited style/source, subject constraints, composition, text/logo risk, artifact risk, and whether it can work as a video first frame when relevant. Do not require a full review table unless the user asks, the task is formal, or there are multiple images.

Use `deliverable_profile` to select checks. Do not judge a graphic/abstract, typography, product, LED/stage, or local-edit asset against unrelated live-action camera/skin rules.

## Inspection Evidence

Open the actual image and relevant references before semantic judgments. If unavailable, provide a limited technical or user-reported diagnosis and mark visual QC unverified. Record inspected asset/version and unresolved checks. Missing formal context limits approval but does not prevent reporting visible defects. QC usability is not client selection.

## QC Decisions

| 判断 | 含义 | 下一步 |
| --- | --- | --- |
| 可用 | 基本符合分镜和风格，可进入 PPT、首帧或交付候选 | 记录可用版本 |
| 可小修 | 方向正确，有轻微问题 | 局部修提示词或后期修图 |
| 定向重出 | 构图/主体/手脸/文字/光线/平台味等问题明显，但前置方向正确 | 只改受影响镜头或平台提示词后重出 |
| 提示词需重写 | 画面偏离根本目标，或风格/主体/参考图约束失效 | 重写该镜头提示词再出图 |
| 前置导演判断错误 | 镜头功能、场戏风格、参考匹配、风格锁或分镜逻辑本身错误 | 回到上游导演层，不直接重出 |

## Failure Attribution

QC must classify the root cause before recommending regeneration:

| 问题归因 | 含义 | 回到哪里 |
| --- | --- | --- |
| 生成偶发问题 | 手、脸、局部瑕疵、轻微结构错误，提示词方向正确 | 定向重出或负面词增强 |
| 提示词表达问题 | 主体、构图、材质、光线或文字语义不准 | 按交付物交给 `$frame-vision-director` / `$kv-image-prompt-director` / `$scene-board-image-prompter` / `$type-png-director` |
| 平台适配问题 | Banana/MJ/imagegen/即梦表现偏平台默认味或执行不稳 | `$prompt-platform-auditor` |
| 背景连续性问题 | 同场戏多张图的房间、墙面、门窗、灯位、桌椅、道具、A/B背景侧或轴线漂移 | `$short-drama-scene-director` / `$shot-language-auditor` / `$frame-vision-director` |
| 风格锁问题 | 证据表明已批准的全局规则有误或互相矛盾，不能只凭重复瑕疵判断 | `$project-style-lock` / `$style-bible-director` |
| 前置导演判断问题 | 镜头本身没叙事功能、场戏风格错、参考图匹配错 | `$scene-style-map-director` / `$shot-language-auditor` / `$style-reference-director` |

Only `风格锁问题` and `前置导演判断问题` justify upstream redesign. Ordinary generation failures must not trigger full style rewrites.

## Issue Tags

Use concise issue tags:

```text
风格漂移 / 背景漂移 / 越轴 / 视线方向错误 / 背景侧错误 / 道具跳位 / 灯位漂移 / 主体错误 / 构图不可用 / 光线不对 / 材质不对 / 文字logo风险 / 手脸异常 / 产品结构错误 / 参考图误用 / AI感过强 / 平台味过重 / 低清晰度 / 视频运动风险 / 首帧不可用 / 提示词需重写 / 前置导演判断错误
```

## QC Checklist

Before semantic QC on saved files, generate objective evidence when the runtime is available:

```powershell
python scripts\technical_image_qc.py --image H:\project\images\S01.png --output-dir H:\project\review\S01 --profile storyboard_frame
python scripts\technical_image_qc.py --image H:\project\images\S01.png --image H:\project\images\S02.png --reference H:\project\references\character.png --output-dir H:\project\review\scene01
```

Use `technical-image-qc.json` and the contact sheet for resolution, ratio, exposure clipping, edge-energy, alpha, file fingerprint, and reference-hash evidence. These measurements never decide identity, composition, continuity, generated-text correctness, or aesthetic quality by themselves.

Check:

- 主体是否正确：人物、产品、场景、道具、舞台关系是否符合分镜。
- 风格是否统一：是否保持风格圣经、摄影感、色彩、材质和光线逻辑。
- 构图是否符合用途：PPT关键帧、LED大屏、视频首帧、社媒竖版是否适配。
- 文本和Logo是否出错：乱码、错误标识、误生成品牌元素、标题空间污染。
- 人物和产品质量：脸、手、姿态、比例、产品结构、材质、反光是否可用。
- 参考图是否正确使用：是否只用了指定局部特征，是否错误改变整组风格。
- 生成瑕疵：水印、边框、AI感、低清、过曝、过锐、无关物体。
- 视频首帧潜力：是否有清晰运动方向、主体是否稳定、边缘是否干净、是否方便做推拉/环绕/转场。

## Same-Scene Background Continuity QC

Use this when images belong to one short-drama scene coverage group: 大景/全景、two-shot、正反打、过肩、对视、反应、物件插入.

Compare every image against `background_continuity_lock` or the `short_drama_scene_continuity_board`:

```text
same room or continuous space
same wall/window/door positions
same furniture and table layout
same practical light positions and light direction
same prop positions
same A/B left-right relationship
same background side behind each character
same eyeline direction and no unmotivated axis flip
```

QC fail examples:

```text
A背后本应是灰绿色墙+半开木门，生成成窗帘或新窗户
B背后本应是暖台灯+旧沙发，生成成白墙或厨房
桌上手机/水杯位置跳到另一侧
正反打里A/B左右关系翻转
过肩镜头前景肩膀属于错误角色
同一场戏灯位从左侧台灯变成右侧窗光
```

If one image has correct character but wrong background, classify as `背景连续性问题`, not broad style failure. Route targeted fixes to `$frame-vision-director` or `$prompt-platform-auditor`; route upstream only if the original `background_continuity_lock` or coverage map was missing/wrong.

## Output

Preserve a learning record for formal QC or a repeated quick-test failure:

```text
generation_observation
asset_id:
deliverable_profile:
platform_target:
failure_type:
prompt_or_source_cause:
successful_fix:
repeat_count:
promotion_target: none / prompt risk profile / style lock / continuity lock
```

Record repeated relevant failures as linked evidence. Propose a rule change only when the diagnosed cause supports it; applying a global lock change requires authorization for that scope. Record successful_fix only after a changed result has actually been inspected.

### 出图质检表

| 镜号 | 图片版本 | 工具 | 图片路径 | 判断 | 问题归因 | 问题标签 | 主要问题 | 可保留内容 | 修改建议 | 是否重出 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

For same-scene groups, add these fields when useful:

```text
scene_id
coverage_role
background_lock_match: yes / partial / no
axis_eyeline_match: yes / partial / no
continuity_board_match: yes / partial / no
```

### 重出建议

If regeneration is needed, output only affected rows:

| 镜号 | 原版本 | 重出方式 | 提示词修改点 | 参考图调整 | 负面词补充 | 新版本建议 |
| --- | --- | --- | --- | --- | --- | --- |

## Rules

- If only one shot fails, do not change the full style bible.
- If multiple S/A shots drift in the same way, recommend updating the style bible.
- If same-scene backgrounds drift but the style is correct, do not change the style bible; repair the background_continuity_lock prompt inheritance or regenerate affected shots with the continuity board as reference.
- If text/logo is wrong, preserve the requested exact-copy and brand intent. Route text assets to the typography owner or propose a layout correction; do not silently remove required text as a shortcut.
- If face/hand/product structure fails, simplify the action and strengthen reference constraints.
- If the image is for video first frame, judge clean motion potential, not only still-frame beauty.
- QC is not a new creative direction step. Do not recommend broad upstream changes unless the root cause is style-lock or director-logic failure.
- For `response_mode: direct`, return only the QC decision and next action. Use the full table only for batch/formal review or `diagnostic`.
