---
name: project-style-lock
description: Lock a formal film AI project's approved visual style into stable reusable variables before image/video prompt writing. Use when a project has chosen a style reference, style bible, scene map, character look, or prompt route and the user wants consistent prompts across shots, regenerations, scenes, Banana/Banana Pro, Jimeng, Midjourney, or Seedance. Prevents the assistant from re-inventing style wording every turn by producing a fixed style_id, master style sentence, camera/lens/light/color/material rules, prompt schema, and forbidden drift list.
---

# Project Style Lock

## Core Role

`$project-style-lock` freezes the approved visual system into stable prompt variables.

It prevents this failure:

```text
same project -> every turn reselects references -> every prompt sounds different
```

Once a formal project style is approved, downstream prompts must inherit the lock instead of re-deciding style from scratch.

## When To Use

Use after:

```text
reference-image-style-matcher
style-reference-director
scene-style-map-director
style-bible-director
```

Use before:

```text
frame-vision-director
ai-video-prompt-director
prompt-platform-auditor
generation
regeneration
added shots
```

## Output: Project Style Lock

| Field | Required content |
| --- | --- |
| upstream_source | where this lock comes from: reference-image-style-matcher, style-reference-director, scene-style-map-director, shot-language-auditor, style-bible-director |
| style_id | stable snake_case id, e.g. `shizong_zhangfu_crime_realism_v1` |
| project_type | short drama / brand film / TVC / event / LED / misc |
| primary_reference_family | one primary mother-library family |
| secondary_reference_family | zero to two support references |
| cinematography_anchor | one top-tier cinematography anchor |
| mother_library_application_packet | active mother-library contract: project DNA, scene function rules, shot execution rules, do_not_copy, forbidden_drift, prompt inheritance |
| director_contribution_packet | compact record of each upstream director's owned visual decision and what downstream prompts must preserve |
| visual_helpfulness_targets | concrete visible targets that each downstream prompt phrase must improve or protect |
| mother_library_translation | prompt-ready light direction, space relation, lens psychology, composition blocking, material touch, performance state, and AI risk control |
| platform_language_strategy | built-in image: Chinese natural instruction; Banana/Banana Pro: Chinese image instruction + English camera/lens/lighting/material keywords + Chinese negatives; Jimeng/Seedance: Chinese short motion sentences |
| anti_ai_realism_rule | preserve real skin texture, fabric wrinkles, life traces, dust/worn objects, natural shadow grain, real depth of field, source-motivated light, and original light ratio |
| image_tool_boundary | formal image generation defaults to built-in imagegen or Banana/Banana Pro; Jimeng is not the default still-image route unless explicitly requested |
| jimeng_seedance_motion_rule | first frame controls image style; text controls one subject action, one camera movement, one subtle environment/light change, and one clear ending frame |
| breath_tail_rule | every short-drama shot ends with a light breath tail; every segment/scene/emotional-beat ending gets a heavier 1-2 second breath tail unless hard cut/beat cut/shock point is requested |
| master_style_sentence | fixed 1-2 sentence executable style language |
| camera_system | one camera/visual system |
| lens_family | allowed focal lengths and their use |
| aperture_depth_rule | depth-of-field and sharpness rule |
| lighting_rule | allowed light sources, direction, contrast |
| color_rule | palette, saturation, contrast, forbidden color drift |
| material_rule | key tactile materials |
| composition_rule | blocking, foreground/background, negative space, screen format |
| grain_texture_rule | grain, softness, highlight rolloff, skin texture |
| reference_image_rule | what references can and cannot control |
| short_drama_hook_packet_source | for formal short drama, the approved hook-audit source that protects the first 3-8 seconds and conflict entry |
| character_continuity_source | for formal short drama, the approved character-continuity source that protects identity, costume, performance, and relationship drift |
| scene_variation_rule | what may change per scene |
| forbidden_drift | cheap/incorrect visual directions |
| negative_prompt_base | reusable base negative terms |

## Master Style Sentence Rule

The `master_style_sentence` must be stable and reusable.

Bad:

```text
电影感，高级，真实，奥斯卡质感。
```

Good:

```text
现实主义犯罪悬疑影像，ARRI Alexa 35质感，低饱和中性灰与自然暗部颗粒，实用光源和窗光主导，长焦轻微压缩人物关系，旧木桌、卷宗、湿泥、布料和真实皮肤保持可触摸质感。
```

## Fixed Prompt Schema

Downstream image prompts must follow this order:

```text
1. 可见画面目标
2. 镜头功能和叙事信息
3. 景别/机位/构图
4. 摄影系统/焦段/光圈或景深
5. 项目 style lock 句
6. mother_library_application_packet 中对应场戏/镜头的应用规则
6A. director_contribution_packet: upstream reference, scene, shot, continuity, and platform decisions that must remain visible
6B. visual_helpfulness_targets: subject, blocking, lens, light, color, material, text/logo, and AI-risk controls
7. mother_library_translation
8. 本场局部光线/色彩/材质变化
9. anti_ai_realism_rule
10. 参考图角色
11. platform_language_strategy / image_tool_boundary
12. 比例和质量
13. 负面词
```

Downstream video prompts must follow this order:

```text
1. 首帧
2. 主体动作
3. 一个主镜头运动
4. 景别变化路径或剪辑动机
5. 项目 style lock 压缩句
6. mother_library_application_packet 的视频安全应用规则
6A. director_contribution_packet: upstream shot, continuity, reference, and prompt-direction decisions
6B. visual_helpfulness_targets: first-frame preservation, subject action, camera path, environment/light change, ending frame, and risk controls
7. jimeng_seedance_motion_rule
8. 光线/材质/色彩
9. 结束画面
10. breath_tail_rule: every shot light breath tail; segment/scene/emotional-beat ending heavy breath tail
11. 禁止项
12. 时长/比例
```

## Cross-Skill Management Gate

Do not create or update a formal project style lock if upstream decisions are missing.

Required upstream_source:

```text
style-reference-director decision
short-drama hook-audit when this is a formal short-drama project
short-drama character-continuity when recurring characters appear
mother_library_application_packet
director_contribution_packet
visual_helpfulness_targets
scene-style-map-director scene map
style-bible-director approved style bible
reference-image-style-matcher result when reference images are used
shot-language-auditor result for short-drama multi-shot work
prompt-platform-auditor target platform expectations
```

If any upstream item is missing, state the missing source and route back to that skill. Do not invent missing style, shot logic, reference roles, or platform policy inside the lock.

## Scene Variation Rule

Allowed to vary per scene:

```text
地点
时间
光源方向
景别
焦段
前景遮挡
情绪强度
关键物件
空间关系
```

Not allowed to vary unless the style lock is updated:

```text
主参考体系
摄影系统
镜头家族
真实度
色彩边界
材质可信度
人物皮肤质感
负面漂移规则
```

## Handoff Contract

`$frame-vision-director` must embed the style lock in every copyable image prompt.

`$ai-video-prompt-director` must compress the style lock into video-safe language.

`$prompt-platform-auditor` must reject formal project prompts that ignore the style lock or re-invent an incompatible style.

Every downstream handoff must preserve:

```text
upstream_source
mother_library_translation
mother_library_application_packet
director_contribution_packet
visual_helpfulness_targets
short_drama_hook_packet_source when applicable
character_continuity_source when applicable
platform_language_strategy
anti_ai_realism_rule
image_tool_boundary
jimeng_seedance_motion_rule
breath_tail_rule
```
