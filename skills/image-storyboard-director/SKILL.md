---
name: image-storyboard-director
description: Design director for standalone image storyboard boards. Use when the user asks for image故事板, 故事板设定板, production design storyboard board, 人物道具场景设定板, 人物动线机位图, or wants a board like character design + props + set design + overhead camera map + shooting execution flow + storyboard preview. This skill actively breaks the story into real directing units/scenes first, then creates character, costume, prop, scene, blocking, movement, camera, shot, lighting, and material design packets before scene-board-image-prompter writes built-in image prompts.
---

# Image Storyboard Director

## Core Role

`$image-storyboard-director` is the director layer for image storyboard boards across story, TVC, product ad, brand ad, program promo, event opener, brand film, and same-scene continuity work.

It is used after `$image-storyboard-workflow` decides that the task is an `image_storyboard_standalone_workflow`, and before `$scene-board-image-prompter` writes the built-in imagegen prompt.

This skill owns the creative setup:

```text
story premise
character design
relationship / conflict
costume and performance state
prop and object design
main set / location design
blocking and movement path
overhead camera map logic
shooting execution flow
shot preview list
lighting and material reference
video-reference inherit / do-not-inherit boundary
```

It does not generate images, write Banana prompts, or write Jimeng/Seedance motion prompts.

## Default Behavior

If the user provides only a theme, reference image, rough story, or scene title, design the missing production settings yourself. Do not block merely because characters, props, camera positions, or set details are absent.

For quick tests, invent a compact but coherent design packet from the available premise.

Only ask or route back when the request has no usable story function, subject, or scene target.

## Real Director Scene Breakdown Rule

Act like a real director before designing the board.

First split the material into shootable scene / beat units. Do not put a whole plot arc, several scene turns, or multiple camera-axis systems into one storyboard board.

For commercial and promo work, split by directing function, not by duration:

```text
TVC / brand ad: hook, problem setup, desire cue, product/brand reveal, benefit proof, emotional reaction, memory point, brand landing.
Product ad / product demo: product reveal, structure detail, hand/use action, functional proof, before-after, scale/context, hero ending frame.
Program promo: character/host reveal, competition object, conflict/high-energy beat, studio/stage geography, package identity, broadcast landing.
Event opener: theme symbol, countdown/ritual action, stage/LED spatial reveal, guest/presenter safety beat, final title/claim landing.
Brand film: human proof, real location, craft/process proof, emotional chapter, brand belief, final manifesto/object landing.
```

Each of these can become its own board unit when the location, axis, product/object interaction, blocking, or emotional function changes. A 15s ad can still need multiple boards; a longer scene can remain one board only when it is truly one continuous setup.

Duration is only a warning signal, not the main rule:

```text
one image storyboard board = one scene, one location setup, one camera-axis system, or one short dramatic/commercial beat unit
very short material may still need multiple boards if the location, axis, emotional turn, or action unit changes
longer material may stay one board only if it is truly one continuous scene unit with the same location, axis, blocking, and dramatic objective
when a story starts to contain multiple setup / confrontation / reveal / reversal / aftermath units, split it into multiple boards
```

Split whenever any of these change:

```text
location or set geography
time of day / light logic
character objective or emotional beat
camera axis / screen direction
blocking pattern or movement path
main prop interaction
scene function: setup / confrontation / reveal / reversal / aftermath / ending hook
```

The director must output a `director_scene_breakdown` before any board design:

```text
director_scene_breakdown
total_duration_estimate:
duration_note: time is advisory only; split by scene function, axis, blocking, and emotional turns first
board_unit_count:
board_units:
  - board_id:
    time_range:
    scene_or_beat_name:
    scene_function:
    character_objective:
    location_axis:
    blocking_pattern:
    characters_present:
    main_action:
    emotional_turn:
    prop_focus:
    camera_axis_change:
    keyframe_count:
    why_separate_board:
    handoff_to_design_packet:
```

Then create one `image_storyboard_design_packet` per `board_unit`. If the breakdown has multiple board units, present the board plan and continue with a multi-board series by default: each board unit gets its own design packet, prompt, and output image. Generate only one selected board when the user explicitly says to do only one selected board unit.

Never make one board that tries to summarize every moment of the story. A master design board may lock characters/props/set, but the actual narrative boards must be split by scene or beat.

Multi-board default:

```text
board_unit_count: 1 -> one design packet, one prompt, one board image.
board_unit_count > 1 -> one design packet per board_unit, one prompt per board_unit, one separate board image per board_unit.
```

Do not downgrade a multi-board series to a single crowded board because the user said "one workflow" or gave an example duration. "One workflow" means one controlled route; it does not mean one output image.

## Handoff Completeness Gate

Do not hand off to `$scene-board-image-prompter` until the selected board unit has a complete design packet.

The packet must include:

```text
director_scene_breakdown
board_id and time_range or beat_range
story_function
scene_function for the selected unit, not the whole plot
character_objective for each main character in this unit
emotional_turn for this unit
character_designs with continuity anchors
relationship_map
prop_designs with story roles
scene_set_design with geography
blocking_and_movement_path with start positions, arrows, eyelines, and hand/contact points
camera_map with axis, camera positions, shot numbers or shot roles, and whether axis changes
shooting_execution_flow with 4-6 clear beat cards when applicable, each with action + shot role + emotion
shot_preview_list with 4-8 continuity-safe preview frames when applicable, each tied to the same board_unit
lighting_material_reference
video_reference_inherit and video_reference_do_not_inherit when board may feed a video model
```

If any required field is missing, output:

```text
design_packet_status: blocked
missing_fields:
route_back_to: image-storyboard-director
next_action: complete the missing director decisions before prompt writing
```

Do not ask `$scene-board-image-prompter` to invent these fields.

## Must-Fail Examples

Return `design_packet_status: blocked` instead of handing off when:

```text
the packet describes the whole story but no selected board_unit
the board_unit has no scene_function or emotional_turn
characters are named but have no stable visual continuity anchors
three-or-more-character scenes have no fixed start positions, eyelines, or camera axis
the scene has a key object but no prop_design story role
shot_preview_list uses different rooms, different light logic, or different character placement across frames
video-reference use is implied but inherit / do-not-inherit boundaries are missing
```

## Required Packet

Always output or preserve:

```text
image_storyboard_design_packet
speed_mode: quick_test / formal_managed
board_type: production_design_storyboard_board / design_reference_board / spatial_continuity_board / ad_sequence_board / short_drama_scene_continuity_board
design_packet_status: complete / blocked
director_scene_breakdown:
board_id:
board_unit_count:
board_output_mode: single_board / multi_board_series / master_overview_only
multi_board_required: true / false
time_range:
storyboard_title:
scene_or_segment_name:
story_function:
genre_tone:
visual_premise:
character_designs:
  - id:
    role:
    age_body_face:
    costume:
    posture_performance:
    continuity_anchor:
relationship_map:
prop_designs:
  - prop:
    story_role:
    shape_material_scale:
    use_state:
scene_set_design:
  location:
  geography:
  entrances_exits_windows:
  furniture_or_stage_or_terrain:
  atmosphere:
blocking_and_movement_path:
  start_positions:
  movement_arrows:
  eyelines:
  handoff_or_contact_points:
camera_map:
  camera_axis:
  camera_positions:
  shot_numbers:
  lens_or_shot_size_logic:
shooting_execution_flow:
shot_preview_list:
lighting_material_reference:
video_reference_inherit:
video_reference_do_not_inherit:
missing_fields:
handoff_to: scene-board-image-prompter
```

## Board-Type Judgment

Use `production_design_storyboard_board` as the default when the user says image故事板 and expects the board itself to contain director decisions.

Use:

```text
production_design_storyboard_board
Default. Combines character design, props, set design, main scene reference, overhead camera map, shooting execution flow, key storyboard preview frames, and lighting/material reference.

design_reference_board
Use when the main need is character / costume / props / set style consistency, with fewer shot mechanics.

spatial_continuity_board
Use when the main risk is blocking, eyelines, movement path, camera axis, or video-model continuity.

ad_sequence_board
Use only when the user explicitly wants a sequence of commercial/promo beats more than a production design control board.

short_drama_scene_continuity_board
Use for same-scene dramatic coverage: master, reverse shots, over-shoulder, clean singles, reactions, inserts, and background-side locks.
```

## Design Rules

Build a board that a director, cinematographer, production designer, and AI image/video team can read.

Include these modules unless the board type clearly does not need one:

```text
Title / project area: mostly blank or simple, not dense readable text.
Hero scene frame: one main visual showing the dramatic or commercial situation.
Character design: front/side/back or 3-4 stable pose cells for each key character when useful.
Props: key object cells with shape, material, scale, wear, and use state.
Set design: room/stage/location geography, entrances, windows, furniture, terrain, or LED/stage zones.
Overhead camera map: character positions, prop positions, movement arrows, camera positions, eyelines, and axis.
Shooting execution flow: 4-6 beat cards showing action, shot size, camera feeling, and emotional change.
Storyboard preview: 4-8 key frames that prove continuity.
Lighting/material strip: practical light, window/stage light, skin, fabric, wood/metal/glass, dust, wear, or atmospheric reference.
```

Do not make a moodboard. Do not only output pretty frames. The board must solve design and blocking.

## Invention Boundaries

When inventing missing settings, stay inside the user's premise and reference intent.

Do:

```text
create character roles and appearances that serve the story function
choose props that create action or story evidence
design the scene geography so the camera map is shootable
assign camera positions with a reason
make movement arrows and eyelines readable
keep the same characters, props, and scene through all preview frames
```

Do not:

```text
change a supplied character identity, product, prop, brand object, or location
invent unrelated subplots
turn the board into a poster, KV, or marketing PPT
fill the board with tiny readable text
ask the image model to render exact long captions
let every preview frame become a different style or location
```

## Direct Video Reference Boundary

If the board will be uploaded to Jimeng/Seedance/Kling as one reference image, explicitly carry:

```text
video_reference_inherit: characters, costumes, props, scene/set/location, color, light, spatial relationship, movement path, eyelines, camera positions, and key action beats.
video_reference_do_not_inherit: white board layout, grid lines, frame numbers, arrows as physical objects, title bands, label boxes, note text, small captions, fake logos, and storyboard sheet itself.
```

## Handoff

Send the complete `image_storyboard_design_packet` to `$scene-board-image-prompter`.

The prompter must translate each packet into one built-in imagegen prompt and must not redesign the packet. When `board_unit_count > 1`, hand off all complete board-unit packets unless the user explicitly selects a single board unit or asks for a master overview only.

If the user later asks for single-frame images, route the selected `shot_preview_list` items to `$frame-vision-director`.

If the user asks to animate from the generated board, route to `$ai-video-prompt-director` with the direct video reference boundary.
