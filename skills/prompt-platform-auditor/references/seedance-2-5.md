# Seedance 2.5 Prompt Compilation

Use this reference only when the user or current project selects `model_target: seedance_2_5`. Keep `platform_target:jimeng` for Dreamina/即梦 execution and `platform_target:seedance_ark` for an Ark/API surface. Never silently upgrade another model to 2.5.

## Contents

- Evidence and live-state boundary
- Prompt packet
- Base formula and reference mapping
- Audio syntax
- Long-video staging
- Locked parameters
- Video edit and extension
- Keyframes, storyboards, and white models
- Montage and seamless transition
- Performance and camera language
- Compilation templates
- Audit checklist and limits

## Evidence And Live-State Boundary

This contract was updated on 2026-08-07 from the user-supplied Chinese guide, `16000字超详细 Seedance 2.5 官方提示词指南及提示词模板`, and the official Dreamina Seedance 2.5 product/prompt pages:

```text
https://mp.weixin.qq.com/s/Jv5iCILkg10q8o-KZ4GpNQ
https://dreamina.capcut.com/seedance/seedance-2-5
https://dreamina.capcut.com/seedance/seedance-2-5-prompt
```

Treat model availability, credit cost, resolution, exact duration choices, upload limits, and CLI/API flags as live platform state. Before execution, inspect the selected Dreamina/Ark surface and `dreamina <subcommand> -h`. The prompt compiler must not invent unsupported parameters.

The production-relevant 2.5 changes are:

```text
up to 30-second continuous generation
up to 50 multimodal reference assets
text, image, video, and audio role mapping
localized video editing from one source master
first/end and ordered multi-keyframe control
forward/backward video extension
coarse white-model motion guidance and fine white-model rerendering
audio-aware montage and seamless transition tasks
```

These are capability ceilings, not instructions to use maximum duration or maximum references. Use the smallest sufficient packet.

## Prompt Packet

Compile from this applicable subset:

```text
model_target: seedance_2_5
task_mode: text_to_video / reference_to_video / first_frame / first_end_frames / multi_keyframe / video_edit / extend_forward / extend_backward / montage / seamless_transition / coarse_white_model / fine_white_model
generation_goal:
source_authority:
reference_asset_map:
entity_map:
must_preserve:
do_not_inherit:
subject_action_or_beats:
stage_plan:
camera_behavior:
environment_or_light_change:
ending_behavior:
edit_master:
edit_scope:
boundary_state:
locked_parameters:
duration:
ratio:
audio_mode:
music_policy:
audio_detail:
negative_or_forbidden:
```

Leave inapplicable fields empty. Do not output packet labels inside the copyable prompt unless the structured heading improves a complex multi-reference, edit, extension, or long-video job.

## Base Formula And Reference Mapping

Use the smallest sufficient base formula:

```text
主体 + 动作或事件 + 场景与环境（可选）+ 视觉风格（可选）+ 运镜或切镜（可选）+ 声音（可选）
```

Describe the main process once. Add detail only for decisive actions, observable end states, continuity, or likely failure points. Keep UI/API generation parameters out of the copyable prompt.

For references, write one explicit role per asset:

```text
@图片1用于<人物A>的五官、发型和服装，不采用图片背景。
@视频1用于<人物A>的动作路径和节奏，不采用视频中的人物身份、服装和场景。
@音频1用于<人物A>的音色和指定台词，不控制画面身份或风格。
```

Do not write `@图片1至@图片4分别定义四名角色`. Bind every asset to a named entity and property. Group larger maps by `【人物】/【道具】/【场景】/【动作与声音】`, then call only the needed assets inside each scene.

If several images show one subject from different angles, say that they jointly define one continuous object and that the output must not duplicate it.

Input ceilings from the supplied guide:

| Kind | Ceiling | Stability-oriented working range |
| --- | --- | --- |
| images | up to 30, each no more than 4K | 1-8 primary subjects; split views into separate images when more than five subjects need multiple views |
| videos | up to 10, combined duration up to 30 seconds | 1-5 primary subjects, usually 5-10 seconds per useful clip |
| audio | up to 10, combined duration up to 30 seconds | only dialogue, voice, ambience, SFX, or music directly needed by the task |
| video edit | source video plus reference images | source usually within 20 seconds and 1-5 reference images; more assets increase drift risk |

Do not reject a platform-accepted job merely because it exceeds a recommended working range. Warn about stability and require stronger role mapping.

## Audio Syntax

Seedance 2.5 accepts natural language. When explicit separation helps, compile:

```text
(背景音乐描述)
<环境声或物理音效>
{人物台词}
【字幕内容】
```

For a non-Chinese line, state language, regional variant/accent when relevant, delivery, speaker, then `{exact line}`.

Default to `music_policy:no_music_allow_sfx` when the user did not request music:

```text
无背景音乐，不要配乐、歌曲或人声演唱；只保留指定对白、自然环境声和与画面动作同步的物理音效。
```

Do not suppress requested dialogue, room tone, Foley, machinery, footsteps, impacts, or other synchronized SFX. `music_requested` and `full_silence` remain explicit user overrides.

## Long-Video Staging

Use stages for multi-event work, especially near 30 seconds. Give each stage one main observable state change:

```text
【阶段一】
开始时：人物、道具、空间和声音的初始状态。
主要事件：一个主要动作或事件。
结束时：可直接看到或听到的结果状态。

【阶段二】
承接上一阶段：必须继承的身份、位置、道具归属、方向和声音。
主要事件：一个主要动作或事件。
结束时：可观察状态。
```

Use time ranges only for pacing budgets and critical handoffs, entrances, exits, transitions, or beats. Keep ranges continuous and non-overlapping. Do not claim frame-accurate timing or use timestamps to force several actions per second.

For every stage, preserve the applicable identity, count, costume, prop ownership, spatial direction, camera axis, light, and audio relationship.

## Locked Parameters

Do not put a conflicting ratio or duration into the prompt/job:

| Task | Ratio | Duration |
| --- | --- | --- |
| video edit | inherited from source video | approximately inherited from source; may vary by about 0.3 seconds |
| first-frame / first-end-frames | inherited from first frame; first and end frames should match | selectable on the live surface |
| extend forward/backward | inherited from source video | extension duration selectable on the live surface |

Keep `locked_parameters` in the audited packet and remove prohibited overrides before execution.

## Video Edit And Extension

For `video_edit`, define one source video as the unique master:

```text
【编辑目标】编辑@视频1，只在<time/region/object/audio class>执行<one exact delta>。
【原视频职责】@视频1是唯一编辑母版，负责人物、场景、动作、构图、镜头、遮挡、声音和事件顺序。
【目标素材职责】@图片1或@音频1只提供目标对象的指定属性。
【编辑范围】只处理明确对象、区域、时间段或声音类别。
【保持内容】其余身份、数量、结构、动作、镜头、遮挡、时间线和声音保持@视频1。
```

For object replacement, inherit every appearance, occlusion, movement, exit time, path, and speed change from the original object. For background replacement, protect the subject silhouette, identity, expression, scale, action, foreground, and camera.

For `extend_backward`, the first new frame must inherit the source tail state, motion trend, camera, light, environment, and sound before the new event begins.

For `extend_forward`, describe the preceding event first, then make the final new frame explicitly reach the source first-frame state. State which later subjects, props, or effects must not appear early.

Extension continuity is visual and audible, not pixel-identical. Check the boundary plus the full extended segment.

## Keyframes, Storyboards, And White Models

For first/end frames, assign each separately:

```text
@图片1作为首帧，定义开始构图、主体位置、姿态、道具、场景和镜头方向。
@图片2作为尾帧，定义结束构图、主体位置、姿态、道具、场景和镜头方向。
画面从@图片1自然开始，经过连续动作后到达@图片2。
```

Other references provide attributes only and must not replace the anchor-frame composition.

For ordered multi-keyframes, begin with `以@图片1至@图片N的顺序作为关键帧`, define every image's visible state, and require continuous transitions. Independent frames are normally safer than one collage when precise stage mapping matters.

For a storyboard grid, state the read order and shot mapping. Keep grids at 15 cells or fewer when possible. Inherit sequence and rough composition; reject borders, captions, arrows, note areas, and placeholder art unless requested.

Classify white-model references:

```text
coarse_white_model -> motion path, blocking, timing, camera, edits, light changes, or sound rhythm only; map every geometry item to a final entity
fine_white_model -> preserve complete structure, action, layout, camera, and edits; rerender only named identity/material/color/scene/style properties
```

Reject coordinate axes, controllers, camera cones, trajectory lines, or incomplete appendage motion as appearance references.

## Montage And Seamless Transition

For `montage`, specify:

```text
asset roles -> image order or permission for thematic reordering -> per-image motion amplitude -> edit rhythm/transitions -> graphic treatment -> sound
```

Do not say only `把这些素材做成视频`. For important people/products, preserve explicit entity mapping across every image.

For `seamless_transition`, define the before video, after video, trigger, camera direction/speed, visual transformation, destination state, and audio bridge. Preserve each original clip's identity and structure, but do not promise pixel-identical preservation through the generated transition.

## Performance And Camera Language

Translate emotion into 2-4 observable cues per turn: eye direction, brow, mouth, breathing, shoulders, hand tension, posture, or speech delivery. Use staged triggers only for several emotional turns.

Common camera terms may remain concise. For ambiguous or niche terms, compile:

```text
term + target subject + visible frame change + foreground/background relation + direction/speed + ending state
```

Prefer visible results over unsupported lens/aperture/shutter number stacks.

## Compilation Templates

Compact reference-to-video:

```text
@资产逐项职责与不采用项。
<主体>在<场景>完成<main event>。
画面呈现<style>; 镜头<camera behavior>; 最终<observable ending state>。
<dialogue/ambience/SFX when applicable>。
<music-policy sentence>。
```

Complex 30-second sequence:

```text
【生成目标】
【素材职责】
【主体设定】
【阶段一/二/三：开始时 + 一个主要事件 + 结束时】
【保持一致】
【声音】
【禁止或不继承】
```

## Audit Checklist And Limits

Before `通过`, confirm:

```text
model_target and task_mode are explicit
every reference has one role and named entity/property mapping
larger reference sets are grouped and called per scene rather than forced on screen together
every long-video stage has one main change and observable ending state
identity/count/costume/prop ownership/space/camera/audio continuity is explicit where needed
edit has one unique master, one exact delta, a bounded scope, and must-preserve rules
extension states the correct source boundary and prevents premature assets
first/end frames are separately assigned and use compatible aspect ratios
white model is classified coarse or fine
timestamps are pacing budgets, not frame-level guarantees
abstract emotion and camera terms are translated into observable behavior
locked ratio/duration rules do not conflict with the job
music_policy exists and defaults to no_music_allow_sfx
```

Never promise exact subtitles, formulas, labels, product parameters, frame-level edit points, pixel-identical edits/transitions, or guaranteed maximum-reference stability. Use prepared visual assets and post-production when exactness is mandatory.
