# Image Storyboard Workflow Regression Self-Test

Use this file when checking that the standalone image故事板 workflow still runs through the required director path. This is a dry run only; do not call imagegen during the test.

## Test Input

```text
用户请求：做一张 image故事板，后面整张喂给 Seedance。场景是三个人在办公室圆桌边对峙：年长女人终于承认秘密，中年男人沉默，年轻女人震惊，桌上有一只白瓷杯作为关键道具。需要防止视频里人物消失、位置错、视线错。
```

## Expected Route

```text
zongkong_route_packet
-> image_storyboard_workflow_packet
-> image-storyboard-director director_scene_breakdown
-> image-storyboard-director image_storyboard_design_packet for selected board_unit
-> scene-board-image-prompter pre_generation_check
-> built-in imagegen prompt only if pre_generation_check: passed
```

## Expected Workflow Packet

```text
speed_mode: quick_test
workflow_variant: standalone_director_board
director_design_required: true
generation_allowed_before_precheck: false
source_type: standalone_storyboard
board_type: production_design_storyboard_board or spatial_continuity_board
jimeng_direct_reference_board: true
required_board_sections: character_design / costume_design / prop_design / set_design / main_scene_reference / movement_path / overhead_camera_map / shooting_execution_flow / storyboard_preview / lighting_material_reference
next_skill: image-storyboard-director
```

## Expected Director Output

The director must output:

```text
director_scene_breakdown
board_unit_count: at least 1
board_units include scene_function, location_axis, characters_present, main_action, emotional_turn, prop_focus, why_separate_board
```

For the selected board unit, the design packet must include:

```text
design_packet_status: complete
story_function
character_designs with continuity anchors for all three people
relationship_map
prop_designs for the white cup
scene_set_design with round table / room geography / doors or windows / light sources
blocking_and_movement_path with fixed start positions, eyelines, arrows
camera_map with axis and camera positions
shooting_execution_flow with 4-6 beat cards
shot_preview_list with 4-8 continuity-safe frames
lighting_material_reference
video_reference_inherit
video_reference_do_not_inherit
```

## Expected Precheck

```text
pre_generation_check
status: passed
source_packet_present: image_storyboard_design_packet
board_unit_clear: true
director_scene_breakdown_present: true
all required_sections_present: true
all continuity_controls_present: true
video_reference_boundary_present: true
generation_allowed: true
```

## Failure Cases

The workflow fails if any of these occur:

```text
imagegen is called before pre_generation_check: passed
storyboard-planner is used for standalone image故事板 without a large-segment reason
the director skips director_scene_breakdown
one board tries to summarize several scene functions or emotional turns
there is no overhead camera map
three characters do not have fixed positions and eyelines
the white cup is not anchored as a prop
video_reference_inherit / video_reference_do_not_inherit are missing
the prompter invents characters, props, scene geography, or camera positions instead of inheriting the design packet
```

## Commercial Multi-Board Test Input

```text
用户请求：做一个产品广告 image故事板，后面要给 Seedance 做视频参考。产品是一款户外运动水壶，广告包含城市通勤痛点、产品结构揭示、登山使用证明、夜间露营情绪反应、品牌落点。导演要帮我拆场，不要全部放在一张图上。
```

## Expected Commercial Route

```text
zongkong_route_packet
-> image_storyboard_workflow_packet
source_type: product_demo or tvc
board_output_mode: multi_board_series
multi_board_required: true
-> image-storyboard-director director_scene_breakdown
board_unit_count: greater than 1
-> one image_storyboard_design_packet per board_unit
-> scene-board-image-prompter one pre_generation_check per board_unit
-> one built-in image prompt per passed board_unit
-> one output image per passed board_unit
```

## Expected Commercial Split

The director should split by advertising/directing function, for example:

```text
Board 01: city commute problem / hook
Board 02: product reveal and structure
Board 03: outdoor use proof
Board 04: emotional reaction / lifestyle moment
Board 05: brand landing / final memory frame
```

Exact count may change with the premise, but `board_unit_count > 1` must produce separate board prompts/images. The workflow fails if the product reveal, use proof, emotional reaction, and brand landing are compressed into one board image.
