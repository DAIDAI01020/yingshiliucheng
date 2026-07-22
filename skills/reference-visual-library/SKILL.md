---
name: reference-visual-library
description: Curated visual mother library for film AI workflows. Use when selecting and translating top-tier film, prestige-series, TVC, documentary, brand-film, KV, key-art, stage, LED, or short-drama references before style locking or prompt writing. Provides separately searchable film/prestige, commercial, domestic TVC, narrative, KV/key-art, and cinematography tracks without copying protected frames or campaign layouts.
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

Use one skill with focused progressive-disclosure reference layers:

- [Film and prestige visual mother library](references/film-prestige-visual-library.md)
- [KV and key-art case mother library](references/kv-key-art-case-library.md)
- [Shared elite cinematography anchors](references/shared-elite-cinematography.md)
- [Commercial and promo library](references/commercial-promo-library.md)
- [Domestic brand TVC case library](references/domestic-brand-tvc-case-library.md)
- [Short-drama and story library](references/short-drama-story-library.md)
- [Workflow contracts](references/workflow-contracts.md)

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

## ShotDeck-First Film Research

For formal film/prestige reference research, use the quality gate and query protocol in [film-prestige-visual-library.md](references/film-prestige-visual-library.md). When the user has an authenticated ShotDeck session and asks for shot research, use it as a shot-level search and deck-building interface. Search by function, framing, lighting, color, composition, location, material, performance emotion, and relevant camera/lens attributes—not only by title.

Never treat “present on ShotDeck” as automatic mother-library admission. Prefer `Core A`; use `Specialist B` only for a named gap. New titles stay outside production recommendations until scored and verified. If ShotDeck was not actually inspected, output a `shotdeck_search_recipe` and set `shotdeck_status: search_recipe_only`; never fabricate shot links or a completed deck.

ShotDeck images remain research/reference material. Store deck/shot links and analysis, not the images as final commercial assets.

## Routing

| Project type | Reference file |
| --- | --- |
| 电影化品牌片 / 正式叙事片 / 高端剧集感 / 历史 / 城市 / 人文 / 类型氛围 | `references/film-prestige-visual-library.md` |
| 品牌片 / 企业宣传片 / 城市片 / 招商片 / 形象片 | `references/commercial-promo-library.md` |
| TVC / 产品广告 / 品牌广告 / 社媒广告 | `references/commercial-promo-library.md` |
| 小米 / 海尔 / 美的 / 华为 / 海信 / 格力等国内品牌TVC案例记录 | `references/domestic-brand-tvc-case-library.md` |
| 品牌KV / 产品KV / 发布会KV / 活动主视觉 / 节目KV / 电影化商业底图 | `references/kv-key-art-case-library.md` + `$kv-director` |
| 活动开场 / LED大屏 / 舞美 / 节目包装 | `references/commercial-promo-library.md` |
| 短剧 / 微短剧 / 竖屏剧情 / 悬疑 / 家庭 / 情感 / 复仇 | `references/short-drama-story-library.md` |

Mandatory cinematography layer:

```text
All formal cinematic/live-action image and video workflows must also use:
references/shared-elite-cinematography.md
```

Pure typography, graphic-only KV, abstract LED, and layout-led work use the appropriate composition, material, typography, or stage/space anchor instead of forcing a cinematography reference.

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

Broader film/prestige projects use:

```text
film-prestige-visual-library.md + shared-elite-cinematography.md
```

Commercial KV and key-art projects use:

```text
kv-key-art-case-library.md
-> kv-director/references/kv-composition-style-library.md
-> composition, safe-area, crop, extension, and asset-split decisions
```

If a KV needs cinematic live-action base art, add `film-prestige-visual-library.md` and `shared-elite-cinematography.md`. The KV case library supplies proven system mechanisms; `$kv-director` retains composition and communication-hierarchy authority.

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
library_route: film-prestige-visual-library / kv-key-art-case-library / commercial-promo-library / domestic-brand-tvc-case-library / short-drama-story-library / shared-elite-cinematography
reference_selection_mode: project_dna / scene_function / kv_system / cinematography_anchor
project_function:
primary_reference_family:
secondary_reference_family: none / one / two, each tied to a named problem
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
shotdeck_status: inspected / search_recipe_only / not_required
shotdeck_deck_or_shot_links: []
shotdeck_search_recipe:
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
- Film/prestige recommendations default to the curated Core A pool and require shot-level mechanisms; title fame, awards, or ShotDeck presence alone never qualifies an entry.
- Use global top-tier cinema, prestige series, elite TVC, documentary, and stage references as the visual standard.
- Do not use low-quality domestic web-film, cheap short-drama, generic idol-drama, or weak corporate-video aesthetics as reference standards.
- Chinese cultural, historical, and location references may inform subject matter, but not replace top-tier visual discipline.
- Translate references into mechanisms: camera, lens, blocking, light source, color, texture, rhythm, and AI risk.
- Make the selected mother-library route strong enough to affect scene grouping, style-lock fields, prompt structure, and prompt-platform-auditor checks.
- Pick at most one primary reference system, one cinematography anchor, and one to two secondary systems for a project.
- For KV, pick one primary case mechanism and at most two supporting mechanisms, then let `$kv-director` own composition mode, title/logo safe area, crop behavior, and extension logic.
- Never put long reference lists directly into final AI prompts. Convert them into concise visual language first.
- The cinematography anchor is mandatory for formal cinematic/live-action image and video work because the user's expected baseline is top-tier cinematic taste; do not force it onto pure typography, graphic-only KV, or abstract LED work.

## Library Maintenance

After adding or changing film/KV entries, run:

```powershell
python scripts/validate_reference_library.py
```

The validator enforces ordered IDs, minimum library depth, required mechanism/prompt/do-not-copy/source fields, direct routing links, and the agent metadata contract.
