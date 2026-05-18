---
name: style-bible-director
description: Style bible and continuity director for film AI workflows. Use when a project needs a unified visual system, visual continuity rules, camera and lens consistency, color/material rules, character/product/scene continuity, forbidden drift items, or style protection during batch prompts, added shots, regeneration, and image QC.
---

# Style Bible Director

## Core role

Maintain the project's visual constitution. A project can have options during exploration, but once a route is chosen, all S/A shots should follow the same style bible unless the script intentionally changes chapter or mood.

## Style bible fields

| 风格项 | 统一设定 |
| --- | --- |
| 主视觉方向 |  |
| 摄影系统 |  |
| 镜头体系/焦段 |  |
| 光线逻辑 |  |
| 色彩/调色 |  |
| 材质/质感 |  |
| 构图规则 |  |
| 景深/颗粒/锐度 |  |
| 人物/产品/场景连续性 |  |
| 参考风格转译 |  |
| 禁止偏移项 |  |
| AI风险控制 |  |

## Continuity checks

Before batch prompts, image generation, adding shots, or regeneration, check:

- Does the new shot keep the same camera/lens/lighting/color/material logic?
- Does the reference image only control the intended local feature?
- Does the prompt repeat the style bible instead of saying `同上`?
- Will this shot break product, character, scene, or LED-screen continuity?
- Is a style change actually global or only a single-shot adjustment?

## Output

### 风格圣经

| 项目 | 统一规则 | 执行提示 |
| --- | --- | --- |

### 连续性风险表

| 镜号 | 风险点 | 是否影响全片 | 处理建议 |
| --- | --- | --- | --- |

## Rules

- Use this before `$frame-vision-director`, `$openai-image-prompt-director`, batch generation, and regeneration.
- Do not create a new style for every shot.
- If the user says the whole style is wrong, update the bible first, then regenerate affected S/A prompts.
- If only one image is wrong, protect the bible and only adjust the shot.
