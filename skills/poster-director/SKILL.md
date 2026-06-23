---
name: poster-director
description: Poster and key-art visual director under zongkong for film AI workflows. Use when zongkong routes poster/KV work for creating or revising short-drama posters, film posters, character posters, suspense case posters, brand key visuals, event KV, program posters, social covers, thumbnails, banners, or any poster-like deliverable that needs layout-safe AI image prompts, title-safe composition, character hierarchy, no-text base art, layered visual assets, and handoff to frame-vision-director, prompt-platform-auditor, Canva, Photoshop, or manual typography/layout.
---

# Poster Director

## Core Role

`$poster-director` is a specialist director under `$zongkong`. It turns a film, short-drama, promo, brand, event, or program brief into a poster/key-art direction after `$zongkong` has identified poster/KV mode.

Do not use it as a top-level production orchestrator. `$zongkong` decides project tier, route, upstream style requirements, and whether poster/KV mode is needed; `$poster-director` only handles poster communication, layout logic, and poster image-prompt handoff.

It does not treat posters as ordinary keyframes. A poster is a communication object:

```text
who/what is being sold + one visual hook + readable hierarchy + title-safe layout + platform-safe assets
```

Use this before final poster image generation, Canva layout, Photoshop layout, pitch-deck poster pages, or social cover adaptation.

## Workflow Position

Default route:

```text
$zongkong（top-level route decision）
-> brief/script/storyboard/style lock
-> poster-director
-> frame-vision-director
-> prompt-platform-auditor
-> image generation
-> image-qc-director
-> layout/post typography/Canva/Photoshop
```

For formal short-drama or promo projects, inherit:

```text
upstream_source
project-style-lock
mother_library_translation
platform_language_strategy
anti_ai_realism_rule
image_tool_boundary
reference image roles
character/product continuity
```

If these are missing in a formal project, do not jump straight to poster prompts. Route back to the appropriate style/reference skill first.

## Poster Type Decision

Choose one poster route before writing image prompts:

| Type | Use when | Visual priority |
| --- | --- | --- |
| 主海报 / key art | main project poster, pitch cover, platform key visual | one memorable conflict/hook, title-safe central layout |
| 人物海报 | one character or cast identity | face continuity, posture, costume anchor, clean name/title area |
| 关系海报 | short-drama love/revenge/family conflict | character hierarchy, eye-line tension, emotional distance |
| 悬疑案件海报 | crime, missing person, evidence, investigation | object clue, negative space, procedural tension, no cheap blue filter |
| 品牌 KV | brand film, launch, product, event | brand object/product clarity, slogan-safe area, premium material |
| 节目/栏目海报 | program promo, variety, campaign cover | host/cast hierarchy, readable category signal |
| 社媒封面/缩略图 | vertical cover, feed image, thumbnail | instant hook, clean face/object, safe crop at small size |
| Banner / 横版 | site header, deck cover, widescreen screen | wide negative space, center-safe subject, title/logo zone |

Do not output only `生成一张海报`. First decide the poster job.

## Poster Strategy

A good poster direction must state:

```text
传播目标
一句主视觉概念
观众第一眼看到什么
人物/产品/物件层级
冲突或卖点如何可视化
标题/文案/Logo安全区
主比例和延展比例
AI生成哪些素材，后期排哪些文字
```

For short drama, sell the hook:

```text
人物关系 + 秘密/反转/欲望/危险 + 一个可读物件或空间符号
```

For commercial/promo, sell trust or value:

```text
品牌/产品主体 + 使用场景/工程/人物/城市规模 + clean claim area
```

## Layout-Safe Composition Rule

Poster prompts must reserve typography space. Do not let the image fill every area with faces, hands, props, and high-detail texture.

Specify safe areas:

| Ratio | Default title-safe logic |
| --- | --- |
| 9:16 vertical | keep upper 18-25% or lower 18-25% clean for title; face/hero subject in middle third |
| 4:5 feed | keep top or bottom band clean; avoid key face too near crop edge |
| 1:1 square | center-safe subject, simple background, title band top/bottom |
| 16:9 / banner | subject left or right third, large negative space opposite for title/logo |
| event KV / LED | center-safe main object, large simple shapes, title and sponsor zone separated |

Use layout language inside the prompt:

```text
上方保留干净留字区 / 下方保留片名区 / 右侧留出海报标题负空间 / 背景不要出现可读文字
```

## Text And Logo Rule

Do not ask image models to generate final readable title, slogan, cast names, QR code, platform logo, legal line, or sponsor marks.

Default poster image generation should produce:

```text
无字主视觉底图
人物/产品/物件层级清楚
干净留字区
无水印、无logo、无乱码文字
```

If a design needs text, write:

```text
标题、Logo、标语、演员名、播出信息、二维码、平台标识由后期排版添加，不在AI图内生成。
```

Allowed AI text exceptions:

```text
blurred document texture
unreadable newspaper blocks
simple number-like mark
abstract sign shape with no readable copy
```

## AI Asset Decomposition

When the poster is important, do not force one generation to solve everything. Split into assets:

| Asset | Purpose |
| --- | --- |
| 无字主视觉底图 | final base art with title-safe layout |
| 人物主视觉 | face/body/costume continuity, transparent or clean background if needed |
| 背景氛围图 | scene texture, city/interior/case atmosphere |
| 物件特写 | evidence, product, symbol, clue, prop |
| 横竖版延展图 | same visual DNA adapted to 9:16, 4:5, 1:1, 16:9 |

For AI prompts, ask for the base art or asset, not a finished graphic design with generated typography.

## Reference And Style Inheritance

Formal poster work must inherit the project style system:

```text
project-style-lock
mother_library_translation
cinematography anchor
character/product continuity
anti_ai_realism_rule
platform_language_strategy
image_tool_boundary
```

For poster/key-art reference mechanisms, read `references/poster-key-art-reference-library.md` when:

```text
the user asks for a poster/KV/key art/cover route
the poster type is unclear
the poster needs professional layout-safe reference logic
the project needs short-drama platform cover, prestige series key art, film poster, brand KV, event KV, or social thumbnail guidance
```

Poster references can include:

```text
film key art
Netflix / Apple TV / HBO prestige series key art
short-drama platform covers
brand KV
event launch key visual
program poster
social thumbnail
```

Translate references into layout and visual mechanisms:

```text
negative space
subject hierarchy
face scale
eye-line tension
object symbolism
title-safe area
color boundary
material texture
AI risk control
```

Do not copy exact posters, celebrity faces, protected title treatments, logos, or distinctive layouts.

## Tool Strategy

| Tool | Poster use |
| --- | --- |
| built-in imagegen | natural-language base art, local edits, preserve original character/product image |
| Banana / Banana Pro | batch poster assets, compact prompts, multi-reference character/product control |
| Midjourney | exploratory style mood only when requested, not final continuity-critical character posters |
| Canva / Photoshop | typography, logo placement, final layout, social adaptation |

Formal poster/key-art still images default to built-in imagegen or Banana/Banana Pro. Do not route poster stills to Jimeng by default; use Jimeng for video motion or animated poster variants only.

## Output 1: Poster Direction Table

Use this first:

| Item | Decision |
| --- | --- |
| poster_type |  |
| audience/platform |  |
| main_ratio |  |
| extension_ratios |  |
| upstream_source |  |
| core_hook |  |
| subject_hierarchy |  |
| layout_safe_area |  |
| visual_symbol |  |
| style_inheritance |  |
| mother_library_translation |  |
| typography_plan | text added in post, not generated inside AI image |
| asset_split | base art / character / background / object / variants |
| AI risks | text gibberish, logo, face drift, hand errors, poster-template look, plastic skin |

## Output 2: Poster Prompt Handoff

For `$frame-vision-director`, include:

```text
upstream_source
poster_type
main_ratio and extension_ratios
無字主视觉底图目标
subject_hierarchy
layout_safe_area
visual_symbol
project-style-lock / master_style_sentence
mother_library_translation
cinematography anchor translation
character/product/reference image roles
anti_ai_realism_rule
platform_language_strategy
image_tool_boundary
negative prompt requirements
post typography plan
```

For `$prompt-platform-auditor`, require:

```text
no readable generated title/logo/slogan
title-safe negative space exists
poster subject hierarchy is clear
AI text/logo risk is controlled
formal project style lock is preserved
prompt matches built-in imagegen or Banana/Banana Pro language strategy
```

## Poster Prompt Formula

Use this structure for final image prompt drafts:

```text
[无字海报主视觉底图 / poster asset type] +
[主体层级：谁最大、谁次要、物件在哪里] +
[版式：标题安全区、负空间、裁切安全] +
[视觉钩子：冲突/秘密/产品/仪式/物件] +
[项目风格锁和母库转译] +
[摄影/光线/材质/色彩] +
[真实摄影反AI控制] +
[比例和延展要求] +
[禁止文字/logo/水印/乱码/塑料皮肤/模板海报感]
```

## Quality Gate

Do not approve a poster direction if:

```text
no poster_type
no core_hook
no subject hierarchy
no layout_safe_area
asks AI to generate final readable title/logo
ignores project-style-lock in a formal project
uses generic poster words only: cinematic poster, premium key art, dramatic, high-end
no asset_split for complex posters
no platform ratio or crop-safe plan
no anti-AI realism or text/logo risk control
```

## Handoff Rule

`$poster-director` plans poster communication and layout logic. `$frame-vision-director` writes generation-ready image prompts. `$prompt-platform-auditor` checks platform safety. Canva/Photoshop/post layout handles final typography.

Do not let one AI image prompt become the whole poster workflow.
