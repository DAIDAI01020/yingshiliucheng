# Packets And Gate Ownership

Use this reference for `formal_managed` intake, missing-field routing, gate applicability, managed execution, and cross-skill handoffs.

## Contents

- Project intake
- Gate ownership
- Director contribution
- Prompt and generation packets
- Missing-field behavior

## Project Intake

Create or check `project_intake_packet` only for `formal_managed` work or when the user explicitly requests formal state.

```text
project_intake_packet
project_tier: formal / quick / misc
project_folder_contract:
output_path_rule:
workflow_mode:
deliverable_type:
deliverable_profile:
main_line: commercial_promo / short_drama_story / other
reference_source: user_reference_image / user_named_reference / mother_library_recommendation / existing_project_lock / none
platform_target:
required_upstream:
available_upstream:
missing_fields:
next_skill:
speed_mode: formal_managed
response_mode: direct / compact / diagnostic
qc_mode: none / light_deferred / formal
```

Do not create this packet for `prompt_only` or `quick_test` unless the user asks to establish managed state.

For managed short-drama work, use `$project-state-manager` to initialize/check state before formal prompt writing, regeneration, or execution. Resolve any direct state command from the `$project-state-manager` skill directory. The script may return `missingFields` and `routeBackTo`; normalize them at the state boundary to `missing_fields` and `route_back_to` before downstream handoff.

## Gate Ownership

| Gate or missing decision | Applies when | Owner / `route_back_to` |
| --- | --- | --- |
| project folder contract / output path | managed project, multiple saved files, scattered files | `$project-folder-director` |
| managed project state | formal managed production | `$project-state-manager` |
| concept / brand claim / story premise | not yet approved | matching concept or specialist director |
| hook audit | formal short-drama opening/episode retention | `$short-drama-episode-writer` |
| character continuity | recurring short-drama characters | `$short-drama-character-bible` |
| reference family / mother-library application | formal visual direction | `$style-reference-director` / `$reference-visual-library` / `$reference-aesthetic-director` |
| reference-image role boundaries | user reference images exist | `$reference-image-style-matcher` |
| scene-level style differences | multi-scene or location-specific visual treatment | `$scene-style-map-director` |
| scene/background continuity lock | same-scene multi-shot coverage | `$short-drama-scene-director` or relevant scene owner |
| shot function / edit motivation / axis | dramatic or multi-shot work | `$shot-language-auditor` |
| shot production state / dependency / legal transition | formal multi-shot or episodic execution | `$project-state-manager`, with shot decisions supplied by `$short-drama-director` and scene/shot owners |
| stable batch visual variables | approved style must persist across a batch | `$project-style-lock` |
| KV master-to-rendition matrix / safe areas | one approved KV must ship in multiple ratios | `$kv-director` |
| image execution wording | approved image/keyframe direction exists | `$frame-vision-director` or the applicable image prompt owner |
| video execution wording | approved motion/shot direction exists | `$ai-video-prompt-director` |
| platform execution audit | formal execution or external platform handoff | `$prompt-platform-auditor` |
| generation-ready job | managed execution | `$project-state-manager` plus the applicable generation controller |
| image/video result diagnosis | output exists | `$image-qc-director` / `$video-qc-director` |

Do not route a missing hook audit to a prompt skill. Do not route missing character continuity to the scene map or platform auditor.

## Applicability Rules

```text
formal commercial KV
-> intake when managed + approved claim/composition + reference/style decision when needed + platform audit + generation-ready
-> no hook audit or character continuity unless the concept actually contains recurring narrative characters

formal typography asset
-> intake when managed + typography specification + platform audit + generation-ready
-> no mother-library, hook, scene map, shot audit, or photorealism gate by default

formal short drama batch
-> intake/state + hook audit when opening/episode applies + character continuity + reference/style + scene map + scene continuity when applicable + shot audit + style lock + shot production registry + prompt audit + generation-ready

formal multi-ratio KV delivery
-> approve one master composition + lock title/logo/sponsor/performer safe areas + build rendition matrix + inspect crop previews + manually recompose only warned ratios + platform audit + generation-ready when generation is still required
-> a new ratio is not permission to invent an unrelated composition

formal single-scene product image
-> intake when managed + product/reference lock + composition/material gate + prompt audit + generation-ready
-> no hook audit, character continuity, scene map, or shot audit unless the deliverable actually requires them
```

## Director Contribution Packet

For formal image/video work, preserve only the contributions relevant to the route:

```text
director_contribution_packet
zongkong: speed_mode, workflow_mode, main_line, platform_target
concept_or_specialist_owner: approved claim/story/composition decision
reference_owner: mother_library_application_packet or reference-role boundaries
scene_owner: scene function and scene/continuity locks when applicable
shot_owner: shot function, edit motivation, axis, and ending state when applicable
character_owner: identity, costume, performance, relationship locks when applicable
project_style_lock: stable batch variables when applicable
prompt_owner: execution wording
platform_auditor: decision and approved execution prompt
```

Final formal prompts must inherit the relevant upstream decisions. They do not need empty fields for directors that do not apply to the deliverable.

## Audited Prompt and Generation Ready

Formal prompt execution requires an `audited_prompt_packet` from `$prompt-platform-auditor` and then a `generation_ready_packet` or equivalent managed job.

```text
generation_ready_packet
final_prompt:
audit_status: passed / passed_after_effect_preserving_compaction
target_tool:
deliverable_profile:
source_lock:
reference_roles:
output_path_rule:
applicable_quality_gate:
response_mode:
qc_mode:
```

For managed video execution, also require the relevant fields:

```text
video_prompt_source_packet:
source_authority:
model_target: when a specific model such as seedance_2_5 is selected
task_mode: when the model/task has distinct reference, edit, extension, keyframe, montage, or transition behavior
complexity_mode: single_beat / staged_action / multi_shot
must_preserve:
reference_asset_map: when multiple or multimodal references exist
subject_action_or_beats:
stage_plan: when one generation contains several connected events
camera_behavior:
environment_or_light_change:
ending_behavior:
edit_master / edit_scope: for local edit
boundary_state: for video extension
locked_parameters: when source media controls ratio or duration
duration:
ratio:
audio_mode: only when applicable
risk_profile:
manual_execution:
```

Require reference URLs, relay paths, start/end frames, audio fields, or platform-specific reference maps only when the selected platform/task needs them.

## Missing-Field Behavior

```text
formal_managed + applicable missing field
-> stop before execution
-> return missing_fields
-> set route_back_to to the owning skill
-> preserve all approved upstream state

quick_test + missing formal-only field
-> continue when the test can be executed safely
-> mark the output as quick_test
-> do not promote it to a formal batch lock

prompt_only
-> do not create formal missing fields merely to satisfy a packet
```

Never ask a downstream prompt, audit, or generation skill to invent an upstream creative or continuity decision.
