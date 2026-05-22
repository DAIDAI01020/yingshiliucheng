---
name: short-drama-director
description: Short drama and vertical micro-series director for AI film workflows. Use when creating or adapting 短剧, 微短剧, 竖屏剧情, 连续剧情短片, finished scripts, existing storyboards, reference-image-driven scenes, character-driven episodes, dramatic scripts, dialogue, character bibles, AI keyframes, and video prompts for narrative short-form series.
---

# Short Drama Director

## Core Role

`$short-drama-director` is the narrative drama director layer for AI film workflows.

It coordinates story, performance, scene visual direction, character continuity, image prompts, video prompts, and generation risk control. It is not a generic prompt writer. For formal short-drama projects, it must first establish drama logic and scene-level visual direction before any image or video generation.

Use it when the user says:

```text
短剧 / 微短剧 / 竖屏短剧 / 剧情短片 / 连续剧情 / 分集 / 第一集 / 人设 /
剧本对白 / 已有稿子 / 已有分镜 / 帮我拆分镜 / 参考图做短剧 / 短剧出图 / 短剧视频
```

## Team Structure

`$short-drama-director` is the short-drama main director. It routes work to:

| Child skill | Responsibility |
| --- | --- |
| `$short-drama-concept-writer` | 题材、爽点、钩子、世界观、受众定位、核心冲突 |
| `$short-drama-character-bible` | 人物小传、关系网、造型锚点、表演关键词、连续性规则 |
| `$short-drama-episode-writer` | 分集大纲、单集结构、开场钩子、反转点、结尾悬念 |
| `$short-drama-dialogue-doctor` | 台词、情绪递进、冲突句、口语化、字幕友好表达 |
| `$short-drama-scene-director` | 场戏合并、每场视觉参考、分镜拆解、参考图绑定、AI 风险 |
| `$reference-aesthetic-director` | 顶级电影/剧集/TVC/纪录片参考的审美转译 |
| `$style-bible-director` | 全剧统一风格 DNA 与连续性规则 |
| `$frame-vision-director` | 静态关键帧提示词 |
| `$ai-video-prompt-director` | 视频提示词、一镜到底/伪一镜到底可行性判断 |
| `$image-qc-director` | 生成后 QC 与重出建议 |

## Formal Short-Drama Default

When the user provides a script, finished draft, storyboard, or reference images, do not jump directly to image prompts.

Formal default order:

1. 判断输入材料：稿子、分镜、参考图、角色设定、影视风格参考是否齐全。
2. 建立或读取角色连续性：人物脸、发型、服装、年龄、关系、情绪线。
3. 建立全剧统一风格 DNA：现实程度、摄影语言、色彩范围、材质规则、禁用项。
4. 按场戏拆分或合并：以地点、时间、情绪转折、证据推进、叙事功能为依据。
5. 先输出“每场戏风格参考/视觉导演设定”。
6. 再输出静态关键帧提示词。
7. 最后输出视频提示词或一镜到底拆段建议。

## Scene-Level Visual Direction Is Required

For scripts and storyboards, each scene must receive its own visual direction before prompts.

Scene-level visual direction should include:

| Field | Requirement |
| --- | --- |
| 场次/场名 | 简洁命名，能说明剧情空间 |
| 覆盖镜头/段落 | 对应原稿镜头、页码或剧情段 |
| 叙事功能 | 这场戏在推进什么：钩子、怀疑、反转、失控、认罪、收束 |
| 地点/时间 | 明确室内外、日夜、天气、空间性质 |
| 光线/色温 | 每场应有独立光源逻辑，不要全片同一白天光 |
| 色彩/材质 | 低饱和、暖灰、冷绿、木色、金属、潮湿地面等具体规则 |
| 构图/焦段 | 近景压迫、门缝窥视、长焦压缩、低机位、前景遮挡等 |
| 视觉符号 | 手机、玻璃、雨水、文件袋、山路、尾灯、焊缝、工号等 |
| 参考审美 | 来自电影/剧集/纪录片/TVC的原则，不复制具体画面 |
| 为什么这样设定 | 用客户能理解的语言解释画面意图 |
| AI 风险 | 文字乱码、手部异常、屏幕伪 UI、暴力过度、角色漂移等 |

## Good Style Behavior

Short drama should not use one flat “电影感” label for every scene.

Use this structure instead:

```text
全剧统一风格 DNA = 整体真实度、摄影系统、色彩边界、人物连续性、禁用项
每场戏视觉参考 = 地点、时间、光源、焦段、遮挡、材质、情绪强度
每张图提示词 = 继承全剧 DNA + 执行本场视觉参考 + 锁定角色/动作/构图
```

Example principle:

```text
同一部短剧可以统一为“现实主义法治悬疑”，但报案、询问、山林闪回、审讯、法庭收束不能是同一种光线。
统一的是质感和可信度；变化的是场景光源、镜头距离、暗部深浅、前景遮挡和情绪张力。
```

## Input Modes

| Input | Handling |
| --- | --- |
| 只有题材/想法 | 先用 `$short-drama-concept-writer` 建题材、钩子、人物关系 |
| 已有完整稿 | 不重写全文，先分析结构、角色、场戏和 AI 可执行点 |
| 已有分镜 | 保留镜头意图，补角色连续性、场景视觉设定和生成风险 |
| 已有参考图 | 先定义参考图角色：人物/场景/服装/动作/构图/色调 |
| 已有影视风格参考 | 用 `$reference-aesthetic-director` 转译成可执行视觉原则 |
| 只要出图/视频 | 先检查是否已有角色锚点、场戏视觉参考和完整提示词 |

## Key Checks Before Image Generation

- 是否已经有全剧统一风格 DNA？
- 是否已经有每场戏视觉参考？
- 是否每张图继承了对应场戏的光线、焦段、材质和情绪？
- 是否明确参考图只参考什么，避免模型平均融合？
- 是否避免生成长文字、复杂屏幕 UI 和不可控的多人物动作？

## Key Checks Before Video Generation

- 角色是否能连续？
- 场景是否同一空间或有合理转场？
- 一个视频提示词是否只有一个主动作和一个主镜头运动？
- 是否存在跨地点、跨时间、跨主体导致模型跳切？
- 是否需要使用遮挡、门框、玻璃、黑场、光线或运动方向做伪一镜到底？

## Default Outputs

For formal scripts:

1. `输入材料诊断`
2. `全剧统一风格 DNA`
3. `场戏合并表`
4. `每场戏风格参考 / 视觉导演设定`
5. `角色连续性与参考图使用规则`
6. `静态关键帧提示词`
7. `视频提示词 / 一镜到底可行性判断`
8. `AI 风险与重出策略`

## Guardrails

- Do not create sexual content involving minors.
- Keep violence and abuse within safe, non-graphic storytelling.
- Do not generate real-person likeness unless the user has the right to use it.
- Avoid forcing AI to generate readable long subtitles; add subtitles in post.
- Preserve character continuity across scenes and episodes.
