---
name: revision-director
description: Revision director for film visual proposals after client feedback or AI prompt output. Use for TVC, brand film, program promo, event opener, LED visual, storyboard, keyframe prompt, and AI video prompt revisions, including changing a shot prompt, adding shots, deleting shots, reordering shots, replacing reference-image constraints, updating the unified style package, and revising video motion, duration, ratio, or negative constraints.
---

# Revision Director

## Process

1. Classify feedback: strategy, information, tone, script, visual, storyboard, frame prompt, video prompt, reference image, unified style, or revision tracking.
2. Identify the affected scope: whole proposal, PPT page, Sheet 2 storyboard, Sheet 3 image priority, Sheet 4 image prompts, Sheet 5 video prompts, Sheet 6 feedback log, Sheet 7 image generation record.
3. Preserve approved parts and only change affected sections.
4. If the user adds a shot, inherit the current unified visual style package unless they explicitly change the overall style.
5. If the user modifies one prompt, change only that shot's subject, action, framing, reference constraint, negative prompt, or video motion unless they explicitly request a style change.
6. If the user changes the whole style, update the unified style package first, then regenerate all affected S/A image prompts and relevant video prompts.
7. Produce a revision summary before revised content.
8. Mark unresolved conflicts as `待确认`.

If feedback is vague client language such as `不够高级`, `太AI`, `不够大气`, `不像品牌`, or `画面太乱`, use the interpretation from `$client-feedback-interpreter` before editing sheets.

## Revision types

| 修改类型 | 处理方式 |
| --- | --- |
| 改某个镜头提示词 | 保留全片统一风格包，只改指定镜头的局部内容 |
| 加新镜头 | 判断插入位置，分配镜号，继承统一风格包，补 Sheet 2-5 |
| 删除镜头 | 标记删除镜号，说明影响，更新分镜、优先级和提示词 |
| 调整镜头顺序 | 更新镜号或使用 S03A 过渡编号，说明是否影响节奏 |
| 替换参考图约束 | 只影响绑定镜头，不改变整组风格 |
| 修改统一风格包 | 影响所有 S/A 镜头，需批量更新提示词 |
| 修改视频运动/时长/比例/禁止项 | 更新 Sheet 5，保持首帧和全片风格一致 |
| 出图后质检修改 | 判断是提示词、参考图、模型生成、还是整体风格问题，再决定单镜头重出或批量更新 |
| 重出某个镜头 | 保留可用内容，更新 Sheet 7 的新版本记录 |

## Adding shots

When the user asks to add a shot:

1. Determine insertion position from the user's instruction. If unclear, place it after the most related shot and mark `待确认`.
2. Assign a shot number:
   - Use `S03A` if inserting between existing shots without renumbering.
   - Use full renumbering only if the user requests a clean final table.
3. Update:
   - `Sheet 2 文稿与分镜`
   - `Sheet 3 出图优先级`
   - `Sheet 4 AI出图提示词` if it needs a keyframe
   - `Sheet 5 AI视频提示词` if it needs motion generation
   - `Sheet 6 客户反馈与修改`
4. Inherit the current `全片统一风格包`.
5. Do not let the new shot break visual consistency.

## Modifying prompts

When the user asks to modify an existing image or video prompt:

1. Output `修改前 / 修改后 / 修改原因` when previous content is available.
2. Keep the unified style package unless the user says the overall style should change.
3. For image prompts, preserve detailed style expansion and update only the requested shot detail.
4. For video prompts, preserve first-frame logic and update only motion, action, duration, ratio, or forbidden items.
5. Record the change in `Sheet 6 客户反馈与修改`.

When modifying a generated image, first look for the matching record in `asset-index.json` if the project is managed by `$project-state-manager`. If no asset index exists, use `Sheet 7 出图生成记录` or `generation-log.json`, then find the matching `prompts/*_prompt.txt` or `prompts/*_prompt.json`. Use that full prompt as the `修改前` source instead of guessing from the image only.

If the user references an image from a review board, such as `改 S01_banana_v01`, locate the original prompt by shot + tool + version. Output `原提示词 / 修改后提示词 / 修改原因 / 新版本建议 / 是否需要重出`.

## After generated images

When feedback is about generated images, such as `这张不行`, `S03换构图`, `人物太假`, `产品不准`, or `背景可以人物不行`:

1. Classify the issue as prompt issue, reference-image issue, model generation issue, post-production issue, or unified-style issue.
2. If only one shot is affected, change only that shot and recommend regenerating that shot.
3. If multiple S/A shots share the same style drift, update the unified style package before regeneration.
4. Record the affected image version and the new target version.
5. Update `Sheet 6 客户反馈与修改` and `Sheet 7 出图生成记录`.

## Output

### 修改判断

| 修改类型 | 影响范围 | 涉及镜号 | 保留内容 | 修改后内容 | 需要同步更新的Sheet |
| --- | --- | --- | --- | --- | --- |

### 修改后表格

Only output the changed rows unless the user asks for a full replacement.

Use the relevant tables:

#### Sheet 2 文稿与分镜

| 镜号 | 时间段 | 时长 | 景别 | 画面段落/画面描述 | 旁白 | 字幕 | 客户提案话术 | 镜头运动 | 音乐音效 | AI生成备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

#### Sheet 3 出图优先级

| 镜号 | 优先级 | 是否出图 | 出图原因 | 推荐生成方式 | 风险点 |
| --- | --- | --- | --- | --- | --- |

#### Sheet 4 AI出图提示词

| 镜号 | 优先级 | 工具 | 参考图说明 | 完整可复制提示词 | 负面提示词 | 比例 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |

#### Sheet 5 AI视频提示词

| 镜号 | 工具 | 首帧要求 | 视频提示词 | 镜头运动 | 主体动作 | 环境/光影变化 | 禁止项 | 时长/比例 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

#### Sheet 6 客户反馈与修改

| 反馈来源 | 反馈内容 | 反馈翻译结果 | 影响范围 | 执行动作 | 修改方式 | 是否触发重出图 | 关联图片版本 | 当前状态 | 版本备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

#### Sheet 7 出图生成记录

| 镜号 | 版本 | 工具 | 模型 | 提示词摘要 | 图片路径 | 提示词TXT | 提示词JSON | 审片面板路径 | 资产状态 | 状态 | 失败原因 | 重出建议 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
