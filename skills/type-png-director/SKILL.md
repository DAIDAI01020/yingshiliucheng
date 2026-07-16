---
name: type-png-director
description: Create semantic prompt packets for exact-text typography assets, custom lettering, 3D title treatments, and transparent/isolated PNG words. Use when Codex must lock glyph content, reference-lettering roles, letterform, spacing, extrusion/bevel/material/light, alpha/edge behavior, post-layout use, and text risks before platform compilation; avoid copying protected logos or proprietary wordmarks without permission.
---

# Type PNG Director

## Role

Define the typography asset and its accuracy boundary. Inherit `deliverable_profile: typography_asset`, `platform_target`, `response_mode`, and `qc_mode` from `$zongkong` when present.

Own letterform/material/output semantics. `$prompt-platform-auditor` owns platform wording and parameters. Do not design a full KV/poster here.

## Safety Boundary

Use references for traits such as stroke skeleton, weight, terminals, spacing rhythm, extrusion, bevel, material, light, color, or mood.

Do not reproduce an exact protected logo, proprietary wordmark, official seal, or title lockup unless the user confirms permission. When ownership is unclear, create custom lettering inspired by the allowed traits.

## Required Inputs

```text
text_content: exact characters
language:
style_goal:
output_format: transparent PNG / alpha / isolated / keyable solid background
post_use:
size_or_ratio:
reference_roles when references exist
platform_target:
```

If exact `text_content` is missing, ask for it. Do not invent substitute characters.

## Source Packet

```text
type_png_prompt_source_packet
source_owner: type-png-director
deliverable_profile: typography_asset
text_content:
language:
letterform_and_spacing:
extrusion_bevel_depth:
material_and_surface:
light_and_shadow:
camera_or_perspective_when_3d:
reference_roles:
do_not_inherit:
output_format:
post_use:
size_or_ratio:
risk_profile:
platform_target:
response_mode:
source_prompt:
```

## Reference Roles

Name the allowed controls:

```text
glyph skeleton
stroke weight and terminals
spacing/alignment rhythm
extrusion/bevel/perspective
material and color
light/shadow
```

State that unrelated logo, background, full layout, symbols, or brand lockup must not be inherited.

## Text Accuracy

Put the exact string early:

```text
只生成准确文字“[TEXT]”；不得多字、少字、错字、假汉字、随机英文或额外符号。
```

For production-critical text, recommend a two-step route: use real vector/font glyphs for accuracy, then apply AI/3D styling, material, light, and texture.

## 3D Direction

When relevant, define front face, stroke width, spacing, extrusion depth, bevel radius, edge highlight, material, surface imperfections, light direction, shadow, camera/perspective, and silhouette edge. Omit these for flat lettering that does not need them.

## Transparent / Isolated Output

Request transparent alpha and a clean isolated silhouette. If the selected tool cannot guarantee alpha, request a plain keyable background, no touching-edge shadow, and clean separation for post extraction.

Do not generate a poster, mockup, scene, frame, watermark, or unrelated graphics around the asset.

## Platform Handoff

Send the source packet to `$prompt-platform-auditor`. The auditor selects built-in imagegen, Banana/Banana Pro, Midjourney, or layout/render wording and the smallest relevant risk set.

Do not duplicate platform templates here.

## User Output

```text
direct -> final copyable prompt only
compact -> prompt + one text-accuracy/production note
diagnostic -> source packet + audit result + final prompt
```

Use a table only for multiple title variants or a batch.

## Quality Gate

Reject or route back when text content, reference roles, isolation/alpha intent, material/construction for 3D type, or text-risk controls are missing. Reject a full-poster result or an unauthorized exact brand-wordmark copy.
