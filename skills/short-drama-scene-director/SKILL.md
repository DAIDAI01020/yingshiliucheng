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

For formal projects, do not create or approve `references/scene-map.md` unless it inherits:

```text
hook_audit_packet
character_continuity_packet
style_lock_packet
mother_library_application_packet
```

Use when the user provides:

- 已有剧本
- 已有分镜
- 场次表
- 参考图
- 影视风格参考
- 需要拆成出图/视频镜头
- 需要每场戏先给风格参考

## Scene Merging Rules

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

## Required Output 2A: Same-Scene Continuity Lock

When several shots share the same location, light, character blocking, or conversation beat, create one `scene_continuity_lock` before writing shot prompts. This is mandatory for master wide, two-shot, reverse-angle, over-shoulder, eye contact, reaction shot, interrogation, confrontation, dining-table dialogue, office dialogue, living-room dialogue, or any same-scene coverage.

```text
scene_continuity_lock
scene_id
space_geography
time_and_light
color_material
prop_anchor
character_blocking
screen_direction
camera_axis
background_side_map
background_continuity_lock
lens_family
wide_master_rule
forbidden_drift
```

For dialogue or confrontation scenes, also output:

```text
dialogue_coverage_packet
coverage_type
coverage_role
source_scene_continuity_lock
character_visible
foreground_shoulder_or_object
eyeline_direction
background_side
shot_size
camera_position
focal_length_logic
edit_motivation
handoff_to_prompt
```

For formal same-scene coverage, create or request one `short_drama_scene_continuity_board` before batch image/video generation when background drift would be costly.

```text
scene_continuity_lock + background_continuity_lock + dialogue_coverage_packet
-> scene-board-image-prompter short_drama_scene_continuity_board
-> frame-vision-director / ai-video-prompt-director uses the board as scene/background reference
-> image/video QC checks generated outputs against the board
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
jimeng_seedance_motion_rule
breath_tail_rule
禁止跳切/换景/多动作
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

For video handoff, mark breath_tail_rule at two levels:

```text
每个镜头：轻气口，动作/台词后保留约0.5-1秒呼吸、眼神停顿和轻微余动作。
每一段/场戏/情绪落点结尾：重气口，保留约1-2秒，人物不再说新台词，只保留呼吸、眼神和情绪余韵。
```

If upstream_source is missing for a formal project, do not move directly to final prompts. Route back to reference-image-style-matcher, style-reference-director, scene-style-map-director, shot-language-auditor, style-bible-director, or project-style-lock as appropriate.

For managed projects, also preserve the state path or packet source in `upstream_source`, such as `project-manifest.json -> references/scene-map.md -> style-lock.json`. Do not rely on a single project-specific prompt file as the source of truth for future short-drama projects.

## AI Risk Rules

- More than two speaking characters in one frame increases consistency risk.
- Long dialogue should be subtitles in post, not generated inside image/video.
- Screens, phones, documents, monitors, case files, and court signs should not contain readable long text.
- Complex fights, crying, kissing, crowds, and hand-object interaction need simplified shots.
- Preserve character identity over fancy camera movement.
- For vertical short drama, prioritize close-up, over-shoulder, two-shot, reaction shot, and controlled blocking.
- For same-scene coverage, missing scene_continuity_lock, background_continuity_lock, camera axis, eyeline direction, background side, or wide/master inheritance is a workflow gap, not a prompt-writing detail.
- Missing mother_library_translation, director_contribution_packet, visual_helpfulness_targets, platform_language_strategy, anti_ai_realism_rule, jimeng_seedance_motion_rule, breath_tail_rule, or upstream_source is a workflow gap, not a prompt-writing detail. Fix the upstream handoff before final prompts.

## Quality Bar

A good scene visual reference should let the user understand:

- 这场戏为什么长这样
- 和上一场有什么区别
- 和全剧风格为什么仍然统一
- 哪些参考图该被继承
- AI 最容易翻车的地方在哪里
- 后续出图和出视频怎么接

If this is not clear, do not move directly to final prompts.
