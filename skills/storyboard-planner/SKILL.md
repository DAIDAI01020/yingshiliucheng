---
name: storyboard-planner
description: Proposal-level cinematic storyboard planner for TVC ads, brand films, program promos, event openers, LED visuals, and AI generation. Use to create storyboards with shot number, duration, image description, client-facing proposal language, camera movement, subtitles or voiceover, music, AI generation notes, and image generation priority.
---

# Storyboard Planner

## Process

1. Use the approved concept, script, and visual style as source.
2. Split into proposal-level shots or chapters.
3. Keep every shot useful: information, emotion, reveal, transition, or rhythm.
4. For dramatic or short-drama sequences, audit shot logic with `$shot-language-auditor` before finalizing the table.
5. Write both production language and client proposal language.
6. Add AI generation notes only where the shot benefits from image or video generation.
7. Classify image generation priority before prompting.

## P1 No Lazy Handoff

For formal storyboard work, do not write random shot lists or let S/A shots go directly to generation.

Each S/A shot must preserve:

```text
upstream_source
shot_function
edit_motivation
reference_route
style_lock_source
prompt_priority
ai_risk
handoff_to_prompt
missing_fields
route_back_to
```

If shot function, edit motivation, reference route, or style source is missing, route back before `$frame-vision-director` / `$ai-video-prompt-director`.

## TVC Segment Storyboard Quick Route

Use this when the user asks for TVC广告故事板测试, 剧情包装广告故事板, 每一大段故事板, or 直接给 image 出故事板.

Default this route to `quick_test`. Do not rebuild the whole formal storyboard unless the user explicitly asks for 逐镜, 正式批量, 客户交付, 入项目状态, or QC.

Assume upstream director/prompt skills may already have decided:

```text
人物形象
服装状态
道具
产品/品牌露出
场景
风格
小分镜提示词
镜头 beat
```

In this route, preserve and organize those decisions. Do not redesign characters, props, products, scenes, or style.

Output one `tvc_segment_storyboard_lock` per large segment/chapter:

```text
tvc_segment_storyboard_lock
board_type: ad_sequence_board / design_reference_board / spatial_continuity_board
jimeng_direct_reference_board: true / false
segment_name:
segment_function:
upstream_source:
character_lock:
costume_lock:
prop_lock:
product_or_brand_lock:
scene_lock:
style_lock_compact:
character_model_sheet_cells:
hero_prop_or_product_cells:
set_design_cells:
color_palette_or_material_swatches:
key_beats: 4-8 visual beats
image_board_focus:
ending_or_brand_landing:
direct_video_reference_usage:
do_not_generate_layout_elements:
ai_risks:
handoff_to: scene-board-image-prompter
next_video_handoff: ai-video-prompt-director when the generated board will be uploaded to Jimeng/Seedance
```

Choose `board_type` by the upstream director's `recommended_board_type` first. If it is absent, infer it from the user's target:

```text
ad_sequence_board: like a TVC ad storyboard sheet, 6-12 large sequential frames, product/brand moments, character action, simple frame numbers, sparse caption zones. Use when the user wants the board itself to show the commercial story flow.
design_reference_board: like a production design guide, character design/model sheet, props/product cells, set design, color/material swatches, and a few key frames. Use when identity, props, costume, product, and environment must be locked before video.
spatial_continuity_board: like a video reference control board, main scene reference, overhead camera map, fixed character positions, eyelines, shooting execution flow, storyboard preview cells, lighting/material strip. Use when the next video model tends to lose people, positions, eyelines, or spatial continuity.
```

Do not split into a full shot-by-shot table unless the user asks for 逐镜. If they ask for 逐镜出图提示词, route S/A shots to `$frame-vision-director` instead.

When the user asks for 每个小分镜提示词, 单独小分镜出图, or 逐镜出图提示词 after a TVC segment board, output a lightweight `tvc_shot_prompt_handoff` before routing. This is still `quick_test` unless the user explicitly says 正式批量, 客户交付, 入项目状态, or QC.

```text
tvc_shot_prompt_handoff
source_segment_lock: tvc_segment_storyboard_lock
board_type:
jimeng_direct_reference_board:
segment_name:
shot_id:
source_key_beat:
shot_function:
prompt_priority: S / A / B / C
character_lock:
costume_lock:
prop_lock:
product_or_brand_lock:
scene_lock:
style_lock_compact:
composition_and_staging:
camera_and_lens:
lighting_and_material:
continuity_from_board:
image_prompt_focus:
ai_risks:
handoff_to: frame-vision-director
next_video_handoff: ai-video-prompt-director when the still frame will become Jimeng/Seedance first-frame or keyframe reference
```

The handoff must inherit characters, props, products, scene, style, and board type from the segment lock. Do not invent new wardrobes, props, product designs, set layouts, or visual style while creating the per-shot handoff.

## Output

| 镜号 | 时长 | 景别/机位 | 镜头功能 | 剪辑动机 | 画面描述 | 客户语言 | 镜头运动 | 字幕/旁白 | 音乐音效 | AI生成备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Then output:

| 镜号 | 优先级 | 是否出图 | 原因 | 推荐生成方式 | 风险 |
| --- | --- | --- | --- | --- | --- |

## Priority rules

- S: 核心视觉，必须出图，给3套风格方案。
- A: 关键产品、人物、空间、节目看点，建议出图。
- B: 辅助镜头，可按需要出图。
- C: 过场、信息、字幕、简单转场，通常文字描述即可。

## Defaults

- 15s: 4-6 shots.
- 30s: 6-10 shots.
- 60s: 10-16 shots.
- Program promos can use high-energy beats and reveal moments.
- LED visuals can use chapters and key frames instead of dense cuts.

## Quality bar

- Include enough detail for AI image prompt generation on S/A shots.
- Shot-size changes must be motivated by story information, action, gaze, sound, object, emotion, occlusion, or spatial transition.
- Do not use random CU/MS/WS coverage. Each shot must have a narrative function.
- Keep text overlays readable and not overloaded.
- Mention aspect ratio when it affects composition.
- Flag AI risks such as faces, hands, dense crowds, readable text, exact logos, and complicated multi-subject action.
