---
name: reference-visual-library
description: Curated visual reference library for film AI workflows. Use when selecting top-tier film, prestige series, TVC, documentary, stage, LED, brand-film, or short-drama aesthetic references before style-bible creation or prompt writing. Provides separate commercial/promo and narrative/short-drama reference tracks plus shared elite cinematography anchors.
---

# Reference Visual Library

## Core Role

`$reference-visual-library` is the curated reference source for visual taste and the source of reusable visual mechanisms.

It does not write final prompts. It selects reference systems and converts them into usable aesthetic principles before `$reference-aesthetic-director`, `$style-bible-director`, `$frame-vision-director`, and `$ai-video-prompt-director` do execution work.

The mother library must not remain a passive name list. For formal work it must produce a `mother_library_application_packet` that downstream skills can inherit and audit.

For formal work it must also preserve its contribution inside `director_contribution_packet`, so downstream prompt directors can see exactly which visual controls came from the mother library instead of replacing them with generic style words.

Use it when:

- The user wants stronger cinematic taste.
- A formal project needs reference films, TVC, documentary, stage, or short-drama direction.
- A script, storyboard, or client brief needs a visual reference system.
- The workflow needs to separate commercial/promo aesthetics from short-drama/story aesthetics.

## Library Structure

Use one skill with three reference layers:

```text
references/shared-elite-cinematography.md
references/commercial-promo-library.md
references/domestic-brand-tvc-case-library.md
references/short-drama-story-library.md
references/workflow-contracts.md
```

Do not use one generic reference list for all projects.

For formal workflow handoff fields, use:

```text
references/workflow-contracts.md
```

This contract defines `project_intake_packet`, `upstream_handoff_packet`, `style_lock_packet`, `audited_prompt_packet`, `generation_ready_packet`, and `qc_feedback_packet`. These packets keep upstream decisions visible across routing, prompt writing, audit, generation, QC, and revision.

## Reverse Matching From Reference Images

When the user provides reference images and asks for a similar or same-level style, do not choose references only from memory.

Use `$reference-image-style-matcher` first:

```text
reference image
-> visible feature analysis
-> closest library family
-> cinematography anchor
-> prompt translation rules
```

The library remains the source of truth, but the matcher is the task-facing image analysis layer. The result must state:

- what the reference image controls
- which library family it is closest to
- which cinematography anchor supports it
- what can be borrowed
- what must not be copied
- what downstream prompts must preserve

## Routing

| Project type | Reference file |
| --- | --- |
| 品牌片 / 企业宣传片 / 城市片 / 招商片 / 形象片 | `references/commercial-promo-library.md` |
| TVC / 产品广告 / 品牌广告 / 社媒广告 | `references/commercial-promo-library.md` |
| 小米 / 海尔 / 美的 / 华为 / 海信 / 格力等国内品牌TVC案例记录 | `references/domestic-brand-tvc-case-library.md` |
| 活动开场 / LED大屏 / 舞美 / 节目包装 | `references/commercial-promo-library.md` |
| 短剧 / 微短剧 / 竖屏剧情 / 悬疑 / 家庭 / 情感 / 复仇 | `references/short-drama-story-library.md` |

Mandatory cinematography layer:

```text
All formal image/video prompt workflows must also use:
references/shared-elite-cinematography.md
```

Commercial/promo projects use:

```text
commercial-promo-library.md + shared-elite-cinematography.md
```

Domestic product, smart-home, appliance, phone, vehicle, and export-market TVC projects may also use:

```text
domestic-brand-tvc-case-library.md
```

The domestic TVC case library is a lookup and translation layer. It must not become final prompt name-dropping. Use it to choose case mechanisms such as product clarity, family-emotion appliance storytelling, function visualization, export-market rhythm, or anti-AI product preservation.

Short-drama/story projects use:

```text
short-drama-story-library.md + shared-elite-cinematography.md
```

## Required Output When Used

| Item | Selection |
| --- | --- |
| 主参考体系 | 选择一个主参考，不堆名片 |
| 辅助参考体系 | 最多两个辅助参考 |
| 顶级摄影锚点 | 必选一个摄影/导演视觉锚点，并转译成镜头、光线、构图语言 |
| 可借鉴视觉原则 | 镜头、光线、色彩、材质、节奏、构图 |
| 不照搬内容 | 明确不能复制的剧情、商标、人物、版权元素 |
| 禁止漂移 | 明确不能变成的廉价风格 |
| 给下游skill的输入 | 可直接交给 `$reference-aesthetic-director` 的风格机制 |

## Mother Library Application Packet

For formal projects, output this packet whenever the library is used:

```text
mother_library_application_packet
library_route: commercial-promo-library / domestic-brand-tvc-case-library / short-drama-story-library / shared-elite-cinematography
project_function:
primary_reference_family:
secondary_reference_family:
cinematography_anchor:
why_this_family_fits:
borrowed_mechanisms:
  camera_distance:
  lens_psychology:
  light_source_direction:
  space_relation:
  composition_blocking:
  color_boundary:
  material_texture:
  rhythm_or_editing:
  performance_state:
scene_function_rules:
  scene_or_chapter:
  mother_library_mechanism:
  must_preserve:
  may_vary:
do_not_copy:
forbidden_drift:
prompt_inheritance:
  image_prompt_must_include:
  video_prompt_compact:
  platform_risk_controls:
owner_skill: reference-visual-library
next_skill: reference-aesthetic-director / scene-style-map-director
```

Director contribution handoff:

```text
director_contribution_packet
owner_skill: reference-visual-library
decision_owned: curated mother-library route and cinematography anchor
visual_controls_contributed: camera distance / lens psychology / light direction / space relation / composition blocking / color boundary / material texture / performance state / AI risk
downstream_must_preserve: prompt inheritance fields as visible controls
```

Strength rule:

```text
项目级母库 = 决定真实度、摄影纪律、色彩边界、材质可信度、禁用漂移
场戏级母库 = 决定每场的光源、空间关系、焦段心理、构图调度、表演状态
镜头级母库 = 只继承可见机制，不在最终提示词里堆片名/导演名/长说明
```

Downstream prompts should not quote the mother library as a reference list. They should inherit the packet's light, lens, space, color, material, performance, and risk-control mechanisms.

## Rules

- Choose references by project type, scene function, and audience, not by famous names alone.
- Use global top-tier cinema, prestige series, elite TVC, documentary, and stage references as the visual standard.
- Do not use low-quality domestic web-film, cheap short-drama, generic idol-drama, or weak corporate-video aesthetics as reference standards.
- Chinese cultural, historical, and location references may inform subject matter, but not replace top-tier visual discipline.
- Translate references into mechanisms: camera, lens, blocking, light source, color, texture, rhythm, and AI risk.
- Make the selected mother-library route strong enough to affect scene grouping, style-lock fields, prompt structure, and prompt-platform-auditor checks.
- Pick at most one primary reference system, one cinematography anchor, and one to two secondary systems for a project.
- Never put long reference lists directly into final AI prompts. Convert them into concise visual language first.
- The cinematography anchor is mandatory for formal image/video work because the user's expected baseline is top-tier cinematic taste.
