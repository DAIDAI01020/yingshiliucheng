---
name: short-drama-scene-director
description: Break down short drama scripts, finished drafts, or storyboards into scene-level visual direction, per-location style references, shot/keyframe requirements, reference-image roles, AI image prompt requirements, video prompt requirements, and generation risk notes.
---

# Short Drama Scene Director

## Core Role

`$short-drama-scene-director` turns a script, finished draft, or storyboard into scene-level visual direction and AI-generatable execution units.

It should not only split shots. It must first decide how scenes are grouped visually: which location, time, light source, emotion, clue, or turning point defines each scene.

For managed formal short-drama projects, this skill owns the scene-level content that should be recorded in:

```text
references/scene-map.md
```

Use `$project-state-manager check --stage generation` as the gate source. If the project state says `scene-map` is missing, produce or update the scene map before any final image/video prompt handoff.

Draft `references/scene-map.md` from the available script, character and visual direction. Reuse an existing style lock; do not require a completed lock before creating the scene map it depends on. Before final production handoff require only applicable hook/character/reference approvals and the completed scene/shot checks.

Inherit total route and state-owner decisions. This skill owns grouping, scene geography, blocking, continuity and shot requirements; it cannot change speed mode, approve generation or replace a missing upstream decision. Follow the [stage handoff contract](../zongkong/references/stage-handoff-contract.md).

Use when the user provides:

- 已有剧本
- 已有分镜
- 场次表
- 参考图
- 影视风格参考
- 需要拆成出图/视频镜头
- 需要每场戏先给风格参考

## Scene Merging Rules

Inherit the project's `format_spec` and actual shot `ratio` from intake; short drama supports 16:9, 9:16 and other specified formats. Preserve the ratio in scene, image and video handoffs. For multi-format scenes, design each rendition's framing while preserving identities, axis and prop state; never assume a centre crop preserves the scene. See the short-drama director's [format and camera reference rules](../short-drama-director/references/adaptation-and-shot-production.md).

For recurring setups, add `camera_id`, camera position/height/direction, axis side and reference role to the existing coverage packet. Bind `camera_reference_shot_id` to the approved frame actually used, not automatically the preceding edit. Inherit current blocking and prop changes instead of copying outdated state. The state owner validates this reference graph before dependent batches.

Do not create one image prompt per script sentence by default.

Merge shots into scene-level concepts when they share:

- 同一地点或连续空间
- 同一时间段或光源逻辑
- 同一情绪阶段
- 同一证据/线索推进
- 同一人物关系状态
- 同一视觉符号

Split into separate scenes when there is:

- 地点变化
- 日夜/天气/光源变化
- 情绪强度显著变化
- 叙事功能变化，例如报案、审问、反转、闪回、认罪、结案
- 视觉系统变化，例如现实空间转为回忆、监控、梦境、新闻、法庭

## Required Output 1: Scene Merge Table

| 场次 | 覆盖原稿段落/镜头 | 场名 | 地点/时间 | 主要人物 | 叙事功能 | 是否需要关键帧 | 是否需要视频 |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Required Output 2: 每场戏风格参考 / 视觉导演设定

For every scene, output this before any prompt:

| 场次 | 场名 | upstream_source | 母库参考机制 | 摄影锚点转译 | 参考审美方向 | 光线/色温 | 色彩/材质 | 构图/焦段 | 人物表演状态 | 视觉符号 | 出图/视频风险分流 | 为什么这样设定 | AI 风险 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

### Field Rules

- `参考审美方向`: Use film/series/documentary/TVC principles, not exact frame copies.
- `upstream_source`: state which reference-image match, mother-library route, scene map, style bible, or project-style-lock this scene inherits.
- `母库参考机制`: must translate the selected library route into light direction, space relation, lens psychology, composition blocking, material touch, performance state, and AI risk control.
- `摄影锚点转译`: convert the shared cinematography anchor into executable camera/light/composition language.
- `光线/色温`: Must be specific: rain after dusk, warm fluorescent room, cold monitor light, dawn forest mist, late-afternoon side light, etc.
- `色彩/材质`: Mention real materials: wet concrete, glass door, phone glow, police desk wood, muddy roots, fluorescent wall, court stone, steel, fabric.
- `构图/焦段`: Mention camera distance and psychological effect: low angle, through glass, over shoulder, long-lens compression, foreground obstruction, close portrait.
- `人物表演状态`: define restrained performance, gaze, breath, silence, hand tension, or emotional release; do not leave acting as a generic mood word.
- `视觉符号`: Name objects that carry drama: phone, text message, glass reflection, monitor, evidence bag, muddy road, taillight, file, badge, door crack.
- `出图/视频风险分流`: state whether the scene needs static keyframes, video movement, or split segments; note hand/face/text/platform-look risks.
- `为什么这样设定`: Explain in plain production language so clients understand the intention.
- `AI 风险`: Identify what generation may break and how to avoid it.

## Required Output 2A: 同场连续性锁 / Coverage Packet

When several shots share the same location, light, character blocking, or conversation beat, create one `scene_continuity_lock` before writing shot prompts. This is mandatory for 大景/全景建立镜头、两人对视、正反打、过肩、反应镜头、同桌谈话、审问、争吵、沉默对峙, or any same-scene coverage.

```text
scene_continuity_lock
scene_id:
space_geography: room layout, doorway/window/table/sofa/desk positions
time_and_light: same time period, practical light source, direction, color temperature
color_material: wall/floor/furniture/fabric/prop material continuity
prop_anchor: phone, file, cup, chair, evidence, lamp, door, window, etc.
character_blocking: A position, B position, distance, posture, who controls the space
screen_direction: A looks left/right, B looks left/right, do not flip eyelines
camera_axis: which side of the 180-degree line the camera stays on
background_side_map: what background belongs behind A, what background belongs behind B
background_continuity_lock: fixed walls, doors, windows, furniture, practical lights, prop positions, background depth
lens_family: wide/master lens and close coverage lens family
wide_master_rule: what the 大景/全景 establishes and what later shots must inherit
forbidden_drift: no new room, no changed wall/window/door, no changed light, no swapped positions, no mirrored eyelines, no moved props
```

`background_continuity_lock` must be practical and visible, not a vague mood phrase:

```text
A背后固定为灰绿色墙面+半开的木门+桌角前景
B背后固定为窗帘+暖台灯+旧沙发边缘
桌上手机在两人中间偏A侧，水杯在B侧
后续所有正反打、过肩、对视、反应镜头都不能新增窗户、换墙色、移动桌椅或改变灯位
```

For dialogue or confrontation scenes, also output:

```text
dialogue_coverage_packet
coverage_type: master_wide / two_shot / ots_on_A / ots_on_B / clean_single_A / clean_single_B / reaction_A / reaction_B / insert_object
coverage_role:
source_scene_continuity_lock:
character_visible:
foreground_shoulder_or_object:
eyeline_direction:
background_side:
shot_size:
camera_position:
focal_length_logic:
edit_motivation:
handoff_to_prompt:
```

### 大景 / Master Wide Rule

Do not treat 大景、全景、远景 as decorative wide shots. Use them only when they establish or re-establish:

```text
空间地理
人物左右关系
权力距离或孤立感
门/窗/桌/证据/出口的位置
后续正反打的轴线和背景侧
```

For 16:9, use readable lateral relationships, environmental clues and depth where appropriate. For 9:16, check that the master still communicates the important geography at viewing size. Choose shot size from narrative function in either format. After the master wide, all close/OTS/reaction prompts must preserve the same `scene_continuity_lock`.

### Continuity Reference Board Handoff

For formal same-scene coverage, create or request one `short_drama_scene_continuity_board` before batch image/video generation when background drift would be costly.

Route:

```text
scene_continuity_lock + background_continuity_lock + dialogue_coverage_packet
-> scene-board-image-prompter short_drama_scene_continuity_board
-> frame-vision-director / ai-video-prompt-director uses the board as scene/background reference
-> image/video QC checks generated outputs against the board
```

Board handoff fields:

```text
continuity_reference_board
board_type: short_drama_scene_continuity_board
scene_id:
source_locks: scene_continuity_lock / background_continuity_lock / dialogue_coverage_packet
must_show: master wide, overhead axis map, A background side, B background side, prop positions, light position, coverage preview cells
use_as_reference_for: same-scene image prompts, first frames, video prompts, QC
state_writeback: references/scene-map.md + asset-index continuity board record
```

## Required Output 3: Shot/Keyframe Table

Only after scene visual direction is approved or clearly implied:

| 镜号 | 场次 | coverage_role | 景别 | 镜头功能 | 剪辑动机 | 角色 | 动作/表情 | 构图 | scene_continuity_lock | background_continuity_lock | screen_direction | 参考图角色 | 是否出图 | 是否出视频 | 风险 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Shot Language Logic Rule

Before finalizing shot/keyframe tables, pass the shot flow through `$shot-language-auditor`.

Short-drama shots must not be random coverage. Each shot needs:

```text
镜头功能
景别递进
机位理由
焦段逻辑
剪辑动机
人物关系或信息推进
```

For 15s short-drama sequences, default to a readable progression:

```text
建立空间/关系 -> 人物压力 -> 关键物件/线索 -> 反应/对质 -> 反转/收束
```

Do not output final prompts if the sequence has repeated close-ups, unclear spatial relation, or no edit motivation.

## Reference Role Table

| 参考图 | 绑定对象 | 参考角色 | 不继承内容 |
| --- | --- | --- | --- |

Reference image roles should be narrow:

- 人物脸/发型
- 服装质感
- 场景地点
- 动作姿态
- 构图关系
- 光线/色调
- 材质细节

Avoid asking the model to average several references into one unclear result.

## Scene-Level Prompt Handoff

When handing to `$frame-vision-director`, include:

```text
upstream_source
director_contribution_packet
visual_helpfulness_targets
全剧统一风格 DNA
本场视觉参考
母库转译机制 / mother_library_translation
摄影锚点转译
platform_language_strategy
anti_ai_realism_rule
image_tool_boundary
角色锚点
参考图角色
scene_continuity_lock
background_continuity_lock
coverage_role
screen_direction / eyeline
background_side
镜头意图
镜头功能
剪辑动机
构图/机位/焦段
光线/色彩/材质
AI 风险与负面词
```

When handing to `$ai-video-prompt-director`, include:

```text
upstream_source
director_contribution_packet
visual_helpfulness_targets
prompt_direction: first_frame_motion / dialogue_coverage / product_motion / reference_continuity / local_edit / multi_shot_omni / quick_motion_test
首帧来源
scene_continuity_lock
background_continuity_lock
coverage_role
screen_direction / eyeline
background_side
project-style-lock 压缩句
mother_library_translation 的视频安全压缩句
主动作
主镜头运动
空间路径
遮挡/衔接方式
结束画面
complexity_mode and per-shot/stage motion intent
ending_behavior
禁止项按镜头意图确定；连续镜头禁止无动机跳切，多镜头保留有动机的切换
```

For dialogue, confrontation, reaction, interrogation, or over-shoulder coverage, set `prompt_direction: dialogue_coverage` and preserve:

```text
coverage_role
eyeline_direction
screen_direction
background_side
foreground_shoulder_or_object
edit_motivation
```

Do not turn long dialogue into generated mouth-sync unless explicitly requested. For normal short-drama video, describe restrained performance, breath, eye movement, hand tension, and reaction timing; subtitles and exact spoken words belong in post.

For video handoff, propose `ending_behavior` from the scene edit intent: hold, breath_light, breath_heavy, hard_cut, action_exit, or loop. Breath tails are optional dramatic choices and must fit the duration; do not append them to every shot. The video prompt owner checks feasibility and the platform auditor compiles the choice.

If upstream_source is missing for a formal project, do not move directly to final prompts. Route back to reference-image-style-matcher, style-reference-director, scene-style-map-director, shot-language-auditor, style-bible-director, or project-style-lock as appropriate.

For managed projects, also preserve the state path or packet source in `upstream_source`, such as `project-manifest.json -> references/scene-map.md -> style-lock.json`. Do not rely on a single project-specific prompt file as the source of truth for future short-drama projects.

## AI Risk Rules

- More than two speaking characters in one frame increases consistency risk.
- Long readable text usually belongs in post. Preserve explicitly requested generated dialogue and route native audio/lip-sync feasibility to the video prompt owner instead of silently removing it.
- Screens, phones, documents, monitors, case files, and court signs should not contain readable long text.
- Complex fights, crying, kissing, crowds, and hand-object interaction need simplified shots.
- Preserve character identity over fancy camera movement.
- Match coverage to the chosen frame and scene: 16:9 can carry lateral two-shots and spatial action; 9:16 needs attention to shoulder occlusion, vertical depth and readable faces. Neither format mandates a sequence of close-ups.
- For same-scene coverage, missing scene_continuity_lock, background_continuity_lock, camera axis, eyeline direction, background side, or wide/master inheritance is a workflow gap, not a prompt-writing detail.
- Missing applicable source, reference, continuity or director decisions must be resolved before final execution. Still-image handoffs do not require motion, ending or audio fields; camera/realism controls are profile-specific.

## Quality Bar

A good scene visual reference should let the user understand:

- 这场戏为什么长这样
- 和上一场有什么区别
- 和全剧风格为什么仍然统一
- 哪些参考图该被继承
- AI 最容易翻车的地方在哪里
- 后续出图和出视频怎么接

If this is not clear, do not move directly to final prompts.
