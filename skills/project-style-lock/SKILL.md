---
name: project-style-lock
description: Freeze approved visual decisions into reusable, deliverable-specific style variables for formal film and AI-visual projects. Use when multiple images/videos or regenerations must preserve an approved look, product structure, graphic system, typography treatment, stage/LED system, character continuity, or reference roles without re-inventing prompt wording each turn.
---

# Project Style Lock

## Role

Freeze only approved upstream decisions that must remain stable across multiple outputs or regenerations.

Inherit `speed_mode`, `deliverable_profile`, `platform_target`, `response_mode`, and `qc_mode` from `zongkong_route_packet` when present. Do not choose those values here.

Do not create a style lock for `prompt_only`, disposable `quick_test`, archive/review, or a single output with no continuity need unless the user explicitly asks to preserve the result as a project standard.

## Authority Boundary

Own stable project variables. Do not:

- invent a reference family or visual concept;
- choose shot function, scene geography, character identity, or product structure;
- perform final platform auditing;
- require mother-library, photographic realism, camera data, breath tails, or audio fields when the deliverable profile does not need them.

The platform target comes from `$zongkong` or the user. The correct order is:

```text
approved creative/reference decisions
-> project-style-lock
-> image/video prompt owner
-> prompt-platform-auditor
```

Never require `$prompt-platform-auditor` as an upstream source for creating the lock.

## Applicable Inputs

Use only the inputs that apply:

```text
approved concept/specialist direction
style-reference decision when an aesthetic reference system is needed
reference-image role analysis when reference images exist
scene map when multiple scenes need different treatment
character/product/typography continuity decisions when applicable
shot-language result when dramatic multi-shot logic applies
explicit user-approved direction
```

If an applicable upstream decision is missing in `formal_managed`, return exact `missing_fields` and `route_back_to`. Do not demand inapplicable packets to complete a template.

## Core Lock Packet

Preserve this compact core for every lock:

```text
style_lock_packet
style_id:
version:
status: draft / approved
upstream_source:
deliverable_profile:
platform_target:
mother_library_application_packet: when applicable
master_style_sentence:
palette_and_contrast:
composition_or_layout_rule:
material_or_surface_rule:
reference_roles:
do_not_inherit:
allowed_variation:
forbidden_drift:
profile_extension:
response_mode:
```

Keep `master_style_sentence` to one or two executable sentences. Translate visible mechanisms; do not store lists of prestige names or empty labels such as `高级感`, `电影感`, or `奥斯卡质感`.

## Profile Extensions

Add only the extension matching `deliverable_profile`.

### `live_action_people` or photographic `storyboard_frame`

```text
camera_language:
lens_or_depth_rule:
motivated_light_rule:
skin_fabric_environment_realism:
character_continuity:
```

Use a camera brand, focal length, or aperture only when it materially controls the image. Mother-library application is optional unless the formal project actually uses a reference system.

### `product_structure`

```text
product_structure_lock:
proportion_and_scale:
material_finish:
color_and_logo_policy:
reflection_and_background_rule:
```

Do not add skin, performance, or breath-tail fields.

### `commercial_kv`

```text
first_read_and_hierarchy:
primary_composition:
negative_space_logic:
title_logo_sponsor_zones:
style_family_and_density:
extension_rule_when_requested:
```

Camera language applies only to photographic KV content.

### `graphic_abstract`

```text
shape_language:
layering_and_density:
palette_boundary:
edge_texture_and_finish:
forbidden_graphic_drift:
```

Do not add photographic realism or cinematography requirements.

### `typography_asset`

```text
exact_text_or_glyph_source:
letterform_rule:
extrusion_bevel_material_when_3d:
transparency_and_edge_rule:
layout_usage:
```

### `led_stage`

```text
screen_geometry_and_ratio:
center_safe_area:
performer_presenter_safety:
distance_readability:
extension_and_loop_behavior:
```

### `local_edit`

```text
base_asset_lock:
target_region:
allowed_delta:
integration_rule:
non_target_preservation:
```

### `video_i2v` or `video_multi_shot`

```text
source_authority:
identity_scene_material_lock:
motion_style_compact:
ending_behavior_default:
audio_mode_default:
platform_drift_risks:
```

Do not store a universal breath tail or no-music sentence. Store `ending_behavior` and `audio_mode` only when approved for the project.

## Variation And Update Rules

Allow scene- or shot-level changes without changing the lock when they stay inside `allowed_variation`, such as location, time, local light direction, framing, camera position, emotion intensity, or a named edit delta.

Create a new lock version when changing project DNA, identity/product structure, palette boundary, graphic system, typography treatment, screen system, or another stable profile variable.

Do not update a global lock because one generation failed. Promote a QC finding only when:

```text
the upstream decision is proven wrong; or
the same platform failure repeats across at least two relevant outputs; or
the user explicitly approves the new rule.
```

## Handoff

Prompt owners inherit the compact core plus the applicable profile extension. They must not paste the entire lock packet into the user-facing prompt. Translate only the visible controls needed by the current output.

`$prompt-platform-auditor` may compact the lock for the target platform but must not change stable creative variables.

Hide the packet for `response_mode: direct`. For `compact`, show `style_id` and a one-line summary. Show the full packet only for `diagnostic` or formal state handoff.
