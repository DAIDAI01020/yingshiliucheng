---
name: script-writer
description: 撰写影视化文稿。用于广告片、品牌片、电视节目宣传片、栏目/综艺预告、发布会/盛典开场片、大屏视觉片和社媒短片，按片长输出画面段落、旁白、字幕、音乐音效和节奏备注。
---

# Script Writer

## Process

1. Confirm format: TVC, brand film, program promo, event opener, LED visual, or social cutdown.
2. Match length and platform rhythm.
3. Write in time-coded sections whose durations sum to the requested runtime. Leave room for pauses, actions, transitions, and the end card; assess read-aloud pacing rather than filling every second with narration.
4. Keep narration speakable and subtitle copy screen-friendly.

## P1 No Lazy Handoff

For formal projects, `$script-writer` develops timed drafts from the approved brief and marks their approval status honestly. It does not choose visual references, create style locks, or send prompts to generation.

Before downstream storyboard or prompt work, preserve:

```text
upstream_source
approved_concept_or_brief
timecoded_sections
voiceover_or_subtitle_intent
music_sound_intent
visual_requirements
missing_fields
route_back_to
```

Resolve creative gaps within the script task and ask only for blocking facts or choices. A generation platform is not required to write a film script. Keep unverified product/brand claims as clearly marked placeholders; do not send them into approved production as facts.

## Output

| 时间段 | 画面段落 | 旁白 | 字幕 | 音乐/音效 | 节奏备注 |
| --- | --- | --- | --- | --- | --- |

Add `版本说明` after the table:

- 核心表达
- 情绪曲线
- 可删减段落
- 待客户确认信息

## Timing defaults

These are drafting examples, not mandatory shot counts; preserve the intended dramatic rhythm and total runtime.

- 15s: 4-6 sections.
- 30s: 6-10 sections.
- 60s: 10-16 sections.
- Event opener and LED visuals may use larger chapters instead of shot-level sections.
