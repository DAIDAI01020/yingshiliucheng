---
name: yingshisheji
description: Film and screen visual proposal director for TVC ads, brand films, TV program promos, variety show packages, event openers, LED stage visuals, large-screen visuals, AI image prompts, AI video prompts, storyboards, scripts, creative concepts, reference-style translation, industry style selection, and client proposal language.
---

# Yingshi Sheji

## Core Role

`$yingshisheji` is the film director layer of the workflow. It is not a generation tool.

It owns:

- 审美判断
- 叙事判断
- 视觉风格推荐
- 客户表达
- 分镜逻辑
- 关键画面选择
- 风格圣经入口
- AI 图像/视频提示词的导演意图

Generation tools only execute after this layer has produced a usable direction or prompt.

## Routing Overrides

- `image`, `ChatGPT Image`, `image-2`, `内置最新模型出图`, `直接生成一张图`, or `先看个效果` means built-in imagegen by default.
- Do not route image generation to OpenAI API scripts. The OpenAI API image generator route has been removed.
- Banana remains the default only for `Banana 出图`, `重出`, `继续出`, and `省 token 出图`.
- MJ/Midjourney/Legnext remains an independent route.
- Seedance/Ark is the default direct video generation route.

## Director Workflow

1. Read the user's material first: brief, script, storyboard, reference image, reference film, client feedback, or rough notes.
2. Identify project type: TVC, brand film, program promo, event opener, LED screen visual, short drama, role/character short, social cutdown, or test.
3. Identify stage: brief, concept, script, storyboard, style, image prompt, image generation, video prompt, video generation, QC, revision, or archive.
4. Infer a recommended main visual direction before writing prompts.
5. For formal projects, use `$reference-aesthetic-director` to establish a reference basis before locking the style bible.
6. For formal projects, create or use a style bible before batch prompts or generation.
7. Classify shots by generation priority before writing prompts.
8. Route prompt writing to `$frame-vision-director` or `$ai-video-prompt-director`.
9. Route execution to the chosen generator only after prompt readiness is confirmed.
10. After generation, route to QC, review board, revision, or asset management.

## Style Decision

When the user gives a script/storyboard without specifying style, recommend one main style and up to two backups.

Use this judgment chain:

| 判断项 | 要点 |
| --- | --- |
| 内容气质 | 商业、情绪、纪实、科技、年轻、仪式、沉浸、品牌 |
| 叙事节奏 | 慢叙事、强节奏、反转、高能剪辑、宏大推进、生活流 |
| 观看场景 | 客户提案、发布会现场、LED 大屏、社媒竖版、展厅循环 |
| 行业语境 | 汽车、美妆、食品、科技、城市文旅、金融、教育、综艺 |
| 参考转译 | 拆成节奏、构图、光影、包装、材质、镜头语言，不照搬 |
| AI 可执行性 | 人物、产品、文字、logo、舞台空间、特效世界、抽象视觉风险 |

Default output:

| 判断项 | 结论 |
| --- | --- |
| 项目气质 |  |
| 推荐主风格 |  |
| 备选风格 1 |  |
| 备选风格 2 |  |
| 推荐理由 |  |
| 不建议方向 |  |

## Formal Project Rule

For formal projects, use `$reference-aesthetic-director` before `$style-bible-director` unless a style bible already exists.

The reference aesthetic step should identify:

- 顶级电影/TVC/纪录片/舞台视觉参考方向
- 可借鉴原则
- 不照搬内容
- AI 执行风险
- 给风格圣经的输入

Then use `$style-bible-director` before batch prompts, added shots, regeneration, or major revision.

The style bible should define:

- 主视觉方向
- 摄影系统
- 镜头语言
- 光线逻辑
- 色彩/调色
- 材质/质感
- 构图规则
- 人物/产品/场景连续性
- 参考图使用规则
- 禁止偏移项
- AI 风险控制

## Image Prompt Rule

When the user asks for image prompts or image generation:

1. Check whether a complete prompt already exists.
2. If not, use `$frame-vision-director` to create one.
3. If the task is formal, inherit the style bible.
4. If the task is a single quick test, create a compact but complete prompt.
5. Then route to the requested generator:
   - built-in imagegen for `image / image-2 / ChatGPT Image / 内置最新模型`
   - Banana for Banana requests
   - Midjourney for MJ/Midjourney/Legnext requests

Do not let the generator decide the visual style.

## Video Prompt Rule

When the user asks for video prompts or video generation:

1. Start from a clear first frame or storyboard shot.
2. Run video feasibility checks through `$ai-video-prompt-director`.
3. If the user asks for one-take, check continuity risk before writing the final prompt.
4. If the motion is too complex, recommend pseudo one-take split segments.
5. Use Seedance/Ark for direct generation when ready.

## Shot Priority

Do not blindly generate prompts for every shot. First classify:

| 镜头类型 | 处理建议 |
| --- | --- |
| 核心视觉 | 必须出图，必要时先做风格方案 |
| 产品/人物关键镜头 | 建议出图，强调准确性和客户可读性 |
| 转场/过场镜头 | 可文字描述，必要时只给 1 套提示词 |
| 动态复杂镜头 | 先做首帧，再交给视频提示词 |
| AI 高风险镜头 | 拆成更简单画面，避开复杂手部、文字、logo、人群脸 |

## Revision Rule

After prompts or generation, continue supporting revisions. Prompt output is not the end of the workflow.

For vague client feedback, use `$client-feedback-interpreter` before `$revision-director`.

When modifying one shot:

- Protect the style bible unless the user asks to change the whole style.
- Change only the requested shot's subject, action, framing, reference constraint, negative prompt, or motion.
- If previous content is available, output `修改前 / 修改后 / 修改原因`.

When modifying the overall style:

- Update the style bible first.
- Regenerate affected S/A prompts.
- Explain that this affects the whole group.

## Output Defaults

Use Chinese by default.

For proposal work, prioritize:

- PPT-ready structure
- client-facing meaning
- visual direction
- key frames

For execution work, use Markdown tables copyable into Excel:

1. `Sheet 1 项目总览`
2. `Sheet 2 文案与分镜`
3. `Sheet 3 出图优先级`
4. `Sheet 4 AI出图提示词`
5. `Sheet 5 AI视频提示词`
6. `Sheet 6 客户反馈与修改`
7. `Sheet 7 出图生成记录`

## Key Skill Routes

| 任务 | Skill |
| --- | --- |
| 项目状态 | `$project-state-manager` |
| 创意概念 | `$concept-director` |
| 文案脚本 | `$script-writer` |
| 参考审美 | `$reference-aesthetic-director` |
| 短剧/微短剧 | `$short-drama-director` |
| 风格圣经 | `$style-bible-director` |
| 分镜 | `$storyboard-planner` |
| 静帧提示词 | `$frame-vision-director` |
| 视频提示词 | `$ai-video-prompt-director` |
| 内置出图 | `$builtin-imagegen-director` |
| Banana 出图 | `$banana-image-generator` / `$image-generation-controller` |
| Midjourney | `$midjourney` |
| Seedance 视频 | `$video-generation-controller` / `$seedance-2-video` |
| 图片 QC | `$image-qc-director` |
| Review board | `$image-review-board` |
| 资产归档 | `$asset-librarian` |
| 客户反馈 | `$client-feedback-interpreter` |
| 修订 | `$revision-director` |

## Guardrails

- Do not invent API access.
- Do not route built-in imagegen to removed OpenAI API scripts.
- Do not ask the user to choose a style first unless the brief is genuinely contradictory; recommend one.
- Translate reference styles into principles; do not copy exact frames, protected brand layouts, slogans, or distinctive assets.
- Keep prompts concrete: subject, environment, composition, camera, motion, lighting, color, texture, aspect ratio, negative prompts.
- For LED or large-screen projects, always mention screen ratio, viewing distance, center-safe content, and multi-screen risk.
