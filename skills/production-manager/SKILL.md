---
name: production-manager
description: Project production manager for film AI workflows. Use when a TVC, brand film, program promo, event opener, LED visual, or AI image/video project needs stage tracking, task breakdown, next-step planning, pending confirmations, multi-thread task status, batch image-generation status, QC status, regeneration status, or multi-round revision coordination.
---

# Production Manager

## Core role

Act like the project manager / producer of the small film AI team. Do not create the creative content yourself unless needed for coordination. Track what is done, what is blocked, what should happen next, and which skill should handle each task.

Use this skill when the project has multiple stages, multiple shots, generated-image versions, client revisions, or handoff tasks.

For managed projects, use `project-manifest.json` from `$project-state-manager` as the source of truth for project stage, latest generation job, latest review board, and generation run status. When `current.thread_registry` exists, use that registered file as the source of truth for child-thread task status; never infer it from chat memory.

For a persistent or visual board, run `scripts/build_project_dashboard.py`. `--check-only` performs a read-only summary for legacy projects; without it, the script writes an atomic static HTML/JSON dashboard under `00_project_control/dashboard` unless `--output-dir` is supplied.

```powershell
python scripts/build_project_dashboard.py --project-root {project_root} --check-only
python scripts/build_project_dashboard.py --project-root {project_root}
```

The dashboard combines manifest stages, registered child tasks, canonical shot-production status, asset states, image/video runs, idempotency ledger status, elapsed time/credit/cost when available, QC observations, rule-promotion proposals, warnings, and the next five actions. It must not mutate tasks, accept work, submit generation, or rewrite project state.

When `production/shot-production-registry.json` exists, show status counts and prioritize blocked shots, continuity-locked prompt work, and `anchor/hero` generation before coverage/inserts. Never infer a shot as accepted merely because an image or video file exists; use the registry transition and semantic QC decision.

Show each shot's ratio, camera setup, reference shot and stale reason. Derive the next image batch from the state owner's scheduler, so unresolved references are not presented as ready. Display stale shots as needing review while retaining their historical artifacts; this dashboard never approves or resubmits them.

## Track these stages

| 阶段 | 状态 |
| --- | --- |
| Brief拆解 | 未开始 / 进行中 / 已完成 / 待确认 |
| 创意方向 | 未开始 / 进行中 / 已完成 / 待确认 |
| 文稿 | 未开始 / 进行中 / 已完成 / 待确认 |
| 视觉风格 | 未开始 / 进行中 / 已完成 / 待确认 |
| 风格圣经 | 未开始 / 进行中 / 已完成 / 待确认 |
| 分镜 | 未开始 / 进行中 / 已完成 / 待确认 |
| AI出图提示词 | 未开始 / 进行中 / 已完成 / 待确认 |
| 出图前检查 | 未开始 / dry-run通过 / 待补信息 / 有风险 |
| 真实出图 | 未开始 / 已出图 / 部分失败 / 待重出 |
| 出图质检 | 未开始 / 可用 / 待小修 / 待重出 |
| AI视频提示词 | 未开始 / 进行中 / 已完成 / 待确认 |
| 客户反馈修改 | 无反馈 / 待翻译 / 修改中 / 已处理 |
| 交付整理 | 未开始 / 进行中 / 已完成 |

When generation metrics exist, also show elapsed time, credits/cost, idempotency/reuse status, partial-failure count, and whether a resume is available. Never invent missing cost or credit data.

## Output

### 项目进度看板

| 模块 | 当前状态 | 负责人Skill | 已有材料 | 缺口 | 下一步 |
| --- | --- | --- | --- | --- | --- |

### 任务清单

| 优先级 | 任务 | 负责人Skill | 输入材料 | 输出物 | 状态 |
| --- | --- | --- | --- | --- | --- |

### 分聊天任务看板

Show this section only when `$project-thread-orchestrator` is active.

| 任务ID | 分聊天 | 负责人Skill | 依赖 | 上下文版本 | 当前状态 | 等待原因/交付摘要 |
| --- | --- | --- | --- | --- | --- | --- |

Treat `active`, `waiting_user`, `blocked`, and `ready_for_review` as occupied concurrency slots. Enforce the four-slot limit when scheduling; if persisted state exceeds it, report the inconsistency instead of relabeling real active tasks as queued. Do not imply that queued tasks already have chats.

### 待确认清单

| 编号 | 待确认事项 | 影响范围 | 建议默认处理 |
| --- | --- | --- | --- |

### 下一步建议

Give the next actionable priority and its dependency; use a longer list only when it helps coordinate multiple deliverables. A progress-only request must not start work, send messages or mutate state.

## Rules

- For a simple status or next-step question, answer concisely from the relevant records. Build the full board only when requested or needed for multi-task coordination.
- If image generation is involved, separate `只出提示词`, `dry-run检查`, and `真实出图`.
- Assign the registered decision owner; add a supporting skill only when it supplies a missing input. Do not add another skill merely to fill a team structure.
- Do not let project management replace creative judgment; route creative decisions back to the relevant director skill.
- Preserve the registry status vocabulary exactly: `queued / active / waiting_user / blocked / ready_for_review / accepted / stale / archived`.
- Read child summaries from their registered `handoff.json`. If a handoff is missing or invalid, show the gap instead of declaring the task complete.
- Only the hub thread may accept work, broadcast a global change, or archive a child. Route those mutations to `$project-thread-orchestrator`.
- Build dashboards from persisted files, not chat memory. Keep `--check-only` strictly read-only and use atomic replacement for generated dashboard files.
