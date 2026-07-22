---
name: yingshisheji
description: Film and screen visual proposal director for commercial and promotional film workflows, including TVC ads, brand films, city films, program promos, variety show packages, event openers, LED stage visuals, large-screen visuals, AI image prompts, AI video prompts, storyboards, scripts, creative concepts, reference-style translation, industry style selection, and client proposal language. Use for宣传片、品牌片、TVC、活动开场、LED大屏、节目包装 and commercial visual proposals; route short drama to short-drama-director.
---

# Yingshi Sheji

## Core Role

`$yingshisheji` is the commercial film and screen proposal director layer.

It is not a generation tool and it should not swallow all specialist directors. Its job is to understand the commercial/promo project, choose the right specialist route, and keep the final output suitable for client presentation and AI execution.

Use it for:

```text
品牌片 / 企业宣传片 / 城市宣传片 / 招商片 / TVC /
产品广告 / 活动开场 / 发布会开场 / LED大屏 / 节目包装 / 社媒切条
```

Do not use it as the main director for short drama. Route short drama, micro-series, character-driven episodes, dialogue scenes, and scene-level drama breakdowns to `$short-drama-director`.

## Responsibilities

`$yingshisheji` owns:

- 商业目标判断
- 受众与传播目标判断
- 创意概念方向
- 客户可理解表达
- 专项导演路由
- 视觉参考方向
- 风格圣经入口
- 分镜和关键画面选择
- PPT提案结构
- AI出图/视频提示词的导演意图

Generation tools only execute after this layer and downstream prompt directors have produced platform-audited prompts.

## Commercial Workflow

Default route:

```text
brief-analyzer
-> concept-director
-> yingshisheji
-> specialist director
-> reference-aesthetic-director
-> style-bible-director
-> script-writer / storyboard-planner
-> pitch-deck-director
-> frame-vision-director / ai-video-prompt-director
-> prompt-platform-auditor
-> generation tool
-> QC / asset management
```

## Specialist Director Routing

| Project type | Route |
| --- | --- |
| 品牌片、企业宣传片、城市宣传片、招商片 | `$brand-film-director` |
| TVC、产品广告、品牌广告 | `$tvc-director` |
| 活动开场、发布会开场、颁奖礼、盛典 | `$event-opener-director` |
| LED大屏、舞美视觉、沉浸式宽屏 | `$led-screen-director` |
| 节目宣传、综艺包装、栏目包装 | `$program-promo-director` |
| 社媒预热视频、切条、竖版传播 | `$social-cutdown-director` |

## Commercial Reference Logic

For commercial/promo projects, reference selection should not use the short-drama crime/family/emotion logic by default.

Prioritize:

```text
Apple product/keynote films
Nike / Wieden+Kennedy manifesto
Mercedes / Porsche / BMW premium films
BBC / Netflix premium documentary
Guinness Surfer
Honda Cog
Moment Factory / Es Devlin / Olympic-scale stage visuals
top brand manifesto films
engineering documentaries
city image films
```

Translate references into:

```text
品牌气质
产品/工程/城市可信度
空间规模
节奏和视觉记忆点
材质和光线
客户可讲述逻辑
```

Do not copy exact ads, slogans, protected brand layouts, or distinctive assets.

## Default Commercial Output

For proposal work, output only what the current stage needs. Common modules:

1. `需求拆解`
2. `创意概念`
3. `推荐视觉方向`
4. `参考审美转译`
5. `风格圣经`
6. `脚本/旁白`
7. `分镜表`
8. `关键帧出图需求`
9. `AI图片提示词`
10. `AI视频提示词`

## Image Storyboard Board Routing

When the user asks for image故事板, 广告故事板, 大段故事板, 直接给 image 出故事板, or a board to feed Jimeng/Seedance, `$yingshisheji` must route through `$image-storyboard-workflow`. Specialist directors may recommend board type, but `$image-storyboard-workflow` owns the final source_type, board_type, direct-video-reference boundary, and handoff path.

Commercial board types:

```text
ad_sequence_board: sequential TVC/ad story frames; best for product use, brand flow, before/after, commercial rhythm.
design_reference_board: character/prop/product/set/costume/color-material reference board; best for locking visual assets.
spatial_continuity_board: scene geography, character positions, eyelines, camera path, shooting beats; best for multi-person or continuity-sensitive video.
```

Routing:

```text
TVC / product ad / brand ad -> tvc-director may recommend board type -> image-storyboard-workflow finalizes.
program promo / variety package / episode promo -> program-promo-director may recommend board type -> image-storyboard-workflow finalizes.
brand film / corporate / city film -> brand-film-director may provide story/scene function -> image-storyboard-workflow finalizes.
```

Handoff must include:

```text
recommended_board_type:
board_type_reason:
jimeng_direct_reference_board:
handoff_to: image-storyboard-workflow
```
11. `PPT页面结构`
12. `生成与QC计划`

## Image Prompt Rule

When the user asks for image prompts or image generation:

1. Check whether a complete prompt already exists.
2. If not, route to `$frame-vision-director`.
3. For formal projects, inherit the style bible.
4. Every copyable prompt must include full style language inside the prompt itself.
5. Send the prompt to `$prompt-platform-auditor` before generation.
6. Route to the requested tool: built-in imagegen, Banana/Banana Pro, or Midjourney.

## Video Prompt Rule

When the user asks for video prompts or video generation:

1. Start from a clear first frame or storyboard shot.
2. Use `$ai-video-prompt-director` for feasibility and motion design.
3. For one-take, check continuity risk before writing final prompt.
4. Send the prompt to `$prompt-platform-auditor` before final output or generation.
5. Use Seedance/Ark or the user-specified external platform.

## PPT Rule

Use `$pitch-deck-director` when the user asks for:

```text
整理PPT / 提案 / 客户方案 / 页面结构 / 讲稿 / 视觉方案排版
```

PPT is not the same as execution table:

```text
PPT = 说服客户
Excel/Markdown表 = 执行落地
```

## Guardrails

- Do not use low-quality domestic web-film or generic short-drama aesthetics as commercial reference standards.
- Do not route short-drama scene work through this skill; use `$short-drama-director`.
- Do not let image/video tools decide the visual style.
- Do not use `高级感`, `电影感`, or `大片感` as the only style description.
- Keep client language clear, but keep generation prompts concrete.
