---
name: image-qc-director
description: Quality-control generated images for film and screen visual workflows. Use after Banana/OpenAI image generation when the user asks whether generated images are usable, need revision, should be regenerated, or should have prompts rewritten. Checks storyboard alignment, unified visual style, subject accuracy, composition, reference-image usage, text/logo risks, face/hand issues, and generation artifacts.
---

# Image QC Director

## Core rule

Use this skill after images have been generated or when the user provides generated image paths/screenshots and asks whether they work.

Judge against the original storyboard, prompt, unified visual style package, reference image constraints, and delivery context. Do not judge only by whether the image looks beautiful.

## QC decisions

Use one of four decisions:

| 判断 | 含义 | 下一步 |
| --- | --- | --- |
| 可用 | 基本符合分镜和风格，可进入PPT或视频首帧 | 记录可用版本 |
| 可小修 | 方向正确，有轻微问题 | 局部修提示词或后期修图 |
| 建议重出 | 构图/主体/质量问题明显，但提示词方向可保留 | 用同一提示词或小改后重出 |
| 提示词需重写 | 画面偏离根本目标，或风格/主体/参考图约束失效 | 重写该镜头提示词再出图 |

## QC checklist

Check:

- 主体是否正确：人物、产品、场景、道具、舞台关系是否符合分镜。
- 风格是否统一：是否保持全片统一风格包、摄影感、色彩、材质和光线逻辑。
- 构图是否符合用途：PPT关键帧、LED大屏、视频首帧、社媒竖版是否适配。
- 文本和Logo是否出错：乱码、错误标识、误生成品牌元素、标题空间污染。
- 人物和产品质量：脸、手、姿态、比例、产品结构、材质、反光是否可用。
- 参考图是否正确使用：是否只用了指定局部特征，是否错误改变整组风格。
- 生成瑕疵：水印、边框、AI感、低清、过曝、过锐、无关物体。

## Output

### 出图质检表

| 镜号 | 图片版本 | 工具 | 图片路径 | 判断 | 主要问题 | 可保留内容 | 修改建议 | 是否重出 | 关联Sheet |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

### 重出建议

If regeneration is needed, output only the affected rows:

| 镜号 | 原版本 | 重出方式 | 提示词修改点 | 参考图调整 | 负面词补充 | 新版本建议 |
| --- | --- | --- | --- | --- | --- | --- |

## Rules

- If only one shot fails, do not change the full style package.
- If multiple S/A shots drift in the same way, recommend updating the unified style package.
- If text/logo is wrong, first recommend removing generated text or reserving blank title space.
- If face/hand/product structure fails, simplify the action and strengthen reference constraints.
- If the image is for video first frame, judge whether it has clean motion potential, not only still-frame beauty.
