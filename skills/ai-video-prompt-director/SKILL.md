---
name: ai-video-prompt-director
description: 生成影视AI视频提示词。用于把关键画面、分镜或AI首帧转成即梦、可灵、Seedance/Ark 可复制使用的视频生成提示词，包含视频可行性判断、首帧、主体动作、镜头运动、环境变化、光影变化、节奏、时长、比例和禁止项，尤其适合一镜到底与伪一镜到底设计。
---

# AI Video Prompt Director

## Core Rule

Video prompts should be simple, continuous, physically plausible, and easy for video models to follow.

Formal project video prompts must inherit the selected top-tier cinematography anchor from `$reference-visual-library/references/shared-elite-cinematography.md`, but the execution prompt must express it as concise camera/light/color/material language instead of a long reference list.

For video prompts, camera detail must be explicit but not overloaded. The prompt must state:

```text
首帧景别/机位 + 镜头运动 + 镜头焦段或镜头感 + 光线方向 + 色彩边界 + 材质/空间质感 + 结束画面
```

If the platform cannot handle full camera specs, compress them into one phrase, such as:

```text
85mm长焦压缩、低饱和冷灰绿、头顶荧光灯压迫感
```

Default to:

- One dominant subject action.
- One dominant camera movement.
- One environment/light change only when useful.
- One clear first frame.
- One clear ending frame.

## Video Language Strategy / 视频语言策略

Jimeng and Seedance/Ark execution prompts must be Chinese-first, short, and motion-clear.

Do not write director essays, long style bibles, or English-heavy camera lists. For image-to-video, the first frame carries:

```text
人物、服装、场景、构图、光线、色调、材质、整体风格
```

The video prompt text controls only:

```text
一个主体动作 + 一个镜头运动 + 一个轻微环境变化 + 一个明确结束画面
```

If a formal project needs style protection, compress it into one short phrase instead of restating the whole image prompt:

```text
保持低饱和现实主义悬疑质感，冷白实用光、长焦压缩、真实皮肤和旧物材质。
```

For Seedance/Ark, use the same motion rule as Jimeng unless the platform-specific task explicitly needs more references. The prompt must still stay continuous, physically plausible, and readable.

## Prompt Direction Selector / 提示词方向决策

Before writing any final copyable prompt, decide `prompt_direction`. Do not mix several directions in one prompt.

Use one of these directions:

```text
first_frame_motion: first frame controls visual style; text only controls motion.
dialogue_coverage: same-scene dialogue, confrontation, reaction, eyeline, or over-shoulder coverage.
product_motion: product, vehicle, mechanical, object, or physical-process motion.
reference_continuity: reference images control identity, costume, product structure, scene, light, or color.
local_edit: modify one named region/object while preserving the rest of the video/frame.
multi_shot_omni: Kling O1/Omni multi-reference or multi-shot storyboard.
quick_motion_test: fast 3-5 second test, less formal but still one action and one camera move.
```

Default short-drama routing:

```text
Jimeng / Seedance: first_frame_motion or dialogue_coverage.
Kling: first_frame_motion, product_motion, or reference_continuity.
Kling O1 / VIDEO 3.0 Omni: reference_continuity, local_edit, or multi_shot_omni.
```

Final copyable video prompt order:

```text
1. source authority: first frame / reference role / video reference role
2. preservation lock: character, costume, scene, light, material, continuity
3. main action: one visible action, with timing when needed
4. camera behavior: one movement or fixed camera
5. environment/light change: one subtle physical change, or none
6. ending frame: clear stop point
7. breath/audio: breath tail when needed; default no music, real SFX allowed
8. forbidden items: 3-8 platform-specific risks
9. duration and ratio
```

If the draft tries to combine several prompt directions, split it before final output. For example, do not combine product insertion, background change, wardrobe change, new camera move, weather change, and native audio in one prompt.

## Visual Helpfulness / Director Contribution Rule

Every final video prompt must improve or protect the picture. Each kept phrase must control one of:

```text
first-frame preservation
subject action
camera movement or fixed-camera behavior
light / environment change
scene continuity / reference role / do-not-inherit boundary
material / color / realism preservation
ending frame
platform risk control
```

If a phrase cannot answer "what will the viewer see change or stay stable?", remove it or translate it into visible language.

For formal work, preserve `director_contribution_packet`:

```text
mother-library director contribution: project/scene function and video-safe translation
scene director contribution: location, light, lens feeling, material, performance state
shot-language contribution: shot function, edit motivation, camera path, transition reason
character/product continuity contribution: identity, costume, structure, relationship state, forbidden drift
prompt director contribution: one-action/one-camera platform-safe execution wording
```

The video prompt director may compress upstream contributions, but must not erase or invent them.

## Default Audio Policy / 默认音频规则

Unless the user explicitly asks for music, score, dialogue, voiceover, or a reference voice, every copyable video prompt must include:

```text
不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白。
```

This default applies to Jimeng, Kling, Kling O1, Kling VIDEO 3.0 Omni, and Seedance/Ark unless the user explicitly requests music, score, dialogue, voiceover, native audio, or a reference voice.

For product, vehicle, mechanical, outdoor, action, or environment-driven shots, replace generic sound wording with concrete real SFX when helpful, such as wheel friction, mechanical clicks, wind, footsteps, fabric movement, water, fire, crowd room tone, or object contact sounds.

For Kling O1 / Omni / native-audio handoff, audio or voice references control only sound or voice. They must not control identity, costume, scene, color, brand elements, lighting, or camera style.

For formal video prompts, inherit `mother_library_application_packet` and compress it into:

```text
mother_library_video_application: scene function + light direction + spatial relation + lens feeling + material/performance realism + platform-risk controls
```

Do not paste long mother-library explanations into video prompts.

## Video Feasibility Check

Before writing the final video prompt, check:

| 检查项 | 风险 | 建议 |
| --- | --- | --- |
| 是否跨空间 | 容易跳切或突然换景 | 用遮挡转场，或拆段 |
| 是否跨时间 | 容易逻辑断裂 | 改成同一时空，或用光线/遮挡过渡 |
| 是否跨主体 | 容易主体漂移 | 锁定一个主体或目标物 |
| 景别变化是否过大 | 容易硬切 | 写清连续推进/后拉路径 |
| 动作是否过多 | 容易混乱 | 保留一个主动作 |
| 镜头是否过快 | 容易画面崩坏 | 降速或分段 |
| 是否有文字/logo | 容易乱码或错误标识 | 避免生成文字，使用提供素材 |
| 是否适合一镜到底 | 跨场景越多越难 | 优先伪一镜到底 |

Output a short feasibility judgment when useful:

| 镜号 | 可行性 | 主要风险 | 建议 |
| --- | --- | --- | --- |

## Shot Language Rule For Multi-Shot Video

When a 15s/30s short-drama video uses multiple shots or pseudo cuts, inherit `$shot-language-auditor` before writing the video prompt.

The video prompt must preserve:

```text
镜头功能
景别递进
剪辑动机
人物视线/动作/物件衔接
```

Do not write a sequence that only lists cinematic shot sizes. A cut from MS to CU/ECU must be motivated by gaze, action, sound, object reveal, emotional reaction, occlusion, or spatial transition.

For vertical short-drama, keep the sequence readable:

```text
MS/MCU 建立关系
-> CU 压迫人物
-> ECU 关键物件
-> OTS/MCU 反应
-> CU 或 WS 收束
```

## Short Drama Breath Tail Rule

For short-drama video prompts, every shot needs a performance breath. Do not let any shot end mechanically on the exact frame of a line, reveal, reaction, or action beat.

Use two levels:

```text
轻气口：每个镜头结尾都加。动作或台词结束后保留约0.5-1秒，让人物有自然呼吸、眼神停顿、手部/衣料/身体轻微余动作，镜头不要立刻切断。
重气口：每一段、每场戏、每个情绪落点或信息段落结尾加。保留约1-2秒，人物不再继续说话或推进动作，只保留呼吸、眼神停顿、情绪余韵和轻微余动作，镜头稳定停在反应表情或段落收束画面。
```

When any shot contains dialogue, silent reaction, emotional realization, phone/message reveal, evidence reveal, accusation, confrontation, or a clear action beat, write the breath level explicitly:

```text
每个镜头结尾都保留轻气口，动作/台词结束后不要立刻停住，留约0.5-1秒自然呼吸、眼神停顿和轻微余动作。
每一段结尾保留重气口，留约1-2秒情绪余韵，人物不再说新台词，只保留呼吸、眼神和身体余动作，镜头稳定停在反应表情或收束画面。
```

For Jimeng/short-drama video, use concise execution wording:

```text
本镜头结尾留轻气口，动作/台词后保留0.5-1秒呼吸和眼神停顿；如果是本段结尾，留1-2秒重气口，人物不再说话，只保留呼吸、眼神停顿和轻微余动作，镜头稳定停在反应表情。
```

Default rule:

```text
短剧每个镜头默认有轻气口；每一段/场戏/情绪落点结尾默认有重气口。只有用户明确要求硬切、卡点、闪断、惊吓点或快速动作切出时，才取消对应气口。
```

Use breath tail for:

```text
每个镜头动作结束后
每个镜头台词结束后
质问后
一句台词说完后
短信/证据看完后
人物抬头或回头后
情绪压住没有爆发时
反转信息出现后
每一段/场戏结尾
```

Do not use breath tail when:

```text
用户明确要硬切、闪断、惊吓点、卡点转场、动作快速切出。
```

## One-Take Rule

For one-take requests, the prompt must include:

- 严格连续镜头。
- 无剪切、无跳切、无硬转场。
- 明确空间路径。
- 明确目标物锁定。
- 明确每个景别变化如何由镜头运动完成。
- 用遮挡物、光线、运动方向、形态匹配或贴近物体完成自然衔接。
- 结尾画面明确。

Avoid asking one model to complete too many cross-space changes in one generation. If needed, recommend pseudo one-take segments:

```text
A段结尾遮挡画面 -> B段从同类遮挡中开始
```

## Process

1. Start from a clear first frame or storyboard shot.
2. For formal projects, inherit the project/scene reference decision from `$style-reference-director`.
3. If the source contains multiple scenes/locations/reference styles, inherit the scene style map from `$scene-style-map-director`.
4. For multi-shot short-drama sequences, inherit `$shot-language-auditor` and keep its corrected shot flow.
5. For formal projects with an approved visual route, inherit `$project-style-lock` and compress it into video-safe language.
6. Run the video feasibility check.
7. Describe one dominant subject action and one dominant camera movement.
8. Add environment and light changes only when they support the shot.
9. For Seedance/Ark, write the prompt so it can pair with 1-9 public `http/https` reference image URLs.
10. Include the cinematography anchor and this scene's local style in compressed executable form: camera path, lens feeling, light direction, color boundary, material texture.
11. Send the draft prompt to `$prompt-platform-auditor` for platform-specific length, action-count, motion, reference-role, and effect-preservation checks.
12. Keep the final prompt copyable and concise enough for the target tool.

## No Lazy Handoff Rule

`$ai-video-prompt-director` turns approved first frames, shot logic, and style locks into video prompts. It does not replace upstream decisions.

Do not use this skill to:

```text
choose project reference style instead of style-reference-director
reverse-match reference images instead of reference-image-style-matcher
divide scene styles instead of scene-style-map-director
fix shot sequence logic instead of shot-language-auditor
invent project-style-lock or style bible
choose a missing first frame
repair missing character/product continuity
```

If formal video prompts lack upstream outputs, do not write a final copyable prompt. Output `待补上游项` and route back to the owning skill.

Required upstream outputs for formal video prompts:

```text
clear first frame / reference image role
one subject action
one camera movement
one ending frame
style-reference / scene-style-map decision
shot-language approval for multi-shot work
project-style-lock
prompt-platform-auditor target platform before execution
```

## Video Style Lock Rule

Do not re-invent style wording for every video prompt in the same formal project.

Use the `$project-style-lock` as the stable source, then compress it:

```text
现实主义犯罪悬疑，ARRI Alexa 35质感，低饱和中性灰，实用光源，长焦压迫，真实皮肤和旧物质感。
```

Only scene-specific camera path, action, light direction, and ending frame should change.

## Platform Prompt Packet Standard

For formal video work, do not output a loose platform prompt. Build a platform packet first, then write the final copyable prompt from that packet.

Use this common packet shape:

```text
video_platform_prompt_packet
target_platform: Jimeng / Seedance-Ark / Kling / Kling O1 / Kling VIDEO 3.0 Omni
task_type: t2v / i2v_first_frame / i2v_first_last_frame / reference_i2v / local_edit / previous_next_shot / multi_shot / native_audio
prompt_direction: first_frame_motion / dialogue_coverage / product_motion / reference_continuity / local_edit / multi_shot_omni / quick_motion_test
director_contribution_packet:
visual_helpfulness_check:
source_project_state:
first_frame_or_reference:
reference_roles:
shot_function:
subject_action: one dominant action
camera_movement: one dominant camera move or fixed camera
environment_or_light_change: one subtle change, or none
ending_frame:
duration:
ratio:
audio_policy: default no music; environment/action SFX allowed / no audio / dialogue / reference voice / native audio
style_lock_compact:
mother_library_video_translation:
mother_library_video_application:
forbidden_items:
missing_fields:
route_back_to:
manual_execution:
  external_platform:
  upload_roles:
  copyable_prompt:
  expected_output_path:
  status: draft / manual_handoff
```

The mother-library role in video is not a long style paragraph. Convert it into `style_lock_compact`, `mother_library_video_application`, and `mother_library_video_translation`:

```text
style_lock_compact: one short sentence protecting the approved look.
mother_library_video_application: which scene-function mechanism is being used, such as interrogation pressure, evidence reveal, product clarity, industrial scale, ritual unveiling, or emotional collapse.
mother_library_video_translation: light direction + spatial relation + lens feeling + material/performance realism + AI/platform-look risks.
```

If the project has both image and video work, keep two style locks:

```text
image_style_lock: fuller prompt language for still frames.
video_style_lock_compact: compressed motion-safe language for video platforms.
```

### Jimeng Prompt Packet

Use Jimeng when the user has a first frame and wants fast image-to-video, a short controlled action, or a motion test.

Jimeng packet requirements:

```text
target_platform: Jimeng
mode: t2v / i2v_first_frame / i2v_first_last_frame
prompt_direction: first_frame_motion / dialogue_coverage / quick_motion_test
first_frame_authority: true when image-to-video
prompt_length: usually 120-250 Chinese characters for i2v
subject_action: one action
camera_movement: one move or fixed
environment_or_light_change: one subtle change
ending_frame: required
style_lock_compact: one short protection phrase only
audio_policy: default "不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白。"
forbidden_items: no face drift, no outfit change, no scene change, no jump cut, no beauty smoothing, no platform-template look
```

Jimeng final prompt must be Chinese-first and motion-clear. If a first frame exists, do not restate the full image style; the first frame carries character, costume, scene, composition, light, color, material, and overall look.

### Seedance / Ark Prompt Packet

Use Seedance/Ark for formal API-driven generation, logged runs, first-frame video, first-last-frame transition, public reference URL workflow, and batch production.

Seedance/Ark packet requirements:

```text
target_platform: Seedance-Ark
mode: t2v / i2v_first_frame / i2v_first_last_frame / reference_i2v
first_frame_or_reference_url: required for image-driven work
reference_roles: image1/image2/... roles, never raw private IDs in prompt text
subject_action: one action unless the model/job explicitly supports multi-shot
camera_movement: one move or fixed
environment_or_light_change: one subtle change
ending_frame: required
duration: required
ratio: required
resolution_expectation: preview / standard / hd when relevant
audio_policy: required when audio is possible
```

For multi-modal Seedance 2.x style work, references can include image, video, and audio, but each reference still needs a role and a `do_not_inherit` boundary when it could overwrite identity, costume, scene, color, light, or camera behavior.

### Kling Prompt Packet

Use regular Kling for controlled continuous motion when the scene is physically simple.

Kling packet requirements:

```text
target_platform: Kling
prompt_direction: first_frame_motion / product_motion / reference_continuity / quick_motion_test
motion_physics: physically plausible, continuous, no unexplained transformation
subject_action: one action
camera_movement: one move or fixed
transition_device: required if crossing space/time or changing shot size
ending_frame: required
audio_policy: default "不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白。"
forbidden_items: no chaotic camera, no unrelated transformation, no uncontrolled crowd/hand complexity
```

Kling regular execution formula:

```text
以首帧/参考图为准，保持人物/产品、服装/结构、场景、光线、色调和真实材质不变。[主体]从[起始状态]到[结束状态]完成一个连续动作，动作过程必须有清楚的物理因果和运动惯性。镜头[一个运动/固定机位]，环境只发生[一个轻微真实变化]，结束在[明确画面]。不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白。禁止跳切、突然换景、主体重绘、比例漂移、镜头失控、无关变形、过度锐化和平台模板感。[时长/比例]。
```

For Kling regular prompts, prefer continuous physical causality over poetic mood. If the action needs multiple stages, write them as `A -> B -> C` instead of adding more adjectives.

### Kling O1 / VIDEO 3.0 Omni Prompt Packet

Use O1/Omni for reference consistency, element insertion/replacement, local edit, start/end frame control, video reference, multi-shot storyboard, or native audio. Omni is a multimodal reference workflow, not a longer text prompt.

Before writing execution text, produce:

```text
kling_omni_reference_role_map
target_model: Kling O1 / Kling VIDEO 3.0 Omni
task_type: image_element_reference / video_motion_reference / video_camera_reference / local_edit / previous_next_shot / start_end_frame / multi_shot_storyboard / native_audio
@ElementA controls:
@ImageB controls:
@VideoC controls:
audio_or_voice_reference controls:
do_not_inherit:
must_preserve:
must_change:
missing_fields:
route_back_to:
```

Role boundaries:

- `@Element` controls identity, product/prop structure, material, color, outfit, and logo/mark position.
- `@Image` controls scene, light, atmosphere, composition, first/end frame, or background only when assigned.
- `@Video` controls only action rhythm, camera movement, continuity, or local edit source. Always state what it must not control.
- `audio_or_voice_reference` controls only voice, accent, tone, dialogue style, or environmental sound. It must not control image style.

If a formal O1/Omni task lacks a role map, return `missing_fields` and route back to `$project-state-manager`, `$scene-style-map-director`, or `$project-style-lock`.

For project-managed Kling/O1/Omni handoff, preserve the final `video_platform_prompt_packet` so `$video-generation-controller` can write a manual `run_manifest.json`. Do not leave the task as a loose copy-paste prompt when it belongs to a managed project.

Default audio policy for Kling O1 / Omni when native audio, music, dialogue, voiceover, or a reference voice is not explicitly requested:

```text
不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白。
```

## Platform Audit Rule

The director draft is not automatically the execution prompt.

Before final output or generation:

- 即梦视频 must be compressed to a short execution prompt when needed.
- 可灵 must keep motion physically plausible and continuous.
- Seedance/Ark must include first-frame/reference role, one action, one camera move, ending frame, duration, and ratio.
- One-take prompts must pass a continuity and transition audit.

If `$prompt-platform-auditor` returns `打回重写` or `建议拆分`, rewrite the prompt before presenting it as final. Do not accept a shorter version if it loses the user's intended visual effect.

## Kling O1 / VIDEO 3.0 Omni Rule

Use this rule when the target platform is 可灵 O1, 可灵 Omni, Kling O1, Kling VIDEO 3.0 Omni, or the user says Omini/Omni.

可灵 Omni is a multimodal reference-and-editing workflow, not just a longer text prompt. Before writing execution text, define what each input controls:

```text
@Element / @Image / @Video role map
subject_identity:
product_or_prop_identity:
costume_or_material:
scene_or_background:
start_frame:
end_frame:
motion_reference_video:
camera_reference_video:
audio_or_voice_reference:
do_not_inherit:
```

If those roles are missing in a formal project, return `missing_fields` and route back to `$project-state-manager` / `$scene-style-map-director` / `$project-style-lock` instead of inventing reference roles.

### Kling Omni Prompt Shapes

Image/element reference:

```text
使用 @ElementA 锁定[人物/产品/道具]的身份、结构、材质和颜色，使用 @ImageB 锁定[场景/背景/氛围]。在[环境]中，[主体]完成[一个主要动作]，与[另一个元素]发生[一个清楚互动]。镜头[一个运动或固定机位]，光线/环境只发生[一个轻微变化]，结束在[明确画面]。禁止改变@ElementA的比例、脸型、服装/产品结构、颜色和标志位置。
```

Video reference for next/previous shot:

```text
基于 @Video 的人物关系、空间方向和光线气氛，生成下一个/上一个镜头：[景别]，[主体]从[起始状态]到[结束状态]，镜头[一个运动]，保持同一场景逻辑和时间连续。
```

Reference video for motion or camera:

```text
以 @Image1 为首帧，保持人物/产品/场景不变，只参考 @Video 的[动作方式/镜头运动]，不要继承 @Video 的人物身份、服装、场景、色调或品牌元素。
```

Start/end frame:

```text
以 @Image1 为首帧、@Image2 为尾帧，中间只描述可被真实摄影机完成的过渡动作：[A -> B -> C]。禁止突然变形、跳切换景、主体重绘、比例漂移。
```

Local video edit / transformation:

```text
保持原视频其他内容不变，只把[明确目标区域/主体]从[当前状态]改为[目标状态]。不改变镜头路径、人物身份、产品结构、背景空间、光比和整体色调。
```

### Kling Omni Limits

- O1 video generation is best treated as 3-10 seconds unless the selected product mode says otherwise.
- VIDEO 3.0 Omni can support longer/multi-shot work, but each shot still needs duration, framing, action, camera movement, and transition logic.
- If using video input plus references, reduce the number of extra image/element roles and avoid contradictory references.
- Multi-subject scenes must name each subject/element and state one interaction; do not ask every subject to perform separate complex actions.
- Native audio or voice reference must be explicit. If audio is not wanted, say so directly.
- For product, vehicle, outfit, and character work, identity/structure preservation is more important than rich style wording.

### Kling Omni Reference Role Map

Before writing a 可灵 O1 / VIDEO 3.0 Omni prompt, output a role map. Omni is a multimodal reference workflow, not a longer text-prompt workflow.

```text
kling_omni_reference_role_map
target_model: Kling O1 / Kling VIDEO 3.0 Omni
task_type: image_element_reference / video_motion_reference / video_camera_reference / local_edit / previous_next_shot / start_end_frame / multi_shot_storyboard / native_audio
@ElementA controls:
@ImageB controls:
@VideoC controls:
audio_or_voice_reference controls:
do_not_inherit:
must_preserve:
must_change:
missing_fields:
route_back_to:
```

Role rules:

- `@Element` controls identity, product/prop structure, material, color, outfit, and logo/mark position.
- `@Image` controls scene, light, atmosphere, composition, first/end frame, or background only when explicitly assigned.
- `@Video` controls only action rhythm, camera movement, continuity, or local edit source. It must not silently control identity, clothing, product design, scene, color, or brand elements.
- `audio_or_voice_reference` controls only voice, accent, tone, dialogue style, or environmental sound. It must not control image style.
- If a formal project lacks a reference role map, output `missing_fields` and route back to `$project-state-manager` / `$scene-style-map-director` / `$project-style-lock`.

### Kling O1 vs VIDEO 3.0 Omni Boundary

Use this boundary:

```text
Kling O1: best for a heavily referenced single shot, element insertion/replacement, local video edit, start/end frame, or short controlled motion.
Kling VIDEO 3.0 Omni: best for multi-reference continuity, video reference, multi-shot storyboard, native audio, longer 15s-style scene work, or stronger scene continuity.
```

Do not use VIDEO 3.0 Omni as an excuse to put every idea into one prompt. Multi-shot work still needs shot count, duration, framing, action, camera movement, transition logic, and per-shot reference roles.

### Kling Omni Task Templates

Image / element reference:

```text
使用 @ElementA 锁定[人物/产品/道具]的身份、结构、材质、颜色、服装/标志位置；使用 @ImageB 只锁定[场景/光线/氛围/构图]。在[环境]中，[主体]完成[一个主要动作]，与[对象]发生[一个清楚互动]。镜头[一个运动/固定机位]，环境只发生[一个轻微变化]，结束在[明确画面]。禁止改变 @ElementA 的脸型、比例、服装/产品结构、材质、颜色和标志位置；不要继承未指定参考的风格或元素。
```

Reference video only for action:

```text
以 @Image1/@ElementA 为身份和场景依据，只参考 @VideoC 的动作节奏：[动作方式]。不要继承 @VideoC 的人物身份、服装、场景、色调、品牌元素或光线风格。[主体]在[场景]中完成[一个动作]，镜头[一个运动/固定机位]，结束在[画面]。
```

Reference video only for camera:

```text
以 @Image1/@ElementA 保持人物/产品/场景不变，只参考 @VideoC 的镜头运动：[推近/横移/跟随/固定机位等]。主体动作保持简单：[一个动作]。不要继承 @VideoC 的人物、服装、背景、色彩或剧情。结束在[明确画面]。
```

Local video edit:

```text
保持 @Video 原视频的镜头路径、人物/产品身份、背景空间、光比、色调和真实材质不变，只修改[目标主体/区域]：从[当前状态]变为[目标状态]。禁止全画面重绘、换景、换脸、改变服装/产品结构、改变镜头运动或改变光线方向。
```

Previous / next shot:

```text
基于 @Video 的空间方向、人物关系和光线连续性，生成[上一镜/下一镜]。保持同一场景逻辑和时间连续。[主体]从[起始状态]到[结束状态]，镜头[一个运动]，结束在[明确画面]。不要改变角色身份、服装、场景、色调和核心道具。
```

Start / end frame:

```text
以 @Image1 为首帧、@Image2 为尾帧，中间只描述真实摄影机能完成的过渡动作：[A -> B -> C]。保持人物/产品结构、场景、光线、色调、材质不变。禁止突然变形、跳切换景、主体重绘、比例漂移、光线乱跳。
```

Multi-shot storyboard:

```text
根据 scene board / storyboard 生成[2-6]个连续镜头。每个镜头单独说明：时长、景别、主体动作、镜头运动、转场动机、结束画面。所有镜头保持同一角色、同一道具、同一空间方向、同一光线逻辑。不要让每个镜头同时改变人物、场景、天气和镜头风格。
```

Native audio:

```text
声音要求：[不要音乐，不要配乐；可以保留真实环境音效和动作音效 / 使用参考音频只控制声音和口音 / 需要对白但不改变画面 / 禁止额外旁白]。音频参考不控制人物长相、服装、场景、色调或镜头风格。
```

### Kling Omni Conflict Controls

Before finalizing, check:

```text
Are two references fighting over identity, costume, product structure, scene, light, or color?
Does @Video have do_not_inherit instructions?
Does each @Image/@Element/@Video appear in the prompt with a specific role?
Does the prompt ask to change subject, background, camera, weather, audio, and style all at once?
Does local edit preserve all non-target regions?
Does multi-shot output define per-shot duration, framing, action, camera movement, and transition?
Does audio reference stay audio-only?
```

If references conflict, simplify the role map before writing the final prompt.

### Scene Board To Kling Omni Route

When a `scene-board-image-prompter` board exists:

```text
Use the board as a control artifact, not as one giant style prompt.
Assign board crops/cells to @Image or @Element roles:
character cells -> identity / costume / performance state
prop cells -> structure / material / scale
set cell -> scene / light / spatial geography
overhead map -> blocking / eyeline / camera direction only
keyframe cells -> first frame / end frame / shot continuity
```

Then write the Omni prompt from the role map and keep the text focused on action, camera, edit, and audio.

## Jimeng Video From Image Rule

When the user uses 即梦 only for video and already has a generated still/first frame, treat the image as the style authority.

Do not let 即梦 re-create the visual style. The prompt should control:

```text
主体一个动作
镜头一个运动
轻微环境/光影变化
结束画面
禁止平台味漂移
```

## Jimeng / Seedance Direct Reference Board Rule

Use this when the input image is a storyboard board, TVC ad sequence board, production design guide, spatial continuity board, or a `scene-board-image-prompter` output that will be uploaded directly to Jimeng/Seedance as a visual reference.

The board is not the video frame. It is a reference control sheet. The video prompt must explicitly say what to inherit and what to ignore.

Inherit from the board:

```text
人物身份、脸型范围、发型、服装、表演状态
产品/道具结构、材质、颜色、比例、使用方式
主场景、空间关系、光线方向、色彩基调、材质质感
关键beat、人物位置关系、视线方向、镜头节奏
```

Ignore from the board:

```text
白色版面、分格线、编号、箭头、标题栏、注释区、小字、乱码文字、排版结构、storyboard sheet itself
```

Default wording for Jimeng/Seedance:

```text
参考上传的故事板作为视觉设定和空间连续性依据，只继承其中的人物、服装、道具/产品、场景、色调、光线和关键动作节拍。不要生成故事板排版本身，不要出现白底分格、编号、箭头、标题栏、注释文字或小字。最终视频必须像真实拍摄画面，不像设计板在动。
```

If the board contains multiple frames, choose one clear video target:

```text
生成第[几]个关键beat / 生成从[beat A]到[beat B]的连续动作 / 生成本大段的[一个主要动作]
```

Do not ask Jimeng/Seedance to animate the whole board at once unless the user explicitly wants an animatic of the board. For normal TVC video, the prompt should extract one scene or one continuous beat from the board.

The prompt should not repeat a long image-generation style essay. For 即梦图生视频, the first frame already controls:

```text
人物长相
服装
场景
色彩
构图
主要光线
材质
```

Hard boundary:

```text
首帧负责画面风格，文字只负责运动。不要用即梦视频提示词重新设计人物、场景、光线、服装、色调或摄影风格。
```

## Jimeng Execution Prompt Compression Rule

For Jimeng image-to-video, do not write a director essay. The first frame carries the cinematic style, character design, scene, color, lighting, composition, and material. The text prompt should only guide motion.

## Jimeng Video Common Constraint Templates

Use these constraints when writing 即梦 / Jimeng image-to-video prompts, especially for product, vehicle, outdoor, weather, action, and redraw tasks.

### Audio Constraint

Default wording:

```text
不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白。
```

For product or vehicle motion:

```text
不要音乐，不要配乐；可以保留轮胎摩擦、机械轻响、风声、地面碎石声等真实音效，不要鼓点，不要夸张音效，不要额外旁白。
```

### Shot Count Constraint

Multi-shot tasks should be split first. Do not force multiple camera angles into one Jimeng prompt.

```text
多镜头任务优先拆成单镜头分别生成。
一镜到底任务必须写：全程一个连续镜头，禁止切镜头，禁止跳切，禁止突然换角度。
```

### Locked Camera Constraint

For fixed-camera tasks, write the camera restriction explicitly:

```text
固定机位，镜头不推拉、不摇晃、不变焦、不跟随、不旋转，画面只让主体在固定构图内完成动作。
```

If the user asks for a controlled camera move, use only one move:

```text
镜头只做一个缓慢动作：[轻微前推/轻微后拉/轻微平移]，不要同时推拉摇移升降。
```

### Timed Action Stages

Actions must be staged by seconds. Do not write only mood or intention.

Use this shape:

```text
0-1秒：[起始状态]
1-2秒：[动作准备/重心变化/部件开始运动]
2-4秒：[主体完成核心动作]
4-5秒：[回稳/余动作/轻气口]
```

If the action is not visually obvious, require the full visible process:

```text
必须清楚看到 A -> B -> C 的完整过程，不要一瞬间完成，不要跳过中间动作。
```

For wheeled/product action:

```text
必须看到前轮开始转动、车身重心变化、后轮跟随、车身回稳的完整过程；禁止轮子突然变大，禁止车身比例变化，禁止主体被重绘。
```

### Weather Change Constraint

Weather and atmosphere must be physical, not dissolve effects.

Use:

```text
天气变化不要叠化、不要渐隐渐现、不要贴图式变天。通过真实云层位移、云影遮挡太阳、环境亮度同步降低、雾气缓慢增强、地面反光轻微变化来表现。
```

For clouds:

```text
云层真实移动并遮挡光线，天空亮度和地面阴影同步变化，禁止CG云层、强辉光、假HDR、突然换天空。
```

### Product / Subject Preservation

For product reference images:

```text
严格保持参考图产品结构、比例、轮子大小、材质、颜色和标志位置不变；只让产品按指定动作运动，不要重绘主体，不要新增零件，不要改变轮距和车身比例。
```

### Jimeng Product Motion Formula

```text
以首帧/参考图为准，严格保持产品结构、比例、材质和场景不变。固定机位，镜头不推拉、不摇晃、不变焦、不跟随。[0-1秒起始状态]，[1-2秒动作准备]，[2-4秒完成核心动作]，[4-5秒回稳并留轻气口]。必须看到[A -> B -> C]完整过程。环境只发生[一个真实变化]。不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白。禁止切镜头、跳切、主体重绘、轮子变大、比例漂移、假HDR、强辉光、塑料感、CG云层。
```

## Jimeng Anti-AI-Look Rule

The goal is not only shorter prompts. The goal is to prevent obvious AI/platform video taste.

For cinematic short-drama or film-style work, every Jimeng image-to-video prompt must protect the first frame's photographic imperfections and physical realism:

```text
保留首帧真实皮肤纹理、自然暗部颗粒、衣料褶皱、环境灰尘、旧物磨损、真实景深和原有光比。
动作幅度小，呼吸、眼神、手指、衣料、发丝、光影变化都要自然克制。
镜头运动慢、稳、可被真实摄影机完成，不做电子变焦感和平台模板运镜。
```

Every Jimeng video prompt for film-style work must include anti-AI controls:

```text
禁止脸型漂移、五官美颜化、皮肤塑料感、磨皮、假景深、HDR锐化、过度补光、网剧柔光、短视频滤镜、平台模板感、动作抽搐、肢体变形、背景融化、光线乱跳。
```

Seedance/Ark film-style prompts must apply the same anti-AI controls when driven by a first frame or reference image:

```text
保留首帧真实皮肤纹理、自然暗部颗粒、衣料褶皱、环境灰尘、旧物磨损、真实景深和原有光比；禁止脸型漂移、五官美颜化、皮肤塑料感、磨皮、假景深、HDR锐化、过度补光、网剧柔光、短视频滤镜、平台模板感、动作抽搐、肢体变形、背景融化、光线乱跳。
```

Positive anti-AI wording is required, not only negative words. Use:

```text
保持真实摄影机拍摄的微弱抖动和自然运动惯性，人物动作克制，皮肤和衣料保持首帧真实纹理，暗部不过度提亮，焦点稳定锁定人物。
```

Use this structure:

```text
保持首帧人物、服装、场景、构图、光线、色调和材质不变。
人物只做一个动作：[动作]。
镜头只做一个运动：[运镜]。
环境只发生一个轻微变化：[风/光/雾/尘/雨影]。
结尾停在：[结束画面]。
禁止换脸、换装、换景、跳切、风格漂移、网剧滤镜、美颜磨皮、AI短视频感。
```

Length guidance:

```text
普通即梦图生视频：120-250 Chinese characters.
复杂一镜到底：can be longer, but still keep one subject action, one camera movement, and one transition device.
```

Hard reject for Jimeng video execution:

```text
重新描述整套出图风格
堆母库电影名或摄影师名
多主体同时动作
推拉摇移升降环绕都要
跨空间/跨时间但没有遮挡或形态匹配
没有明确结束画面
只写“电影感、高级感、真实感”
```

If a Jimeng video prompt needs high-end cinematic quality, express it as a short style lock, not a long style paragraph:

```text
保持低饱和现实主义悬疑质感，冷白实用光、长焦压缩、真实皮肤和旧物材质。
```

Execution wording should include:

```text
严格保持首帧人物、场景、构图、色调和光线质感
不要改变人物脸型和服装
不要重新美化皮肤
不要变成短视频网感或平台模板感
```

Default 即梦图生视频 formula:

```text
以首帧为准，严格保持人物、场景、构图、色调和真实材质。[主体][一个动作]，镜头[一个运动]，[一处轻微光影/环境变化]，结束在[画面]。保持[压缩风格锁]。禁止跳切、换景、脸变、服装变、网剧柔光、美颜磨皮、AI短视频感、过度锐化。[时长/比例]。
```

For short drama, prefer subtle motion:

```text
抬眼、停顿、呼吸、手指收紧、回头、低头、缓慢靠近、窗光轻微变化、雨影/灯影轻微移动
```

Avoid:

```text
大幅转身、奔跑、复杂打斗、多人动作、换景、强烈变焦、绕拍、过度升降、夸张表情变化
```

## Output

| 镜号 | 工具 | 视频提示词 | 首帧要求 | 运动重点 | 结束画面 | 禁止项 | 时长/比例 |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Tool Guidance

For formal platform-specific work, output or preserve the packet as well:

```text
video_platform_prompt_packet
target_platform:
task_type:
prompt_direction:
first_frame_or_reference:
reference_roles:
subject_action:
camera_movement:
environment_or_light_change:
ending_frame:
duration:
ratio:
audio_policy:
style_lock_compact:
director_contribution_packet:
visual_helpfulness_check:
forbidden_items:
final_prompt:
audit_status:
```

- 即梦: for image-to-video, first frame controls style; prompt controls only one action, one camera movement, subtle light/environment change, and ending frame. Add anti-platform-look negatives.
- Seedance/Ark: specify first frame/reference role, one subject action, one camera movement, one environment/light change, ending frame, duration, ratio, resolution, and forbidden artifacts. Use Chinese-first short motion language and preserve the first-frame style instead of rewriting it.
- 可灵: keep motion simple, continuous, and cinematic; avoid multiple competing transformations.
- 可灵 O1 / VIDEO 3.0 Omni: first map every `@Image`, `@Element`, and `@Video` to a role, then write a concise action/camera/edit instruction. Use Omni for reference consistency, element insertion, video reference, start/end frame, local edit, or multi-shot storyboarding; do not use it as an excuse for overloaded prompts.

## Avoid

- Too many subjects moving in different directions.
- Fast chaotic camera movement unless explicitly needed.
- Complex text generation inside video.
- Brand logo generation unless a provided asset workflow exists.
- Cross-space transformation without a transition device.
- Full scene replacement in a claimed one-take shot.
