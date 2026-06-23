---
name: scene-style-map-director
description: Scene-level visual style mapper for film AI workflows. Use when the user provides a script, storyboard, shot list, reference images, or style references and needs each scene/location/time block to receive its own visual style direction while preserving the project's unified cinematic DNA. Works for short drama, brand film, promo film, TVC, event openers, and AI image/video prompt preparation.
---

# Scene Style Map Director

## Core Role

`$scene-style-map-director` sits after `$style-reference-director` and before prompt writing.

It reads scripts, storyboards, shot lists, reference images, and requested style references, then creates a scene-by-scene visual map:

```text
same project DNA
+ different scene/location/time/emotion visual strategy
+ prompt-ready camera/light/color/material rules
```

It prevents two common failures:

- Every scene looks identical because one global style was applied too literally.
- Every scene becomes a different film because references were assigned randomly.

## When To Use

Use this skill when:

- The user provides a script and asks for scene visual references.
- The user provides finished storyboards and wants Banana/Jimeng/Seedance prompts.
- Different scenes/locations should have different light, lens, color, or mood.
- The user provides reference images and asks what each one should control.
- A short drama has multiple locations, time periods, flashbacks, phone evidence, interrogation, home scenes, or confrontation scenes.
- A promo film has multiple chapters, such as history, factory, city, people, product, future, event opening, or LED sequence.

Do not use it for a single quick image unless the user asks for scene/style planning.

## Required Inputs

Use whatever is available only for `quick/test` work.

For quick/test work:

```text
create a lightweight scene map
mark it as quick/test
state missing upstream decisions
do not allow it to masquerade as formal batch execution
```

For formal projects, do not silently continue when required upstream decisions are missing. Mark the missing item and route back.

Required formal upstream:

```text
hook_audit_packet for formal short-drama projects
character_continuity_packet for formal short-drama projects with recurring characters
style-reference-director decision
mother_library_application_packet
reference-image-style-matcher result when reference images are used
project-style-lock or explicit instruction to create/update one after the map
shot-language-auditor result for short-drama or dramatic multi-shot work before final prompts
```

| Input | Use |
| --- | --- |
| script / finished draft | identify scene blocks, emotional beats, visual changes |
| storyboard / shot list | map lens, shot size, camera movement, keyframes |
| reference images | assign strict roles: character, location, lighting, composition, texture |
| reference films/TVC | convert into mechanisms, not copied frames |
| character bible | preserve face, wardrobe, emotional baseline |
| style bible | preserve project DNA |

If reference images are present, inherit `$reference-image-style-matcher` output before mapping scenes. The scene map must say which scene uses which matched reference mechanism and which parts of the image are not inherited.

## No Lazy Handoff Rule

`$scene-style-map-director` maps scene-level style. It does not invent project references, reference-image matches, style locks, or shot-language logic.

If formal scene mapping lacks hook-audit, character-continuity, style-reference, reference-image-match, project-style-lock, or shot-language inputs, output `待补上游项` and route back to the owning skill before downstream prompt writing.

## Scene Grouping Rule

Group shots into one scene style when they share:

- same location or continuous space
- same time and light source
- same emotional phase
- same evidence/clue/action function
- same visual symbol or object anchor
- same chapter of a promo film

Split into a new scene style when there is:

- location change
- day/night/weather/light-source change
- flashback, memory, phone/monitor/evidence mode, dream, news, court, stage, or graphic mode
- emotional intensity shift
- different visual function: hook, reveal, confrontation, collapse, proof, ritual, product reveal, final claim

## Output 1: Scene Style Map

Always output this before final prompts.

| 场戏 | 覆盖段落/镜头 | upstream_source | 场景功能 | 地点/时间 | 主体/人物 | 母库应用机制 | 本场风格机制 | mother_library_translation | 顶级摄影锚点转译 | 景别/焦段倾向 | 光线 | 色彩 | 材质 | 构图/调度 | 人物表演状态 | 参考图角色 | AI风险 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Field requirements:

- `本场风格机制`: describe how this scene should feel visually, not just an adjective.
- `upstream_source`: state which reference-image match, style-reference decision, style bible, project-style-lock, and shot-language result this scene inherits.
- `母库应用机制`: name the selected mother-library family and the exact scene function mechanism being used; do not use only a film/director name.
- `mother_library_translation`: light direction, space relation, lens psychology, composition blocking, material touch, performance state, and AI risk control.
- `顶级摄影锚点转译`: camera/light/composition language from the shared cinematography layer.
- `景别/焦段倾向`: specify lens logic, such as 35mm handheld proximity, 85mm compression, 100mm macro evidence detail.
- `光线`: practical source and direction, such as overhead fluorescent, window side light, sodium streetlight, sunset backlight.
- `色彩`: controlled palette, not vague “高级”.
- `材质`: visible tactile materials.
- `构图/调度`: foreground obstruction, negative space, over-shoulder, doorway, reflection, center-safe, low angle, etc.
- `人物表演状态`: restrained performance, gaze direction, breath, silence, hand tension, or emotional release.
- `参考图角色`: each reference must have a narrow role.
- `AI风险`: face drift, unreadable text, logo, hands, screen UI, plastic skin, cheap drama look, over-CG.

## Output 2: Scene-to-Prompt Handoff

For each scene that needs image prompts, hand off to `$frame-vision-director` with:

```text
upstream_source
director_contribution_packet
hook_audit_packet source
character_continuity_packet source
全片统一DNA
mother_library_application_packet id / selected rule
本场风格机制
mother_library_translation
顶级摄影锚点转译
platform_language_strategy
anti_ai_realism_rule
image_tool_boundary
人物/主体连续性
参考图角色
每个镜头的景别、机位、焦段、光圈/景深
光线、色彩、材质、构图
负面词风险
visual_helpfulness_targets: what the prompt must visibly improve or protect
```

For each scene that needs video prompts, hand off to `$ai-video-prompt-director` with:

```text
upstream_source
director_contribution_packet
首帧要求
character_continuity_packet source
scene_continuity_lock / background_continuity_lock when this is same-scene coverage
project-style-lock 压缩句
mother_library_application_packet video rule
mother_library_translation 的视频安全压缩句
主体动作
镜头运动
景别变化路径
焦段或镜头感
光线/环境变化
自然衔接方式
结束画面
jimeng_seedance_motion_rule
breath_tail_rule
禁止项
visual_helpfulness_targets: what the video prompt must visibly move, preserve, or protect
```

## Professional Rule: Different Scenes, Same Film

Every scene may vary:

```text
location, light source, color temperature, shot size, focal length, camera distance,
foreground obstruction, texture, emotional pressure, object symbol
```

But formal projects must keep:

```text
visual realism level, camera family, character continuity, color boundary,
skin texture, material credibility, reference discipline, forbidden drift
```

## Reference Image Role Rules

Never average multiple references.

For formal projects, reference image roles must come from or be checked against `$reference-image-style-matcher`:

```text
参考图视觉解析 -> 母库匹配 -> 场戏分配 -> 提示词转译
```

Assign each reference to one or more exact roles:

| Role | Meaning |
| --- | --- |
| character face | face shape, age, hairstyle only |
| wardrobe | clothing type, fabric, color anchor |
| location | space layout, architecture, wall/floor material |
| lighting | light direction, contrast, color temperature |
| composition | framing, foreground/background relationship |
| prop/material | object design, texture, wear, scale |
| mood only | atmosphere only, not content |

Also specify what not to inherit:

```text
不继承背景 / 不继承文字 / 不继承logo / 不继承人物脸 / 不继承色调 / 不继承构图
```

## Prompt Quality Gate

Do not allow a downstream image prompt unless each selected shot has:

```text
upstream_source + mother_library_translation + platform_language_strategy + anti_ai_realism_rule + image_tool_boundary + 景别 + 机位 + 构图 + 摄影机/影像系统 + 焦段 + 光圈/景深 + 光线 + 色彩 + 材质 + 比例 + 负面词
director_contribution_packet + visual_helpfulness_targets
```

Do not allow a downstream video prompt unless it has:

```text
upstream_source + jimeng_seedance_motion_rule + breath_tail_rule decision（每镜头轻气口；每段/场戏/情绪落点结尾重气口） + 首帧景别/机位 + 主体动作 + 镜头运动 + 焦段或镜头感 + 光线方向 + 色彩边界 + 材质/空间质感 + 结束画面
director_contribution_packet + visual_helpfulness_targets
```

If a formal scene map cannot identify upstream_source or mother_library_translation, route back to `$style-reference-director` / `$reference-image-style-matcher` before final prompt writing. If shot function or edit motivation is missing, route through `$shot-language-auditor`.

For formal short-drama work, also route back before prompt writing when the scene map cannot identify:

```text
hook_audit_packet
character_continuity_packet
scene_continuity_lock / background_continuity_lock for same-scene coverage
```

## Rejection Rules

Reject these as scene style maps:

```text
每场都写电影感/高级感/真实感
只写片名或导演名
每个镜头随便换一个大师参考
只写景别和焦段，没有光线和构图
只写统一风格，不解释本场戏为什么不同
提示词靠 live-action cinematic documentary still 这种模板撑住
```

## Default Pipeline Position

```text
script/storyboard/reference images
-> style-reference-director
-> reference-visual-library
-> reference-aesthetic-director
-> scene-style-map-director
-> style-bible-director
-> frame-vision-director / ai-video-prompt-director
-> prompt-platform-auditor
-> generation
```
