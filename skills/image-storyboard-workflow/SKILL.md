---
name: image-storyboard-workflow
description: Own the standalone workflow for image storyboard boards under zongkong. Use when the user asks for image故事板, 广告故事板, 大段故事板, 直接给 image 出故事板, production design storyboard board, 角色道具场景设定板, 人物动线机位图, 空间连续性控制板, 同场戏背景连续性参考板, or a storyboard/reference board that will be uploaded to Jimeng/Seedance. Decide source_type, board_type, whether a director design packet is needed, direct-video-reference boundaries, and route to image-storyboard-director, storyboard-planner, scene-board-image-prompter, frame-vision-director, or ai-video-prompt-director without replacing their execution roles.
---

# Image Storyboard Workflow

## Core Role

`$image-storyboard-workflow` is the owner for image storyboard board routing.

It sits below `$zongkong` and above the execution skills:

```text
zongkong
-> image-storyboard-workflow
-> image-storyboard-director / storyboard-planner / scene-board-image-prompter / frame-vision-director / ai-video-prompt-director
```

It decides the board workflow. It does not write final image prompts, video prompts, or generate images.

## Standalone Workflow Rule

Treat `image故事板` as its own workflow, not as a TVC-only sub-route and not as a generic storyboard thumbnail route.

This workflow includes:

```text
TVC ads
product ads / product demos
brand ads / brand films
program promos
event openers
commercial story scenes
short-drama same-scene continuity boards
standalone production-design storyboard boards
```

When a commercial or product request asks for `image故事板`, keep it in this workflow. The workflow must let the director split the material into board units first, then produce one board image per required board unit. Do not route commercial boards away merely because the source is TVC/product advertising.

Default route:

```text
zongkong
-> image-storyboard-workflow
-> image-storyboard-director
-> scene-board-image-prompter
-> built-in imagegen
```

Use this route when the user expects the board to include director decisions: characters, costumes, props, set/location, spatial geography, character movement path, eyelines, overhead camera map, shooting execution flow, key storyboard preview frames, lighting, and material references.

Only use `storyboard-planner` before the director when the user specifically asks for a large commercial segment, chapter beat整理, TVC大段故事板, or a shot list extracted from a longer script. Even then, `storyboard-planner` only provides the upstream segment/beat lock; `$image-storyboard-director` still owns the final board-unit split and production board design.

`$image-storyboard-director` must actively split the material into real directing units before board design. Split by scene function, location/set geography, camera axis, blocking/movement path, prop interaction, and emotional turns. Duration is only advisory; do not hard-cut by a fixed second count, and do not compress several directing units into one board.

## Run-Through Contract

The workflow is not allowed to jump directly from a user story to built-in imagegen.

Every run must pass these artifacts in order:

```text
1. zongkong_route_packet
2. image_storyboard_workflow_packet
3. director_scene_breakdown
4. image_storyboard_design_packet for each required board_unit
5. scene-board-image-prompter pre_generation_check for each required board_unit
6. one built-in imagegen prompt per passed board_unit
7. built-in imagegen only after that board_unit pre_generation_check: passed
```

Direct image execution rule:

```text
If the user asked for direct image output rather than prompt-only output, a passed `scene-board-image-prompter` pre_generation_check is the permission to call built-in imagegen. Do not treat the built-in imagegen prompt as the final deliverable unless the user asked only for prompts, the precheck failed, or a missing field routes back to an owner skill.
```

If any artifact is missing, route back to the owner instead of generating:

```text
missing image_storyboard_workflow_packet -> route_back_to: image-storyboard-workflow
missing director_scene_breakdown or image_storyboard_design_packet -> route_back_to: image-storyboard-director
missing required board sections or prompt constraints -> route_back_to: scene-board-image-prompter
```

If the director splits the material into multiple board units, do not silently merge them into one crowded board. Set `multi_board_required: true`, output the board-unit plan, and prepare/generate one separate board prompt/image per board unit by default. Only make a single master overview board when the user explicitly asks for a single master board, and label it as an overview, not as the actual narrative board series.

## Regression Dry Run

When changing this workflow or checking whether it still runs correctly, use:

```text
references/regression-self-test.md
```

The self-test is a dry run. It must prove the chain reaches `pre_generation_check: passed` before any imagegen call. Do not use image generation during the self-test.

## Required Packet

Always output or preserve this compact packet before handoff:

```text
image_storyboard_workflow_packet
speed_mode: quick_test / formal_managed
workflow_variant: standalone_director_board / large_segment_board / single_shot_handoff / video_reference_handoff / same_scene_continuity_board
director_design_required: true / false
generation_allowed_before_precheck: false
source_type: standalone_storyboard / tvc / product_demo / program_promo / event_opener / brand_film / short_drama_scene_continuity / other_commercial
board_type: production_design_storyboard_board / ad_sequence_board / design_reference_board / spatial_continuity_board / short_drama_scene_continuity_board
board_output_mode: single_board / multi_board_series / master_overview_only
multi_board_required: true / false
board_unit_count:
board_generation_plan:
  - board_id:
    board_title:
    source_type:
    board_type:
    output_image_required: true / false
    prompt_required: true / false
    depends_on:
jimeng_direct_reference_board: true / false
upstream_source:
segment_or_scene_name:
segment_function:
character_lock:
costume_lock:
prop_lock:
locked_object: product / brand object / program object / event symbol / real-location anchor / scene prop
scene_lock:
style_lock_compact:
key_beats:
required_board_sections: character_design / costume_design / prop_design / set_design / main_scene_reference / movement_path / overhead_camera_map / shooting_execution_flow / storyboard_preview / lighting_material_reference
director_scene_breakdown:
video_reference_inherit:
video_reference_do_not_inherit:
missing_fields:
handoff_path:
next_skill:
```

For `quick_test`, fill the packet from available upstream material and mark missing fields only when they block the board. For `formal_managed`, missing upstream decisions must route back to the owning director.

## Speed Mode

Default to `quick_test` for:

```text
image故事板
人物道具场景设定板
人物动线机位图
production design storyboard board
TVC广告故事板测试
剧情包装广告故事板
每一大段故事板
直接给 image 出故事板
先做一张参考板
先喂即梦/Seedance试一下
```

Use `formal_managed` only when the user says:

```text
正式项目
批量
客户交付
入项目状态
QC
写manifest
继续项目目录
```

Do not add formal state gates to quick tests.

## Source Type

Choose `source_type` before choosing `board_type`.

```text
standalone_storyboard: a self-contained production board where the workflow/director must invent or lock characters, props, set, movement, camera map, and shot preview logic before image generation.
tvc: product ad, brand ad, commercial story, usage scene, before/after, product benefit, TVC rhythm.
product_demo: product structure, product use, vehicle/mechanical/object demonstration, controlled action proof.
program_promo: program promo, variety package, episode promo, host/guest/contestant, stage/studio, competition object, broadcast landing.
event_opener: event opener, launch opener, gala/forum opener, theme reveal, stage/LED geography, countdown, ritual moment.
brand_film: brand film, corporate/city film, real people, real location, proof object, brand belief, chapter emotion.
short_drama_scene_continuity: same-scene background lock, reverse-shot background control, eyeline/over-shoulder/dialogue coverage board.
other_commercial: commercial/promo work that does not cleanly fit the above.
```

Use the upstream specialist director's recommendation when present. If it conflicts with the user's current target, preserve both and state the reason for the final choice.

## Board Type

Choose one board type:

```text
production_design_storyboard_board
Default for standalone image故事板. Use when the board must contain a director-designed package: character design, costume, props, set design, main scene reference, overhead camera map, movement path, eyelines, shooting execution flow, shot preview cells, and lighting/material strip.

ad_sequence_board
Use when the board itself must show the flow: 6-12 readable commercial/promo beats, product use, program hook, reveal sequence, event countdown, brand chapter flow.

design_reference_board
Use when the main risk is consistency: character, costume, props, product, program object, stage/set/location, color/material, package identity, or 3-6 key design frames.

spatial_continuity_board
Use when the video model may lose space: multi-person blocking, eyelines, table/stage positions, camera axis, movement path, continuity-sensitive action.

short_drama_scene_continuity_board
Use only for short-drama same-scene coverage: master wide, reverse shots, over-shoulder, clean singles, reactions, prop inserts, background-side map.
```

Do not use poster, KV, or marketing-page language for a storyboard board. If the user wants a main visual, poster, or KV, route back to `$kv-director` or `$poster-director`.

## Direct Video Reference Boundary

Set `jimeng_direct_reference_board: true` when the generated board will be uploaded as one reference image to Jimeng/Seedance.

Fill:

```text
video_reference_inherit: characters, costume, props/product/program objects/event symbol, scene/set/stage/location, color, light, spatial relationship, key action beats
video_reference_do_not_inherit: white board layout, grid lines, frame numbers, arrows, title band, label boxes, note areas, small text, fake logos, storyboard sheet itself
```

For first-frame extraction, keep the same boundary but route to `$frame-vision-director` for a clean still frame instead of asking the video model to animate the whole board.

## Handoff Routes

Use these routes:

```text
standalone image storyboard:
image-storyboard-workflow -> image-storyboard-director director_scene_breakdown + image_storyboard_design_packet(s) -> scene-board-image-prompter one prompt per board_unit -> built-in imagegen one image per passed board_unit

large segment board:
image-storyboard-workflow -> storyboard-planner tvc_segment_storyboard_lock -> image-storyboard-director director_scene_breakdown + image_storyboard_design_packet(s) -> scene-board-image-prompter one prompt per board_unit -> built-in imagegen one image per passed board_unit

direct board prompt when all scene/character/prop/camera decisions already exist:
image-storyboard-workflow -> scene-board-image-prompter -> built-in imagegen

single-shot image prompts after a segment board:
image-storyboard-workflow -> storyboard-planner tvc_shot_prompt_handoff -> frame-vision-director

video prompt from a generated board or uploaded board:
image-storyboard-workflow -> ai-video-prompt-director

short-drama same-scene continuity board:
image-storyboard-workflow -> short-drama-scene-director scene_continuity_lock -> scene-board-image-prompter
```

If the task already contains a valid `tvc_segment_storyboard_lock`, `scene_continuity_lock`, or `tvc_shot_prompt_handoff`, do not rebuild it. Attach the workflow packet and continue to the next skill.

## Missing Fields

For quick tests, only block on missing fields that make the board impossible:

```text
no segment/scene function
no story premise, subject, or scene target that lets the director design the board
no board target when the user asks for direct video reference
```

For formal managed boards, route back when upstream decisions are missing:

```text
specialist director recommendation
scene/style map
shot logic for dramatic or multi-shot work
project-style-lock when batch output is requested
prompt-platform-auditor before execution
```

## Output Contract

Reply with:

```text
image_storyboard_workflow_packet
[filled packet]

handoff:
next_skill:
why:
```

Then invoke or hand off to the next skill. Keep the explanation short; this skill is a router and workflow owner, not a proposal writer.

When `next_skill` ultimately returns `pre_generation_check.status: passed` and the original user intent was direct image generation, continue to built-in imagegen instead of ending the turn with only the prompt.
