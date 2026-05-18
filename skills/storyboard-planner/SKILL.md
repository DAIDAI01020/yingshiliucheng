---
name: storyboard-planner
description: Proposal-level cinematic storyboard planner for TVC ads, brand films, program promos, event openers, LED visuals, and AI generation. Use to create storyboards with shot number, duration, image description, client-facing proposal language, camera movement, subtitles or voiceover, music, AI generation notes, and image generation priority.
---

# Storyboard Planner

## Process

1. Use the approved concept, script, and visual style as source.
2. Split into proposal-level shots or chapters.
3. Keep every shot useful: information, emotion, reveal, transition, or rhythm.
4. Write both production language and client proposal language.
5. Add AI generation notes only where the shot benefits from image or video generation.
6. Classify image generation priority before prompting.

## Output

| 镜号 | 时长 | 画面描述 | 客户语言 | 镜头运动 | 字幕/旁白 | 音乐音效 | AI生成备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |

Then output:

| 镜号 | 优先级 | 是否出图 | 原因 | 推荐生成方式 | 风险 |
| --- | --- | --- | --- | --- | --- |

## Priority rules

- S: 核心视觉，必须出图，给3套风格方案。
- A: 关键产品、人物、空间、节目看点，建议出图。
- B: 辅助镜头，可按需要出图。
- C: 过场、信息、字幕、简单转场，通常文字描述即可。

## Defaults

- 15s: 4-6 shots.
- 30s: 6-10 shots.
- 60s: 10-16 shots.
- Program promos can use high-energy beats and reveal moments.
- LED visuals can use chapters and key frames instead of dense cuts.

## Quality bar

- Include enough detail for AI image prompt generation on S/A shots.
- Keep text overlays readable and not overloaded.
- Mention aspect ratio when it affects composition.
- Flag AI risks such as faces, hands, dense crowds, readable text, exact logos, and complicated multi-subject action.
