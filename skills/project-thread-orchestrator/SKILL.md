---
name: project-thread-orchestrator
description: Orchestrate context-isolated Codex child threads inside one managed film/visual project. Use when a long manuscript, multi-part production, parallel deliverables, or explicit context-isolation request should be split into separately reviewable tasks while every chat stays in the same Codex project and every file stays under the same project root. Handles split proposals, one-time confirmation, project-scoped thread creation, a four-thread queue, task packets, handoffs, global-context broadcasts, stale results, adoption, and archival.
---

# Project Thread Orchestrator

## Core role

Keep one hub thread as project control and create clean child threads for bounded work. Preserve two containment rules:

```text
chat containment -> every child uses the same saved Codex projectId
file containment -> every child task workspace stays under the same project_root
container_mode -> shared_project_shared_root
```

Do not make specialist creative decisions. Let `$zongkong` choose the route and let the owning director decide the meaningful content boundaries. Use `$project-state-manager` for persisted project state and `$production-manager` for the user-facing board.

Read [references/thread-orchestration-contracts.md](references/thread-orchestration-contracts.md) before creating, adopting, broadcasting to, or archiving child threads.

## Activation boundary

Use this skill when any of these applies:

- a manuscript or production contains several independently revisable parts;
- different deliverables, platforms, references, approvals, or specialist skills should not share a chat context;
- the user explicitly asks for a master project with separate chats;
- a managed project needs up to four parallel child tasks with traceable handoffs.

Keep one short, coherent task in the current chat. Do not split merely because a document is long.

## Split workflow

1. Locate the managed `project_root` and its saved Codex project with the project-listing tool. Require an exact project-path match.
2. Ask the owning director to make `thread_split_plan`; do not replace its creative judgment with paragraph counts.
3. Hard-split when deliverable/platform, reference set, or approval dependency differs.
4. Suggest a split when at least two change: narrative function, time/location, character group, asset set, or independent revision need.
5. Merge adjacent short units that share characters, scene, style, references, and approval path.
6. Put global prerequisites such as brief, concept, style, character, or product locks before dependent tasks.
7. Show the split table to the user. Do not create a child thread or task folder until the user confirms the plan once.

After confirmation, initialize/register through:

```powershell
python C:\Users\admin\.codex\skills\project-thread-orchestrator\scripts\manage_thread_registry.py init --project-root {project_root} --project-id {project_id} --project-path {project_path} --project-name "{project_name}"
python C:\Users\admin\.codex\skills\project-thread-orchestrator\scripts\manage_thread_registry.py register-plan --project-root {project_root} --input {confirmed_plan_json}
```

The script owns deterministic files only. It never creates or claims to create a Codex thread.

If no hub is registered and the user has explicitly asked for the master-chat structure, create or reuse one clean thread in the exact saved project, title it `[项目简称][总控]`, pin it, then persist the real returned ID:

```powershell
python C:\Users\admin\.codex\skills\project-thread-orchestrator\scripts\manage_thread_registry.py bind-hub --project-root {project_root} --thread-id {thread_id} --thread-title "[项目简称][总控]" --pinned
```

Do not bind a workflow-maintenance or unrelated chat as the project hub.

## Thread creation and queue

Use `next-batch` to select eligible queued tasks. The default and hard maximum are four active child threads:

```powershell
python C:\Users\admin\.codex\skills\project-thread-orchestrator\scripts\manage_thread_registry.py next-batch --project-root {project_root}
```

For each returned task:

1. Read its `task-packet.json`.
2. Call the Codex thread-creation tool with exactly:

```text
target.type: project
target.projectId: registry.project_id
target.environment.type: local
prompt: compact child task packet and file paths only
```

3. Never use fork, projectless, a different project, or a worktree for these children.
4. Rename the new thread to `[项目简称][P01][任务名称]`.
5. Only after creation succeeds, bind the returned thread ID:

```powershell
python C:\Users\admin\.codex\skills\project-thread-orchestrator\scripts\manage_thread_registry.py bind-thread --project-root {project_root} --task-id P01 --thread-id {thread_id} --thread-title "{thread_title}"
```

If thread tools are unavailable, return copyable child task packets and say that no threads were created. Never write fake thread IDs.

## Child isolation contract

Send only the child packet, the current global-context path/version, approved locks, source paths, dependencies, allowed workspace, deliverables, and handoff path. Never copy the hub history into a child.

Require every child to:

- write working files only inside its unique `00_project_control/thread-tasks/{task_id}/working` directory;
- treat global project files and locks as read-only;
- propose global changes through `global_change_proposals` instead of editing global state;
- write `handoff.json` before declaring review readiness;
- return output paths for promotion into the project's existing delivery folders after acceptance.

Only the hub may modify `project-context.md`, `thread-registry.json`, or project-level manifest pointers.

## Sync, acceptance, and continuation

When the user says `汇总进度`, `继续项目`, or `同步分聊天`:

1. List/read only registered active child threads.
2. Ask each ready child to refresh its standard `handoff.json` if needed.
3. Import a handoff with `sync-handoff`; reject a missing, incomplete, mismatched, or out-of-root handoff.
4. Update the `$production-manager` thread board.
5. Start the next eligible batch only when slots and dependencies allow.

Use these state values exactly:

```text
queued / active / waiting_user / blocked / ready_for_review / accepted / stale / archived
```

The hub alone changes `ready_for_review` to `accepted`. Promote accepted deliverables to the existing project output structure, then archive the child with the Codex archive tool and mark the registry entry `archived`. Keep the registered hub thread unarchived and pinned.

## Global context changes

Version global changes instead of replaying the full project history:

1. Update `project-context.md` and increment `context_version`.
2. Calculate affected registered tasks from `inherited_locks`.
3. Show the affected child list and obtain one confirmation.
4. Send only the delta to those thread IDs.
5. Run `mark-stale` for affected tasks; queued tasks inherit the new version without becoming stale.
6. Leave unaffected tasks unchanged.

Do not broadcast before confirmation and do not silently replace accepted work.

## Existing threads and guardrails

- Never auto-adopt existing chats. List same-project candidates, let the user confirm task bindings once, then run `adopt --confirmed`.
- Reject project ID/path mismatches, duplicate task IDs, duplicate thread bindings, dependency cycles, task workspaces outside the project root, and more than four active children.
- Do not add heartbeat, cron, or background polling in v1. Synchronize only on a user command or an active hub turn.
- Do not store secrets, private URLs, or complete chat histories in packets or registry state.
- Preserve existing project files. Initialization may add `00_project_control` and non-destructive manifest pointers; it must not rewrite `asset-index.json` or migrate legacy deliverables.
