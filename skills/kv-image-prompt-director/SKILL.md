---
name: kv-image-prompt-director
description: Image prompt director for commercial/event KV workflows under zongkong. Use after kv-director has produced a KV direction packet, asset split, reference mechanism, layout-safe areas, and post typography plan, when Codex needs copyable prompts for no-text KV base art, subject/product assets, background assets, symbol/object assets, or ratio variants for built-in imagegen, Banana/Banana Pro, or Midjourney. Do not use to decide the KV concept, brand claim, reference family, layout strategy, or final typography; route missing KV decisions back to kv-director and route platform execution checks to prompt-platform-auditor.
---

# KV Image Prompt Director

## Core Role

`$kv-image-prompt-director` turns an approved `$kv-director` `kv_direction_packet` into generation-ready image prompt drafts.

It writes prompts for:

```text
无字KV主视觉底图
主体/产品/人物/舞台中心资产
背景氛围资产
符号/物件特写资产
16:9 / 9:16 / 4:5 / 1:1 / LED / ultra-wide 延展变体
```

It does not decide:

```text
kv_type
brand_or_event_claim
core_visual_hook
reference mechanism
primary composition and supporting geometry
primary style family and supporting style family
palette / material / lighting / density system
subject hierarchy
layout safe area
title/logo/sponsor zones
asset split
post typography plan
```

If these are missing, output `待补上游项` and route back to `$kv-director`.

## Workflow Position

Default route:

```text
$zongkong
-> kv-director
-> kv-image-prompt-director
-> prompt-platform-auditor
-> image generation
-> image-qc-director
-> Canva / Photoshop / manual layout
```

For formal projects, inherit:

```text
kv_direction_packet
asset_split
reference mechanism from kv-reference-library
project-style-lock / master_style_sentence
mother_library_translation
cinematography anchor translation
product/brand/reference image roles
anti_ai_realism_rule
platform_language_strategy
image_tool_boundary
post typography plan
```

## Required Input Packet

Before writing final prompts, require:

```text
packet_name: kv_direction_packet
proposal_to_kv_packet when the KV inherits an approved proposal
kv_type
target_platform: built-in imagegen / Banana / Banana Pro / Midjourney
main_ratio
extension_ratios
brand_or_event_claim
core_visual_hook
subject_hierarchy
kv_composition_style_packet
kv_composition_mode
composition_reference_source
reference_mechanism_translation
master_kv_layout_spec
led_screen_layout_spec when this is LED / stage screen / big-screen KV
large_screen_experience_packet when this is LED / stage screen / big-screen KV
safe_area_map
extension_crop_map
layout_safe_area
title_logo_sponsor_zones
visual_symbol
asset_split
reference_mechanism
style_inheritance
negative_prompt_requirements
post_typography_plan
```

For reference images, require narrow roles:

```text
产品结构 / logo位置参考但不生成logo / 人物身份 / 服装 / 舞台空间 / 材质 / 构图 / 色调 / 光线 / 背景
do_not_inherit
```

## Prompt Types

Choose the prompt type from the asset split:

| Prompt type | Purpose | Must include |
| --- | --- | --- |
| no-text base art | final KV background for post layout | subject hierarchy, kv_composition_mode, master_kv_layout_spec, layout safe area, title/logo/sponsor zones, ratio |
| subject asset | product/person/symbol for compositing | clean shape, material, transparent or simple background when useful |
| background asset | venue/city/stage/texture field | no text, no logo, low detail where typography goes |
| symbol/object close-up | ceremony/product/detail metaphor | material truth, crop safety, no fake labels |
| ratio variant | same visual DNA in another format | preserved hook, extension_crop_map, new safe area, crop-safe subject |

## Composition Translation Rule

`$kv-image-prompt-director` does not invent the KV composition or style. It inherits `kv_composition_style_packet`, `kv_composition_mode`, `master_kv_layout_spec`, `led_screen_layout_spec`, `safe_area_map`, and `extension_crop_map` from `$kv-director`.

Translate each mode into visible prompt language:

| Mode | Prompt language must include |
| --- | --- |
| center_axis_ritual | centered symbol/product/light axis, symmetric visual weight, clean separated title/sponsor zones |
| third_subject_negative_space | subject on left/right third, opposite large negative space, crop-safe margins |
| product_pedestal_stage | product on grounded pedestal/stage, controlled reflections, clear claim band |
| human_environment_manifesto | person/environment relation, credible scale, quiet brand-safe space |
| symbolic_object_superscale | one enlarged metaphor object, simple field, no clutter around copy zone |
| diagonal_momentum | readable diagonal energy path, safe counter-space for title, limited particles |
| modular_grid_system | clean modules, stable grid, limited elements, no tiny text |
| portal_depth_corridor | central depth/portal, stable vanishing point, readable center-safe area |
| panoramic_horizon | wide horizon, side extension fields, no edge-critical subject |
| split_screen_triptych | modular panels, consistent visual DNA, each panel crop-safe |

## Style Translation Rule

Translate `kv_composition_style_packet` into visible prompt language. Every no-text base-art prompt must express:

```text
first_read and focal_hierarchy
gaze_path and visual_balance
depth_model and negative_space_logic
typography_relationship and crop_behavior
primary_style_family and any supporting_style_family
palette_logic
material_language
lighting_model
photographic_vs_graphic_balance
realism_level and surface_finish
image_density and atmosphere_behavior
anti_template_rule and forbidden_style_drift
```

Do not print field names or style IDs without describing the visible frame. For example, `luxury_material` must become controlled tactile metal/glass/stone, precise highlight shape, quiet background, real contact shadow, and no glossy plastic CG. `technology_precision` must become exact geometry, restrained data/light cues, precise material boundaries, and no generic blue particle wallpaper.

The composition controls where the eye goes. The style controls what the visual world feels physically like. Preserve both.

For LED / stage-screen prompts, also translate `led_screen_layout_spec`:

```text
center-safe key object
far-distance readable large shapes
presenter/performance safe area if needed
low-detail side extension
no tiny lines, no edge-critical faces, no readable generated text
```

Also inherit the selected `primary_large_screen_adaptation`, optional supporting adaptation, `screen_system`, `stage_occupancy`, `camera_and_audience_readability`, and `moire_flicker_luminance_risks` from `large_screen_experience_packet`. Translate them into visible prompt language while preserving `kv_composition_style_packet`; do not treat the screen adaptation as a new style.

The prompt must protect both the physical stage and the generated image:

```text
large readable value masses
clean silhouette behind presenter / performer / product
low-detail side extensions where required
no hairline grids, dense repeating dots, micro UI, or edge-critical subject
controlled large white areas and saturated red/blue for camera capture
screen-mask and panel-gap safety when applicable
```

## Text And Logo Rule

Never ask the image model to generate final readable:

```text
title
logo / wordmark
slogan
sponsor marks
date / venue / CTA
QR code
legal line
price or ecommerce badge
channel or platform id
```

Write these as post-layout notes:

```text
标题、Logo、Slogan、赞助商、日期、地点、二维码、法律信息由后期排版添加，不在AI图内生成。
```

The image prompt must ask for clean negative space where those items will be placed.

## Reference Mechanism Translation

If the chosen reference is CCTV / national media:

```text
translate into: dignified central symbol, official clarity, restrained color, human or cultural truth, clean title field, no fake logo/seal/emblem.
```

If the chosen reference is China commercial poster / KV:

```text
translate into: product-first hierarchy, fast readability, material truth, claim-safe band, no fake price tag/platform badge/logo.
```

If the chosen reference is event/launch KV:

```text
translate into: ritual center, stage readability, separated title/logo/sponsor zones, broad simple shapes.
```

If the chosen reference is LED/stage screen:

```text
translate into: distant readability, center-safe symbol, low-detail side extension, no thin lines or tiny text.
```

Do not write only `央视风`, `商业海报风`, `高级KV`, `大气`, `震撼`, or `国际化`. Convert the reference into visible composition, light, material, color, safe areas, and AI risk controls.

## Tool Profiles

### Built-In Imagegen / ChatGPT Image

Use natural Chinese visual instructions. Put visible image and layout first.

Best structure:

```text
生成一张无字KV主视觉底图：[主体和场景]。
构图与风格：[kv_composition_style_packet 可见转译，包括第一眼、焦点层级、视线动线、负空间、标题关系、主风格、色彩、材质、光线、图形/摄影比例和密度]。
构图模式：[kv_composition_mode + master_kv_layout_spec；如果是大屏/LED，写入led_screen_layout_spec]。
版式：[主体位置、前中后景、safe_area_map、标题/logo/sponsor安全区、extension_crop_map]。
参考机制：[CCTV/商业/活动/产品/LED机制的可见转译]。
光线和材质：[现实光源、材质触感、色彩边界]。
后期：[哪些文字/logo由后期添加，不在图内生成]。
避免：[文字、logo、水印、乱码、假HDR、塑料材质、模板感]。
比例：[ratio]。
```

### Banana / Banana Pro

Use compact Chinese visible-frame instruction plus English camera/lens/material keywords only when useful.

Best structure:

```text
[无字KV主视觉底图]，[主体 + 场景 + 主视觉钩子]，
[kv_composition_style_packet visible translation + kv_composition_mode + master_kv_layout_spec + 版式安全区 + 标题/logo/sponsor zones + extension_crop_map]，
[reference mechanism translation]，
[camera/lens/light/material/color]，
[anti-AI realism]，[ratio]。
负面词：[文字/logo/slogan/sponsor/二维码/水印/乱码/塑料材质/模板感/产品漂移]
```

### Midjourney

Use only when the user asks for MJ/Midjourney/Legnext. Keep it concise and include `--ar`.

Best structure:

```text
no-text commercial key visual base art, [subject], [scene], [layout safe negative space], [reference mechanism translated visually], [light/material/color], clean area for typography, no logos, no readable text --ar 16:9 --style raw --v 7
```

## Output Contract

Use this table by default:

| asset_name | prompt_type | target_tool | ratio | layout_safe_area | reference_roles | copyable_image_prompt | negative_prompt | post_layout_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Also include a compact handoff for `$prompt-platform-auditor`:

```text
source_prompt_owner: kv-image-prompt-director
source_kv_owner: kv-director
target_platform:
task_type: KV no-text base art / KV asset / KV ratio variant
ratio:
kv_composition_style_packet:
kv_composition_mode:
master_kv_layout_spec:
led_screen_layout_spec:
large_screen_experience_packet:
safe_area_map:
extension_crop_map:
reference_roles:
must_preserve:
must_not_generate:
post_typography_plan:
director_contribution_packet:
visual_helpfulness_targets:
```

## Quality Gate

Do not approve a KV image prompt draft if:

```text
it lacks target_tool or ratio
it lacks visible subject and scene
it lacks kv_composition_style_packet
it lacks kv_composition_mode
it lacks master_kv_layout_spec
LED / big-screen KV lacks led_screen_layout_spec
LED / big-screen KV lacks large_screen_experience_packet or fails to translate its selected style and screen risks
it lacks safe_area_map or extension_crop_map for ratio variants
it lacks layout_safe_area
it lacks title/logo/sponsor zones
it asks AI to generate readable title/logo/slogan/sponsor marks
it begins with generic words instead of the visible KV frame
it names a reference style without translating it
it names a style family without translating palette, material, light, density, realism, and forbidden drift
it does not preserve first-read, focal hierarchy, gaze path, negative space, or typography relationship
it ignores product/brand/reference roles
it cannot extend to the requested ratios
it lacks anti-AI material and text/logo risk controls
it contradicts proposal_to_kv_packet without an explicit approved change
```

Final prompts must be self-contained. Do not write `同上`, `延续上一张`, or `保持前面风格`.
