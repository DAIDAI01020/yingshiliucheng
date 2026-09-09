---
name: ai-video-prompt-director
description: Turn approved first frames, reference images/videos/audio, storyboard beats, dialogue coverage, product motion, local edits, video extensions, transitions, long staged sequences, or multi-shot plans into concise video-prompt source packets. Use for Jimeng/Seedance 2.5, Seedance/Ark, Kling, Kling O1, or Kling VIDEO 3.0 Omni when Codex must define model/task mode, source authority, preservation locks, motion complexity, action or stage beats, camera and ending behavior, reference roles, edit/boundary state, duration/ratio, and conditional audio intent before platform compilation.
---

# AI Video Prompt Director

## Role

Own motion semantics and feasibility. Describe what changes over time and what must remain stable.

Inherit `speed_mode`, `deliverable_profile`, `platform_target`, `response_mode`, and `qc_mode` from `zongkong_route_packet` when present. Do not reclassify the route or silently switch platforms.

Do not duplicate platform syntax here. `$prompt-platform-auditor` owns final Jimeng, Seedance/Ark, Kling, Kling O1, and Omni execution wording.

## Authority Boundary

Do not invent:

- a missing first frame or reference role;
- character/product identity or scene geography;
- style lock or mother-library decision;
- shot/edit logic for formal multi-shot dramatic work;
- platform capabilities, model limits, or upload syntax.

For `formal_managed`, return exact `missing_fields` and `route_back_to` when an applicable upstream decision is absent.

## Source Packet

Build:

```text
video_prompt_source_packet
source_authority:
deliverable_profile: video_i2v / video_multi_shot
model_target:
task_type:
task_mode:
complexity_mode: single_beat / staged_action / multi_shot
shot_or_sequence_function:
must_preserve:
must_change:
reference_roles:
reference_asset_map:
do_not_inherit:
subject_action_or_beats:
stage_plan:
camera_behavior:
environment_or_light_change:
ending_behavior: hold / breath_light / breath_heavy / hard_cut / action_exit / loop
edit_master:
edit_scope:
boundary_state:
locked_parameters:
duration:
ratio:
audio_mode: unsupported / none / environment_only / dialogue / native_audio / reference_audio
music_policy: no_music_allow_sfx / music_requested / full_silence
audio_detail:
style_lock_compact:
risk_profile:
platform_target:
response_mode:
missing_fields:
route_back_to:
source_prompt:
```

Leave inapplicable fields empty. Do not write generic audio, breath, or anti-AI clauses merely to fill the packet.

## Source Authority

Select one primary authority:

```text
first_frame
first_and_end_frames
identity_or_product_reference
scene_reference
motion_reference_video
camera_reference_video
source_video_for_local_edit
source_video_for_extension
source_videos_for_transition
storyboard_or_scene_board
ordered_keyframes
coarse_white_model
fine_white_model
text_only
```

State what each source controls and what it must not control. A motion reference must not silently replace identity, costume, scene, color, product structure, or light.

When a storyboard board is used, inherit its characters, props/products, scene geography, light, and selected beat. Do not inherit borders, panels, arrows, labels, note areas, or tiny text unless the user asks for an animatic board.

## Complexity Modes

### `single_beat`

Use one dominant subject action and one camera behavior or fixed camera. Add at most one subtle environment/light change when it supports the beat. End on one clear state.

### `staged_action`

Use a physically connected A -> B -> C process when the action needs preparation, contact, transition, and settling. Timing stages are optional and useful when a model might skip the middle of the action.

Do not treat the connected stages as unrelated actions.

### `multi_shot`

Use only when the user/platform task actually requests a multi-shot sequence. Preserve per-shot:

```text
duration
framing
subject action
camera behavior
transition or edit motivation
continuity
ending state
reference roles
```

Do not apply the single-action rule to the whole sequence. Split when the requested changes fight over identity, space, style, camera, weather, or reference roles.

## Motion Feasibility

Check:

- Is the action physically possible in the duration?
- Does the camera path fit the space?
- Does a shot-size or space change have a motivated path, occlusion, edit, or transition?
- Are references competing over identity, structure, scene, color, light, or motion?
- Can the requested ending be reached without morphing or a hidden cut?
- Is a local edit narrow enough to preserve non-target regions?

Return `建议拆分` with a concrete split when one execution unit cannot remain stable.

## Ending Behavior

Choose from shot/edit intent:

```text
hold -> stabilize on the final composition
breath_light -> short natural residual performance/action pause
breath_heavy -> longer emotional hold at a segment or scene end
hard_cut -> finish on an immediate edit point
action_exit -> carry motion out of frame
loop -> reconnect ending to the first state
```

Do not add a breath tail to every short-drama shot. Use it for dialogue, reaction, reveal, accusation, emotional settling, or another motivated hold; use hard cut/action exit where the edit requires momentum.

## Audio And Music Policy

Choose `audio_mode` only when relevant:

```text
unsupported -> omit audio wording
none -> no generated audio
environment_only -> room tone and named physical SFX only
dialogue -> named speaker/dialogue ownership
native_audio -> intentional dialogue/music/environment mix
reference_audio -> reference controls voice/sound only
```

Select `music_policy` independently from `audio_mode`:

```text
no_music_allow_sfx -> default; no background music, scoring, songs, or sung vocals; synchronized natural ambience and physical SFX are allowed
music_requested -> use only when the user explicitly requests music; describe the requested music in audio_detail
full_silence -> use only when the user explicitly requests a silent result; set audio_mode:none
```

When the user gives no music instruction, always use `music_policy:no_music_allow_sfx`. Preserve this default even when `audio_mode:unsupported`; unsupported platforms may ignore it, but the copyable negative prompt must still carry the user's baseline.

For `no_music_allow_sfx`, require this meaning in `negative_or_forbidden`:

```text
不要背景音乐、配乐、歌曲或人声演唱；允许与画面动作同步的自然环境声和物理音效。
```

Do not let this sentence suppress requested dialogue, room tone, Foley, machinery, footsteps, impacts, or other synchronized effects. If the user explicitly requests music, omit the default no-music sentence. If the user requests full silence, replace it with a stronger no-audio instruction rather than saying sound effects are allowed.

## Task Profiles

### First-frame motion

Make the first frame the authority for identity, costume/product structure, scene, composition, light, color, and material. Text should focus on movement and ending state, not rebuild the still image.

### Product or mechanical motion

Lock structure, proportions, moving parts, material, color, logo position, contact points, and physical inertia. Use staged action when the complete motion path matters.

### Dialogue coverage

Preserve same-scene geography, background side, eyeline, performance state, and edit intent. Select ending behavior from the dialogue beat rather than using a universal pause.

### Local edit

Lock the source video, camera path, timing, background, non-target subjects, light, and color. State one target region and one exact delta.

### Long staged sequence

When one generation contains several connected events, define stages. Give each stage one main observable state change, its start/continuation state, and its ending state. Use timestamps only as pacing budgets for critical handoffs or transitions; never promise frame-accurate edits.

### Multi-asset reference work

Name each person, product, prop, location, motion, and sound owner. Map every asset to what it controls and what it must not import. Select assets per scene instead of asking all uploaded references to appear at once.

### Video extension

For backward extension, inherit the source tail state before adding new action. For forward extension, describe the preceding action and make the new final frame reach the source first-frame state. Preserve identity, prop ownership, space, motion trend, camera, light, and audio across the boundary.

### Generated transition

Define the before source, after source, trigger, camera direction, visual transformation, destination composition, motion trend, and audio bridge. Do not promise pixel-identical preservation through a generative transition.

### White-model guidance

Classify the source first. A coarse white model controls motion paths, blocking, timing, camera, edits, or light/sound rhythm; a fine white model controls complete structure, action, layout, and camera while named appearance properties are rerendered. Never mix these authority levels.

### Reference continuity or Omni work

Assign roles to every image, element, video, and audio reference. Use `do_not_inherit` for all roles that could contaminate identity, structure, scene, color, brand elements, light, or camera behavior.

## Formal Gates

Require only what applies:

```text
style lock -> stable visual variables across outputs
scene map/continuity lock -> multi-scene or same-scene coverage
shot audit -> dramatic or multi-shot edit logic
character/product continuity -> recurring identity or exact structure
reference role map -> multiple or multimodal references
```

Do not demand a mother-library, scene map, shot audit, audio policy, or breath tail for a simple product motion test unless it actually needs one.

## Platform Handoff

Send `video_prompt_source_packet` to `$prompt-platform-auditor`. The auditor loads the selected platform reference and returns the final copyable prompt.

For managed external execution, preserve the audited prompt and role map for `$video-generation-controller`; do not create a loose manual prompt without provenance.

## User Output

```text
direct -> final platform-compiled prompt only
compact -> final prompt + one feasibility/assumption note
diagnostic -> source packet, feasibility result, and audited packet
```

Do not output a default table for one prompt. Use per-shot rows only for actual batch or multi-shot work.
