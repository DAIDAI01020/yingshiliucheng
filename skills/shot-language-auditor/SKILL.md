---
name: shot-language-auditor
description: Audit cinematic shot logic for short drama, storyboard, promo, image prompt, and video prompt workflows. Use when writing or reviewing shot lists, 15s/30s short-drama sequences, scene breakdowns, keyframe plans, or video prompts to verify shot-size progression, camera angle, focal length, edit motivation, screen direction, spatial clarity, vertical framing, and whether each shot has a narrative function instead of random cinematic-looking coverage.
---

# Shot Language Auditor

## Core Role

`$shot-language-auditor` checks whether a shot sequence has real film language.

It does not choose the visual style. It audits:

```text
景别是否有递进
机位是否有理由
焦段是否匹配心理距离
剪辑点是否有动机
人物视线和空间关系是否清楚
竖屏/横屏构图是否可读
每个镜头是否有叙事功能
```

If the sequence is only a random list of CU/MS/ECU shots, reject it.

## When To Use

Use before finalizing:

- short-drama shot lists
- 15s/30s dramatic sequences
- storyboard tables
- image keyframe plans
- video prompt beats
- one-take or pseudo one-take designs
- user-provided storyboards that need professional tightening

## Required Shot Logic

Every shot must have one primary function:

| Function | Meaning |
| --- | --- |
| 建立空间 | show where people are and who controls the space |
| 建立关系 | show who is facing whom, who has power, who is isolated |
| 推进动作 | show a physical action that changes the scene |
| 揭示信息 | show object, evidence, message, expression, or spatial reveal |
| 压迫情绪 | move closer or compress space to increase pressure |
| 反应 | show how a character receives new information |
| 转场 | create a motivated bridge through action, gaze, object, sound, or occlusion |

Reject shots with no function.

## Shot Size Progression Rules

Reasonable 15s short-drama default:

```text
MS / WS 建立空间或关系
-> MCU / CU 压迫人物
-> ECU 物证、手机、手、眼神、关键细节
-> OTS / MCU 反应或对峙
-> CU / WS 反转、收束或空间压迫
```

Rules:

- Do not start with repeated close-ups unless the opening hook is an object/evidence hook.
- Do not use three or more similar close-ups in a row without changing information.
- Use ECU only for story information: eyes, hands, phone, photo, file, lock, blood trace, ring, weapon, document edge, key object.
- Use WS/EWS sparingly in vertical short drama; only for location, isolation, threat, or final pressure.
- Every jump in shot size must have motivation.

## Same-Scene Coverage Rules

For same-location dialogue, confrontation, eye contact, reverse-angle, over-shoulder, interrogation, argument, dining-table, living-room, or office conversation, audit the sequence as one coverage group instead of isolated pretty shots.

Require a `scene_continuity_lock` or equivalent:

```text
space_geography
time_and_light
prop_anchor
character_blocking
screen_direction
camera_axis
background_side_map
background_continuity_lock
lens_family
wide_master_rule
```

Reject or rewrite if:

```text
A and B swap left/right without motivated crossing
A looks the wrong direction in the reverse shot
both characters look the same direction during supposed eye contact
background behind A and B randomly changes
props jump positions between master wide and close coverage
OTS foreground shoulder belongs to the wrong character
reverse angles use unrelated lens families or lighting logic
```

For formal batch work, recommend a `short_drama_scene_continuity_board` when background drift would be costly.

## Edit Motivation Rules

Each cut must be motivated by at least one:

| Motivation | Example |
| --- | --- |
| 视线接 | character looks at phone -> phone close-up |
| 动作接 | hand reaches door lock -> lock close-up |
| 声音接 | message tone -> screen or reaction |
| 物件接 | file opens -> document detail |
| 情绪接 | line lands -> other character reaction |
| 遮挡接 | body passes lens -> new angle |
| 空间接 | doorway/window/glass leads viewer into the next shot |

Reject a sequence if cuts are only decorative.

## Focal Length Logic

| Need | Recommended logic |
| --- | --- |
| spatial setup | 24mm-35mm, readable geography, avoid distortion unless intentional |
| two-person confrontation | 35mm-50mm, over-shoulder or blocked two-shot |
| emotional pressure | 65mm-85mm, compressed background, face readable |
| evidence/detail | 85mm-100mm macro, shallow depth, one object only |
| one-take movement | 24mm-35mm, clear path, avoid chaotic lens changes |
| vertical close drama | 50mm-85mm equivalent, face and hands readable |

Reject focal lengths that fight the shot's function.

## Output: Shot Language Audit Table

| 镜号 | upstream_source | 原景别/机位 | 镜头功能 | 是否合理 | 问题 | 建议调整 | 剪辑动机 | handoff_to_prompt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

`handoff_to_prompt` must tell `$frame-vision-director` / `$ai-video-prompt-director` what to preserve:

```text
shot function + edit motivation + lens psychology + scene_continuity_lock + background_continuity_lock + coverage_role + screen_direction + background_side + required end state + whether this shot needs image keyframe, video motion, or split execution
```

Also output:

```text
director_contribution_packet
owner_skill: shot-language-auditor
decision_owned: shot function, edit motivation, coverage role, screen direction, continuity locks, split recommendation
visual_controls_contributed: shot size, camera angle, focal length logic, blocking, eyeline, background side, required end state, breath tail level
downstream_must_preserve: handoff_to_prompt, scene_continuity_lock, background_continuity_lock, edit_motivation, coverage_role, screen_direction

visual_helpfulness_targets
visible subject/action change, motivated camera path, readable spatial relation, protected background continuity, ending frame state
```

Decision values:

```text
通过
调整景别
调整顺序
删除冗余镜头
补建立镜头
补反应镜头
拆成两段
```

## Output: Corrected Shot Flow

When the original sequence is weak, output a corrected flow:

| 镜号 | 时长 | 景别 | 机位/焦段 | 画面内容 | 镜头功能 | 与上一镜衔接 | handoff_to_prompt |
| --- | --- | --- | --- | --- | --- | --- | --- |

For short-drama video, every corrected flow must also mark:

```text
是否适合一个主体动作
是否适合一个镜头运动
是否需要轻气口：每个镜头都需要，动作/台词后约0.5-1秒
是否需要重气口：每一段/场戏/情绪落点结尾需要，约1-2秒
是否建议拆段
```

## Hard Rejection Rules

Reject or rewrite:

```text
连续多个特写但没有新信息
同场正反打没有 scene_continuity_lock
同场镜头没有 background_continuity_lock
正反打越轴或人物左右关系无故翻转
对视镜头眼神方向不成立
同一场景的背景侧、道具位置、光源方向随机变化
只写景别和焦段，没有镜头功能
从大全景硬切极特写但没有视线/动作/声音/物件动机
角色关系不清楚
空间方向混乱
竖屏里频繁大全景导致信息不可读
为了电影感而写无意义空镜
15s里镜头过多导致AI视频不可控
```

## Downstream Handoff

For `$short-drama-scene-director`:

```text
director_contribution_packet
visual_helpfulness_targets
scene function
scene_continuity_lock
background_continuity_lock
coverage_role
shot function
shot-size progression
edit motivation
vertical readability risk
```

For `$frame-vision-director`:

```text
director_contribution_packet
visual_helpfulness_targets
each image prompt must preserve the shot function, not just style
handoff_to_prompt
scene_continuity_lock
background_continuity_lock
coverage_role
screen_direction
background_side
lens psychology
edit motivation
required end state
```

For `$ai-video-prompt-director`:

```text
director_contribution_packet
visual_helpfulness_targets
video prompt must keep one dominant camera move and one shot-size path
handoff_to_prompt
scene_continuity_lock
background_continuity_lock
coverage_role
screen_direction
background_side
jimeng_seedance_motion_rule
breath_tail_rule decision
split recommendation when one action/one camera move cannot hold the beat
```

Cross-skill management rule:

```text
If upstream_source is missing, state which upstream table or scene decision is missing.
Preserve upstream mother_library_translation, platform_language_strategy, and anti_ai_realism_rule as protected handoff context; do not rewrite them inside shot-language-auditor.
Preserve or create director_contribution_packet and visual_helpfulness_targets so downstream prompt skills cannot reduce shot logic to decorative camera labels.
If the shot has no function, no edit motivation, or cannot fit one subject action and one camera movement, do not let downstream prompt skills convert it into a final video prompt.
Every short-drama shot must mark breath_tail_rule as light breath tail unless the user explicitly requests a hard cut, beat cut, flash cut, or shock point.
If the shot ends a segment, scene, accusation, evidence reveal, phone/message reading, silent reaction, emotional realization, or confrontation, mark breath_tail_rule as heavy breath tail.
```

This skill does not choose visual style, but its handoff must protect the style pipeline by naming what downstream prompts must preserve.
