---
name: video-qc-director
description: Quality-control AI-generated videos for film AI workflows. Use after Jimeng, Seedance/Ark, Kling, or other image-to-video/video-redraw runs when checking motion accuracy, first-frame preservation, product structure, character consistency, camera stability, weather realism, breath tail, audio requirements, platform artifacts, and whether to reuse, revise, split, or route back upstream.
---

# Video QC Director

## Core Role

`$video-qc-director` reviews generated video outputs. It does not write a new creative concept, choose references, or submit generation.

It classifies the failure and produces a `qc_feedback_packet` for `$revision-director`, `$product-video-revision-director`, `$ai-video-prompt-director`, `$prompt-platform-auditor`, or `$project-state-manager`.

## Route Authority Boundary

Inherit `deliverable_profile`, `response_mode`, `qc_mode`, route decisions, and project state from `$zongkong` when present.

This skill owns video QC diagnosis, failure attribution, and revision routing. It does not choose project tier, change `speed_mode`, approve missing formal gates, rewrite creative direction, or submit regeneration.

For formal work, locate prompt, first frame, audit status, run manifest, and asset-index records before judging when available. If they are missing, output `missing_fields` and `route_back_to` instead of guessing.

## Inputs

Use whatever is available:

```text
generated video path or description
first frame / reference image
approved video prompt
audited_prompt_packet
generation_ready_packet
run_manifest.json
project asset-index record
scene_continuity_lock / background_continuity_lock / continuity reference board
user/client feedback
```

If a managed project has `asset-index.json`, locate the source prompt, first frame, audit status, and run manifest before judging. If state is missing, output `missing_fields` instead of guessing.

## Inspection Evidence

Inspect actual video playback or temporally sufficient samples for each claimed visual finding; listen to audio before judging dialogue, music or sound effects. A contact sheet alone cannot verify continuous motion, lip-sync, flicker or audio. If a channel cannot be inspected, mark it unverified and limit the judgment; do not invent a full pass from metadata. Record the inspected time ranges and artifact version. A QC pass is not client selection.

## QC Checks

For a saved video, first create bounded technical evidence when FFmpeg is available:

```powershell
python scripts\technical_video_qc.py --video H:\project\video-runs\S03.mp4 --reference-first-frame H:\project\references\S03.png --output-dir H:\project\review\S03
```

Use the resulting JSON, sample frames, and contact sheet to inspect duration, codec, resolution, FPS, audio-stream presence/level, black intervals, freezes, and first-frame hash distance. Treat black/freeze findings as review flags because an intentional hold or cut may be valid. Audio presence does not prove music; music versus ambience/SFX remains a semantic listening decision.

| Area | Check |
| --- | --- |
| first-frame preservation | face, product, costume, scene, material, color, light ratio stay stable |
| action clarity | each approved beat/stage is visible, readable and complete; multi-shot action follows its intended order and timing |
| camera behavior | camera follows the approved rule; fixed camera does not push, shake, zoom, or follow |
| product/vehicle | structure, proportions, wheel size, wheelbase, material, logo placement do not drift |
| character | no face drift, beauty rewrite, plastic skin, body distortion, costume morph |
| environment | no background melting, fake HDR, over-sharpening, CG clouds, light jumping |
| same-scene continuity | same room, same wall/window/door/furniture, same prop positions, same background side, same eyeline/axis logic |
| weather | no dissolve/fade sky swap; clouds, fog, shadow, brightness move physically |
| ending behavior | output matches the approved hold / breath_light / breath_heavy / hard_cut / action_exit / loop intent |
| audio | output matches the approved unsupported / none / environment_only / dialogue / native_audio / reference_audio mode and the selected music policy |
| platform look | no short-video filter, web-drama soft glow, template motion, fake depth |

## Kling O1 / VIDEO 3.0 Omni QC

When the source platform is 可灵 O1, 可灵 Omni, Kling O1, Kling VIDEO 3.0 Omni, or Omini/Omni, compare the output against the audited reference role map before judging.

Check:

| Area | Check |
| --- | --- |
| reference role fidelity | each `@Image`, `@Element`, and `@Video` controls only its assigned role |
| identity / element lock | face, body, outfit, product structure, material, color, logo position, prop shape stay consistent |
| reference contamination | motion-reference video does not import the wrong person, scene, color, costume, or brand element |
| multi-subject integration | each named subject/element remains separate and performs only the assigned interaction |
| local edit boundary | only the requested target area changes; background, lens path, lighting, color, and other subjects are not repainted |
| start/end frame | start and end frames are respected without sudden morphing, jump cuts, or impossible interpolation |
| multi-shot storyboarding | every shot follows approved duration, framing, action, camera movement, and transition logic |
| native audio / voice | audio follows the approved requirement: none, environmental only, dialogue, or provided voice reference |

Failure types specific to Kling Omni:

```text
reference_role_confusion
element_identity_drift
reference_contamination
local_edit_overpaint
multi_subject_merge
start_end_interpolation_failure
storyboard_timing_failure
audio_requirement_mismatch
```

Route back by cause:

```text
reference role missing/conflicting -> prompt-platform-auditor
wrong upstream identity/style/source reference -> project-state-manager / project-style-lock
motion too complex or multi-shot overloaded -> ai-video-prompt-director
local edit polluted full frame -> prompt-platform-auditor
generated output good but needs exact change wording -> product-video-revision-director / revision-director
```

## QC Decisions

Use one decision:

```text
可用
可小修
定向重出
提示词需重写
前置导演判断错误
建议拆分
```

Routing:

```text
motion/camera/weather/product feedback -> product-video-revision-director when product/vehicle/mechanical
general video prompt issue -> ai-video-prompt-director
platform wording issue -> prompt-platform-auditor
missing first frame/run state -> project-state-manager / asset-librarian
shot logic wrong -> shot-language-auditor
style/reference wrong -> style-reference-director / scene-style-map-director / project-style-lock
```

## Same-Scene Background Continuity QC

Use this for short-drama same-scene video shots: 大景/全景、正反打、过肩、对视、反应、clean single、物件插入.

Compare the video to `background_continuity_lock`, the first frame, and any `short_drama_scene_continuity_board`:

```text
room does not change
wall/window/door/furniture positions stay fixed
practical light position and light direction stay fixed
props do not jump or disappear
A/B left-right relationship and eyeline direction remain valid
background side behind each character matches the coverage map
camera does not cross axis unless the upstream shot explicitly motivates it
```

Failure types:

```text
background_continuity_drift
axis_flip
eyeline_mismatch
prop_jump
light_position_drift
wrong_background_side
room_repaint
```

Route back by cause:

```text
prompt omitted background_continuity_lock -> ai-video-prompt-director / prompt-platform-auditor
first frame already has wrong background -> frame-vision-director / image-qc-director
coverage map or axis was missing/wrong -> short-drama-scene-director / shot-language-auditor
video model drifts despite correct first frame and prompt -> targeted regeneration with stronger first-frame preservation
```

## Output Contract

Return this packet:

```text
qc_feedback_packet
asset_id:
source_generation_ready_packet:
deliverable_profile:
qc_decision:
failure_type:
continuity_check:
  background_lock_match:
  axis_eyeline_match:
  prop_light_match:
  continuity_board_match:
preserve:
revise:
route_back_to:
revision_instruction:
state_writeback:
generation_observation:
```

For quick/test work, one short judgment is enough, but still name the failure type and next owner.

For formal QC or a repeated quick-test failure, write a `generation_observation` with inspected evidence and failure cause; record a successful fix only after inspecting the corrected output. Repeated evidence may support a targeted rule proposal, but applying a global style-lock change needs authorization for that scope. Keep diagnosis, proposed repair and verified repair distinct.

## Hard Rules

- Do not rewrite the whole visual style because one video failed.
- Do not route back to style/reference unless the failure proves the upstream visual decision is wrong.
- Do not blame the prompt if the generated video only needs a targeted motion/camera/weather correction.
- Do not approve product videos with wheel growth, body redraw, fake weather, or one-instant action completion.
- Do not approve cinematic/short-drama videos with face drift, beauty rewrite, damaging sharpening, light jumping, or a mismatch with the selected ending behavior.
- When `music_policy:no_music_allow_sfx`, do not approve unexpected background music, scoring, songs, or sung vocals; synchronized ambience and physical SFX remain allowed.
- Use the profile-specific checks only; do not impose live-action, product, breath, or audio requirements on unrelated deliverables.
