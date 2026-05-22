---
name: ai-video-prompt-director
description: 生成影视AI视频提示词。用于把关键画面、分镜或AI首帧转成即梦、可灵、Seedance/Ark 可复制使用的视频生成提示词，包含视频可行性判断、首帧、主体动作、镜头运动、环境变化、光影变化、节奏、时长、比例和禁止项，尤其适合一镜到底与伪一镜到底设计。
---

# AI Video Prompt Director

## Core Rule

Video prompts should be simple, continuous, physically plausible, and easy for video models to follow.

Default to:

- One dominant subject action.
- One dominant camera movement.
- One environment/light change only when useful.
- One clear first frame.
- One clear ending frame.

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
2. Run the video feasibility check.
3. Describe one dominant subject action and one dominant camera movement.
4. Add environment and light changes only when they support the shot.
5. For Seedance/Ark, write the prompt so it can pair with 1-9 public `http/https` reference image URLs.
6. Keep the final prompt copyable and concise enough for the target tool.

## Output

| 镜号 | 工具 | 视频提示词 | 首帧要求 | 运动重点 | 结束画面 | 禁止项 | 时长/比例 |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Tool Guidance

- 即梦: specify first frame, camera movement, subject action, light change, and ending frame.
- Seedance/Ark: specify first frame/reference role, one subject action, one camera movement, one environment/light change, duration, ratio, resolution, and forbidden artifacts.
- 可灵: keep motion simple, continuous, and cinematic; avoid multiple competing transformations.

## Avoid

- Too many subjects moving in different directions.
- Fast chaotic camera movement unless explicitly needed.
- Complex text generation inside video.
- Brand logo generation unless a provided asset workflow exists.
- Cross-space transformation without a transition device.
- Full scene replacement in a claimed one-take shot.

