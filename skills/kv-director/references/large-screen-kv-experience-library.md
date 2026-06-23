# Large-Screen KV Experience Library

Use this reference when `$kv-director` handles an event KV, launch KV, gala KV, conference KV, program main visual, LED main visual, stage backdrop, ultra-wide screen, irregular screen, or multi-screen system.

This library is a physical-screen adaptation layer. It does not choose the project's main composition or style from zero. First inherit `kv_composition_style_packet` from `kv-composition-style-library.md`, then translate that approved visual system into stage-safe composition, screen readability, material, light, extension logic, and post-layout requirements.

## Mandatory Read Triggers

Read this file before approving a KV direction when any of these are true:

```text
LED / 大屏 / 舞台 / 发布会 / 晚会 / 论坛 / 峰会 / 颁奖 / 节目主视觉
ultra-wide / wraparound / irregular screen / side screens / floor screen
the master KV must be adapted to a live-event screen
the user already has a proposal and needs a stage-facing KV system
```

For ordinary brand, product, or social KV without a screen deliverable, use `kv-reference-library.md`; do not force this large-screen gate.

Hard rule:

```text
kv_composition_style_packet first
large_screen_experience_packet second
```

If the screen adaptation would replace the approved primary composition or style, route back to `$kv-director` and declare the change instead of silently redesigning the KV.

## Research Provenance

The experience layer is distilled from professional public case-study families and design-discovery sites. Use official case sites to understand complete systems; use discovery platforms only to find leads.

| Source family | Learn from it | Do not copy |
| --- | --- | --- |
| Moment Factory official project cases | immersive scale, architecture-content integration, audience journey, spatial rhythm | exact show world, signature installation, client IP |
| Es Devlin Studio official project cases | stage as narrative object, sculptural center, performer-space relation, reveal logic | exact stage sculpture or show identity |
| STUFISH official project cases | touring-stage geometry, multi-screen hierarchy, sightline-aware spectacle | exact stage plan, scenic structure, artist identity |
| 59 Productions official project cases | projection/LED storytelling, architecture-led image, chapter transitions | exact mapped content or theatrical sequence |
| Territory Studio official project cases | interface-free data worlds, cinematic information hierarchy, screen ecosystems | proprietary UI, franchise graphics, title systems |
| FutureDeluxe and ManvsMachine official work | premium CG material, brand motion language, product/symbol transformation | exact campaign render, logo treatment, motion signature |
| Pentagram and official brand/event case pages | identity system, typography hierarchy, ratio family, campaign consistency | exact identity, font treatment, logo placement |
| Behance | complete KV and event-identity case systems | project artwork, typography, sponsor layout |
| Pinterest | fast composition and stage-reference discovery | unverified attribution, exact image, trend collage |
| Dribbble | spacing, modular rhythm, current surface treatments | isolated shot treated as a complete system |

When live browsing is used, preserve a compact research note:

```text
source_name:
source_url_or_search_term:
project_type:
observed_mechanism:
transferable_rule:
do_not_copy:
research_date:
```

Do not write only `参考某某工作室风格`. Convert the observation into visible and technical rules.

## Master KV And Screen KV Are Different Deliverables

```text
master_kv = communication hierarchy + brand/event claim + typography/logo/sponsor layout
screen_kv = master visual DNA translated for physical screen shape + stage occupancy + viewing distance + cameras
motion_kv = screen KV prepared for restrained animation, reveal, loop, or opener handoff
```

Never stretch a 16:9 master KV across an ultra-wide screen and call it a screen design. Recompose it.

## Screen-Type Decision

Choose the physical screen system before choosing the screen composition.

| screen_system | Typical use | Required judgment |
| --- | --- | --- |
| standard_main_screen | conference, forum, keynote | title zone, presenter zone, camera-safe contrast |
| main_plus_side_wings | gala, launch, award | main screen owns meaning; wings extend atmosphere |
| ultra_wide_screen | summit, immersive event, exhibition | strong center, low-detail side fields, horizon control |
| wraparound_screen | immersive launch, exhibition, experience | continuity across corners, no edge-dependent subject |
| split_multi_screen | program, concert, awards, hybrid event | modular ownership, gap-aware composition, independent crops |
| irregular_masked_screen | scenic LED, logo-shaped or fragmented screen | pixel-map-aware assets, no important content across masks |
| screen_plus_floor | launch, fashion, ceremony | floor stays low-detail and performer-safe; avoid false steps |
| XR_virtual_stage | broadcast, virtual production | camera frustum, parallax, floor/wall continuity, moire control |

If actual resolution, pixel map, mask, stage drawing, camera positions, or presenter blocking exists, preserve it as the authority. Do not infer a standard 16:9 canvas.

## Large-Screen Adaptation Mechanisms

Choose one primary screen adaptation mechanism and at most one supporting mechanism. They must inherit the approved `primary_style_family`, palette, material, and lighting from `kv_composition_style_packet`; they are not a second KV style decision.

| adaptation_id | Best use | Visible mechanism | Screen caution |
| --- | --- | --- | --- |
| monumental_axis | ceremony, government/city, anniversary | central axis, monumental symbol, restrained symmetry | keep center clear if a presenter stands there |
| light_gate_reveal | launch, opening, future theme | luminous portal, depth corridor, controlled reveal center | avoid thin concentric lines and cheap neon |
| energy_core_radiance | technology, brand summit, product reveal | one energy core with broad radial fields | keep rays broad; no dense particles behind copy |
| sculptural_emblem | brand event, awards, culture | one large three-dimensional brand metaphor | do not fake the logo or build unreadable micro-detail |
| ribbon_flow_field | finance, mobility, communication, lifestyle | broad ribbon or stream creates direction and extension | preserve negative space; avoid tangled silk screensaver look |
| material_monument | luxury, automotive, product, industry | metal, glass, stone, fabric, liquid as monumental form | material must remain tactile, not glossy plastic CG |
| product_altar | product launch, automotive, device | grounded hero object, pedestal, controlled reflection | product structure and presenter sightline are authority |
| panoramic_world | city, culture, travel, engineering | broad horizon, real spatial scale, atmospheric depth | side fields extend; avoid fantasy mega-city clutter |
| architectural_grid | enterprise, city, engineering, summit | structural lines, modules, disciplined perspective | avoid moire-producing fine grids |
| data_constellation | AI, science, network, finance | sparse nodes and paths with one clear hierarchy | no tiny UI, fake dashboards, or uniform particle noise |
| topographic_layers | ecology, geography, strategy, development | contour-like layers, terrain depth, directional growth | use broad bands, not hairline maps |
| cultural_reconstruction | heritage, city, festival, museum | artifact/craft mechanism rebuilt as contemporary spatial form | no literal motif pile-up or fake ancient text |
| ink_light_landscape | Chinese culture, poetry, national media | restrained ink mass, light, mist, negative space | protect contrast on LED; avoid gray muddy screen |
| paper_craft_relief | education, family, festival, public culture | layered paper/sculptural relief, tactile shadows | avoid childish template look unless intended |
| ecological_growth | ESG, nature, health, sustainability | organic growth path, real material, quiet vitality | no generic glowing tree or greenwashing particles |
| performance_silhouette | music, sports, show, gala | readable human silhouette with large-scale environmental rhythm | do not place high-detail faces at screen edges |
| modular_story_panels | program, forum, multi-topic agenda | a controlled family of panels/scenes with shared DNA | each screen/module must work independently |
| optical_depth_chamber | immersive tech, product, exhibition | layered translucent planes, depth and parallax | avoid unsafe rapid flicker and over-dense glass layers |
| cinematic_environment | brand manifesto, documentary, city story | photographic world with credible human/environment scale | stage wash must not flatten dark photographic detail |
| graphic_color_field | youth, sports, festival, campaign | large color blocks, bold silhouette, fast distant reading | maintain copy contrast and prevent color clipping on camera |

## Composition Modes For Physical Screens

| layout_mode | Use when | Required composition |
| --- | --- | --- |
| center_safe_emblem | title reveal, ceremony, symbolic KV | one readable center symbol; copy and sponsor zones separated |
| performer_safe_void | host, speaker, singer, product stands in front | center/lower area quiet; energy frames the live subject |
| ultra_wide_center_wings | 21:9, 32:9, wraparound | meaning in center; side wings carry low-detail atmosphere |
| stage_depth_frame | keynote, product reveal, opener | screen creates depth behind stage without a false floor edge |
| modular_screen_ownership | main plus sides or split screens | main screen owns claim; side modules extend color/material/rhythm |
| panoramic_horizon_lock | city, landscape, engineering | horizon and scale remain stable across the full width |
| asymmetrical_presenter_field | keynote with presenter on one side | content weight moves away from presenter; title remains readable |
| scenic_mask_integration | irregular or fragmented screens | visual masses respect masks and scenic gaps; no broken key object |

## Live-Event Experience Rules

### Audience And Camera Must Both Read

- Judge the image from the front row, back row, wide venue camera, medium presenter camera, and photographed still.
- Large shapes and value grouping matter more than texture visible only on a laptop.
- Keep a clean silhouette behind people and products; the live subject must not merge into the screen.
- Large white fields can overpower cameras and faces. Use controlled luminance and preserve skin exposure.
- Saturated red and blue may clip or contaminate faces. Keep a camera-safe palette boundary.

### Avoid Screen And Camera Failure

- Avoid hairline grids, one-pixel lines, dense high-frequency patterns, tiny repeating dots, and close parallel stripes that can cause moire.
- Avoid rapid flicker, high-frequency strobing, uncontrolled edge motion, and fast full-screen luminance changes.
- Do not place critical faces, logos, or products across panel gaps, scenic masks, corners, or screen joins.
- Do not rely on subtle near-black detail if stage light or venue ambient light will wash it out.
- Do not put dense floor graphics under performers; they create false depth and unsafe visual footing.

### Stage Relation

- Record presenter, host, performer, product, podium, award table, stairs, entrance, and camera positions.
- Treat the lower center as occupied when people or products stand in front, unless the stage plan proves otherwise.
- Side screens should normally extend atmosphere, not repeat full title blocks or compete with the main screen.
- If IMAG/live camera feeds use side screens, keep them visually quieter and reserve their crop zones.

## Proposal-To-Large-Screen Translation

When an approved proposal already exists, extract rather than reinvent:

```text
approved_theme
core_claim
narrative_or_ceremony_arc
approved_visual_symbols
brand_colors_and_forbidden_colors
product_or_character_authority
stage_or_venue_context
required_title_logo_sponsor_content
master_kv_deliverables
screen_deliverables
```

Then decide:

```text
what remains identical across master KV and screen KV
what must be recomposed for the physical screen
what becomes post typography
what becomes a motion/reveal layer
what must be generated as a separate asset
```

Do not restart concept development unless the proposal cannot produce one clear claim, one visual hook, or one workable stage relationship.

## Required Large-Screen Experience Packet

```text
large_screen_experience_packet
screen_system:
actual_ratio_resolution_or_pixel_map:
viewing_distance_class: near / medium / far / mixed
stage_occupancy:
presenter_performer_product_safe_area:
camera_and_audience_readability:
primary_large_screen_adaptation:
supporting_adaptation:
style_mechanism_translation:
screen_layout_mode:
center_and_edge_rules:
main_and_side_screen_ownership:
moire_flicker_luminance_risks:
extension_strategy:
motion_handoff_potential:
missing_fields:
route_back_to:
```

For a quick visual test, unknown physical fields may be marked `assumed_for_preview`. For formal delivery, actual screen and stage information must replace assumptions before final layout or motion production.

## Selection Rule

The director must explain why the selected style fits the proposal:

```text
approved KV composition/style -> stage function -> screen adaptation mechanism -> physical layout -> screen risk control
```

Reject a direction that is only `高级、大气、科技、震撼、国际化`. Those are desired impressions, not visual mechanisms.
