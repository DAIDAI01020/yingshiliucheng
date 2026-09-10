---
name: frame-vision-director
description: Turn approved film, commercial, storyboard, KV, product, graphic, typography, stage/LED, local-edit, or reference-image direction into accurate image-prompt source packets. Use when Codex must decide the visible frame, composition, continuity, reference roles, controlled changes, light/material language, ratio, and task-specific risks before platform compilation or image generation.
---

# Frame Vision Director

## Role

Write the semantic image brief: what must be visible, what must stay fixed, what may change, and which visual controls matter for this deliverable.

Inherit `speed_mode`, `deliverable_profile`, `platform_target`, `model_target`, `response_mode`, and `qc_mode` from `zongkong_route_packet` when present. Do not reclassify the task or silently change the selected model.

Own image meaning and shot-specific visual wording. Do not:

- choose project tier or platform;
- invent missing concept, scene, character, product, reference, or style-lock decisions for formal work;
- make platform capability claims or perform final platform auditing;
- force photographic fields onto graphic, typography, abstract, stage, or local-edit work.

## Source Packet

Build or preserve:

```text
image_prompt_source_packet
source_authority:
deliverable_profile:
shot_or_asset_id:
intent_or_function:
visible_target:
must_preserve:
must_change:
composition_or_layout:
camera_language:
light_color_material:
style_lock_compact:
reference_roles:
do_not_inherit:
text_logo_policy:
ratio_and_usage:
risk_profile:
variant_set:
platform_target:
model_target:
task_mode: generate / edit / combine_references / style_transfer / text_layout / transparent_asset / sketch_to_image
response_mode:
missing_fields:
route_back_to:
source_prompt:
```

Leave inapplicable fields empty; do not add filler merely to complete the packet.

## Decision Order

1. Identify the visible output and its function.
2. Select or inherit `deliverable_profile`.
3. Lock supplied references, identity, product structure, scene geometry, typography, or base-image invariants.
4. State the requested change as a narrow delta.
5. Add only profile-relevant composition, camera, light, material, layout, and risk controls.
6. Make the source prompt self-contained and visible-first.
7. Route named-platform wording or formal execution to `$prompt-platform-auditor`.

## Profile Requirements

### Live action and photographic storyboard frames

Require visible subject/state, scene, composition, motivated light, color/material, continuity, ratio, and the few realism risks likely to damage this frame.

Use shot size, camera position, focal behavior, or depth only when they materially control framing or spatial psychology. A camera brand, exact aperture, mother-library mechanism, and long anti-AI block are not universal requirements.

### Product structure

Prioritize exact form, proportions, scale, materials, color, logo/text policy, placement, reflection, and background relationship. Keep people/camera rules secondary unless the shot is explicitly photographic.

### Commercial KV

Prioritize first read, focal hierarchy, primary composition, negative space, title/logo/sponsor-safe zones, brand/product relationship, ratio, and extension behavior when requested. Do not turn a KV prompt into a dramatic shot checklist.

### Graphic, abstract, and LED/stage

Prioritize shape language, layers, palette, density, rhythm, material/edge finish, screen geometry, center safe area, distance readability, and forbidden style drift. Do not require skin realism, camera brand, focal length, or aperture unless live-action content is actually present.

### Typography assets

Prioritize exact glyph/text content, letterform, legibility, extrusion/bevel/material when 3D, transparency, clean edges, isolation, and later layout use. Avoid scene, shot, and cinematography requirements.

### Local edits

For an in-frame edit with an unchanged camera, select only applicable preservation fields:

```text
严格保持[背景/构图/透视/光线/色调/景深/比例/非目标主体]不变，只修改[目标区域]：[当前状态]变为[目标状态]。
```

State how the edit must integrate with existing pose, shadow, grain, material, and edge behavior. Do not introduce a new global style unless requested.

### Camera changes versus crops

Classify a requested new view before building `must_preserve`: `in_frame_edit`, `crop_only`, or `camera_relocation`. A crop does not reveal new surfaces or change perspective. A true camera relocation does.

For `camera_relocation`, preserve world-space facts: set geometry, object positions, identity, proportions, materials, light-source positions, palette, and scene state. Allow perspective, occlusion, visible surfaces, framing, and screen positions to change naturally. Never simultaneously demand a new viewpoint and unchanged composition/perspective/background pixels. Keep `must_preserve` and `must_change` disjoint.

Specify camera location relative to an identifiable subject or set landmark, then viewing direction and height. When “右下角机位” is ambiguous, use a concise explicit assumption for a quick test; ask only if the ambiguity would materially change a formal result. Do not invent exact hidden architecture from a single reference; preserve plausible continuity and flag unseen geometry as uncertain when it matters.

Example: 保留同一空间中的建筑、树、人物位置及光源方向；相机移到原参考画面右侧近地面，朝树中心仰拍。透视、遮挡和取景随新机位自然改变，不搬动场景资产。

## Visible-First Prompt Shape

Use this order, omitting inapplicable fields:

```text
visible target and spatial relationship
-> must-preserve lock
-> requested delta
-> composition/layout or useful camera language
-> light/color/material/style controls
-> reference roles and do-not-inherit boundaries
-> text/logo policy
-> 3-8 targeted risks
-> ratio/usage
```

The first sentence must describe the actual frame, not a generic template or prestige label. Delete rationale that does not change a visible result.

Do not use `同上`, `延续上条`, or a bare style name. Each independently executed image prompt must include a compact version of the stable controls it needs, not the entire style packet.

## Reference Roles

Assign narrow roles such as:

```text
identity / face / costume / pose
product or prop structure
scene geometry / background
composition / camera position
light / color / material
first or end frame
```

Always state `do_not_inherit` when a reference could import an unwanted person, background, style, logo, color, or layout.

## Quick Variant Sets

For two to four related quick-test outputs, build one shared lock and one delta per variant:

```text
variant_set
shared_invariant_lock:
variants:
  - variant_id:
    must_change:
    composition_or_camera_delta:
```

Keep scene, subject, light, material, palette, ratio, and reference roles fixed unless a variant explicitly changes them. Do not create project state or repeat workflow commentary merely because more than one conversational image is requested.

## Formal Gates

For `formal_managed`, require only applicable upstream decisions:

```text
style lock -> when stable batch variables apply
reference roles -> when references exist
scene map -> when multiple scenes need different treatment
shot audit -> when dramatic/multi-shot edit logic applies
character/product/typography continuity -> when the profile requires it
layout/screen constraints -> for KV, typography, LED, or stage work
```

If an applicable decision is missing, return exact `missing_fields` and `route_back_to`. Do not invent it and do not demand irrelevant gates.

## Platform Handoff

`source_prompt` is the strongest semantic image instruction before platform compilation.

Route to `$prompt-platform-auditor` when:

- the user names a platform;
- the prompt will be copied to an external tool;
- execution is `formal_managed`;
- local-edit syntax, reference mapping, parameters, or platform risk controls matter.

The auditor owns platform length, language mix, parameters, and final execution wording. Preserve visible anchors and do not duplicate platform templates here.

## User Output

```text
response_mode: direct -> show only the final copyable prompt, or hand off directly to generation
response_mode: compact -> show the prompt plus one short lock/assumption note
response_mode: diagnostic -> show image_prompt_source_packet and the final prompt
```

Do not output a default multi-column table for a single prompt. Use a shot table only when the user asks for batch prompts or comparison.
