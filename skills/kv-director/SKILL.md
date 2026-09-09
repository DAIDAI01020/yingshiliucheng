---
name: kv-director
description: Commercial/event KV and key visual director under zongkong for film AI workflows. Use when zongkong routes commercial, brand, launch, product, program, event, conference, gala, LED, stage-screen, campaign, banner, or main visual requests that need a KV system, brand claim-safe composition, no-text base art, layered visual assets, extension ratios, and handoff to kv-image-prompt-director, prompt-platform-auditor, Canva, Photoshop, or manual layout. Do not use for short-drama character posters, film posters, social thumbnails, or poster-like narrative key art; route those to poster-director.
---

# KV Director

## Core Role

`$kv-director` is a commercial/event KV specialist under `$zongkong`. It turns a brand, launch, product, program, event, LED, campaign brief, or approved proposal into a composition-led, style-specific, layout-safe key visual system before final image prompts and post layout.

Do not use it as a top-level orchestrator. `$zongkong` decides project tier, main line, upstream style/reference requirements, and whether commercial KV mode is needed.

Use this skill for 品牌KV / 活动KV / 发布会KV / 产品上市主视觉 / 节目主视觉 / LED主视觉 / campaign KV / key visual / banner system.

Do not use it for 短剧人物海报 / 电影海报 / 悬疑案件海报 / 剧集key art / 社媒缩略图 / poster-like narrative cover.

Route those to `$poster-director`.

## Workflow Position

Default route: `$zongkong` -> brief / brand / event / product / program / LED upstream direction -> `$kv-director` -> `$kv-image-prompt-director` -> `$prompt-platform-auditor` -> image generation -> `$image-qc-director` -> Canva / Photoshop / manual layout / social or screen adaptation.

For formal commercial/promo projects, inherit:

```text
upstream_source
brand proposition / event theme / product claim
project-style-lock
mother_library_translation
cinematography anchor
product / logo / brand asset reference roles
anti_ai_realism_rule
platform_language_strategy
image_tool_boundary
```

If these are missing in a formal project, do not jump straight to KV prompts. Route back to the appropriate style/reference or specialist director.

## Approved Proposal To KV Route

When the user already has an approved proposal, PPT direction, creative concept, script direction, event theme, product-launch logic, or program package direction, inherit it. Do not restart brief analysis or invent a second concept.

Extract a `proposal_to_kv_packet`:

```text
proposal_source:
approved_theme:
core_claim:
target_audience_and_context:
approved_visual_symbols:
narrative_or_ceremony_arc:
brand_product_event_authority:
approved_colors_materials_and_tone:
required_title_logo_sponsor_content:
forbidden_drift:
master_kv_deliverables:
screen_kv_deliverables:
missing_fields:
```

The KV director owns the conversion from proposal logic into one static communication hierarchy, one visual hook, a composition system, a screen adaptation, and an asset split. It may simplify the proposal for readability, but it must not change the approved claim or visual DNA without saying so.

Route back only when the proposal cannot establish a clear claim, authority source, mandatory content, or deliverable. Missing decorative detail is not a reason to restart concept development.

## KV Type Decision

Choose one KV route before writing image prompts:

| Type | Use when | Visual priority |
| --- | --- | --- |
| 品牌KV | brand film, corporate image, campaign identity | brand proposition, trust, human/environment credibility |
| 发布会/活动KV | launch, conference, gala, forum, ceremony | theme reveal, ritual center, sponsor/title-safe hierarchy |
| 产品上市KV | product launch, product campaign, retail hero visual | product clarity, material truth, slogan-safe area |
| 节目主视觉 | program, variety, documentary, channel campaign | category signal, host/cast/product hierarchy |
| LED/舞美主视觉 | event screen, stage backdrop, immersive widescreen | distant readability, center-safe symbol, screen extension |
| Banner system | website, deck cover, social header, widescreen material | wide negative space, crop-safe subject, title/logo zone |

Do not output only `做一个KV`. First decide the KV job.

## KV Composition And Style Research Gate

Before writing any KV prompt handoff, `$kv-director` must decide both the composition system and the style system. A KV is not "one nice poster"; it is a visual system that must control attention, material, light, color, title relationship, crop behavior, and extensions.

For formal KV research, first use the mother library's [KV and key-art case mechanisms](../reference-visual-library/references/kv-key-art-case-library.md) when available. It supplies verified studio/case mechanisms and source traces. It does not decide the final layout.

Authority split:

```text
kv-key-art-case-library = case mechanism, why it fits, source trace, do_not_copy
kv-composition-style-library = composition and style archetype authority
kv-director = final hierarchy, safe area, crop, extension, asset split, and handoff
```

Select one primary case mechanism and at most two supporting mechanisms. Each supporting mechanism must solve a named problem such as product truth, event ritual, multi-screen extension, title safety, or multi-format consistency. Do not put studio names or campaign names into the final generation prompt.

Reading `references/kv-composition-style-library.md` is mandatory for every KV. It is the primary visual judgment library. `references/kv-reference-library.md` supplies category/reference mechanisms, while `references/large-screen-kv-experience-library.md` only adapts the approved visual system to physical screens.

When the user asks for a formal KV, event KV, launch KV, main visual, LED main visual, stage screen, or banner system, use references from `references/kv-reference-library.md` and, when browsing is available or the user requests it, inspect public inspiration sources such as Pinterest ideas, Behance project searches, Dribbble searches, official campaign pages, event/stage design references, and brand design case sites. Do not copy exact designs, logos, typography, or campaign layouts. Translate them into composition mechanisms.

For LED, stage-screen, large-screen, ultra-wide, irregular-screen, wraparound, or multi-screen KV, reading `references/large-screen-kv-experience-library.md` is mandatory. `$kv-director` owns the screen-facing visual judgment. Use `$led-screen-director` as a technical collaborator when actual screen drawings, viewing distance, stage blocking, motion behavior, or multi-screen constraints need deeper validation; do not hand away the KV concept or style decision.

Every formal KV direction must choose one `kv_composition_mode` before prompt writing:

| Composition mode | Best use | Required visible mechanism |
| --- | --- | --- |
| center_axis_ritual | event, launch, ceremony, gala, national/city theme | central symbol/product/light axis, symmetric weight, title zone separated |
| third_subject_negative_space | brand, product, deck cover, web hero | subject on left/right third, clean opposite title/logo field |
| product_pedestal_stage | product launch, automotive, tech, device | product hero on a grounded platform/stage, controlled reflection, claim-safe band |
| human_environment_manifesto | brand film, corporate, public value | credible person/environment relationship, restrained negative space, trust signal |
| symbolic_object_superscale | campaign, theme reveal, culture/city | one enlarged symbolic object or metaphor, simple background, clean claim zone |
| diagonal_momentum | sports, youth, sales, energetic campaign | readable diagonal force path, not cluttered particles, safe title counterweight |
| modular_grid_system | program, summit, multi-topic campaign | controlled grid/collage, limited modules, clear hierarchy and no tiny text |
| portal_depth_corridor | tech, future, conference, immersive visual | depth tunnel/portal, stable vanishing point, center-safe message area |
| panoramic_horizon | city, engineering, documentary, ultra-wide | wide depth, horizon control, side extension fields, human/product scale |
| split_screen_triptych | multi-screen stage, program package, comparison theme | modular panels, consistent color/material, each panel crop-safe |

These modes are compact defaults. Use the expanded archetypes in `kv-composition-style-library.md` whenever they fit the communication problem better.

Every KV must also choose:

```text
one primary_style_family
at most one supporting_style_family
palette_logic
material_language
lighting_model
photographic_vs_graphic_balance
image_density
anti_template_rule
forbidden_style_drift
```

The style must be a visible mechanism, not a mood adjective. Explain why it fits as `claim -> audience response -> composition -> style family -> material/light/color -> title relationship`.

For LED / stage-screen / large-screen KV, also output `led_screen_layout_spec`. Choose one:

| LED layout mode | Use when | Required screen logic |
| --- | --- | --- |
| center_safe_emblem | main stage backdrop, ceremony reveal | key object inside center safe zone, no edge-critical detail |
| performer_safe_void | live host/speaker/performance in front | lower/center performance area clean, visual energy around it |
| ultra_wide_center_wings | 21:9 / 32:9 / wraparound LED | strong center plus low-detail side wings, no important text near edges |
| stage_depth_frame | product/keynote/event opener | background creates depth behind stage, floor/foreground not too busy |
| split_screen_modular | multi-screen or side-screen system | main screen owns key symbol, side screens extend atmosphere only |

Required composition packet:

```text
kv_direction_packet
proposal_to_kv_packet: required when an approved proposal exists
kv_composition_style_packet: required for every KV
kv_composition_mode:
composition_reference_source: Pinterest / Behance / Dribbble / design site / user reference / mother-library route
reference_mechanism_translation: what is borrowed as hierarchy, safe area, scale, rhythm, and extension logic
master_kv_layout_spec: subject position, visual weight, title/logo/sponsor zones, negative space, crop margins
led_screen_layout_spec: screen ratio, center safe zone, performer/presenter safe area, side extension, far-distance readability
large_screen_experience_packet: required for LED / stage / big-screen KV
safe_area_map: top / bottom / left / right / center-safe / sponsor-safe
extension_crop_map: how 16:9, 9:16, 4:5, 1:1, LED, and ultra-wide preserve the same visual DNA
kv_rendition_matrix: normalized safe-area coordinates, deterministic master-image crops, overlays, previews, and manual-recomposition warnings
director_contribution_packet: kv-director owns KV type, composition mode, subject hierarchy, layout safety, asset split, post typography plan
visual_helpfulness_targets: what the prompt must visibly protect or improve
```

If `kv_composition_mode`, `master_kv_layout_spec`, or required LED layout decisions are missing, route back to `$kv-director` instead of writing image prompts.

If `kv_composition_style_packet` is missing, generic, internally contradictory, or contains only taste adjectives, route back to `$kv-director`. Do not let the prompt director invent the KV style.

For screen work, choose one `primary_large_screen_adaptation` and at most one supporting adaptation from `large-screen-kv-experience-library.md`. They must preserve `kv_composition_style_packet`; do not introduce a second unrelated KV style. Explain the selection as `approved KV visual system -> stage function -> screen adaptation -> physical layout -> risk control`.

## KV Strategy

A good KV direction must state:

```text
传播目标
品牌主张 / 活动主题 / 产品卖点
一句主视觉概念
观众第一眼看到什么
主体层级：品牌 / 产品 / 人物 / 场景 / 符号
主视觉钩子如何可视化
主KV采用哪一种构图母型
KV采用哪一种主风格机制，以及色彩、材质、光线和图形/摄影比例
大屏KV / LED KV采用哪一种屏幕构图逻辑
标题 / slogan / logo / sponsor 安全区
主比例和延展比例
AI生成哪些无字素材，后期排哪些文字和标识
```

For commercial/event KV, sell a claim that can be laid out:

```text
品牌/产品/活动主体 + one visual hook + title/logo/sponsor-safe layout + extension-ready system
```

## Layout-Safe Composition Rule

KV prompts must reserve typography and brand zones. Do not let the image fill every area with faces, props, particles, city detail, sponsor clutter, or unreadable generated text.

Layout safe is not enough. The director must name the composition form: center-axis, third-subject negative space, product pedestal, human-environment manifesto, superscale symbol, diagonal momentum, modular grid, depth portal, panoramic horizon, or split-screen system. The prompt must then describe visible placement and safe areas instead of saying only "clean layout" or "premium KV".

| Ratio | Default layout-safe logic |
| --- | --- |
| 16:9 / deck cover | subject left or right third, large negative space opposite for title/logo |
| 9:16 vertical | hero subject in middle third, top or bottom 18-25% clean for title |
| 4:5 feed | simple subject hierarchy, top/bottom clean claim band |
| 1:1 square | center-safe symbol or product, clean title/logo zone |
| LED / stage screen | center-safe main symbol, large simple shapes, title and sponsor zones separated |
| ultra-wide screen | central hero or stage-safe axis, side extension with low-detail atmosphere |

Use layout language inside the prompt:

```text
右侧留出标题和logo负空间 / 上方保留干净主题字区 / 下方保留赞助商安全区 / 背景不要出现可读文字
```

## Text, Logo, And Sponsor Rule

Do not ask image models to generate final readable title, slogan, logo, sponsor marks, QR code, legal line, venue/date text, or brand wordmark.

Default KV image generation should produce:

```text
无字主视觉底图
品牌/产品/活动主体清楚
干净留字区
无水印、无logo、无乱码文字
```

If a design needs text, write:

```text
标题、Logo、Slogan、赞助商、日期、地点、二维码、法律信息由后期排版添加，不在AI图内生成。
```

If the user wants a separate stylized title, 3D lettering, or transparent PNG text asset for the KV, route that asset to `$type-png-director` instead of baking text into the KV base art.

Allowed AI text exceptions:

```text
abstract sign shape with no readable copy
blurred background document texture
simple number-like mark when not brand-critical
unreadable screen glow blocks
```

## AI Asset Split

Important KV work should not force one generation to solve the whole design. Split into assets:

| Asset | Purpose |
| --- | --- |
| 无字主视觉底图 | final base art with title/logo/sponsor-safe layout |
| 主体资产 | product, symbolic object, host, speaker, city, engineering, or stage center |
| 背景氛围图 | venue, city, product environment, stage space, abstract brand texture |
| 符号/物件特写 | ceremony object, product detail, trophy, device, data object, brand metaphor |
| 横竖版延展图 | same visual DNA adapted to 16:9, 9:16, 4:5, 1:1, LED or ultra-wide |

For AI prompts, ask for the base art or asset, not a finished graphic design with generated typography.

## Master-To-Rendition Gate

Approve one master composition before deriving delivery ratios. Do not regenerate each ratio as an unrelated new KV unless the crop matrix proves the subject cannot survive the target format.

Create and validate the rendition plan with:

```powershell
python scripts\build_kv_rendition_matrix.py --input templates\kv-rendition-plan-template.json --output-dir H:\project\kv\renditions --check-only
python scripts\build_kv_rendition_matrix.py --input H:\project\kv\kv-rendition-plan.json --output-dir H:\project\kv\renditions
```

Use normalized `x/y/w/h` boxes for title, logo, sponsor, and performer-safe zones. The script writes `kv-rendition-matrix.json`, SVG safe-area overlays, and crop previews when a master image is provided. A `subject_box_larger_than_crop_manual_recomposition_required` warning means the director must recompose that ratio; do not solve it by silently changing the KV style.

## Reference And Style Inheritance

For every KV, first read `references/kv-composition-style-library.md`. Then read `references/kv-reference-library.md` when:

```text
the KV type is unclear
the user asks for brand KV, event KV, launch KV, product KV, program KV, LED main visual, or banner system
the work needs professional title/logo/sponsor-safe layout logic
the project needs a commercial reference mechanism before frame-vision-director prompts
```

For LED, stage, big-screen, ultra-wide, wraparound, irregular, or multi-screen deliverables, also read `references/large-screen-kv-experience-library.md` and preserve its `large_screen_experience_packet`.

Translate references into:

```text
brand proposition
kv_composition_style_packet
kv_composition_mode
master_kv_layout_spec
led_screen_layout_spec
subject hierarchy
negative space
stage/screen readability
product material truth
ritual center
title/logo/sponsor safe zones
extension ratio strategy
AI text/logo risk control
```

Do not copy exact brand campaigns, logos, title treatments, sponsor layouts, celebrity faces, or distinctive protected designs.

## Tool Strategy

| Tool | KV use |
| --- | --- |
| built-in imagegen | natural-language base art, edits, product/scene preservation |
| Banana / Banana Pro | batch KV assets, product/control references, compact prompts |
| Midjourney | exploratory mood only when requested, not final brand/product continuity |
| Canva / Photoshop | typography, logo, sponsor layout, final KV system adaptation |

Formal KV still images default to built-in imagegen or Banana/Banana Pro. Do not route still KV images to Jimeng by default; use Jimeng mainly for animated KV or image-to-video handoff.

## Output 1: KV Direction Table

Use this first:

| Item | Decision |
| --- | --- |
| kv_type |  |
| audience/platform |  |
| main_ratio |  |
| extension_ratios |  |
| upstream_source |  |
| proposal_to_kv_packet | required when the upstream source is an approved proposal/PPT/concept |
| brand_or_event_claim |  |
| core_visual_hook |  |
| subject_hierarchy |  |
| layout_safe_area |  |
| title_logo_sponsor_zones |  |
| visual_symbol |  |
| kv_composition_style_packet | primary composition, hierarchy, gaze path, negative space, title relation, style, palette, material, light, density, drift control |
| kv_composition_mode |  |
| composition_reference_source |  |
| reference_mechanism_translation |  |
| master_kv_layout_spec |  |
| led_screen_layout_spec | required for LED / stage screen / big-screen KV |
| large_screen_experience_packet | required for LED / stage screen / big-screen KV |
| safe_area_map |  |
| extension_crop_map |  |
| kv_rendition_matrix | normalized safe areas, crop coordinates, overlays, previews, manual-recomposition warnings |
| style_inheritance |  |
| mother_library_translation |  |
| director_contribution_packet |  |
| visual_helpfulness_targets |  |
| typography_plan | text/logo/sponsor added in post, not generated inside AI image |
| asset_split | base art / subject / background / symbol / variants |
| AI risks | text gibberish, fake logo, sponsor clutter, product drift, plastic material, template look |

## Output 2: KV Asset Split

For each asset, state:

```text
asset_name
asset_purpose
ratio
subject_or_background
safe_area
reference_roles
generation_tool
post_layout_use
```

## Output 3: KV Prompt Handoff

For `$kv-image-prompt-director`, include:

```text
packet_name: kv_direction_packet
upstream_source
proposal_to_kv_packet when an approved proposal exists
kv_type
main_ratio and extension_ratios
kv_composition_style_packet
kv_composition_mode
composition_reference_source
reference_mechanism_translation
master_kv_layout_spec
led_screen_layout_spec
large_screen_experience_packet for LED / stage / big-screen KV
safe_area_map
extension_crop_map
无字主视觉底图目标
brand_or_event_claim
core_visual_hook
subject_hierarchy
layout_safe_area
title_logo_sponsor_zones
visual_symbol
project-style-lock / master_style_sentence
mother_library_translation
cinematography anchor translation
product/brand/reference image roles
anti_ai_realism_rule
platform_language_strategy
image_tool_boundary
negative prompt requirements
post typography plan
director_contribution_packet
visual_helpfulness_targets
```

For `$prompt-platform-auditor`, require:

```text
no readable generated title/logo/slogan/sponsor text
title/logo/sponsor-safe negative space exists
brand/product/event subject hierarchy is clear
extension ratios are possible from the same visual DNA
AI text/logo risk is controlled
formal project style lock is preserved
prompt matches built-in imagegen or Banana/Banana Pro language strategy
```

## Output 4: Post Layout Plan

State what post layout must add:

```text
title / theme line
logo / wordmark
slogan / claim
date / venue / CTA
sponsor zone
QR code
legal or platform information
social or LED crop variants
```

Also state what the AI image must leave clean for post layout.

## KV Prompt Formula

Use this structure for final image prompt drafts:

```text
[无字KV主视觉底图 / KV asset type] +
[品牌/活动/产品主体层级] +
[构图视觉系统：第一眼、焦点层级、视线动线、负空间、标题关系] +
[风格视觉系统：主风格、色彩、材质、光线、图形/摄影比例、密度、禁止漂移] +
[版式：标题、logo、sponsor安全区和延展裁切] +
[主视觉钩子：品牌主张/产品卖点/仪式/舞台/符号] +
[项目风格锁和母库转译] +
[摄影/光线/材质/色彩] +
[真实摄影反AI控制] +
[比例和延展要求] +
[禁止文字/logo/slogan/sponsor/水印/乱码/塑料材质/模板KV感]
```

## Quality Gate

Do not approve a KV direction if:

```text
no kv_type
no brand_or_event_claim
no core_visual_hook
no subject hierarchy
no kv_composition_style_packet
no kv_composition_mode
no master_kv_layout_spec
LED / big-screen KV has no led_screen_layout_spec
LED / big-screen KV has no large_screen_experience_packet or selected primary_large_screen_adaptation
no composition_reference_source or reference mechanism translation for formal KV
no layout_safe_area
no title_logo_sponsor_zones
asks AI to generate final readable title/logo/slogan/sponsor marks
ignores project-style-lock in a formal project
uses generic words only: premium, futuristic, high-end, cinematic, shocking
style has no palette, material, light, image-density, photographic-vs-graphic, or drift-control decision
composition has no first-read, focal hierarchy, gaze path, negative-space logic, or typography relationship
no asset_split for complex KV
no extension ratio plan
no safe_area_map or extension_crop_map
formal multi-ratio delivery has no kv_rendition_matrix or approved manual-recomposition decision
no anti-AI realism or text/logo risk control
an approved proposal exists but the KV direction changes its claim or visual DNA without declaring the change
```

## Handoff Rule

`$kv-director` plans commercial/event KV communication, system logic, asset split, and layout-safe image direction. `$kv-image-prompt-director` writes generation-ready KV image prompt drafts. `$prompt-platform-auditor` checks platform safety. Canva/Photoshop/post layout handles final typography, logo, sponsor, QR code, and delivery variants.

Do not let one AI image prompt become the whole KV workflow.
