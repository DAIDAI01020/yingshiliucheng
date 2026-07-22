# Thread Orchestration Contracts

Use these contracts when the hub prepares a split, creates child threads, imports handoffs, broadcasts context deltas, or adopts existing threads.

## Ownership and storage

```text
{project_root}/
  project-manifest.json
  asset-index.json
  00_project_control/
    project-context.md
    thread-registry.json
    thread-tasks/
      P01/
        task-packet.json
        handoff.json
        working/
```

`$project-state-manager` owns the persisted schema and project-manifest pointer. `$project-thread-orchestrator` is the only workflow allowed to mutate the registry. A child may write its own working directory and handoff only. `$production-manager` renders registry state; it does not mutate it.

The registry also stores one hub record:

```json
{
  "hub": {
    "thread_id": "",
    "host_id": null,
    "thread_title": "[项目][总控]",
    "status": "unbound",
    "pinned": false,
    "updated_at": ""
  }
}
```

Bind only a real same-project thread ID. Keep one hub per registry.

## `thread_split_plan`

```json
{
  "schema_version": 1,
  "project_id": "H:\\project",
  "project_path": "H:\\project",
  "project_root": "H:\\project",
  "container_mode": "shared_project_shared_root",
  "split_reason": "",
  "global_prerequisites": ["P01"],
  "parallel_limit": 4,
  "confirmed": true,
  "tasks": [
    {
      "task_id": "P01",
      "title": "",
      "goal": "",
      "scope_boundary": "",
      "source_files": [],
      "inherited_locks": [],
      "dependencies": [],
      "owning_skill": "",
      "deliverables": [],
      "output_path_rule": "",
      "status": "queued"
    }
  ]
}
```

Require `confirmed:true` before `register-plan`. `parallel_limit` must be `1..4`; default to `4`.

## `child_thread_task_packet`

```json
{
  "schema_version": 1,
  "project_id": "",
  "project_root": "",
  "task_id": "P01",
  "thread_title": "[项目][P01][名称]",
  "goal": "",
  "scope_boundary": "",
  "source_files": [],
  "global_context_path": "00_project_control/project-context.md",
  "global_context_version": 1,
  "must_inherit": [],
  "must_not_change": [],
  "owning_skill": "",
  "deliverables": [],
  "task_workspace": "00_project_control/thread-tasks/P01/working",
  "output_path_rule": "",
  "handoff_path": "00_project_control/thread-tasks/P01/handoff.json"
}
```

The initial child prompt should summarize these fields and tell the child to read the packet from disk. Do not include unrelated hub turns.

## `thread_result_packet`

Store it in `handoff.json`:

```json
{
  "schema_version": 1,
  "task_id": "P01",
  "thread_id": "",
  "status": "ready_for_review",
  "summary": "",
  "deliverables": [],
  "decisions": [],
  "open_issues": [],
  "needs_main_decision": false,
  "global_change_proposals": [],
  "context_version": 1,
  "updated_at": ""
}
```

Child-authored status may be `active`, `waiting_user`, `blocked`, or `ready_for_review`. Only the hub may accept or archive.

## Registry task record

Keep these fields for every task:

```text
task_id / title / thread_title / goal / status
dependencies / inherited_locks / owning_skill
task_workspace / task_packet_path / handoff_path
deliverables / output_path_rule / source_files
thread_id / host_id
context_version / stale_reason
created_at / updated_at
```

Treat `active`, `waiting_user`, `blocked`, and `ready_for_review` as occupied concurrency slots. Dependencies are satisfied only by `accepted` or `archived` tasks.

## Tool sequence

```text
list projects -> exact path match
create/reuse hub -> pin -> bind-hub
show split plan -> user confirms once
registry init/register -> next-batch
create_thread(project + local) -> set title -> bind-thread
read/send child threads -> sync-handoff
user accepts -> promote output -> archive tool -> registry archived
```

Never call a fork operation. A fork copies completed chat history and defeats context isolation.

## Context delta packet

```json
{
  "type": "project_context_delta",
  "from_version": 1,
  "to_version": 2,
  "changed_locks": ["character_lock"],
  "summary": "",
  "required_action": "review_and_refresh_affected_output"
}
```

Send this only to confirmed affected thread IDs. Record the reason in `stale_reason` and preserve unaffected results.

## Failure handling

- Missing thread tools: output task packets only; keep tasks `queued`.
- Thread creation failure: do not bind; keep the task `queued`.
- Missing or invalid handoff: keep current state and return the invalid fields.
- Project mismatch: stop before any thread creation.
- Global proposal from child: route to the hub; never let the child edit the context or registry.
- Existing thread: require same project, explicit user confirmation, and a standard handoff before trusting its result.
