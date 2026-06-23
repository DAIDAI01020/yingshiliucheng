---
name: style-bible-director
description: Style bible and continuity director for film AI workflows. Use when a project needs a unified visual system, visual continuity rules, camera and lens consistency, color/material rules, reference-image usage rules, character/product/scene continuity, forbidden drift items, or style protection during batch prompts, added shots, regeneration, and image QC.
---

# Style Bible Director

## Core Role

Maintain the project's visual constitution.

A project can explore options early, but once a route is chosen, all S/A priority shots should follow the same style bible unless the script intentionally changes chapter, time, location, or mood.

Use this before:

- Batch image prompts
- Batch image generation
- Added shots
- Regeneration
- Video prompt groups
- Image or video QC
- Client revision that may affect style

For formal projects, prefer receiving style inputs from `$reference-aesthetic-director` first. The reference aesthetic step provides top-level film/TVC/documentary/stage principles; this skill turns those principles into enforceable production rules.

After the style bible is approved, formal projects should create or update `$project-style-lock`.

The style bible is the full constitution. The style lock is the compact, reusable execution layer that downstream prompt skills must inherit every time.

## Style Bible Fields

Formal style bibles must include these machine-checkable fields in addition to the human-readable style table:

```text
director_contribution_packet
visual_helpfulness_targets
```

`director_contribution_packet` records the owned decisions from reference, scene, shot-language, character/product continuity, and platform prompt directors. `visual_helpfulness_targets` lists the concrete visible controls that downstream prompts must protect: subject identity, blocking, lens, light, color, material, motion, ending frame, and AI risk.

| 风格项 | 统一设定 | 执行提示 |
| --- | --- | --- |
| style_id |  |  |
| 主视觉方向 |  |  |
| 摄影系统 |  |  |
| 镜头语言/焦段 |  |  |
| 光线逻辑 |  |  |
| 色彩/调色 |  |  |
| 材质/质感 |  |  |
| 构图规则 |  |  |
| 景深/颗粒/锐度 |  |  |
| 人物连续性 |  |  |
| 产品/道具连续性 |  |  |
| 场景连续性 |  |  |
| 参考图使用规则 |  |  |
| 参考风格转译 |  |  |
| upstream_source |  | 记录参考图匹配、母库路线、场戏地图、镜头语言审核、风格锁来自哪里 |
| mother_library_application_packet |  | 母库如何控制项目DNA、场戏功能、镜头执行、平台风险，不只是参考名 |
| director_contribution_packet |  | Preserve upstream director decisions: reference route, scene function, shot function, character/product continuity, and platform prompt translation |
| visual_helpfulness_targets |  | Concrete visible controls that downstream prompts must protect: subject identity, blocking, lens, light, color, material, motion, ending frame, and AI risk |
| mother_library_translation |  | 光线方向、空间关系、焦段心理、构图调度、材质触感、人物表演状态、AI风险控制 |
| platform_language_strategy |  | 内置 image / Banana-Banana Pro / Jimeng-Seedance 的语言策略 |
| anti_ai_realism_rule |  | 真实皮肤纹理、衣料褶皱、生活痕迹、灰尘旧物、暗部颗粒、真实光源、原有光比、不过锐、不磨皮、不假HDR |
| image_tool_boundary |  | 正式出图默认内置 imagegen 或 Banana/Banana Pro；即梦主要用于图生视频，除非用户明确要即梦图片 |
| jimeng_seedance_motion_rule |  | 首帧负责画面风格；文字只负责一个主体动作、一个镜头运动、一个轻微环境变化、一个结束画面 |
| breath_tail_rule |  | 短剧每个镜头结尾默认轻气口；每一段/场戏/情绪落点结尾默认1-2秒重气口 |
| 顶级参考来源 |  |  |
| 禁止偏移项 |  |  |
| AI 风险控制 |  |  |

## Project Style Lock Handoff

When a route is chosen, output or update:

```text
upstream_source
mother_library_application_packet
director_contribution_packet
visual_helpfulness_targets
style_id
master_style_sentence
mother_library_translation
platform_language_strategy
anti_ai_realism_rule
image_tool_boundary
jimeng_seedance_motion_rule
breath_tail_rule
camera_system
lens_family
lighting_rule
color_rule
material_rule
composition_rule
scene_variation_rule
forbidden_drift
negative_prompt_base
```

Downstream prompts must inherit these fixed variables. Do not allow later prompts to rephrase the core style freely unless the user asks to update the whole style.

Do not hand off a formal style bible to `$project-style-lock` if it only contains camera/lens/light/color/material. The handoff must include mother_library_application_packet, director_contribution_packet, visual_helpfulness_targets, mother_library_translation, platform_language_strategy, anti_ai_realism_rule, image_tool_boundary, jimeng_seedance_motion_rule, and breath_tail_rule so the next layer can manage image and video execution without gaps.

## Continuity Checks

Before prompts, generation, added shots, or regeneration, check:

- Does the shot keep the same camera/lens/lighting/color/material logic?
- Does the reference image only control the intended local feature?
- Does the prompt repeat the style bible instead of saying `同上`?
- Does the prompt inherit the current `$project-style-lock` instead of re-inventing a new style?
- Does the prompt preserve mother_library_translation instead of reducing the style to film names or adjectives?
- Does the prompt inherit the right rule from mother_library_application_packet for this scene function?
- Does the prompt preserve director_contribution_packet instead of deleting upstream reference, scene, shot, continuity, or platform decisions?
- Does every style phrase map to a visible helpful target rather than a generic taste adjective?
- Does the shot obey platform_language_strategy and image_tool_boundary?
- Does the shot preserve anti_ai_realism_rule: real skin/material texture, dust/worn objects, natural shadow grain, real light source, and original light ratio?
- For Jimeng/Seedance video, does it obey jimeng_seedance_motion_rule?
- For short-drama shots, does every shot keep a light breath_tail_rule and every segment/scene/emotional-beat ending keep a heavier 1-2 second breath_tail_rule unless the user requested a hard cut?
- Will this shot break character, product, scene, LED-screen, or brand continuity?
- Is the requested change global style change or only a single-shot adjustment?
- Does the shot create new text/logo/hand/face/product-structure risks?

## Drift Decisions

| 判断 | 含义 | 处理 |
| --- | --- | --- |
| 无漂移 | 完全继承风格圣经 | 继续 |
| 单镜头调整 | 只影响一个镜头，不改变全片风格 | 只改该镜头 |
| 局部章节变化 | 同一项目内的章节/时间/空间变化 | 建立章节子风格 |
| 全片风格变化 | 影响所有 S/A 镜头 | 先更新风格圣经，再重写受影响提示词 |

## Output

### 风格圣经

| 项目 | 统一规则 | 执行提示 |
| --- | --- | --- |

### 连续性风险表

| 镜号 | 风险点 | 是否影响全片 | 处理建议 |
| --- | --- | --- | --- |

### 重出保护规则

| 情况 | 是否允许改风格 | 处理方式 |
| --- | --- | --- |
| 单图构图失败 | 否 | 只调构图/机位/负面词 |
| 多图同类漂移 | 可能 | 先判断是否更新风格圣经 |
| 客户说整体不高级 | 是 | 先改风格圣经 |
| 手/脸/文字错误 | 否 | 简化动作、增强负面词 |

## Rules

- Do not create a new style for every shot.
- If the user says the whole style is wrong, update the bible first.
- If only one image is wrong, protect the bible and only adjust the shot.
- For reference images, define exactly what each reference controls: pose, composition, material, color detail, style, or character identity.
- Do not let a single reference image override the project style.
