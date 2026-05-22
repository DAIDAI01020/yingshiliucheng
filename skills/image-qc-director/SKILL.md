---
name: image-qc-director
description: Quality-control generated images and video first frames for film and screen visual workflows. Use after built-in imagegen, Banana, Midjourney, or other image generation when the user asks whether generated images are usable, need revision, should be regenerated, or should have prompts rewritten. Checks storyboard alignment, unified visual style, subject accuracy, composition, reference-image usage, text/logo risks, face/hand issues, generation artifacts, and video first-frame motion potential.
---

# Image QC Director

## Core Rule

Use this skill after images have been generated or when the user provides generated image paths/screenshots and asks whether they work.

Judge against:

- Original storyboard or shot intent.
- Prompt.
- Unified style bible.
- Reference image constraints.
- Delivery context.
- Whether the image will be used as a video first frame.

Do not judge only by whether the image looks beautiful.

## QC Decisions

| 判断 | 含义 | 下一步 |
| --- | --- | --- |
| 可用 | 基本符合分镜和风格，可进入 PPT、首帧或交付候选 | 记录可用版本 |
| 可小修 | 方向正确，有轻微问题 | 局部修提示词或后期修图 |
| 建议重出 | 构图/主体/质量问题明显，但提示词方向可保留 | 小改后重出 |
| 提示词需重写 | 画面偏离根本目标，或风格/主体/参考图约束失效 | 重写该镜头提示词再出图 |

## Issue Tags

Use concise issue tags:

```text
风格漂移 / 主体错误 / 构图不可用 / 光线不对 / 材质不对 / 文字logo风险 / 手脸异常 / 产品结构错误 / 参考图误用 / AI感过强 / 低清晰度 / 视频运动风险 / 首帧不可用 / 提示词需重写
```

## QC Checklist

Check:

- 主体是否正确：人物、产品、场景、道具、舞台关系是否符合分镜。
- 风格是否统一：是否保持风格圣经、摄影感、色彩、材质和光线逻辑。
- 构图是否符合用途：PPT关键帧、LED大屏、视频首帧、社媒竖版是否适配。
- 文本和Logo是否出错：乱码、错误标识、误生成品牌元素、标题空间污染。
- 人物和产品质量：脸、手、姿态、比例、产品结构、材质、反光是否可用。
- 参考图是否正确使用：是否只用了指定局部特征，是否错误改变整组风格。
- 生成瑕疵：水印、边框、AI感、低清、过曝、过锐、无关物体。
- 视频首帧潜力：是否有清晰运动方向、主体是否稳定、边缘是否干净、是否方便做推拉/环绕/转场。

## Output

### 出图质检表

| 镜号 | 图片版本 | 工具 | 图片路径 | 判断 | 问题标签 | 主要问题 | 可保留内容 | 修改建议 | 是否重出 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

### 重出建议

If regeneration is needed, output only affected rows:

| 镜号 | 原版本 | 重出方式 | 提示词修改点 | 参考图调整 | 负面词补充 | 新版本建议 |
| --- | --- | --- | --- | --- | --- | --- |

## Rules

- If only one shot fails, do not change the full style bible.
- If multiple S/A shots drift in the same way, recommend updating the style bible.
- If text/logo is wrong, first recommend removing generated text or reserving blank title space.
- If face/hand/product structure fails, simplify the action and strengthen reference constraints.
- If the image is for video first frame, judge clean motion potential, not only still-frame beauty.

