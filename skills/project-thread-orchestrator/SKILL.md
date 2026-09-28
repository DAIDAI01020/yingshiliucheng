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

Keep one short, coherent task in the current chat. A structural split may be proposed, but only an explicit user request for separate chats or approval of the concrete split authorizes their creation. Do not split merely because a document is long.

## Split workflow

1. Locate the managed `project_root` and its saved Codex project with the project-listing tool. Require an exact project-path match.
2. Ask the owning director to make `thread_split_plan`; do not replace its creative judgment with paragraph counts.
3. Hard-split when deliverable/platform, reference set, or approval dependency differs.
4. Suggest a split when at least two change: narrative function, time/location, character group, asset set, or independent revision need.
5. Merge adjacent short units that share characters, scene, style, references, and approval path.
6. Put global prerequisites such as brief, concept, style, character, or product locks before dependent tasks.
7. Make the split concrete and user-visible. A current request or prior approval covering that exact plan satisfies confirmation; ask only for a material unapproved change. Do not create child threads based solely on inferred complexity.

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
2. Read available handoffs first. Request a refresh only when user authorization covers messaging that child; a progress-only request is not permission to send new prompts.
3. Import a handoff with `sync-handoff`; reject a missing, incomplete, mismatched, or out-of-root handoff.
4. Update the `$production-manager` thread board.
5. Start the next eligible batch only within the approved creation/coordination scope and when slots and dependencies allow; a read-only progress request does not launch another batch.

Use these state values exactly:

```text
queued / active / waiting_user / blocked / ready_for_review / accepted / stale / archived
```

The hub alone changes `ready_for_review` to `accepted`. Promote accepted deliverables within the authorized delivery scope. Archive a child with the Codex archive tool only when the user requested archival or approved a lifecycle plan including it, then mark the registry entry `archived`. Acceptance alone does not imply chat archival. Keep the registered hub thread unarchived and pinned.

## Global context changes

Version global changes instead of replaying the full project history:

1. Update `project-context.md` and increment `context_version`.
2. Calculate affected registered tasks from `inherited_locks`.
3. Identify affected recipients and the delta. Reuse existing user authorization covering that scope; otherwise obtain one confirmation.
4. Send only the delta to those thread IDs.
5. Run `mark-stale` for affected tasks; queued tasks inherit the new version without becoming stale.
6. Leave unaffected tasks unchanged.

Do not broadcast outside user-authorized scope and do not silently replace accepted work. A child request to reply/report is not independent authorization to message another chat.

## Existing threads and guardrails

- Never auto-adopt existing chats. List same-project candidates, let the user confirm task bindings once, then run `adopt --confirmed`.
- Reject project ID/path mismatches, duplicate task IDs, duplicate thread bindings, dependency cycles, task workspaces outside the project root, and more than four active children.
- Do not add background polling by default. Synchronize within an authorized active workflow; an explicit monitoring request uses the app automation tools and current tool contract.
- Do not store secrets, private URLs, or complete chat histories in packets or registry state.
- Preserve existing project files. Initialization may add `00_project_control` and non-destructive manifest pointers; it must not rewrite `asset-index.json` or migrate legacy deliverables.
