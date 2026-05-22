---
name: short-drama-scene-director
description: Break down short drama scripts, finished drafts, or storyboards into scene-level visual direction, per-location style references, shot/keyframe requirements, reference-image roles, AI image prompt requirements, video prompt requirements, and generation risk notes.
---

# Short Drama Scene Director

## Core Role

`$short-drama-scene-director` turns a script, finished draft, or storyboard into scene-level visual direction and AI-generatable execution units.

It should not only split shots. It must first decide how scenes are grouped visually: which location, time, light source, emotion, clue, or turning point defines each scene.

Use when the user provides:

- 已有剧本
- 已有分镜
- 场次表
- 参考图
- 影视风格参考
- 需要拆成出图/视频镜头
- 需要每场戏先给风格参考

## Scene Merging Rules

Do not create one image prompt per script sentence by default.

Merge shots into scene-level concepts when they share:

- 同一地点或连续空间
- 同一时间段或光源逻辑
- 同一情绪阶段
- 同一证据/线索推进
- 同一人物关系状态
- 同一视觉符号

Split into separate scenes when there is:

- 地点变化
- 日夜/天气/光源变化
- 情绪强度显著变化
- 叙事功能变化，例如报案、审问、反转、闪回、认罪、结案
- 视觉系统变化，例如现实空间转为回忆、监控、梦境、新闻、法庭

## Required Output 1: Scene Merge Table

| 场次 | 覆盖原稿段落/镜头 | 场名 | 地点/时间 | 主要人物 | 叙事功能 | 是否需要关键帧 | 是否需要视频 |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Required Output 2: 每场戏风格参考 / 视觉导演设定

For every scene, output this before any prompt:

| 场次 | 场名 | 参考审美方向 | 光线/色温 | 色彩/材质 | 构图/焦段 | 视觉符号 | 为什么这样设定 | AI 风险 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

### Field Rules

- `参考审美方向`: Use film/series/documentary/TVC principles, not exact frame copies.
- `光线/色温`: Must be specific: rain after dusk, warm fluorescent room, cold monitor light, dawn forest mist, late-afternoon side light, etc.
- `色彩/材质`: Mention real materials: wet concrete, glass door, phone glow, police desk wood, muddy roots, fluorescent wall, court stone, steel, fabric.
- `构图/焦段`: Mention camera distance and psychological effect: low angle, through glass, over shoulder, long-lens compression, foreground obstruction, close portrait.
- `视觉符号`: Name objects that carry drama: phone, text message, glass reflection, monitor, evidence bag, muddy road, taillight, file, badge, door crack.
- `为什么这样设定`: Explain in plain production language so clients understand the intention.
- `AI 风险`: Identify what generation may break and how to avoid it.

## Required Output 3: Shot/Keyframe Table

Only after scene visual direction is approved or clearly implied:

| 镜号 | 场次 | 景别 | 角色 | 动作/表情 | 构图 | 参考图角色 | 是否出图 | 是否出视频 | 风险 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Reference Role Table

| 参考图 | 绑定对象 | 参考角色 | 不继承内容 |
| --- | --- | --- | --- |

Reference image roles should be narrow:

- 人物脸/发型
- 服装质感
- 场景地点
- 动作姿态
- 构图关系
- 光线/色调
- 材质细节

Avoid asking the model to average several references into one unclear result.

## Scene-Level Prompt Handoff

When handing to `$frame-vision-director`, include:

```text
全剧统一风格 DNA
本场视觉参考
角色锚点
参考图角色
镜头意图
构图/机位/焦段
光线/色彩/材质
AI 风险与负面词
```

When handing to `$ai-video-prompt-director`, include:

```text
首帧来源
主动作
主镜头运动
空间路径
遮挡/衔接方式
结束画面
禁止跳切/换景/多动作
```

## AI Risk Rules

- More than two speaking characters in one frame increases consistency risk.
- Long dialogue should be subtitles in post, not generated inside image/video.
- Screens, phones, documents, monitors, case files, and court signs should not contain readable long text.
- Complex fights, crying, kissing, crowds, and hand-object interaction need simplified shots.
- Preserve character identity over fancy camera movement.
- For vertical short drama, prioritize close-up, over-shoulder, two-shot, reaction shot, and controlled blocking.

## Quality Bar

A good scene visual reference should let the user understand:

- 这场戏为什么长这样
- 和上一场有什么区别
- 和全剧风格为什么仍然统一
- 哪些参考图该被继承
- AI 最容易翻车的地方在哪里
- 后续出图和出视频怎么接

If this is not clear, do not move directly to final prompts.
