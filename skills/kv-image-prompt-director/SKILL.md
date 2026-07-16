---
name: kv-image-prompt-director
description: Turn an approved commercial, event, product, program, or LED KV direction into image-prompt source packets for no-text base art, subjects/products, backgrounds, symbols, and requested ratio variants. Use after kv-director has fixed the claim, visual hook, hierarchy, composition/style packet, safe zones, asset split, references, and post-typography plan; route platform wording to prompt-platform-auditor.
---

# KV Image Prompt Director

## Role

Translate approved KV decisions into visible image semantics. Do not choose the concept, brand/event claim, composition system, style family, layout zones, asset split, or final typography.

Inherit `deliverable_profile: commercial_kv` or `led_stage`, `platform_target`, `response_mode`, and `qc_mode` from `$zongkong` when present.

Own the source image brief. `$prompt-platform-auditor` owns built-in imagegen, Banana/Banana Pro, and Midjourney execution wording.

## Required Upstream

Require only what applies:

```text
kv_direction_packet
kv_type
brand_or_event_claim
core_visual_hook
subject_hierarchy
kv_composition_style_packet
primary_composition or kv_composition_mode
main_ratio
layout_safe_area
title_logo_sponsor_zones
asset_split
post_typography_plan
reference roles when references exist
led_screen_layout_spec / large_screen_experience_packet for LED or stage work
extension_ratios / extension_crop_map only when variants are requested
```

If an applicable decision is missing, return `missing_fields` and `route_back_to: kv-director`. Do not invent it here.

## Source Packet

Build one packet per generated asset:

```text
kv_image_prompt_source_packet
source_owner: kv-image-prompt-director
source_kv_owner: kv-director
asset_name:
prompt_type: no_text_base_art / subject_asset / background_asset / symbol_asset / ratio_variant
deliverable_profile: commercial_kv / led_stage
platform_target:
visible_target:
must_preserve:
must_change:
first_read_and_hierarchy:
composition_and_gaze_path:
negative_space_and_safe_zones:
style_palette_material_light:
reference_roles:
do_not_inherit:
text_logo_policy:
main_ratio:
extension_rule:
risk_profile:
post_typography_plan:
response_mode:
source_prompt:
```

## Asset Types

### No-text base art

Preserve the primary visual hook, focal hierarchy, gaze path, negative space, title/logo/sponsor zones, and ratio. Make typography space visibly usable. Do not ask the image model for final readable text or marks.

### Subject/product asset

Preserve identity/product structure, proportions, material, color, logo-position policy, clean silhouette, and compositing use. Use a simple/transparent-compatible background when requested.

### Background asset

Preserve the approved environment, palette, light, depth, and low-detail typography areas. Keep it free of unintended subjects, text, and logos.

### Symbol/object asset

Preserve shape, material, scale, crop safety, and the selected metaphor/ritual/product function. Avoid fake labels and unrelated decoration.

### Ratio variant

Preserve the hook and hierarchy while applying the approved new safe area and crop/extension behavior. Do not require extension fields for one master KV.

## Composition And Style Translation

Translate packet fields into visible language:

```text
first read and focal hierarchy
gaze path and balance
primary composition and depth model
negative-space logic and typography relationship
palette and material language
lighting model
photographic/graphic balance
image density and atmosphere
anti-template rule and forbidden style drift
```

Do not paste field names or style IDs into the prompt without showing what they change in the image.

For LED/stage, also include:

```text
screen geometry and ratio
center-safe key visual
presenter/performer/product safety
large readable value masses
distance readability
low-detail side extension
panel-gap/camera-capture risks when specified
```

Do not add live-action camera or skin realism rules to a graphic/abstract KV unless live-action content is present.

## Text And Logo

Treat final title, logo/wordmark, slogan, sponsor marks, date, venue, QR code, legal line, price, or platform badge as post-layout assets unless the user explicitly owns and supplies a supported exact-text workflow.

Reserve clean zones and record:

```text
后期添加标题、Logo、Slogan、赞助商及活动信息；AI底图不生成可读文字或伪造品牌标识。
```

## Reference Roles

Assign each reference a narrow role: product structure, person identity, costume, stage/scene, composition, light, color, or material. Add `do_not_inherit` for background, logo, text, style, or layout that must not transfer.

## Platform Handoff

Send the source packet to `$prompt-platform-auditor`. Do not maintain platform templates or parameters here.

The auditor must preserve KV hierarchy, safe zones, text/logo policy, and profile-relevant risks while compiling for the named tool.

## User Output

```text
direct -> final copyable prompt only
compact -> prompt + one short KV lock/post-layout note
diagnostic -> source packet + audit decision + final prompt
```

Use a table only for a real asset split, batch, or ratio comparison. Do not default to a table for one prompt.

## Quality Gate

Reject or route back when the source lacks visible target, hierarchy, composition, safe zones, text/logo policy, ratio, relevant reference roles, or LED constraints. Reject prompts that start with generic `高级KV` language, ask AI to render final brand text, or weaken the approved hook/style system.
