---
name: ai-video-prompt-director
description: 生成影视AI视频提示词。用于把关键画面、分镜或AI首帧转成即梦和可灵可复制使用的视频生成提示词，包含首帧、主体动作、镜头运动、环境变化、光影变化、节奏、时长、比例和禁止项。
---

# AI Video Prompt Director

## Process

1. Start from a clear first frame or storyboard shot.
2. Describe one dominant subject action and one dominant camera movement.
3. Add environment and light changes only when they support the shot.
4. Keep motion physically plausible and easy for video models to follow.

## Output

| 镜号 | 工具 | 视频提示词 | 首帧要求 | 运动重点 | 禁止项 | 时长/比例 |
| --- | --- | --- | --- | --- | --- | --- |

## Tool guidance

- 即梦: specify first frame, camera movement, subject action, light change, and ending frame.
- 可灵: keep motion simple, continuous, and cinematic; avoid multiple competing transformations.

## Avoid

- Too many subjects moving in different directions.
- Fast chaotic camera movement unless explicitly needed.
- Complex text generation inside video.
- Brand logo generation unless a provided asset workflow exists.
