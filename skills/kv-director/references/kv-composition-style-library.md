# KV Composition And Style Library

This is the primary visual judgment library for `$kv-director`.

Use it for every commercial/event KV: brand, product, launch, campaign, program, conference, gala, city, culture, banner, LED, or stage-screen work. Large-screen rules are an adaptation layer after this visual system is decided.

The library does not provide finished designs to copy. It gives composition archetypes, style mechanisms, selection logic, and a packet that downstream image prompts can execute.

## Core Rule

Every KV direction must answer two separate questions:

```text
composition: how attention is organized
style: what visual world, material, light, color, and image behavior carry the claim
```

Do not replace either answer with adjectives such as `高级、大气、科技、国际化、震撼、电影感`.

Quick KV work may use a compact packet. Formal KV work must use the full packet.

## Composition Decision Dimensions

Before selecting an archetype, decide:

```text
first_read: what is seen in the first second
second_read: what supports or explains it
focal_hierarchy: primary / secondary / atmosphere / post typography
gaze_path: center-out / left-to-right / diagonal / circular / depth / modular
visual_balance: symmetric / asymmetric / weighted / distributed
depth_model: flat graphic / layered relief / photographic depth / spatial world
negative_space: where and why it stays quiet
typography_relationship: title beside / above / inside / across / separate from image mass
crop_behavior: what survives 16:9 / 9:16 / 4:5 / 1:1 / banner / screen
image_density: sparse / controlled / rich, with a stated quiet zone
```

## Composition Archetypes

Choose one primary archetype. A supporting geometry may be added only when it strengthens hierarchy.

| composition_id | Best use | Visible construction | Typography and crop behavior |
| --- | --- | --- | --- |
| center_axis_monument | ceremony, national/city, anniversary, launch | one central subject or symbol, stable vertical axis, broad supporting mass | title above/below or in a separated band; center survives most crops |
| third_subject_negative_space | brand, product, corporate, web hero | subject on left/right third, opposite field remains quiet | strong title/logo field; easy horizontal adaptation |
| radial_core | technology, product reveal, energy theme | one core with broad radial force and clear falloff | copy outside the core; keep rays away from small text |
| ring_orbit | ecosystem, platform, collaboration, anniversary | central authority with limited orbiting elements | title remains outside orbit; do not create a busy halo |
| diagonal_force | sports, youth, mobility, growth | dominant diagonal path with one counterweight | title sits in counter-space; preserve direction across crops |
| s_curve_flow | lifestyle, finance, mobility, beauty | one controlled flowing path connects foreground and background | copy sits in calm bend or opposite field; avoid tangled ribbons |
| portal_depth | future, conference, transformation, immersive theme | stable vanishing point, framed opening, depth corridor | title in center-safe opening or clean side plane |
| panoramic_horizon | city, engineering, documentary, culture | long horizon, scale reference, atmospheric depth | title in sky/ground quiet field; side extension remains possible |
| superscale_symbol | campaign, culture, theme reveal | one oversized metaphor object dominates the frame | title uses protected negative space; object must remain crop-safe |
| product_pedestal | automotive, device, FMCG, product launch | grounded hero product, pedestal or surface, controlled reflection | claim band separated from product; structure cannot drift |
| macro_material_crop | beauty, food, luxury, craft, product detail | tactile close crop, one material event, shallow or graphic depth | typography overlays only on controlled low-detail area |
| dual_subject_tension | partnership, comparison, before/after, competition | two authorities create a clear relationship or opposition | title occupies center gap or outer field; avoid equal-weight confusion |
| human_environment_manifesto | brand, ESG, corporate, public value | credible person/environment scale and emotional relation | quiet proposition field; human remains authentic, not stock-photo posed |
| cinematic_tableau | brand story, city, cultural campaign, premium program | staged photographic world with foreground/midground/background action | title occupies motivated environmental space; preserve narrative read |
| modular_grid | summit, program, multi-topic campaign, system brand | limited modules with one dominant cell and controlled rhythm | title aligns to grid; no tiny equal-weight collage |
| layered_collage | entertainment, youth, multi-character program | one hero layer, limited supporting cutouts, depth separation | title has its own layer; avoid crowded cast-wall template |
| frame_within_frame | culture, architecture, product, transformation | architectural/object frame directs attention inward | title sits on outer quiet plane or inside protected opening |
| top_down_system | product set, food, toolkit, process, collection | overhead organization with strong spacing and object hierarchy | typography uses one empty module; objects must not become inventory clutter |
| asymmetric_editorial | fashion, art, premium culture, modern brand | off-center subject, deliberate imbalance, editorial cropping | typography balances image weight; requires precise margins |
| split_triptych | program, multi-screen, chapters, comparison | two or three modules share visual DNA but have clear ownership | each module crops independently; main title remains outside panel noise |
| graphic_shape_field | youth, sports, festival, public campaign | large color/shape masses with fast silhouette read | typography integrates with simple geometry, not AI-generated letters |
| minimal_object_field | premium product, luxury, institutional clarity | one object, controlled ground, generous emptiness | title and logo receive high-value space; material accuracy is critical |

## Style Decision Dimensions

Style must be translated into visible controls:

```text
primary_style_family
supporting_style_family
palette_logic
material_language
lighting_model
photographic_vs_graphic_balance
realism_level
surface_finish
atmosphere_behavior
detail_density
edge_behavior
anti_template_rule
forbidden_style_drift
```

Choose one primary style family and at most one supporting family. Do not mix styles because they are individually attractive.

## Style Families

| style_id | Best use | Visible grammar | Avoid |
| --- | --- | --- | --- |
| official_monumental | public value, national/city, institutional event | stable axis, restrained palette, real architecture/material, dignified scale | fake seals, slogan propaganda template, excessive red/gold |
| international_modernist | summit, corporate, design-led brand | disciplined grid, bold negative space, limited palette, clean geometry | empty generic minimalism, random Bauhaus shapes |
| editorial_art_direction | fashion, culture, premium program | deliberate crop, asymmetry, graphic-photo tension, refined spacing | magazine imitation without a clear claim |
| luxury_material | automotive, beauty, jewelry, premium product | tactile metal/glass/stone/fabric, controlled highlights, deep quiet background | plastic CG gloss, black-gold template |
| cinematic_epic | city, engineering, brand manifesto, major launch | atmospheric depth, monumental scale, motivated light, restrained spectacle | fantasy concept-art overload, fake HDR |
| documentary_truth | corporate trust, ESG, people/city, factual program | real location, human scale, available-light credibility, lived texture | stock-photo posing, over-clean AI environment |
| premium_product_minimal | device, FMCG, beauty, retail hero | product-first hierarchy, precise surface, simple ground, claim-safe space | floating ungrounded product, fake label, sterile emptiness |
| technology_precision | hardware, AI, enterprise tech, science | exact geometry, controlled data/light cues, cool-neutral material | blue particle wallpaper, fake UI, neon cyberpunk default |
| future_spatial | conference, transformation, immersive launch | portal/depth planes, restrained volumetric light, clear vanishing structure | cheap neon tunnel, excessive transparent glass layers |
| data_intelligence | platform, network, finance, research | sparse nodes, meaningful paths, one information hierarchy | uniform particles, tiny dashboards, decorative code |
| architectural_urban | city, real estate, infrastructure, engineering | structural rhythm, real scale, depth, civic material | impossible mega-city, warped architecture |
| industrial_engineering | manufacturing, energy, automotive, machinery | metal truth, process scale, controlled sparks/dust, functional geometry | generic factory stock image, overdramatic sparks |
| contemporary_culture | heritage, museum, city culture, festival | one cultural mechanism rebuilt with modern material and spacing | motif pile-up, fake ancient text, souvenir-shop styling |
| eastern_poetic | Chinese culture, nature, humanities | restrained ink/light/mist rhythm, quiet asymmetry, material emptiness | gray muddy screen, generic ink-wash filter |
| craft_tactile | craft, food, culture, family, handmade product | paper, wood, textile, ceramic, hand traces, soft directional light | childish craft template, perfect synthetic surfaces |
| ecological_organic | sustainability, health, agriculture, nature | real growth structures, natural material, breathable palette | glowing tree cliche, greenwashing particles |
| surreal_conceptual | campaign metaphor, fashion, culture, creative brand | one impossible but legible visual proposition, realistic material logic | unrelated dream objects, visual puzzle without a claim |
| youth_kinetic | youth brand, social campaign, campus, music | bold crop, directional shape, energetic color, controlled layering | sticker clutter, trend collage, illegible density |
| sports_impact | competition, fitness, automotive performance | strong silhouette, diagonal force, compression, tactile motion trace | random lightning, fake muscles, particle explosion |
| festival_ceremonial | gala, anniversary, awards, celebration | ritual center, warm controlled energy, crafted symbolic material | confetti overload, plastic trophy, generic red-gold |
| entertainment_show | variety, music, talent, program identity | readable cast/action hierarchy, stage energy, graphic rhythm | overcrowded faces, sitcom lighting, fake show logo |
| fashion_image | fashion, beauty, lifestyle, talent | body/garment line, editorial light, controlled color world | beauty smoothing, generic luxury pose |
| liquid_metallic | mobility, beauty, technology, luxury | one controlled liquid/metal transformation, precise reflection | chrome blob trend with no brand meaning |
| graphic_color_block | public campaign, youth, sports, festival | large flat masses, strong silhouette, fast read | small decorative shapes, palette without hierarchy |
| paper_relief | education, culture, family, festival | layered relief, crafted shadow, simplified forms | low-end cut-paper template, excessive cute styling |
| sensory_fmcg | food, beverage, skincare, household | tactile droplets, steam, foam, fruit/fabric/skin truth, controlled freshness | fake splash explosion, plastic food, impossible condensation |
| broadcast_premium | program, channel, documentary series | category clarity, polished depth, restrained package graphics | generic TV template, fake lower thirds or channel logos |
| spatial_light_art | event, launch, exhibition, premium brand | light as a sculptural volume, clean darkness, architectural scale | random beams, overexposure, concert-light cliche |

## Type-To-Style Starting Matrix

These are starting points, not fixed presets.

| KV type | Strong starting styles | Common composition choices |
| --- | --- | --- |
| brand/corporate | documentary_truth, cinematic_epic, international_modernist | human_environment_manifesto, third_subject_negative_space, panoramic_horizon |
| event/conference | international_modernist, future_spatial, spatial_light_art | center_axis_monument, portal_depth, modular_grid |
| product launch | premium_product_minimal, luxury_material, technology_precision | product_pedestal, radial_core, minimal_object_field |
| automotive/industrial | luxury_material, industrial_engineering, cinematic_epic | product_pedestal, diagonal_force, panoramic_horizon |
| program/entertainment | broadcast_premium, entertainment_show, editorial_art_direction | layered_collage, modular_grid, asymmetric_editorial |
| culture/city | contemporary_culture, eastern_poetic, cinematic_epic | superscale_symbol, panoramic_horizon, cinematic_tableau |
| youth/sports | youth_kinetic, sports_impact, graphic_color_block | diagonal_force, graphic_shape_field, layered_collage |
| FMCG/beauty | sensory_fmcg, premium_product_minimal, fashion_image | macro_material_crop, product_pedestal, asymmetric_editorial |
| public/national | official_monumental, documentary_truth, contemporary_culture | center_axis_monument, human_environment_manifesto, superscale_symbol |

## Reference Research Rule

Use official brand/event/design case pages for complete systems and Behance/Pinterest/Dribbble for discovery only. A reference is useful only after it becomes a mechanism.

Preserve:

```text
composition_reference_source
style_reference_source
observed_composition_mechanism
observed_style_mechanism
transferable_rule
do_not_copy
```

Never copy exact typography, logo placement, campaign artwork, celebrity likeness, proprietary product render, sponsor system, or a studio's signature design.

## Required KV Composition Style Packet

```text
kv_composition_style_packet
communication_objective:
first_read:
second_read:
primary_composition:
supporting_geometry:
focal_hierarchy:
gaze_path:
visual_balance:
depth_model:
negative_space_logic:
typography_relationship:
crop_behavior:
image_density:
primary_style_family:
supporting_style_family:
palette_logic:
material_language:
lighting_model:
photographic_vs_graphic_balance:
realism_level:
surface_finish:
atmosphere_behavior:
anti_template_rule:
forbidden_style_drift:
composition_reference_source:
style_reference_source:
reference_mechanism_translation:
```

For a quick KV, the compact minimum is:

```text
first_read
primary_composition
focal_hierarchy
negative_space_logic
typography_relationship
primary_style_family
palette_logic
material_language
lighting_model
forbidden_style_drift
```

## Quality Gate

Reject the visual direction when:

```text
composition is only "居中、大气" without a focal hierarchy or gaze path
style is only adjectives without palette, material, light, density, and realism decisions
more than one primary composition competes for attention
more than one primary style family is mixed without a communication reason
the visual hook cannot be described in one sentence
title/logo/sponsor space is an afterthought
the composition works only in one crop but extensions are required
the style resembles a template, trend collage, or generic AI wallpaper
reference names are listed without transferable mechanisms
```

## Adaptation Order

```text
proposal / brief
-> kv_composition_style_packet
-> master_kv_layout_spec
-> asset_split
-> ratio adaptation
-> large-screen experience adaptation when needed
-> image prompts
-> post typography and delivery
```

The screen, platform, or ratio adapts the visual system. It does not define the visual system.
