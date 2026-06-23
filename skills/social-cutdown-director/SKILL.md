---
name: social-cutdown-director
description: 社媒切条专项导演。用于把TVC、品牌片、节目宣传片、活动开场片或大屏视觉创意，改编为短视频、预热视频、倒计时片、竖版物料、金句卡点和平台传播版本。
---

# Social Cutdown Director

## Priorities

- Hook within 3 seconds.
- Reframe composition for vertical, square, or feed formats.
- Use subtitles and on-screen text as primary comprehension support.
- Keep each cutdown to one message or emotional beat.

## Output

## P1 No Lazy Handoff

For formal cutdown work, `$social-cutdown-director` must preserve the source film and platform target before prompt or generation handoff:

```text
upstream_handoff_packet
upstream_source: master film / approved script / approved frames / platform brief
platform_target:
duration:
hook_frame_or_line:
safe_text_area:
source_style_lock:
handoff_to: storyboard-planner / frame-vision-director / ai-video-prompt-director / prompt-platform-auditor
missing_fields:
route_back_to:
```

If source film, platform target, duration, or hook is missing, output `missing_fields` instead of inventing a new cutdown concept.

| 物料 | 比例 | 时长 | 钩子 | 内容结构 | 字幕/包装 | AI生成建议 |
| --- | --- | --- | --- | --- | --- | --- |

## Common adaptations

- 9:16 teaser.
- 15s product highlight.
- 6s bumper.
- Countdown short.
- Program high-energy moment.
- Quote or slogan card motion.
