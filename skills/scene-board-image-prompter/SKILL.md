---
name: scene-board-image-prompter
description: Turn approved image-storyboard design packets, commercial segment locks, or short-drama scene-continuity locks into concise built-in imagegen board-prompt source packets. Use when characters, props/products, set geography, blocking, camera map, shot beats, lighting/material, board layout, and video-reference inherit/do-not-inherit rules are already decided and Codex must prepare one professional board image per board unit.
---

# Scene Board Image Prompter

## Role

Write the board image semantics after directing decisions exist. Inherit `$zongkong` and `$image-storyboard-workflow` route packets, including `speed_mode`, `response_mode`, `qc_mode`, and board variant.

Own one board prompt source per approved `board_unit`. Do not choose story, character, prop/product, scene style, blocking, camera axis, shot logic, or video motion.

Default platform is `built_in_image`. Route final language to `$prompt-platform-auditor`; do not maintain a separate built-in platform policy here.

## Read References On Demand

- Board preflight, common layout, text rules, and multi-board behavior: read [references/board-preflight-and-layout.md](references/board-preflight-and-layout.md).
- Production-design, commercial segment, ad-sequence, design-reference, or spatial-control boards: read [references/production-and-commercial-boards.md](references/production-and-commercial-boards.md).
- Short-drama same-scene/background continuity boards: read [references/same-scene-continuity-board.md](references/same-scene-continuity-board.md).

Load only the selected board variant.

## Required Authority

Use one:

```text
image_storyboard_design_packet
tvc_segment_storyboard_lock
scene_continuity_lock + background_continuity_lock
selected board_unit from an approved workflow packet
```

Use upstream data for characters, costumes, props/products, set, positions, movement path, camera map, eyelines, shot beats, light/material, continuity, and video-reference boundaries. If applicable decisions are missing, return `missing_fields` and `route_back_to` rather than inventing them.

## Board Variants

```text
production_design_storyboard_board
commercial_segment_board
ad_sequence_board
design_reference_board
spatial_continuity_board
short_drama_scene_continuity_board
master_overview_only
```

Choose from the upstream workflow. Do not combine several variants into a crowded universal board.

## Multi-Board Rule

```text
one board_unit
-> one pre_generation_check
-> one board_prompt_source_packet
-> one platform-compiled prompt
-> one board image
```

When `board_unit_count > 1`, output a series. Do not collapse units into one image unless the user explicitly requests `master_overview_only`.

## Preflight

Before final prompt or generation, preserve:

```text
pre_generation_check
status: passed / failed
board_id:
board_variant:
source_packet_present:
board_unit_clear:
required_sections_present:
continuity_controls_present:
video_reference_boundary_present:
generation_allowed:
missing_fields:
route_back_to:
```

Read [references/board-preflight-and-layout.md](references/board-preflight-and-layout.md) for variant-specific requirements. A failed check stops prompt compilation and generation.

## Source Packet

```text
board_prompt_source_packet
source_owner: scene-board-image-prompter
board_id:
board_variant:
deliverable_profile: storyboard_frame
platform_target: built_in_image
visible_board_goal:
must_preserve:
must_change:
sections_and_layout:
character_prop_set_locks:
blocking_camera_eyeline_locks:
shot_or_beat_cells:
lighting_material_cells:
text_and_label_policy:
video_reference_inherit:
video_reference_do_not_inherit:
content_risk_profile:
ratio:
response_mode:
source_prompt:
```

## Board Prompt Principles

- Make the board look like a professional production control artifact, not a poster or marketing PPT.
- Use large parseable visual cells, clear hierarchy, white/light-gray board space, simple numbers/arrows, and blank label bands.
- Do not ask imagegen for dense readable text, brand marks, legal copy, or long annotations.
- Lock identity, product/prop structure, set geography, positions, eyelines, camera axis, light direction, and continuity only when the selected board needs them.
- Apply photographic realism controls only to photographic preview/reference cells. Do not force skin/dust/camera realism onto diagrams, graphic cells, typography bands, or abstract boards.
- If a board will feed a video model, explicitly separate content to inherit from board layout artifacts to ignore.

## Video Reference Boundary

When the whole board is uploaded as a video reference:

```text
inherit: assigned characters, costumes, props/products, set/stage, spatial relation, light/color/material, selected beats, positions, eyelines, camera-direction logic
do_not_inherit: board background, grid lines, frame numbers, arrows, title/label bands, note areas, small text, fake logos, storyboard sheet itself
```

Do not ask a video model to animate the entire board unless the user explicitly wants a board animatic. Select one scene or beat target downstream.

## Platform And Generation Handoff

Send passed source packets to `$prompt-platform-auditor` with `platform_target: built_in_image`.

If the user requested direct image output and the audit/preflight passed, continue to `$builtin-imagegen-director` and built-in imagegen. Do not stop at prompt-only output unless the user asked for prompts.

For successful built-in generation, end with the image result. QC follows `qc_mode` and never appears after the image in the same response.

## User Output

```text
direct -> final prompt or generated board only
compact -> one-line preflight result + final prompt/artifact
diagnostic -> preflight + source packet + audit result
```

For a multi-board series, repeat only the compact block per `board_id`. Avoid repeating shared workflow explanation.

## Hard Rules

- Do not redesign upstream decisions.
- Do not compress multiple board units into one image.
- Do not write Banana cell prompts or video-motion prompts here.
- Do not generate dense readable board text.
- Do not use a universal anti-AI block across all cell types.
