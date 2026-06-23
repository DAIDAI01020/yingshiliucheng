# Workflow Contracts v1

Use this file as the shared handoff contract for formal film AI workflows.

These packets do not replace director judgment. They standardize what each skill must pass downstream so prompts, audits, generation, QC, and revisions do not lose upstream decisions.

## Contract Rule

Formal projects must not move from brief, script, storyboard, reference image, taste words, or generated output directly to final prompt or generation.

Before any downstream step, check the current packet:

```text
complete packet -> continue
missing creative/style/shot/platform/state field -> route_back_to the owning skill
quick/test packet -> may continue only as quick/test, never as formal batch approval
```

## project_intake_packet

Created or checked by `$zongkong` before formal routing.

```text
project_intake_packet
project_tier: formal / quick / misc
workflow_mode: proposal / short_drama / storyboard / poster_key_art / image / video / product_ai_video / review / archive
deliverable_type:
main_line: commercial_promo / short_drama_story / other
reference_source: user_reference_image / user_named_reference / mother_library_recommendation / existing_project_lock / none
mother_library_route:
platform_target: built_in_image / Banana / Banana Pro / Jimeng / Kling / Seedance / Ark / Midjourney / layout
required_upstream:
available_upstream:
missing_fields:
next_skill:
quick_test_flag: true / false
```

Required behavior:

- Formal work must list `required_upstream` and `missing_fields` before prompt writing.
- If `quick_test_flag` is true, list what must be completed before formal batch use.
- `next_skill` must be the owner of the next missing decision, not an execution tool.

## upstream_handoff_packet

Used by reference, scene, shot-language, poster, and prompt director layers.

```text
upstream_handoff_packet
upstream_source:
reference_image_match:
reference_roles:
mother_library_route:
mother_library_application_packet:
  library_route:
  project_function:
  primary_reference_family:
  cinematography_anchor:
  borrowed_mechanisms:
  scene_function_rules:
  do_not_copy:
  forbidden_drift:
  prompt_inheritance:
mother_library_translation:
  light_direction:
  space_relationship:
  lens_psychology:
  composition_blocking:
  material_touch:
  performance_state:
  ai_risk_control:
director_contribution_packet:
  owner_skill:
  decision_owned:
  visual_controls_contributed:
  downstream_must_preserve:
scene_style_map:
shot_language_approval:
style_bible_source:
project_style_lock_source:
platform_language_strategy:
anti_ai_realism_rule:
image_tool_boundary:
jimeng_seedance_motion_rule:
breath_tail_rule:
missing_fields:
route_back_to:
```

Required behavior:

- Do not compress `mother_library_application_packet` or `mother_library_translation` into a reference name or adjectives.
- Do not invent missing reference roles, scene logic, shot function, or style lock.
- Preserve the relevant director contribution as visible controls, not as long explanation.
- If `missing_fields` is not empty, route back before final prompt output.

## style_lock_packet

Created by `$project-style-lock` after style approval.

```text
style_lock_packet
style_id:
master_style_sentence:
camera_system:
lens_rules:
light_rules:
color_boundary:
material_rules:
character_or_product_continuity:
mother_library_translation:
mother_library_application_packet:
platform_language_strategy:
anti_ai_realism_rule:
image_tool_boundary:
jimeng_seedance_motion_rule:
breath_tail_rule:
forbidden_drift:
prompt_schema:
upstream_source:
```

Required behavior:

- Prompt directors inherit this packet and vary only shot-specific camera, light, composition, action, and platform wording.
- A formal batch without `style_lock_packet` and `mother_library_application_packet` is not generation-ready.

## audited_prompt_packet

Returned by `$prompt-platform-auditor`.

```text
audited_prompt_packet
decision: 通过 / 保效精简后通过 / 打回重写 / 建议拆分
target_platform:
approved_prompt:
negative_or_forbidden:
changed_reason:
missing_fields:
route_back_to:
split_suggestion:
source_prompt_owner:
source_lock:
mother_library_application_packet:
director_contribution_check:
visual_helpfulness_check:
reference_roles:
```

Required behavior:

- Generation may use only `通过` or `保效精简后通过`.
- If `decision` is `打回重写` or `建议拆分`, execution tools must stop.
- Auditor may stabilize platform wording but must not create missing creative decisions.
- Auditor must reject prompts whose kept words do not visibly improve or protect the frame, motion, light, composition, material, continuity, or platform-risk control.

## generation_ready_packet

Required by image/video execution controllers before real generation.

```text
generation_ready_packet
target_tool:
project_root:
shot_or_asset_id:
final_prompt:
negative_or_forbidden:
audit_status:
audited_prompt_packet:
source_lock:
mother_library_application_packet:
director_contribution_packet:
visual_helpfulness_check:
reference_roles:
first_frame_or_image_refs:
duration:
ratio:
output_path_rule:
state_writeback:
```

Required behavior:

- Controllers execute only from this packet or an equivalent managed job that contains these fields.
- Missing `final_prompt`, `audit_status`, `target_tool`, `reference_roles`, or first-frame/public URL for video means route back, not prompt invention.

## qc_feedback_packet

Returned by QC/revision layers after generation or client review.

```text
qc_feedback_packet
asset_id:
source_generation_ready_packet:
qc_decision: 可用 / 可小修 / 定向重出 / 提示词需重写 / 前置导演判断错误
failure_type:
preserve:
revise:
route_back_to:
revision_instruction:
state_writeback:
```

Required behavior:

- Ordinary generation failure should route to targeted revision, not full style reinvention.
- Only `前置导演判断错误` routes back to reference, scene map, shot language, or style lock.
- Managed projects should write QC and revision decisions back through `$project-state-manager`.
