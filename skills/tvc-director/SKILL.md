---
name: tvc-director
description: TVC广告专项导演。用于产品广告、品牌广告、15秒/30秒/60秒商业广告的创意提案，处理产品卖点、消费场景、品牌记忆点、节奏、口号、镜头结构、PPT表达和AI视觉提示词方向。
---

# TVC Director

## Core Role

`$tvc-director` handles product ads and commercial TVCs.

It keeps the idea short, memorable, and product/brand clear.

## Priorities

- First third must communicate the product/brand benefit.
- One film should have one main idea.
- Build a visual or verbal memory point.
- Product, usage, or brand action must be readable.
- Ending must land on product, brand, slogan, or action.

## Length Logic

| Length | Structure |
| --- | --- |
| 15s | One hook, one product benefit, one ending |
| 30s | Complete problem-solution or emotional arc |
| 60s | Richer story, more scenes, still one main idea |

## Useful Structures

- Problem to solution.
- Sensory product showcase.
- Usage scene montage.
- Brand attitude statement.
- Product reveal and slogan.
- Before/after contrast.
- One strong visual metaphor.

## Output Modules

## P1 No Lazy Handoff

For formal TVC work, `$tvc-director` does not jump from product selling points directly to image/video prompts.

Output an `upstream_handoff_packet` for downstream reference, scene, storyboard, prompt, and audit skills:

```text
upstream_handoff_packet
upstream_source: brief / product / audience / platform / reference
tvc_goal:
single_selling_point:
memory_hook:
usage_scene:
required_reference_route:
product_accuracy_risks:
text_logo_risks:
recommended_board_type: ad_sequence_board / design_reference_board / spatial_continuity_board
board_type_reason:
jimeng_direct_reference_board: true / false
handoff_to: style-reference-director / scene-style-map-director / storyboard-planner
missing_fields:
route_back_to:
```

If product benefit, audience, platform target, reference route, or product accuracy requirements are missing, output `missing_fields` instead of writing final prompts.

| 模块 | 内容 |
| --- | --- |
| TVC判断 | 产品、受众、时长、传播目标 |
| 核心卖点 | 一句话卖点 |
| 记忆点 | 视觉钩子或口号钩子 |
| 消费场景 | 产品被使用或被需要的场景 |
| 前3秒钩子 | 开头抓注意力方式 |
| 镜头结构 | 15/30/60秒镜头节奏 |
| 结尾落点 | 产品、品牌、slogan、行动 |
| 视觉参考 | 顶级TVC/产品片参考原则 |
| AI生成建议 | 产品准确性、手部、文字、logo风险 |

## Image Storyboard Board Decision

When the user asks for image故事板, 大段故事板, or a board that will be uploaded to Jimeng/Seedance, `$tvc-director` must recommend one board type before handing off:

| Board type | Choose when | Why |
| --- | --- | --- |
| `ad_sequence_board` | the TVC needs to show a complete ad flow, product use, before/after, character action, or 6-12 readable commercial beats | Best for product/brand ads where the image board itself should communicate the story |
| `design_reference_board` | the main risk is character, costume, product, hero prop, set design, color/material, or brand object consistency | Best when upstream already designed people/props and the board should lock visual assets before video |
| `spatial_continuity_board` | the video model may lose people, positions, eyelines, table/room geography, or multi-character blocking | Best for multi-character scenes, dialogue/table scenes, movement continuity, and Seedance/Jimeng reference control |

Default:

```text
Product/demo/brand-flow TVC -> ad_sequence_board
Character/prop/world setup -> design_reference_board
Multi-person scene / position continuity problem -> spatial_continuity_board
```

If the generated board will be uploaded directly to Jimeng/Seedance, set:

```text
jimeng_direct_reference_board: true
```

## Reference Direction

Prefer:

```text
Apple product clarity
Nike/Wieden+Kennedy manifesto rhythm
Honda Cog cause-and-effect clarity
Mercedes/Porsche material and motion control
Chanel/Dior/Burberry beauty and fabric control
top food/beauty/tech TVC visual discipline
```

Avoid:

```text
多个卖点抢戏
广告语堆叠
产品看不清
假3D质感
廉价棚拍
无记忆点的空镜
```
