# Video Platform Compilation

Use only the section matching `platform_target`. Treat exact feature limits as workflow state that may change; preserve explicit user/platform settings over generic defaults.

## Contents

- Common video rules
- Jimeng
- Seedance and Ark
- Kling
- Kling O1 and VIDEO 3.0 Omni
- Audio and ending behavior

## Common Video Rules

Compile from `video_prompt_source_packet`. Do not rebuild image style when a first frame or reference already controls identity, scene, composition, light, color, and material.

Use:

```text
source authority
-> preservation lock
-> action or beat sequence
-> camera behavior
-> environment/light change if any
-> ending behavior
-> audio mode if applicable
-> music policy in the negative block
-> targeted forbidden items
-> duration/ratio
```

## Jimeng

For first-frame image-to-video, make the first frame the visual authority. Keep text motion-first and Chinese-first.

`single_beat`:

```text
one dominant action + one camera behavior + optional subtle physical environment/light change + clear ending
```

`staged_action` may use a short timed or causal A -> B -> C process when the action would otherwise happen instantly. Preserve product/character structure and physical inertia.

Reject full style redesign, unrelated multi-actions, conflicting camera moves, unexplained scene changes, or missing ending state.

## Seedance And Ark

Require duration and ratio for executable jobs. For image-driven work, require a usable reference/first-frame source and explicit roles. Preserve relay/public-reference requirements in managed execution state, not as raw private tokens in the prompt.

Use `single_beat`, `staged_action`, or an explicitly supported multi-shot task. Do not assume a multi-shot mode merely because the narrative has several beats.

## Kling

Prioritize physically continuous motion and stable subject/product structure. Use one camera behavior for `single_beat`. Express a staged physical process as A -> B -> C rather than adding unrelated actions.

## Kling O1 And VIDEO 3.0 Omni

Require a role map when multiple references are used:

```text
kling_omni_reference_role_map
target_model:
task_type:
image_roles:
element_roles:
video_roles:
audio_or_voice_role:
do_not_inherit:
must_preserve:
must_change:
```

Use reference video only for its assigned motion, camera, edit source, or continuity role. Prevent it from silently importing identity, costume, product design, scene, color, brand elements, or lighting.

For local video edits, lock all non-target regions and the original camera path before the delta.

For `multi_shot`, define each shot's duration, framing, action, camera behavior, transition motivation, and ending state. Do not overload one shot with subject, background, wardrobe, weather, style, camera, and audio changes simultaneously.

## Audio Modes

Compile positive audio instructions only when the platform/task can use them or the user specifies them:

```text
unsupported -> omit audio wording
none -> explicitly request no generated audio only when the platform needs the instruction
environment_only -> allow named room tone/action SFX; exclude music/narration if needed
dialogue -> specify dialogue ownership and keep it from changing the visual reference roles
native_audio -> define music/dialogue/environment balance
reference_audio -> state that the reference controls sound/voice only, not visual identity or style
```

Apply one independent music policy to every copyable video prompt:

```text
no_music_allow_sfx -> default negative: 不要背景音乐、配乐、歌曲或人声演唱；允许与画面动作同步的自然环境声和物理音效。
music_requested -> explicit user override; omit the default negative and preserve the requested music
full_silence -> explicit user override; prohibit all generated audio, including music, dialogue, ambience, and SFX
```

If `audio_mode:unsupported`, omit positive audio-generation wording but retain the default no-music/allow-SFX negative. Do not duplicate the same audio sentence in both the positive prompt and negative block unless the platform workflow requires both.

## Ending Behaviors

Compile exactly one:

```text
hold -> stabilize on the final composition
breath_light -> short natural residual motion or performance pause
breath_heavy -> longer emotional hold at a scene/segment ending
hard_cut -> action or reaction ends for an immediate cut
action_exit -> subject exits or motion carries out of frame
loop -> ending state reconnects to the first state
```

Do not add breath behavior to every short-drama shot automatically. Select it from shot/edit intent.
