---
name: program-promo-director
description: 电视节目宣传片专项导演。用于电视节目、综艺、栏目包装、节目预告、人物宣传和赛制看点包装，处理节目钩子、人物关系、冲突悬念、高能片段、播出信息和包装节奏。
---

# Program Promo Director

## Priorities

- Start from watchability: why should viewers watch now?
- Surface host, guests, contestants, stakes, format, conflict, emotion, or novelty.
- Use fast information rhythm while keeping播出信息 clear.

## Promo structure

1. 一句话节目钩子。
2. 人物/赛制/任务/关系快速建立。
3. 高能瞬间或悬念升级。
4. 情绪/笑点/冲突集中释放。
5. 节目名、播出平台、播出时间落版。

## Output addition

## P1 No Lazy Handoff

For formal program-promo work, `$program-promo-director` must hand off watchability and package logic before prompt writing:

```text
upstream_handoff_packet
upstream_source: program brief / episode material / guest or contestant info / broadcast info
viewer_hook:
key_people_or_stakes:
conflict_or_suspense:
package_rhythm:
broadcast_info:
required_reference_route:
recommended_board_type: ad_sequence_board / design_reference_board / spatial_continuity_board
board_type_reason:
jimeng_direct_reference_board: true / false
handoff_to: style-reference-director / storyboard-planner / frame-vision-director
missing_fields:
route_back_to:
```

If hook, key people/stakes, broadcast info, or reference route is missing, output `missing_fields` instead of final prompts.

| 节目宣传判断 | 建议 |
| --- | --- |
| 节目钩子 |  |
| 关键人物/看点 |  |
| 冲突或悬念 |  |
| 包装节奏 |  |
| 播出信息 |  |

## Image Storyboard Board Decision

When a program promo, variety package, or episodic promo needs an image故事板 for video-model reference, recommend the board type:

| Board type | Choose when |
| --- | --- |
| `ad_sequence_board` | the promo needs to show a clear sequence of hooks, high-energy moments, reveals, and ending broadcast landing |
| `design_reference_board` | the promo must lock host/guest/contestant appearance, package props, stage/set, graphic mood, or recurring visual identity |
| `spatial_continuity_board` | the promo involves multi-person blocking, table/stage positions, eyelines, competition geography, or the model may lose people |

Set `jimeng_direct_reference_board: true` when the image board will be uploaded directly to Jimeng/Seedance.
