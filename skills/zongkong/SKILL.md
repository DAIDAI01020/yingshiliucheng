---
name: zongkong
description: Top-level production orchestrator for all local AI creative workflows. Use at the start of a new conversation, new project, or ambiguous request to decide project setup, project tier, workflow mode, skill routing, image/video generation route, and next action across film, image, video, asset, and workflow tasks.
---

# Zongkong

## Core Role

`$zongkong` is the highest-level entry skill. It sits above `$yingshisheji`.

It decides:

- Whether the task is a formal project, quick project, or misc test.
- Which project folder should be used or created.
- Which workflow mode is active.
- Whether the request needs director/prompt work before execution.
- Which generation route should be used.
- Whether generated outputs need QC, review board, or asset indexing.

It should keep the user's work fast, organized, and low-friction. It should not become a long planning ceremony.

## Project Tiers

Use three project tiers:

| 层级 | 使用场景 | 默认处理 |
| --- | --- | --- |
| 正式项目 | 有客户、片名、长期制作目标、成组镜头或交付需求 | 建独立项目文件夹，建立风格圣经，记录资产和版本 |
| 快速项目 | 有明确主题但只做少量图/视频或快速提案 | 可建轻量项目文件夹，保留关键 prompt 和输出路径 |
| 杂项目/_misc | 测试模型、单张图、临时视频、随手试 prompt | 放入 `H:\yingshi\projects\_misc\`，只做轻量 QC |

Formal and quick projects use:

```text
H:\yingshi\projects\{projectSlug}\
```

Misc tests use:

```text
H:\yingshi\projects\_misc\
```

Route to `_misc` when the user says `先测一下`、`随便试试`、`临时跑一个`、`看个效果`, or when the task has no client/title/long-term asset value.

If unclear, ask one short question:

```text
这是正式项目，还是先放到杂项目测试池？
```

## Workflow Modes

Classify the current request into one mode:

| 模式 | 触发 | 主路由 |
| --- | --- | --- |
| 方案模式 | 方案、创意、PPT、客户提案 | `$yingshisheji` → proposal/type skills |
| 短剧模式 | 短剧、微短剧、竖屏剧情、分集、角色剧本 | `$short-drama-director` |
| 分镜模式 | 分镜、镜头表、执行表 | `$yingshisheji` → `$storyboard-planner` |
| 出图模式 | 静帧、关键帧、出图、重出 | director/prompt check → image route |
| 视频模式 | 出视频、让图动起来、一镜到底 | video feasibility check → `$ai-video-prompt-director` → Seedance |
| 审片修订模式 | 质检、能不能用、客户反馈、重出建议 | `$image-qc-director` / `$revision-director` |
| 归档模式 | 整理素材、找版本、交付 | `$asset-librarian` / `$project-state-manager` |

## Default Startup

At the start of a new formal project, ask only the minimum needed:

1. 项目名称是什么？
2. 项目类型是什么？例如 TVC、品牌片、节目包装、活动开场、LED 大屏、角色短片、单张出图、视频测试。
3. 本轮目标是什么？例如写方案、写分镜、出静帧、出视频、审片、整理资产、测试模型。

If the user already provides enough information, do not ask again. Create or use the project folder directly.

Create projects with:

```powershell
node H:\yingshi\skills\project-state-manager\scripts\manage-project-state.mjs init --project-name "项目名称"
```

## Tool Routing

Use this routing order:

| User Intent | Route |
| --- | --- |
| 影视方案、分镜、影视提示词、品牌片、TVC、活动片、LED 大屏 | `$yingshisheji` |
| 短剧、微短剧、竖屏剧情、连续剧情、角色对白 | `$short-drama-director` |
| 短剧题材/钩子/卖点 | `$short-drama-concept-writer` |
| 短剧人物小传/角色一致性 | `$short-drama-character-bible` |
| 短剧分集/单集结构 | `$short-drama-episode-writer` |
| 短剧对白优化 | `$short-drama-dialogue-doctor` |
| 短剧分镜拆解/参考图绑定/AI镜头执行 | `$short-drama-scene-director` |
| 顶级电影/TVC/纪录片/舞台视觉参考、审美基准 | `$reference-aesthetic-director` |
| 正式项目统一风格、风格延续、风格不漂 | `$style-bible-director` |
| 静帧提示词、关键帧提示词、出图前补提示词 | `$frame-vision-director` |
| 只想快速内置出图、image、image-2、ChatGPT Image、先看效果 | `$builtin-imagegen-director` + built-in imagegen |
| Banana 出图、省 token、重出、继续出 | `$banana-image-generator` or `$image-generation-controller` |
| Midjourney、MJ、Legnext | `$midjourney` |
| 出视频、让图动起来、Seedance、即梦、Ark | `$ai-video-prompt-director` → `$video-generation-controller` / `$seedance-2-video` |
| 审片、判断图能不能用、是否重出 | `$image-qc-director` |
| 对比图、图和提示词放一起看 | `$image-review-board` |
| 客户反馈转修改 | `$client-feedback-interpreter` + `$revision-director` |
| 整理素材、命名、归档 | `$asset-librarian` |
| 项目文件夹、资产索引、版本记录 | `$project-state-manager` |
| 同步 workflow、提交更新 | `$workflow-sync-manager` |

## Image Execution Rule

Image tools are execution tools. They do not decide the aesthetic.

Before real image generation, check whether there is a complete prompt:

| 检查项 | 要求 |
| --- | --- |
| 主体 | 人物/产品/场景/道具明确 |
| 场景 | 时间、空间、环境明确 |
| 动作 | 静态姿态或关键动作明确 |
| 构图 | 景别、机位、前中后景明确 |
| 摄影 | 摄影系统、镜头/焦段明确 |
| 光线 | 主光、逆光、环境光或光线逻辑明确 |
| 色彩 | 调色方向明确 |
| 材质 | 关键材质和质感明确 |
| 比例 | 默认 16:9，除非用户另说 |
| 负面词 | 文字/logo/手脸/变形/AI感等风险明确 |
| 参考图角色 | 每张参考图只控制指定特征 |

If the prompt is incomplete:

- Formal project: route through `$yingshisheji` / `$reference-aesthetic-director` / `$style-bible-director` / `$frame-vision-director` first.
- Quick project: route through `$frame-vision-director` first; use `$reference-aesthetic-director` only when the user asks for premium/reference-driven style.
- Misc test: quickly补齐一个可执行提示词，再生成。

User preferences:

- `image`, `image-2`, `ChatGPT Image`, `内置最新模型`, `直接生成一张图`, `先看个效果` means built-in imagegen.
- Built-in imagegen does not require `OPENAI_API_KEY`.
- Do not use or suggest the removed OpenAI API image generator route.
- Banana is used only when the user explicitly says Banana or the current task context is already Banana.
- Midjourney is used only when the user explicitly says MJ, Midjourney, or Legnext.
- For Banana, default to `2K` and compact prompts.

## Video Execution Rule

Before writing or executing a video prompt, run a feasibility check:

| 检查项 | 风险 |
| --- | --- |
| 是否跨空间 | 容易变成跳切或换场 |
| 是否跨时间 | 容易出现逻辑断裂 |
| 是否跨主体 | 容易主体漂移 |
| 景别变化是否过大 | 容易从全景硬切特写 |
| 动作是否过多 | 容易运动混乱 |
| 是否需要遮挡/形态匹配 | 用于伪一镜到底或自然衔接 |

For one-take requests, require:

- 严格连续镜头。
- 明确空间路径。
- 明确目标物锁定。
- 用遮挡、光线、运动方向或形态匹配做自然衔接。
- 明确禁止剪切、跳切、突然换景、镜头瞬移。

If the requested one-take is too complex, recommend pseudo one-take split segments.

Video defaults:

- Use Seedance/Ark for direct video generation.
- Prefer public image URLs.
- Use local relay only when needed or requested.
- Save video outputs and manifests when running through a project workflow.

## Post-Generation Rule

After generation:

- Formal project: build or update review board, run QC, update asset records when available.
- Quick project: return preview/path plus short QC.
- Misc test: return preview/path plus one-line judgment.

QC decisions:

```text
可用 / 可小修 / 建议重出 / 提示词需重写
```

Asset states:

```text
候选 / 入选 / 待重出 / 待修图 / 待修片 / 废稿
```

## Output Style

During execution, keep responses short:

- Route used.
- Project folder or output path.
- Image/video preview when available.
- One short QC note.

For workflow design, use:

```text
总控 -> 项目 -> 具体 skill -> 输出
```

## Guardrails

- Do not print API keys or tokens.
- Do not commit, push, or sync workflow changes unless the user explicitly asks.
- Do not delete generated outputs unless the user explicitly asks.
- Do not route built-in image requests to OpenAI API scripts.
- Do not route MJ requests through Banana or built-in imagegen.
- Do not route Banana tasks through MJ.
- Prefer executing when the user asks for action; ask only when missing information blocks the task.
