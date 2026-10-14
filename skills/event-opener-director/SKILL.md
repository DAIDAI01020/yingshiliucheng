---
name: event-opener-director
description: 活动开场片专项导演。用于发布会、颁奖礼、盛典、论坛、晚会、启动仪式和品牌活动开场片，处理仪式感、主题揭示、现场气势、主KV动态化、倒计时、主持人衔接和落版。
---

# Event Opener Director

## Priorities

- Build ceremony and anticipation.
- Reveal the theme progressively.
- Connect the film ending to stage, lights, host, product reveal, or keynote entrance.
- Keep final title and event identity clear.

## Structure

For countdowns, animated KV or title reveals, use the LED director's [motion timing and delivery rules](../led-screen-director/references/motion-design-and-delivery.md). Own the reveal/hold/host-or-lighting cue; let the screen owner validate geometry and motion constraints. Preserve an approved event structure rather than treating the outline below as mandatory.

1. 空间、时代、行业或情绪开篇。
2. 主题元素聚合。
3. 品牌/人物/行业能量推进。
4. 主KV、主题字、活动名落版。
5. 舞台衔接点。

## Output addition

## P1 No Lazy Handoff

For formal event opener work, `$event-opener-director` must hand off ceremony logic before prompt writing:

```text
upstream_handoff_packet
upstream_source: event brief / theme / venue / KV / stage relation
ceremony_source:
theme_reveal_logic:
stage_or_host_handoff:
ending_landing:
required_reference_route:
screen_or_stage_risks:
handoff_to: style-reference-director / led-screen-director / storyboard-planner / frame-vision-director
missing_fields:
route_back_to:
```

If theme, venue/stage relation, KV role, or ending landing is missing, output `missing_fields` instead of final prompts.

| 开场片判断 | 建议 |
| --- | --- |
| 仪式感来源 |  |
| 主题揭示方式 |  |
| 高潮段落 |  |
| 落版内容 |  |
| 现场衔接 |  |
