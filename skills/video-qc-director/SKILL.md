---
name: video-qc-director
description: Quality-control AI-generated videos for film AI workflows. Use after Jimeng, Seedance/Ark, Kling, or other image-to-video/video-redraw runs when checking motion accuracy, first-frame preservation, product structure, character consistency, camera stability, weather realism, breath tail, audio requirements, platform artifacts, and whether to reuse, revise, split, or route back upstream.
---

# Video QC Director

## Core Role

`$video-qc-director` reviews generated video outputs. It does not write a new creative concept, choose references, or submit generation.

It classifies the failure and produces a `qc_feedback_packet` for `$revision-director`, `$product-video-revision-director`, `$ai-video-prompt-director`, `$prompt-platform-auditor`, or `$project-state-manager`.

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
user/client feedback
```

If a managed project has `asset-index.json`, locate the source prompt, first frame, audit status, and run manifest before judging. If state is missing, output `missing_fields` instead of guessing.

## QC Checks

| Area | Check |
| --- | --- |
| first-frame preservation | face, product, costume, scene, material, color, light ratio stay stable |
| action clarity | one action is visible, staged, complete, not finished in one instant |
| camera behavior | camera follows the approved rule; fixed camera does not push, shake, zoom, or follow |
| product/vehicle | structure, proportions, wheel size, wheelbase, material, logo placement do not drift |
| character | no face drift, beauty rewrite, plastic skin, body distortion, costume morph |
| environment | no background melting, fake HDR, over-sharpening, CG clouds, light jumping |
| weather | no dissolve/fade sky swap; clouds, fog, shadow, brightness move physically |
| short-drama breath | each shot has light breath tail; segment/scene end has heavy 1-2s breath tail unless hard cut requested |
| audio | if prompt required it, only real environmental sound effects, no music or extra narration |
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

## Output Contract

Return this packet:

```text
qc_feedback_packet
asset_id:
source_generation_ready_packet:
qc_decision:
failure_type:
preserve:
revise:
route_back_to:
revision_instruction:
state_writeback:
```

For quick/test work, one short judgment is enough, but still name the failure type and next owner.

## Hard Rules

- Do not rewrite the whole visual style because one video failed.
- Do not route back to style/reference unless the failure proves the upstream visual decision is wrong.
- Do not blame the prompt if the generated video only needs a targeted motion/camera/weather correction.
- Do not approve product videos with wheel growth, body redraw, fake weather, or one-instant action completion.
- Do not approve cinematic/short-drama videos with face drift, beauty rewrite, HDR sharpening, light jumping, or missing required breath tail.
