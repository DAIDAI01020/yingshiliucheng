---
name: style-reference-director
description: Project-level and scene-level style reference director for film AI workflows. Use when the user provides a script, storyboard, shot list, reference images, or named film/TVC/style references and needs a clear visual reference direction before style bible, scene style mapping, image prompts, or video prompts. Mandatory for formal projects before image/video prompt generation.
---

# Style Reference Director

## Core Role

`$style-reference-director` is the explicit front door for reference style decisions.

It does not write final image or video prompts. It reads the project material and selects a professional reference direction before downstream skills start execution.

It answers:

```text
这个项目应该参考哪一类顶级影视/TVC/纪录片/舞台视觉？
这些参考到底借鉴什么？
每场戏/章节应该怎么分配参考风格？
哪些东西绝不能照搬？
这些参考怎么转成镜头、焦段、摄影机、光线、色彩、材质、构图？
```

## Mandatory Use

For formal projects, use this skill before:

- `$reference-aesthetic-director`
- `$scene-style-map-director`
- `$style-bible-director`
- `$frame-vision-director`
- `$ai-video-prompt-director`

Do not jump directly from script/storyboard/reference images to Banana/Jimeng/Seedance prompts.

## Inputs

Use all available inputs:

| Input | Use |
| --- | --- |
| script / finished draft | identify story type, emotional logic, scene functions |
| storyboard / shot list | identify visual beats, shot priorities, scene grouping |
| reference images | assign roles and prevent averaging |
| user-named style references | validate and translate, not blindly copy |
| project type | choose commercial/promo or short-drama/story reference track |
| character or product references | protect continuity and visual anchors |

If the user gives incomplete inputs, still output the best available reference direction and state assumptions.

## Mother-Library Recommendation Rule

For formal short-drama, story, commercial, promo, TVC, event, or LED projects, the mother library is not forbidden. It is the professional taste source.

When the user has not named a style, proactively recommend:

```text
1 primary mother-library reference family
0-2 supporting references, each only if it solves a named scene, communication, or deliverable problem
1 top cinematography anchor
```

Use the expanded mother-library routes deliberately:

| Need | Preferred route |
| --- | --- |
| 电影化品牌片、正式叙事、历史、人文、城市、类型氛围 | `reference-visual-library/references/film-prestige-visual-library.md` |
| 商业KV、产品KV、发布会/活动主视觉、节目KV | `reference-visual-library/references/kv-key-art-case-library.md` -> `$kv-director` |
| 竖屏剧情、短剧冲突、连续场戏 | `reference-visual-library/references/short-drama-story-library.md` |
| 正式电影化实拍/生成 | add `reference-visual-library/references/shared-elite-cinematography.md` |

For graphic-only KV, pure typography, or abstract LED, use the applicable composition, material, typography, or stage/space anchor; do not force a cinematography reference. For a cinematic KV base image, combine one KV case mechanism with one film-world mechanism, then let `$kv-director` retain composition and safe-area authority.

When the user names a film, director, TVC, photographer, or visual style, validate whether it fits the project. If it fits, translate it. If it does not fit, say why and recommend a closer mother-library route.

For film/prestige research, presence on ShotDeck, awards, popularity, or a famous cinematographer is not enough. Apply `$reference-visual-library`'s ShotDeck-first quality gate, start with the `Core A` pool, and select at shot-mechanism level. Use `Specialist B` only when it solves a named gap. If the authenticated ShotDeck session was not actually inspected, return a search recipe instead of claiming a deck or shot match.

When the user provides reference images, inherit `$reference-image-style-matcher` first. Do not skip the mother-library recommendation just because a reference image exists.

Every recommendation must output two layers:

```text
母库推荐层：
主参考体系 / 0-2个有明确任务的辅助参考 / 适用锚点 / 适用原因 / 不适用部分

提示词转译层：
光线 / 空间 / 构图 / 焦段 / 色彩 / 材质 / 表演 / AI风险
```

For formal projects, also output or preserve:

```text
mother_library_application_packet
```

This packet makes the mother library an active production constraint. It must say how the selected reference family controls project DNA, scene function, and shot execution. It is not enough to name a film, director, TVC, or cinematographer.

The final downstream prompt must inherit the translated visual mechanism, not just the reference name.

Hard failure:

```text
用户没有给参考时，不主动推荐母库方向
只写“电影感、真实感、高级感、低饱和”
只堆电影名、导演名、摄影师名
没有说明为什么适合这部片/这场戏
没有把参考转译成光线、空间、焦段、构图、材质和表演
```

## Relationship To Other Reference Skills

Use this order:

```text
script/storyboard/reference images
-> reference-image-style-matcher（when reference images are provided）
-> style-reference-director
-> reference-visual-library
-> reference-aesthetic-director
-> scene-style-map-director
-> style-bible-director
-> frame-vision-director / ai-video-prompt-director
-> prompt-platform-auditor
```

Responsibilities:

| Skill | Role |
| --- | --- |
| `reference-visual-library` | curated source library, not the task-facing decision layer |
| `reference-image-style-matcher` | analyzes reference images and reverse-matches them to the curated mother library |
| `style-reference-director` | chooses and organizes the project/scene reference style |
| `reference-aesthetic-director` | translates chosen references into deeper visual principles |
| `scene-style-map-director` | distributes the chosen style across scenes/chapters |
| `style-bible-director` | locks continuity rules |

## Reference Image Reverse Matching Rule

If the user provides one or more reference images in a formal project, first inherit the result from `$reference-image-style-matcher`.

Do not jump from a reference image directly to prompt writing. The style decision must include:

```text
参考图视觉解析
母库匹配方向
顶级摄影锚点
可借鉴机制
不照搬内容
AI风险
```

Use the matcher result as evidence. If the matcher says confidence is low, present the closest 2-3 routes instead of pretending the reference is an exact match.

## Output 1: 项目级风格参考表

Always output this first for formal projects.

| 项目类型 | 主参考体系 | 辅助参考 | 顶级摄影锚点 | 适用原因 | 可借鉴机制 | 不适用部分/不照搬内容 | 转译后的画面机制 | AI风险 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Rules:

- `主参考体系`: one primary reference family only.
- `辅助参考`: zero to two, only when they solve a specific visual problem.
- `顶级摄影锚点`: mandatory; choose one cinematography/director visual anchor.
- `适用原因`: explain why this reference mechanism fits this project/scene, not just why it is famous.
- `可借鉴机制`: must include camera/lens/light/color/material/composition.
- `不照搬内容`: no copied frames, logos, celebrities, protected production design, exact composition.
- `转译后的画面机制`: must be a prompt-ready sentence containing light, space, lens, composition, color, material, performance, and AI risk.
- `AI风险`: explain likely generation failures.

After this table, output a compact `mother_library_application_packet` with:

```text
library_route
project_function
primary_reference_family
cinematography_anchor
borrowed_mechanisms
scene_function_rules
do_not_copy
forbidden_drift
prompt_inheritance
```

Also output a compact director contribution packet:

```text
director_contribution_packet
owner_skill: style-reference-director
decision_owned: project/scene reference direction and mother-library application
visual_controls_contributed: light / space / lens / composition / color / material / performance / AI risk
downstream_must_preserve:
must_not_be_overwritten_by: frame-vision-director / ai-video-prompt-director / prompt-platform-auditor
```

## Output 2: 场戏/章节风格参考表

Use for scripts, storyboards, multi-scene projects, short dramas, promo chapters, TVC sequences, event openers, or LED films.

| 场戏/章节 | 叙事功能 | 母库应用机制 | 参考风格 | 摄影锚点转译 | 光线 | 色彩 | 材质 | 构图/焦段 | 后续提示词要求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Rules:

- Every scene/chapter may have a different visual mechanism.
- Every scene/chapter must still belong to the same project DNA.
- Explain why the scene is visually different.
- Explain what downstream image/video prompts must preserve.

## Commercial / Promo Logic

Use for brand films, corporate films, city films, TVC, product ads, event openers, LED, and social cutdowns.

Typical scene/chapter functions:

```text
品牌开场、历史源起、工程制造、人物劳动、产品清晰、城市规模、服务网络、未来愿景、活动仪式、落版
```

Reference standards:

```text
Apple / Nike / Wieden+Kennedy / Mercedes / Porsche / BMW
BBC / Netflix / National Geographic documentary
Guinness Surfer / Honda Cog
Moment Factory / Es Devlin / Olympic-scale stage visuals
```

## Short Drama / Story Logic

Use for short drama, micro-series, vertical drama, suspense, romance, family, revenge, and character-driven narratives.

Typical scene functions:

```text
开场钩子、报案/求助、对质、审讯、监控/手机/文件、闪回、犯罪现场、情绪崩溃、反转、收束
```

Reference standards:

```text
Fincher / Mindhunter / Prisoners / Zodiac / True Detective
The Night Of / Mare of Easttown / A Separation / Kore-eda
Park Chan-wook / Decision to Leave / Bong Joon-ho / Wong Kar-wai
```

## Reference Image Role Rule

Every reference image must be assigned a narrow role:

```text
人物脸 / 发型 / 服装 / 动作姿态 / 场景空间 / 光线 / 色调 / 构图 / 材质 / 道具
```

Also specify what not to inherit:

```text
不继承背景 / 不继承人物脸 / 不继承文字 / 不继承logo / 不继承色调 / 不继承构图
```

Never average multiple reference images into a vague result.

## Hard Rejection Rules

Reject these as style reference output:

```text
只写电影感/高级感/真实感
只写奥斯卡感/大片感/纪录片感
只堆电影名、导演名、摄影师名
每个镜头随便换一个大师
没有说明景别、焦段、摄影机、光线、色彩、材质、构图
没有说明每场戏为什么不同
没有说明如何仍属于同一项目
```

## Downstream Handoff

When handing off to `$reference-aesthetic-director`, include:

```text
项目类型
主参考体系
辅助参考
顶级摄影锚点
可借鉴机制
禁止照搬
AI风险
```

When handing off to `$scene-style-map-director`, include:

```text
全片/全剧统一DNA
mother_library_application_packet
场戏/章节参考风格
每场戏为什么不同
每场戏必须继承的摄影锚点
参考图角色
后续提示词要求
```
