---
name: prompt-platform-auditor
description: Compile and audit semantic AI image/video prompts for ChatGPT Images/GPT Image 2.5, built-in imagegen, Banana/Banana Pro, Jimeng/Seedance 2.5, Seedance/Ark, Kling, Kling O1/VIDEO 3.0 Omni, and Midjourney. Use after an image/video prompt owner or when the user supplies a prompt that needs platform/model-ready wording, multimodal reference-role checks, precision editing, exact-text or transparent-asset controls, long-stage structure, edit/extension boundaries, locked-parameter checks, complexity control, conditional risk controls, or an execution pass/fail decision.
---

# Prompt Platform Auditor

## Role

Act as the single source of truth for platform execution language.

Inherit `speed_mode`, `deliverable_profile`, `platform_target`, `response_mode`, and `qc_mode` from `zongkong_route_packet` when present. Do not change them.

Own:

- platform language, length, syntax, and parameter fit;
- reference-role and local-edit execution clarity;
- action/camera complexity checks;
- task-specific risk compaction;
- final pass/rewrite/split decision.

Do not invent concept, composition, style lock, scene geography, shot function, character/product identity, typography content, or reference roles that belong upstream.

## Read References On Demand

- Built-in imagegen, Banana/Banana Pro, Jimeng Image, or Midjourney: read [references/image-platforms.md](references/image-platforms.md).
- Explicit ChatGPT Images/GPT Image 2.5, or a new built-in image request routed to the Images 2.5 default: also read [references/gpt-image-2-5.md](references/gpt-image-2-5.md) and audit the model boundary, task mode, reference roles, preservation locks, exact text, transparency, and parameter separation.
- Jimeng video, Seedance/Ark, Kling, Kling O1, or Kling VIDEO 3.0 Omni: read [references/video-platforms.md](references/video-platforms.md).
- Explicit Seedance 2.5 in Dreamina/即梦 or Ark: also read [references/seedance-2-5.md](references/seedance-2-5.md) and audit the model-specific task mode, references, stages, edit/boundary state, and locked parameters.
- Deliverable-specific required fields and targeted risk controls: read [references/profile-risk-controls.md](references/profile-risk-controls.md).

Do not copy platform tables back into this file. Each platform rule has one source of truth.

For a formal or complex Seedance 2.5 packet, validate the structured packet before `通过`:

```powershell
python scripts\audit_seedance_25_packet.py --input H:\project\prompts\seedance-2.5-packet.json
```

Use [templates/seedance-2-5-prompt-packet.json](templates/seedance-2-5-prompt-packet.json) as the optional packet shape. The validator checks prompt structure and documented limits only; it does not replace live model/CLI/API capability checks.

## Input Contracts

Prefer:

```text
image_prompt_source_packet
or
video_prompt_source_packet
```

Accept a user-provided prompt directly when enough intent is visible. For `prompt_only` and `quick_test`, create only the minimum internal structure needed to compile it. Do not activate project state or formal gates.

For `formal_managed`, require applicable upstream state, not every possible packet:

```text
style lock -> when stable batch variables apply
scene/shot decisions -> when multi-scene or dramatic multi-shot work applies
reference roles -> when references exist
character/product/typography continuity -> when the profile needs it
layout/screen constraints -> for KV, typography, LED, or stage work
```

Return exact `missing_fields` and the owning `route_back_to` when an applicable formal decision is absent.

## No Creative Repair

You may:

- move visible instructions earlier;
- compact repetition;
- translate the source prompt into platform-safe language;
- reduce conflicting actions or camera moves;
- select only profile-relevant risk controls;
- preserve effect while shortening.

You may not invent an upstream decision. If the source is creatively incomplete, return `打回重写` to the specific owner rather than hiding the gap with generic cinematic language.

## Audit Decisions

Use exactly one:

```text
通过
保效精简后通过
打回重写
建议拆分
```

Generation is allowed only for `通过` or `保效精简后通过`.

Use `建议拆分` when a single execution unit contains incompatible spaces, excessive transformations, conflicting reference roles, or complexity beyond the selected task mode. Do not use generation as a workaround for a failed audit.

## Compilation Order

Compile in this order, omitting inapplicable parts:

```text
1. visible target or source authority
2. must-preserve lock
3. requested change/action
4. composition/camera behavior or layout
5. light/color/material/style controls
6. reference roles and do-not-inherit
7. ending/audio when applicable and video music policy
8. 3-8 targeted risk controls, including the default video no-music/allow-SFX line
9. ratio/duration/parameters
```

Lead with the actual visible frame or motion. Remove:

- client rationale and director essays;
- repeated prestige references;
- generic `电影感/高级感/真实感` stacks;
- redundant camera-brand piles;
- universal negative lists unrelated to this profile;
- internal packet labels from the copyable prompt.

Preserve exact structure, identity, scene geometry, typography content, continuity, or reference boundaries when those are the reason the output will remain accurate.

## Conditional Requirements

Use `deliverable_profile` to determine completeness. Do not apply these globally:

```text
camera system/focal/aperture
photographic anti-AI realism
mother-library translation
skin/hand controls
product structure controls
title/logo safe zones
transparent-background/glyph controls
breath tail
audio policy
music policy for video prompts
```

Examples:

- A live-action frame may need camera/depth and skin realism.
- A graphic KV needs hierarchy, palette, density, and safe zones instead.
- A typography PNG needs exact glyphs, alpha, edges, and no poster background.
- A local edit needs a base lock and narrow delta before any style language.
- A video always needs `music_policy`; positive audio wording is needed only when `audio_mode` is applicable.

Read [references/profile-risk-controls.md](references/profile-risk-controls.md) for the profile matrix.

## Image Audit

Reject or rewrite when:

- the actual frame is buried behind a generic template;
- the prompt asks one still image to show several sequential actions;
- a reference has no role or `do_not_inherit` boundary;
- a local edit may repaint non-target areas;
- text/logo/glyph requirements conflict with the profile;
- platform parameters or language are wrong;
- task-relevant structure, layout, material, or continuity is missing.

For GPT Image 2.5, apply [references/gpt-image-2-5.md](references/gpt-image-2-5.md). Require only the controls relevant to the selected task mode. For precision edits, require one explicit delta plus a concrete preservation boundary; for multi-reference work, require numbered roles and `do_not_inherit`; for exact text, require quoted copy, occurrence count, placement, hierarchy, and no-extra-text control. Keep model, quality, size, background, and output format as execution parameters rather than prompt prose.

Do not require exact camera brand, focal length, aperture, or photographic realism unless they materially improve this deliverable.

## Video Audit

Check:

```text
source_authority
model_target and task_mode
complexity_mode: single_beat / staged_action / multi_shot
must_preserve
reference_asset_map
subject_action_or_beats
stage_plan when one generation contains several connected events
camera_behavior
environment_or_light_change
ending_behavior
edit_master/edit_scope for local editing
boundary_state for extension
locked_parameters when the source controls ratio or duration
duration_and_ratio
audio_mode when applicable
music_policy
reference_roles and do_not_inherit
```

`single_beat` normally uses one dominant action and one camera behavior. `staged_action` may use a physically connected A -> B -> C process. `multi_shot` requires per-shot duration, framing, action, camera, transition motivation, and ending state; do not apply the single-action rule to the whole sequence.

Do not add a breath tail by default. Compile `ending_behavior`, `audio_mode`, and `music_policy` exactly as selected by the prompt owner or user.

Unless the user explicitly requests music or full silence, normalize missing `music_policy` to `no_music_allow_sfx` and ensure `negative_or_forbidden` contains this meaning:

```text
不要背景音乐、配乐、歌曲或人声演唱；允许与画面动作同步的自然环境声和物理音效。
```

Do not remove requested dialogue or synchronized sound effects. For `music_requested`, omit the default no-music line and preserve the requested score. For `full_silence`, use a stronger no-audio negative and do not claim that sound effects are allowed.

## Platform Normalization

Normalize names internally:

```text
ChatGPT Image / image / 内置 image -> built_in_image
ChatGPT Images 2.5 / GPT Image 2.5 / Image 2.5 -> built_in_image + model_target:gpt_image_2_5
GPT-Image-2.5 Flare -> built_in_image + model_target:gpt_image_2_5_flare
GPT-Image-2.5 Sunburst -> built_in_image + model_target:gpt_image_2_5_sunburst
image-2 / GPT Image 2 -> built_in_image + model_target:gpt_image_2
Banana -> banana
Banana Pro -> banana_pro
即梦 -> jimeng
Ark / Seedance -> seedance_ark
可灵 -> kling
可灵 O1 -> kling_o1
可灵 Omni / Omini / VIDEO 3.0 Omni -> kling_video_3_omni
MJ / Midjourney / Legnext -> midjourney
```

Keep the human-facing product name in prose. Never silently switch platforms.

## Output Packet

Preserve for formal work:

```text
audited_prompt_packet
decision: 通过 / 保效精简后通过 / 打回重写 / 建议拆分
platform_target:
model_target:
deliverable_profile:
task_type:
task_mode:
approved_prompt:
negative_or_forbidden:
changed_reason:
source_prompt_owner:
source_lock:
reference_roles:
reference_asset_map:
stage_plan:
edit_master:
edit_scope:
boundary_state:
locked_parameters:
ending_behavior:
audio_mode:
music_policy:
duration:
ratio:
missing_fields:
route_back_to:
split_suggestion:
response_mode:
qc_mode:
```

Use snake_case in skill packets. When a script returns camelCase, normalize it at the state boundary rather than mixing both styles downstream.

## User Output

```text
direct -> final copyable prompt only
compact -> final prompt + one short audit note
diagnostic -> decision, changed reason, missing fields/owner, and full audited_prompt_packet
```

Do not output a long audit table unless the user asks for comparison or batch review.

## Hard Rules

- Preserve effect before shortening.
- Do not approve a prompt merely because it is short or field-complete.
- Do not convert a weak concept into a new concept.
- Do not hide missing formal decisions in generic style language.
- Do not duplicate platform policy inside prompt-owner skills.
- Do not apply Seedance 2.5 limits or syntax unless `model_target:seedance_2_5` or the user/current project explicitly selects that model.
- Do not apply GPT Image 2.5 prompting or execution assumptions to a project or prompt pinned to GPT Image 2 or an older model. New generic built-in work may use `model_target:gpt_image_2_5` only when `$zongkong` has selected the migrated default.
- Do not claim that direct ChatGPT/Codex imagegen used Flare or Sunburst unless the execution surface exposes that exact submodel.
- Do not drop the default video no-music/allow-SFX negative unless explicit music or full silence overrides it.
