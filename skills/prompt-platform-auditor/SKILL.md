---
name: prompt-platform-auditor
description: Audit and rewrite AI image/video prompts for platform-specific execution. Use after frame-vision-director or ai-video-prompt-director writes a prompt, and before Banana/Banana Pro, built-in imagegen, Jimeng, Kling, Seedance/Ark, or Midjourney execution. Checks prompt length, platform fit, action count, camera count, reference-image roles, style overload, local edit boundaries, text/logo risk, one-take feasibility, effect preservation, and returns either an approved execution prompt, a rewritten platform prompt, or a rewrite request.
---

# Prompt Platform Auditor

## Core Role

`$prompt-platform-auditor` is the platform compliance and execution-stability layer.

It does not decide the creative concept or visual taste. It checks whether a director prompt can actually work on the target generation platform.

Its job is not simply to shorten prompts. Its job is:

```text
效果保住 > 画面准确 > 平台稳定 > 文字精简
```

## No Creative Repair Rule

`$prompt-platform-auditor` may compress, clarify platform language, remove redundant wording, enforce action counts, and stabilize the prompt shape.

It must not create missing upstream decisions:

```text
do not invent mother-library references
do not invent project-style-lock
do not invent reference image roles
do not invent shot function or edit motivation
do not invent scene map or scene style
do not invent character/product continuity rules
do not invent short-drama hook audit or character continuity locks
do not invent KV composition/style packet, composition mode, master KV layout, big-screen layout, safe-area map, or extension crop map
do not turn a weak creative direction into a new concept
```

If a prompt lacks creative, style, reference, shot-language, or scene decisions, return `打回重写` and name the upstream skill to route back to:

```text
style-reference-director
reference-image-style-matcher
scene-style-map-director
shot-language-auditor
project-style-lock
frame-vision-director
ai-video-prompt-director
poster-director
kv-director
kv-image-prompt-director
```

Compress by removing explanation, repeated adjectives, client-facing rationale, and platform-irrelevant details. Never remove the strongest visual anchors.

Use it after:

- `$frame-vision-director` writes image prompts.
- `$ai-video-prompt-director` writes video prompts.
- A user provides a prompt and asks whether it can be used.
- A prompt is going to Banana, Banana Pro, built-in imagegen, Jimeng, Kling, Seedance/Ark, or Midjourney.

## Workflow Position

```text
brief / script / storyboard
-> director skill writes prompt
-> prompt-platform-auditor checks platform fit and effect preservation
-> if pass: output final execution prompt
-> if too long: rewrite into accurate compact execution prompt
-> if wrong: send back to director or mark rewrite needed
-> generation tool
```

## Audit Result

Use one of four decisions:

| Decision | Meaning | Action |
| --- | --- | --- |
| `通过` | Prompt fits the target platform and preserves the intended effect | Return final execution prompt |
| `保效精简后通过` | Direction is right but wording is too long/noisy | Return a compact prompt that preserves the visual anchors |
| `打回重写` | Prompt structure is wrong or loses the intended effect | State why and request director rewrite |
| `建议拆分` | Video/one-take/image edit is too complex for one generation | Split into safer prompts or segments |

Generation may run only when the decision is:

```text
通过
保效精简后通过
```

If the decision is `打回重写` or `建议拆分`, do not use generation as a workaround. Return to the director/prompt layer or split the task.

Do not show a long audit table unless the user asks. Usually output one short note:

```text
审核提示：已保留首帧、主动作、镜头运动和核心光线，只删掉导演解释和重复风格词。
```

## Effect Preservation Rule

Before rewriting or compressing, identify the non-negotiable visual anchors:

| Anchor | Must preserve |
| --- | --- |
| 主体 | who/what the image or video is about |
| 场景 | location, time, spatial context |
| 动作 | one key action or state |
| 镜头 | shot size, camera angle, dominant camera movement |
| 光线 | main light source, direction, tone |
| 色彩 | color range and contrast |
| 材质 | key tactile details |
| 情绪 | intended pressure, beauty, suspense, scale, or atmosphere |
| 母库应用规则 | selected scene-function rule from `mother_library_application_packet` |
| 母库转译机制 | translated reference mechanism: light direction, space relation, lens psychology, composition, material, performance |
| 参考图角色 | what each reference controls |
| 禁止项 | failures most likely to ruin the result |

Delete only:

- why-the-shot-matters explanations
- repeated style adjectives
- long lists of film references
- abstract symbolism with no visible instruction
- multiple camera-brand names
- secondary actions that compete with the main action
- redundant negative terms

If a shorter prompt would lose the intended visual effect, do not approve it as compact. Mark it `打回重写`.

## Visual Helpfulness Gate / 画面有效性门槛

Approved prompts must be visually useful, not just better worded.

Every instruction kept in the final prompt must map to at least one real image/video control:

```text
visible subject / object shape / prop / costume / scene layout
composition / foreground / midground / background / camera position / lens / depth
light source / light direction / exposure / color boundary / material texture
reference-image role / continuity lock / do-not-inherit boundary
video action / camera path / physical cause-and-effect / ending frame
text-logo-risk / face-hand-risk / platform-look-risk / identity-drift control
```

Use this test before approval:

```text
If this phrase cannot answer "which pixels, motion, light, material, composition, or continuity will change or be protected?", remove it or translate it into visible language.
```

Do not approve prompts padded with weak non-visual language:

```text
高级感、电影感、质感拉满、氛围拉满、大片感、震撼、好看、真实、精致、克制、压抑
```

These words may remain only when immediately translated into concrete visible controls, such as:

```text
冷白荧光灯从头顶压下，门框和桌沿形成前景遮挡，65mm长焦压缩空间，低饱和灰绿墙面和旧木桌材质带出压迫感。
```

When returning an audited packet for formal work, include:

```text
visual_helpfulness_check:
  kept_visual_controls:
  removed_or_translated_fluff:
  risk_controls_that_protect_the_frame:
  decision:
```

For formal work, also audit director contribution integrity:

```text
director_contribution_check:
  mother_library_application_used:
  scene_style_map_used:
  shot_language_used:
  character_or_product_continuity_used:
  prompt_director_translation_used:
  missing_or_erased_contribution:
  route_back_to:
```

If a final prompt erases the mother-library mechanism, scene function, shot function, reference role, or continuity lock that upstream directors provided, return `打回重写` even when the wording is platform-friendly.

## Fielded Storyboard Accuracy Check

When auditing image prompts derived from a structured storyboard, treat the storyboard fields as higher priority than generic style wording. A valid execution prompt should carry the current shot's:

- visible subject, scene, action/state, and prop/character continuity locks
- shot size, camera position, lens/focal length, and foreground/midground/background composition
- light source/direction, color boundary, material texture, realism level, and aspect ratio
- text/logo/signage rules and the most relevant negative controls

Reject or rewrite if the user or upstream prompt sends an entire storyboard, multiple shots, or a full scene block as one image prompt. Route it into one shot at a time.

## KV Layout Audit

When auditing commercial/event KV prompts from `$kv-image-prompt-director`, treat `$kv-director` fields as higher priority than generic image-prompt style language. A valid KV execution prompt must carry:

```text
kv_type
kv_composition_style_packet
kv_composition_mode
composition_reference_source or reference_mechanism_translation
master_kv_layout_spec
main_ratio
layout_safe_area
title_logo_sponsor_zones
safe_area_map
asset_split or prompt_type
post_typography_plan
```

`kv_composition_style_packet` must preserve at least:

```text
first_read
focal_hierarchy
gaze_path
negative_space_logic
typography_relationship
primary_composition
primary_style_family
palette_logic
material_language
lighting_model
photographic_vs_graphic_balance
image_density
anti_template_rule
forbidden_style_drift
```

For a single master-KV image, do not require extension fields. Require `extension_ratios` and `extension_crop_map` only when the user explicitly requests ratio variants, banners, social adaptations, or a KV extension system.

For LED / stage-screen / big-screen KV, also require:

```text
led_screen_layout_spec
actual or intended screen ratio
center-safe area
presenter/performance safe area when people stand in front of the screen
side-extension logic
far-distance readability
```

Reject or route back to `$kv-director` if:

```text
the prompt only says 主KV / 大屏KV / 高级KV / 震撼KV without a composition mode
kv_composition_style_packet is missing, contains only taste adjectives, or is not translated into visible composition, palette, material, light, density, and drift controls
main KV and big-screen KV are treated as the same layout without screen-specific rules
title/logo/sponsor zones are missing
AI is asked to generate final readable title, logo, slogan, sponsor marks, QR code, date, venue, or legal text
the subject fills all areas and leaves no post-layout negative space
LED design uses tiny lines, dense particles, edge-critical faces, or small readable details
extension ratios cannot preserve the same visual DNA
```

The final extension-ratio rejection applies only when extension deliverables are requested.

Routing ownership:

```text
missing or invalid kv_composition_style_packet -> route_back_to: kv-director
valid packet exists but the execution prompt erases or weakens it -> route_back_to: kv-image-prompt-director
```

Approve only when the prompt is a no-text base art or asset prompt with explicit layout-safe areas and post typography plan.

For `保效精简`, separate global style from shot-specific execution:

```text
keep: current shot visible anchors + required continuity locks + concrete light/lens/color/material language
remove: repeated style paragraphs, explanation, camera-brand piles, duplicate negatives, abstract mood language with no visible instruction
```

Do not shorten away the details that make the image accurate. For historical, product, prop, character, or scene-continuity work, the object's shape, placement, material, era rules, and forbidden mistakes are non-negotiable anchors.

## Universal Checks

Before approval, check:

- Target platform is clear.
- Prompt has one dominant visual goal.
- Prompt preserves the user's intended effect.
- Prompt does not mix director explanation with execution instructions.
- Visible image/action details come before abstract meaning.
- Each kept phrase passes the Visual Helpfulness Gate.
- Formal prompts preserve the relevant `director_contribution_packet`.
- Reference image roles are explicit.
- Formal reference-image prompts have inherited or stated the mother-library match from `$reference-image-style-matcher`.
- Formal prompts inherit the correct `mother_library_application_packet` rule for this shot or scene.
- Formal prompts preserve the mother-library translation as concrete light/space/lens/material/performance language.
- Formal project prompts inherit the current `$project-style-lock` or clearly state the same locked visual DNA.
- Formal short-drama prompts inherit `hook_audit_packet` and `character_continuity_lock` when recurring characters or batch generation are involved.
- Text/logo generation risk is controlled.
- KV prompts preserve `kv_composition_style_packet`; single-master-KV work is not blocked by unrequested extension fields.
- Negative prompt is useful and not bloated.
- Copyable prompts do not use `同上`, `延续上条`, or missing style details.
- For formal image/video work, the prompt is an execution brief, not an attempt to discover style through generation.
- The prompt contains upstream creative decisions; the auditor is not being asked to invent them.

## Platform Language Strategy / 平台语言策略

Approve final prompts only when their language matches the platform:

- 内置 imagegen / ChatGPT Image: Chinese natural-language image direction first; English only for necessary camera/lens/lighting/material terms. Avoid parameter dumps and oversized negative blocks.
- Banana / Banana Pro: Chinese visible-frame instruction + English camera/lens/lighting/material keywords + Chinese negative prompt. The first 60-90 Chinese characters must describe the actual frame, not a generic style shell.
- Jimeng / Seedance video: Chinese first, short sentences, clear motion. Do not stack English terms, camera-brand lists, director notes, or long mother-library essays.

For formal image prompts, return `打回重写` if anti-AI photographic realism is missing. The prompt must preserve or request:

```text
真实皮肤纹理、轻微瑕疵、衣料褶皱、生活痕迹、环境灰尘、旧物磨损、自然暗部颗粒、明确现实光源、真实景深、原有光比、不过度锐化、不磨皮、不做假HDR。
```

For Jimeng / Seedance video from first frame, approval requires:

```text
首帧负责画面风格；文字只负责一个主体动作、一个镜头运动、一个轻微环境变化、一个明确结束画面。
```

If video text tries to rebuild the image style, change the face/costume/scene, or add multiple actions and camera moves, return `打回重写` or `建议拆分`.

If a formal project prompt uses a reference image but does not say what the reference controls, what mother-library style it maps to, and what must not be inherited, return `打回重写`.

If a formal prompt compresses the style down to only `电影感`, `真实感`, `高级感`, `低饱和`, `纪实感`, or a reference name without the translated mechanism, return `打回重写`.

If a formal prompt includes mother-library translation but does not say which mother-library application rule controls the scene function, return `打回重写` or route back to `$scene-style-map-director` / `$project-style-lock`.

If a prompt names a film, director, cinematographer, TVC, or mother-library route but does not translate it into visible light, space, lens, composition, color, material, performance, and AI-risk controls, return `打回重写`.

If a formal project prompt changes the camera system, color boundary, realism level, or main style wording without an explicit style-lock update, return `打回重写`.

If a formal prompt lacks the upstream decisions required for generation, return `打回重写`:

```text
no project-style-lock
no short-drama hook-audit for formal short-drama work
no character-continuity lock for formal short-drama recurring characters
no shot function
no shot-language approval for short-drama multi-shot work
unclear reference roles
unclear platform target
```

## Garbage Template Rejection Rule

Reject or rewrite any prompt that looks like a generic prompt shell rather than a real image/video brief.

Hard reject these patterns:

```text
生成一张 9:16 原生竖屏 4K live-action cinematic documentary still
live-action cinematic documentary still
cinematic, premium, realistic, documentary, Oscar-level, high-end
only shot metadata: MS / CU / ECU / 50mm / f2.8
style names without visual translation: Nolan style, Fincher style, Deakins style
mother-library reference without translated visual mechanism
```

These words may appear only if surrounded by concrete visual instructions. A valid prompt must explain:

```text
visible subject + visible space + action/state + composition + camera/lens + light source/direction + color boundary + material texture + ratio + major negatives
```

For formal short-drama and promo work, also require:

```text
mother-library translated mechanism + performance state + platform-risk control
```

For image prompts, approval requires all mandatory camera fields:

```text
景别 + 机位 + 构图 + 摄影机/影像系统 + 镜头焦段 + 光圈或景深 + 光线来源/方向 + 色彩边界 + 材质质感 + 比例 + 负面词
```

If any mandatory field is missing, return `打回重写` or rewrite before approval. Do not approve a prompt that only has shot metadata such as `MS | 50mm | f/2.8` without visible composition and lighting.

For Banana/Banana Pro and Jimeng image, the execution prompt should be primarily Chinese. English is allowed for camera systems, lens names, model names, and short technical terms only.

If the prompt starts with a generic template sentence, rewrite it so the first 40-80 Chinese characters describe the actual visible frame.

Example rewrite:

```text
Before: 生成一张9:16原生竖屏4K live-action cinematic documentary still。黄岚坐在询问室桌前。
After: 派出所询问室中景，黄岚坐在旧木桌前，桌面台灯和门框形成前景压迫，灰绿色墙面和模糊白板在背景。低饱和冷灰绿调，头顶荧光灯作为真实光源，长焦轻微压缩空间，ARRI Alexa 35质感，50mm，9:16。
```

## Image Platform Rules

### Built-In Imagegen / ChatGPT Image

Approve when:

- Prompt is natural and visual.
- Subject, composition, lighting, and reference roles are clear.
- It is not overloaded with camera-brand jargon.
- The prompt uses natural-language image direction rather than parameter dumping.
- Anti-AI realism is written as positive preservation, not only a long negative list.
- For edits/replacements, unchanged areas are locked before the requested change is described.
- Language is Chinese natural instruction first, with only limited English camera/lens/lighting/material terms where they improve precision.

Rewrite if:

- It reads like a parameter dump.
- It has huge negative prompt blocks.
- It asks for too many unrelated style systems.
- It only says `不要AI感` without specifying skin, light, material, sharpness, depth, and background failure types.
- It may repaint the whole image during a local edit.

Built-in imagegen anti-AI requirement:

```text
保留真实摄影的不完美：自然皮肤纹理、轻微瑕疵、衣料褶皱、生活痕迹、灰尘、真实暗部颗粒、明确现实光源、不过度锐化、不磨皮、不做假HDR。
```

### Banana / Banana Pro

Approve when:

- First sentence clearly states the image target.
- One image has one dominant subject and one clear scene.
- Shot size, camera position, composition, material, lighting, camera/lens, focal length, aperture/depth, ratio, and negatives are explicit.
- Reference roles are narrow.
- The prompt is compact but dense enough for execution.
- Positive prompt includes tactile imperfections and exposure discipline.
- Negative prompt explicitly controls plastic skin, beauty face, fake depth, HDR sharpening, over-clean backgrounds, text/logo risk, and face/hand drift.
- Prompt follows the required language mix: Chinese image instruction + English camera/lens/lighting/material keywords + Chinese negative terms.

Rewrite if:

- It is a director essay.
- It has conflicting styles.
- It describes multiple sequential actions in one static image.
- It uses abstract meaning before visible content.
- It begins with generic template wording instead of the visible frame.
- It relies on English style shells such as `live-action cinematic documentary still`.
- It is too clean, too glossy, or too polished and does not preserve realistic imperfections.

For Banana Pro, prefer a clean compact execution prompt. Keep the strongest visible image target in the first 60-90 Chinese characters.

Banana/Banana Pro anti-AI requirement:

```text
正向保真：真实摄影质感，皮肤细纹、自然暗部颗粒、衣料褶皱、旧物磨损、环境灰尘、真实景深，明确现实光源，暗部不过度提亮。
负面控制：塑料皮肤、美颜磨皮、AI模特脸、假景深、HDR锐化、过度补光、平台模板感、网剧柔光、背景融化、五官漂移、文字乱码、logo、水印。
```

### Banana / Banana Pro Local Edit

For person replacement, face replacement, object replacement, or local redraw, the prompt must begin with:

```text
只替换原图中的[目标]，严格保留原图背景、构图、机位、镜头透视、光线方向、色调、景深、画面比例、其他人物和环境细节。
```

Reject or rewrite if:

- It does not lock the base image.
- It asks for a new cinematic style that may repaint the whole image.
- It does not specify which reference controls face, hair, costume, pose, or background.

### Jimeng Image

Approve when:

- Chinese prompt is direct and shot-oriented.
- Subject/action/scene comes first.
- Camera, light, material, ratio, and negative terms are clear.

Rewrite if:

- It is too poetic or abstract.
- It contains too much English jargon.
- It leaves text/logo/hand/face risks uncontrolled.

### Midjourney

Approve when:

- Prompt is concise and phrase-based.
- Parameters are correct.
- Visual nouns, composition, light, material, and mood are clear.

Rewrite if:

- It is a long paragraph.
- It contains director explanations.
- It lacks `--ar` or appropriate parameters.

## Video Platform Rules

Default audio policy for Jimeng, Kling, Kling O1, Kling VIDEO 3.0 Omni, and Seedance/Ark video prompts:

```text
不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白。
```

Only change this when the user explicitly requests music, score, dialogue, voiceover, native audio, or a reference voice.

### Prompt Direction Audit Gate

For formal video prompts, require one clear `prompt_direction`:

```text
first_frame_motion
dialogue_coverage
product_motion
reference_continuity
local_edit
multi_shot_omni
quick_motion_test
```

Approve only when the prompt direction matches the platform and task. Reject or split when one copyable prompt combines several directions, such as product insertion + background replacement + wardrobe change + new camera move + weather change + native audio.

Final copyable video prompt order must be:

```text
source authority -> preservation lock -> main action -> camera behavior -> environment/light change -> ending frame -> breath/audio -> forbidden items -> duration/ratio
```

If the prompt is a director note, visual essay, or style discovery request instead of an execution prompt, return `打回重写`.

### Platform Packet Audit Gate

For formal video prompts, require a `video_platform_prompt_packet` or equivalent fields before approval:

```text
target_platform
task_type
prompt_direction
first_frame_or_reference
reference_roles
subject_action
camera_movement
environment_or_light_change
ending_frame
duration
ratio
audio_policy
style_lock_compact
mother_library_video_translation
mother_library_video_application
forbidden_items
manual_execution when the target is an external Jimeng/Kling platform
```

If the packet is missing but the task is quick/test, the auditor may create a lightweight packet from the user request and mark it `quick_test`. If the task is formal, return `missing_fields` and route back to `$ai-video-prompt-director` or the owning upstream skill.

Audit platform fit by target:

```text
Jimeng: first frame is style authority; text must be short, Chinese-first, one action, one camera move, one subtle environment/light change, ending frame.
Seedance-Ark: first-frame/reference URL roles, duration, ratio, resolution expectation, audio policy, and ending frame are required for logged/API work.
Kling: motion must be continuous and physically plausible; no unrelated transformation bundle.
Kling O1 / VIDEO 3.0 Omni: require reference role map for @Image/@Element/@Video/audio, with do_not_inherit boundaries.
```

Do not approve a prompt that uses a mother-library name or cinematographer name as the execution style. Approve only when the mother-library is translated into compact light, space, lens, material, performance, and platform-risk language. For formal work, also approve only when the mother-library application rule is visible: project DNA, scene function, or shot execution rule must be present in compact form.

### Jimeng Video

Jimeng video is sensitive to prompt overload. Execution prompts should usually be 120-250 Chinese characters. Complex one-take prompts may be longer, but still must stay simple.

If Jimeng is used only for video from a first frame, the first frame is the style authority. The execution prompt must not try to regenerate the whole visual style. It should preserve the image and only guide motion.

Official-like Jimeng execution principle:

```text
首帧负责画面：人物、服装、场景、构图、光线、色调、材质、整体风格。
文字负责运动：一个主体动作、一个镜头运动、一个轻微环境变化、一个结束画面。
```

Reject any Jimeng image-to-video prompt that uses video text to rebuild the whole image style. Keep only the compact style lock needed to prevent platform drift.

## 即梦视频审核清单

Before approving a Jimeng video prompt, check the platform-specific traps. For product, vehicle, outdoor action, weather, redraw, or reference-driven motion prompts, approve only when these items are explicit:

```text
不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白
动作按秒数拆阶段：0-1秒 / 1-2秒 / 2-4秒 / 4-5秒
如果动作不明显，必须写清楚必须看到 A -> B -> C 的完整过程
多镜头任务优先拆镜头；一镜到底必须写禁止切镜头、禁止跳切、禁止突然换角度
固定机位任务必须写不推拉、不摇晃、不变焦、不跟随、不旋转
产品/车辆必须限制主体结构、比例、轮子大小、材质、颜色不变
禁止主体重绘、禁止轮子突然变大、车身比例漂移、新增零件、轮距变化
天气变化禁止叠化、渐隐渐现、贴图式变天；必须用云层真实位移、云影遮光、雾气增强、地面反光变化
禁止假HDR、过锐、塑料感、强辉光、CG云层、平台模板感
参考图角色必须说明：场景 / 比例 / 运动 / 风格 / 产品结构分别控制什么
```

Avoid high-risk action wording when a safer physical description works:

```text
避免：冲上去、开炮、暴力、撞击、爆炸、攻击、碾压
改写：快速驶近、设备启动、机械动作展开、越过障碍、尘土被带起、车身轻微震动
```

If these constraints are missing but the visual intent is clear, return `保效精简后通过` only after adding the missing execution constraints. If the product structure, reference roles, action stages, or camera rules are unclear, return `打回重写`.

Approve only when:

- One subject action.
- One camera movement.
- One clear first frame.
- One clear ending frame.
- For short-drama shots, every shot ending includes a light breath tail; every segment/scene/emotional-beat ending includes a heavier 1-2 second breath tail unless the user requests a hard cut.
- At most one light/environment change.
- No long director explanation.
- For image-to-video, it explicitly preserves first-frame character, costume, scene, composition, color, lighting, and material.
- It includes anti-platform-look controls when the goal is cinematic realism.

Rewrite if:

- It reads like a full storyboard.
- It has multiple camera moves: push, pull, orbit, rise, dive, zoom, fly, all in one.
- It has multiple subject actions.
- It asks for cross-space transformation without a clear transition.
- It overuses style adjectives.
- It asks Jimeng to restyle the image instead of animating the first frame.
- It lacks controls against Jimeng-style beautification or short-video platform look.

Compression must preserve:

- first frame
- one subject action
- one camera movement
- key light/color/material atmosphere
- ending frame
- the 3-5 most important forbidden items

Use compact style locks:

```text
低饱和现实主义犯罪片质感，冷白荧光灯，长焦压缩，玻璃反射。
```

Use anti-platform-look controls for cinematic short drama:

```text
禁止网剧柔光、美颜磨皮、AI模特脸、平台模板感、短视频滤镜、假景深、过度锐化、HDR、廉价悬疑蓝。
```

For Jimeng cinematic video, anti-AI controls must be both positive and negative.

Positive preservation required:

```text
保留首帧真实皮肤纹理、自然暗部颗粒、衣料褶皱、环境灰尘、旧物磨损、真实景深和原有光比。
保持真实摄影机拍摄的微弱抖动和自然运动惯性，人物动作克制，焦点稳定锁定主体。
```

Negative controls required:

```text
禁止脸型漂移、五官美颜化、皮肤塑料感、磨皮、假景深、HDR锐化、过度补光、网剧柔光、短视频滤镜、平台模板感、动作抽搐、肢体变形、背景融化、光线乱跳。
```

If a Jimeng cinematic prompt only says `禁止AI感` but does not specify the visual failure types above, rewrite before approval.

Avoid empty style stacks:

```text
电影感、高级感、奥斯卡感、顶级悬疑大片感、真实、克制、厚重、压抑。
```

Default Jimeng video execution formula:

```text
首帧为[画面]，镜头[一个运动]，[主体][一个动作]。[光线/环境一个变化]，结束在[画面]。整体为[简短风格锁定]。禁止[跳切/变形/乱码/多余主体/风格漂移]。[时长/比例]。
```

Default Jimeng image-to-video execution formula:

```text
以首帧为准，严格保持人物、服装、场景、构图、色调、光线和真实材质。[主体一个动作]，镜头[一个运动]，[轻微光影/环境变化]，结束在[画面]。保持[简短风格锁定]。禁止跳切、换景、脸变、服装变、网剧柔光、美颜磨皮、AI短视频感、过度锐化。[时长/比例]。
```

Do not expand this formula into a full image-generation prompt. If the draft contains long mother-library explanation, director rationale, camera-brand lists, or scene redesign, compress it back to the formula above.

Short-drama breath-tail requirement:

```text
Every short-drama shot must append a light breath tail:
本镜头结尾留轻气口，动作/台词后保留0.5-1秒自然呼吸、眼神停顿和轻微余动作。

If the shot is the end of a segment, scene, evidence reveal, phone/message reading, silent reaction, accusation, confrontation, or emotional realization, append a heavy breath tail:
本段结尾留1-2秒重气口，人物不再说新台词，只保留呼吸、眼神停顿、情绪余韵和轻微余动作，镜头稳定停在反应表情或收束画面。
```

Do not require the corresponding breath tail when the user explicitly asks for hard cut, shock cut, flash cut, beat-synced transition, or immediate action exit.

### Kling Video

Approve when motion is physically plausible and continuous.

Rewrite if:

- Camera is too fast or chaotic.
- It requires multiple unrelated transformations.
- It has crowd or complex hand interaction without simplification.

### Kling O1 / VIDEO 3.0 Omni

Use this checklist when `target_platform` is 可灵 O1, 可灵 Omni, Kling O1, Kling VIDEO 3.0 Omni, or the user says Omini/Omni.

Approve only when the prompt defines the role of each uploaded input:

```text
@Image / @Element / @Video role:
- identity / face / body / product structure / prop
- costume / material / color / logo position
- scene / background / light / atmosphere
- start frame / end frame
- motion reference / camera reference
- audio / voice reference
- do_not_inherit
```

Reject or rewrite when:

- It uploads multiple references but does not say what each one controls.
- Two references conflict on identity, costume, product structure, scene, or lighting.
- A motion-reference video is likely to overwrite identity, costume, scene, or color because `do_not_inherit` is missing.
- A local edit prompt may repaint the whole frame instead of modifying the named target area.
- It combines unrelated tasks in one pass, such as adding a product, changing background, changing wardrobe, restyling, and new camera movement at the same time.
- It asks for multi-shot output but does not specify per-shot duration, framing, action, camera movement, and transition logic.
- It asks for group interaction without naming which element performs which action.
- It asks for native audio, dialogue, or voice cloning but does not specify whether audio is required, forbidden, environmental only, or based on a provided voice/audio reference.

For reference-video tasks, require one of these intents:

```text
generate previous/next shot in same context
use @Video only as camera movement reference
use @Video only as action reference
edit named content inside @Video while preserving everything else
extend @Video without changing identity, scene, light, or style
```

Default approval formula for Kling Omni image/element reference:

```text
使用 @ElementA 锁定[身份/产品结构/材质]，使用 @ImageB 锁定[场景/光线/氛围]。[主体]在[环境]中完成[一个主要动作]，镜头[一个运动]，结束在[画面]。禁止改变[身份/比例/结构/颜色/服装/标志位置]，不要继承未指定参考的风格或元素。
```

Default approval formula for Kling Omni local edit:

```text
保持原视频其他内容不变，只修改[目标主体/区域]：[当前状态]变为[目标状态]。保留人物/产品结构、镜头路径、背景空间、光比、色调和真实材质，禁止全画面重绘。
```

If the Omni prompt is for a formal project and the role map is missing, output `missing_fields` and `route_back_to: project-state-manager / scene-style-map-director / project-style-lock` instead of approving.

For managed projects, approved Kling/O1/Omni prompts must also preserve the manual execution fields needed by `$video-generation-controller`: external platform/model, upload roles, copyable prompt, expected output path, and status `manual_handoff` until a downloaded video is attached.

### Kling Omni Reference Conflict Audit

Before approving 可灵 O1 / VIDEO 3.0 Omni, require a `kling_omni_reference_role_map` or equivalent role statement:

```text
target_model
task_type
@Image role
@Element role
@Video role
audio_or_voice_reference role
do_not_inherit
must_preserve
must_change
```

Reject or return `打回重写` if:

- The prompt uploads multiple references but does not name what each one controls.
- `@Video` is used as motion/camera reference but lacks `do_not_inherit` for identity, clothing, scene, color, brand elements, and light style.
- Two references conflict on face, outfit, product structure, scene, light, color, or camera behavior.
- Local edit does not lock non-target regions.
- The prompt asks to change subject, background, camera, weather, audio, and style in one task.
- Multi-shot output lacks per-shot duration, framing, action, camera movement, transition, and ending frame.
- Native audio or reference audio is requested but the prompt does not say whether music, dialogue, environmental sound, voice, or accent should be used.

Kling O1 / VIDEO 3.0 Omni boundary:

```text
Kling O1: single controlled shot, element insertion/replacement, local edit, start/end frame.
Kling VIDEO 3.0 Omni: multi-reference continuity, video reference, multi-shot storyboard, native audio, longer scene work.
```

Scene-board rule:

```text
If a scene-board-image-prompter board is used, each board cell must be assigned a role before approval: character cell, prop cell, set cell, overhead map, keyframe cell, lighting/material cell.
The board itself is not a long style prompt.
```

Audio rule:

```text
If music, dialogue, voiceover, native audio, or a reference voice is not explicitly requested: 不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白。
If audio reference is used: 参考音频只控制声音、口音、情绪和对白节奏，不控制画面、人物、服装、场景、色调或镜头。
```

### Seedance / Ark

Approve when:

- Reference image role or first frame is clear.
- Prompt includes one subject action and one camera movement.
- Duration, ratio, resolution expectations, and forbidden artifacts are clear.
- Public reference URL workflow is assumed when images are used.
- Video text treats first frame/reference as the style authority and only controls motion: one subject action, one camera movement, one subtle environment/light change, and one ending frame.
- Language is Chinese-first, short, direct, and not a director essay.

Rewrite if:

- It depends on local image paths in the prompt.
- It has too many sequential beats for one generation.
- It lacks ending frame.
- It tries to regenerate the full image style instead of preserving the first frame.

## One-Take Audit

For one-take prompts, check:

- Is it truly one space or does it cross spaces?
- Are transitions handled by camera path, occlusion, light, or shape match?
- Is there one target object/subject anchoring the motion?
- Are shot-size changes physically motivated?
- Is the ending frame clear?

If not stable, return `建议拆分` and propose pseudo one-take segments:

```text
A段结尾用遮挡物贴近画面 -> B段从相同遮挡物中开始
```

## Output Contract

Always return or preserve an `audited_prompt_packet` for formal project work:

```text
audited_prompt_packet
decision: 通过 / 保效精简后通过 / 打回重写 / 建议拆分
target_platform:
task_type:
approved_prompt:
negative_or_forbidden:
changed_reason:
missing_fields:
route_back_to:
split_suggestion:
source_prompt_owner:
source_lock:
reference_roles:
duration:
ratio:
audio_policy:
prompt_direction:
director_contribution_check:
visual_helpfulness_check:
kv_composition_style_packet:
video_platform_prompt_packet:
mother_library_application_packet:
manual_execution:
```

Packet rules:

- `approved_prompt` may be used for generation only when `decision` is `通过` or `保效精简后通过`.
- `missing_fields` must name the exact absent creative/style/platform/state fields.
- `route_back_to` must name the owning upstream skill, not a generic "rewrite".
- Auditor may compress or stabilize execution wording but must not create missing mother-library, scene, shot, reference-role, style-lock, character/product continuity, or platform target decisions.

For prompt-only requests:

```text
审核提示：[通过/保效精简后通过/打回重写/建议拆分 + 一句话原因]

最终执行提示词：
[platform-specific final prompt]

负面/禁止项：
[if needed]
```

For tables, add these fields when useful:

```text
审核结果 | 平台执行提示词 | 修改原因
```

## Hard Rules

- Do not approve a prompt only because it is short.
- Do not approve a prompt that loses the intended visual effect.
- Do not approve a prompt whose impressive words cannot change or protect visible pixels, motion, light, composition, material, or continuity.
- Do not approve a video prompt with many actions just because it sounds cinematic.
- Do not approve a Jimeng video prompt that is a long paragraph of director notes.
- Do not approve image edit prompts that may repaint the whole image.
- Do not approve reference-image prompts without explicit reference roles.
- Do not repair missing creative decisions; route back to the upstream owner instead.
- If the prompt is wrong for the platform, rewrite it or mark it `打回重写`.
