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

## Style Bible Fields

| 风格项 | 统一设定 | 执行提示 |
| --- | --- | --- |
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
| 顶级参考来源 |  |  |
| 禁止偏移项 |  |  |
| AI 风险控制 |  |  |

## Continuity Checks

Before prompts, generation, added shots, or regeneration, check:

- Does the shot keep the same camera/lens/lighting/color/material logic?
- Does the reference image only control the intended local feature?
- Does the prompt repeat the style bible instead of saying `同上`?
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
