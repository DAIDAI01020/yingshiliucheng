from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
CONTROL_REL = Path("00_project_control")
REGISTRY_REL = CONTROL_REL / "thread-registry.json"
CONTEXT_REL = CONTROL_REL / "project-context.md"
TASKS_REL = CONTROL_REL / "thread-tasks"
MANIFEST_NAME = "project-manifest.json"
CONTAINER_MODE = "shared_project_shared_root"
MAX_ACTIVE_HARD_LIMIT = 4
VALID_STATUSES = {
    "queued",
    "active",
    "waiting_user",
    "blocked",
    "ready_for_review",
    "accepted",
    "stale",
    "archived",
}
OCCUPIED_STATUSES = {"active", "waiting_user", "blocked", "ready_for_review"}
DEPENDENCY_DONE = {"accepted", "archived"}
CHILD_HANDOFF_STATUSES = {"active", "waiting_user", "blocked", "ready_for_review"}
TRANSITIONS = {
    "queued": {"active"},
    "active": {"waiting_user", "blocked", "ready_for_review", "stale"},
    "waiting_user": {"active", "blocked", "ready_for_review", "stale"},
    "blocked": {"active", "waiting_user", "ready_for_review", "stale"},
    "ready_for_review": {"active", "accepted", "stale"},
    "accepted": {"stale", "archived"},
    "stale": {"active", "archived"},
    "archived": set(),
}
TASK_ID_RE = re.compile(r"^[A-Z][A-Z0-9_-]{1,31}$")


class RegistryError(ValueError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel_text(path_value: Path) -> str:
    return path_value.as_posix()


def normalized_path(value: str | Path) -> str:
    return os.path.normcase(os.path.normpath(str(Path(value).resolve())))


def same_path(left: str | Path, right: str | Path) -> bool:
    return normalized_path(left) == normalized_path(right)


def resolve_inside(project_root: Path, value: str | Path, label: str) -> Path:
    candidate = Path(value)
    resolved = candidate.resolve() if candidate.is_absolute() else (project_root / candidate).resolve()
    try:
        resolved.relative_to(project_root.resolve())
    except ValueError as exc:
        raise RegistryError(f"{label} must stay inside project_root: {value}") from exc
    return resolved


def read_json(path_value: Path) -> dict[str, Any]:
    try:
        data = json.loads(path_value.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise RegistryError(f"missing file: {path_value}") from exc
    except json.JSONDecodeError as exc:
        raise RegistryError(f"invalid JSON in {path_value}: {exc}") from exc
    if not isinstance(data, dict):
        raise RegistryError(f"expected a JSON object: {path_value}")
    return data


def write_json(path_value: Path, data: dict[str, Any]) -> None:
    path_value.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path_value.with_suffix(f"{path_value.suffix}.tmp")
    temp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp_path.replace(path_value)


def project_paths(project_root: str | Path) -> dict[str, Path]:
    root = Path(project_root).resolve()
    return {
        "root": root,
        "control": root / CONTROL_REL,
        "registry": root / REGISTRY_REL,
        "context": root / CONTEXT_REL,
        "tasks": root / TASKS_REL,
        "manifest": root / MANIFEST_NAME,
    }


def validate_project_binding(project_root: Path, project_id: str, project_path: str) -> None:
    if not project_id:
        raise RegistryError("project_id is required")
    if not project_path:
        raise RegistryError("project_path is required")
    if not same_path(project_root, project_path):
        raise RegistryError(f"project_path does not match project_root: {project_path} != {project_root}")
    if Path(project_id).is_absolute() and not same_path(project_id, project_root):
        raise RegistryError(f"path-based project_id does not match project_root: {project_id} != {project_root}")


def context_default(project_name: str) -> str:
    return (
        f"# {project_name} · Project Context\n\n"
        "context_version: 1\n\n"
        "## Approved global decisions\n\n"
        "- Add only confirmed project-wide decisions here.\n\n"
        "## Global locks\n\n"
        "- Keep brief, style, character, product, platform, and delivery locks versioned.\n\n"
        "## Change log\n\n"
        "- v1: thread orchestration initialized.\n"
    )


def update_manifest_pointer(paths: dict[str, Path], max_active: int) -> None:
    manifest = read_json(paths["manifest"])
    current = manifest.setdefault("current", {})
    workflow = manifest.setdefault("workflow", {})
    if not isinstance(current, dict) or not isinstance(workflow, dict):
        raise RegistryError("project-manifest current/workflow fields must be objects")
    current["thread_registry"] = rel_text(REGISTRY_REL)
    workflow["thread_orchestration"] = {
        "schema_version": SCHEMA_VERSION,
        "enabled": True,
        "container_mode": CONTAINER_MODE,
        "registry": rel_text(REGISTRY_REL),
        "project_context": rel_text(CONTEXT_REL),
        "task_root": rel_text(TASKS_REL),
        "max_active": max_active,
    }
    write_json(paths["manifest"], manifest)


def init_registry(
    project_root: str,
    project_id: str,
    project_path: str,
    project_name: str = "",
    max_active: int = MAX_ACTIVE_HARD_LIMIT,
    dry_run: bool = False,
) -> dict[str, Any]:
    if not 1 <= max_active <= MAX_ACTIVE_HARD_LIMIT:
        raise RegistryError("max_active must be between 1 and 4")
    paths = project_paths(project_root)
    if not paths["root"].is_dir():
        raise RegistryError(f"project_root does not exist: {paths['root']}")
    if not paths["manifest"].is_file():
        raise RegistryError(f"project-manifest.json is required: {paths['manifest']}")
    validate_project_binding(paths["root"], project_id, project_path)
    manifest = read_json(paths["manifest"])
    name = project_name or manifest.get("projectName") or manifest.get("project") or paths["root"].name

    if paths["registry"].is_file():
        registry = read_json(paths["registry"])
        if registry.get("project_id") != project_id:
            raise RegistryError("existing registry project_id mismatch")
        if not same_path(registry.get("project_root", ""), paths["root"]):
            raise RegistryError("existing registry project_root mismatch")
        return {"action": "already_initialized", "registry": registry, "dry_run": dry_run}

    timestamp = now_iso()
    registry = {
        "schema_version": SCHEMA_VERSION,
        "project_id": project_id,
        "project_path": str(Path(project_path).resolve()),
        "project_root": str(paths["root"]),
        "project_name": name,
        "container_mode": CONTAINER_MODE,
        "max_active": max_active,
        "context": {
            "path": rel_text(CONTEXT_REL),
            "version": 1,
            "updated_at": timestamp,
        },
        "split_reason": "",
        "global_prerequisites": [],
        "hub": {
            "thread_id": "",
            "host_id": None,
            "thread_title": f"[{name}][总控]",
            "status": "unbound",
            "pinned": False,
            "updated_at": timestamp,
        },
        "tasks": [],
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    if dry_run:
        return {
            "action": "would_initialize",
            "dry_run": True,
            "would_create": [str(paths["context"]), str(paths["registry"]), str(paths["tasks"])],
            "would_update": [str(paths["manifest"])],
            "registry": registry,
        }

    paths["tasks"].mkdir(parents=True, exist_ok=True)
    if not paths["context"].exists():
        paths["context"].write_text(context_default(name), encoding="utf-8")
    write_json(paths["registry"], registry)
    update_manifest_pointer(paths, max_active)
    return {"action": "initialized", "registry_path": str(paths["registry"]), "registry": registry}


def load_registry(project_root: str | Path) -> tuple[dict[str, Path], dict[str, Any]]:
    paths = project_paths(project_root)
    registry = read_json(paths["registry"])
    if not same_path(registry.get("project_root", ""), paths["root"]):
        raise RegistryError("registry project_root does not match the requested project_root")
    return paths, registry


def find_task(registry: dict[str, Any], task_id: str) -> dict[str, Any]:
    for task in registry.get("tasks", []):
        if task.get("task_id") == task_id:
            return task
    raise RegistryError(f"unknown task_id: {task_id}")


def validate_dependencies(tasks: list[dict[str, Any]]) -> None:
    ids = [task["task_id"] for task in tasks]
    if len(ids) != len(set(ids)):
        raise RegistryError("duplicate task_id in plan")
    id_set = set(ids)
    for task in tasks:
        unknown = sorted(set(task.get("dependencies", [])) - id_set)
        if unknown:
            raise RegistryError(f"{task['task_id']} has unknown dependencies: {unknown}")
        if task["task_id"] in task.get("dependencies", []):
            raise RegistryError(f"{task['task_id']} cannot depend on itself")

    graph = {task["task_id"]: list(task.get("dependencies", [])) for task in tasks}
    visiting: set[str] = set()
    visited: set[str] = set()

    def walk(node: str) -> None:
        if node in visiting:
            raise RegistryError(f"dependency cycle detected at {node}")
        if node in visited:
            return
        visiting.add(node)
        for dependency in graph[node]:
            walk(dependency)
        visiting.remove(node)
        visited.add(node)

    for task_id in graph:
        walk(task_id)


def packet_for_task(registry: dict[str, Any], raw: dict[str, Any]) -> dict[str, Any]:
    task_id = raw["task_id"]
    task_root = TASKS_REL / task_id
    project_name = registry.get("project_name", "项目")
    title = str(raw.get("title") or task_id).strip()
    thread_title = str(raw.get("thread_title") or f"[{project_name}][{task_id}][{title}]")
    return {
        "schema_version": SCHEMA_VERSION,
        "project_id": registry["project_id"],
        "project_root": registry["project_root"],
        "task_id": task_id,
        "thread_title": thread_title,
        "goal": str(raw.get("goal", "")).strip(),
        "scope_boundary": str(raw.get("scope_boundary", "")).strip(),
        "source_files": list(raw.get("source_files", [])),
        "global_context_path": rel_text(CONTEXT_REL),
        "global_context_version": registry["context"]["version"],
        "must_inherit": list(raw.get("inherited_locks", [])),
        "must_not_change": list(raw.get("must_not_change", [])),
        "owning_skill": str(raw.get("owning_skill", "")).strip(),
        "deliverables": list(raw.get("deliverables", [])),
        "task_workspace": rel_text(task_root / "working"),
        "output_path_rule": str(raw.get("output_path_rule", "")).strip(),
        "handoff_path": rel_text(task_root / "handoff.json"),
    }


def register_plan(project_root: str, input_path: str) -> dict[str, Any]:
    paths, registry = load_registry(project_root)
    plan = read_json(Path(input_path).resolve())
    if plan.get("confirmed") is not True:
        raise RegistryError("register-plan requires confirmed:true")
    for field, expected in [
        ("project_id", registry["project_id"]),
        ("container_mode", CONTAINER_MODE),
    ]:
        if plan.get(field) != expected:
            raise RegistryError(f"plan {field} mismatch")
    for field in ["project_path", "project_root"]:
        if not same_path(plan.get(field, ""), paths["root"]):
            raise RegistryError(f"plan {field} mismatch")

    parallel_limit = int(plan.get("parallel_limit", MAX_ACTIVE_HARD_LIMIT))
    if not 1 <= parallel_limit <= MAX_ACTIVE_HARD_LIMIT:
        raise RegistryError("parallel_limit must be between 1 and 4")
    raw_tasks = plan.get("tasks")
    if not isinstance(raw_tasks, list) or not raw_tasks:
        raise RegistryError("plan tasks must be a non-empty list")

    normalized: list[dict[str, Any]] = []
    for raw in raw_tasks:
        if not isinstance(raw, dict):
            raise RegistryError("every plan task must be an object")
        task_id = str(raw.get("task_id", "")).strip().upper()
        if not TASK_ID_RE.fullmatch(task_id):
            raise RegistryError(f"invalid task_id: {task_id}")
        item = dict(raw)
        item["task_id"] = task_id
        item["dependencies"] = list(item.get("dependencies", []))
        item["status"] = "queued"
        for source in item.get("source_files", []):
            resolve_inside(paths["root"], source, f"{task_id}.source_files")
        normalized.append(item)
    validate_dependencies(normalized)

    prerequisites = list(plan.get("global_prerequisites", []))
    task_ids = {item["task_id"] for item in normalized}
    if not set(prerequisites).issubset(task_ids):
        raise RegistryError("global_prerequisites must reference plan task IDs")

    existing_by_id = {task["task_id"]: task for task in registry.get("tasks", [])}
    created: list[str] = []
    unchanged: list[str] = []
    timestamp = now_iso()
    for raw in normalized:
        packet = packet_for_task(registry, raw)
        task_id = raw["task_id"]
        task_dir = resolve_inside(paths["root"], TASKS_REL / task_id, "task_dir")
        packet_path = task_dir / "task-packet.json"
        handoff_path = task_dir / "handoff.json"
        candidate = {
            "task_id": task_id,
            "title": str(raw.get("title") or task_id),
            "thread_title": packet["thread_title"],
            "goal": packet["goal"],
            "status": "queued",
            "dependencies": list(raw.get("dependencies", [])),
            "inherited_locks": list(raw.get("inherited_locks", [])),
            "owning_skill": packet["owning_skill"],
            "task_workspace": packet["task_workspace"],
            "task_packet_path": rel_text(TASKS_REL / task_id / "task-packet.json"),
            "handoff_path": packet["handoff_path"],
            "deliverables": packet["deliverables"],
            "output_path_rule": packet["output_path_rule"],
            "source_files": packet["source_files"],
            "thread_id": None,
            "host_id": None,
            "context_version": registry["context"]["version"],
            "stale_reason": None,
            "created_at": timestamp,
            "updated_at": timestamp,
        }
        if task_id in existing_by_id:
            existing = existing_by_id[task_id]
            comparable = [
                "title",
                "goal",
                "dependencies",
                "inherited_locks",
                "owning_skill",
                "deliverables",
                "output_path_rule",
                "source_files",
            ]
            if any(existing.get(key) != candidate.get(key) for key in comparable):
                raise RegistryError(f"task {task_id} already exists with different immutable fields")
            unchanged.append(task_id)
            continue

        (task_dir / "working").mkdir(parents=True, exist_ok=True)
        write_json(packet_path, packet)
        write_json(
            handoff_path,
            {
                "schema_version": SCHEMA_VERSION,
                "task_id": task_id,
                "thread_id": "",
                "status": "queued",
                "summary": "",
                "deliverables": [],
                "decisions": [],
                "open_issues": [],
                "needs_main_decision": False,
                "global_change_proposals": [],
                "context_version": registry["context"]["version"],
                "updated_at": timestamp,
            },
        )
        registry.setdefault("tasks", []).append(candidate)
        created.append(task_id)

    registry["max_active"] = parallel_limit
    registry["split_reason"] = str(plan.get("split_reason", ""))
    registry["global_prerequisites"] = prerequisites
    registry["last_plan_confirmed_at"] = timestamp
    registry["updated_at"] = timestamp
    write_json(paths["registry"], registry)
    update_manifest_pointer(paths, parallel_limit)
    return {"action": "plan_registered", "created": created, "unchanged": unchanged, "task_count": len(registry["tasks"])}


def dependencies_satisfied(task: dict[str, Any], registry: dict[str, Any]) -> bool:
    status_by_id = {item["task_id"]: item["status"] for item in registry.get("tasks", [])}
    return all(status_by_id.get(dependency) in DEPENDENCY_DONE for dependency in task.get("dependencies", []))


def bind_hub(
    project_root: str,
    thread_id: str,
    thread_title: str = "",
    host_id: str = "",
    pinned: bool = False,
) -> dict[str, Any]:
    paths, registry = load_registry(project_root)
    if not thread_id:
        raise RegistryError("thread_id is required")
    duplicate = next((task for task in registry.get("tasks", []) if task.get("thread_id") == thread_id), None)
    if duplicate:
        raise RegistryError(f"hub thread_id is already bound to child task {duplicate['task_id']}")
    hub = registry.setdefault(
        "hub",
        {
            "thread_id": "",
            "host_id": None,
            "thread_title": f"[{registry.get('project_name', '项目')}][总控]",
            "status": "unbound",
            "pinned": False,
            "updated_at": now_iso(),
        },
    )
    if hub.get("thread_id") == thread_id:
        hub["thread_title"] = thread_title or hub["thread_title"]
        hub["host_id"] = host_id or hub.get("host_id")
        hub["pinned"] = pinned or hub.get("pinned", False)
        hub["status"] = "active"
        hub["updated_at"] = now_iso()
        registry["updated_at"] = hub["updated_at"]
        write_json(paths["registry"], registry)
        return {"action": "hub_already_bound", "hub": hub}
    if hub.get("thread_id"):
        raise RegistryError("registry already has a different hub thread_id")
    hub.update(
        {
            "thread_id": thread_id,
            "host_id": host_id or None,
            "thread_title": thread_title or hub["thread_title"],
            "status": "active",
            "pinned": pinned,
            "updated_at": now_iso(),
        }
    )
    registry["updated_at"] = hub["updated_at"]
    write_json(paths["registry"], registry)
    return {"action": "hub_bound", "hub": hub}


def next_batch(project_root: str, limit: int | None = None) -> dict[str, Any]:
    _, registry = load_registry(project_root)
    active_count = sum(task.get("status") in OCCUPIED_STATUSES for task in registry.get("tasks", []))
    available = max(0, registry.get("max_active", MAX_ACTIVE_HARD_LIMIT) - active_count)
    if limit is not None:
        if limit < 1:
            raise RegistryError("limit must be positive")
        available = min(available, limit)
    eligible = [
        task
        for task in registry.get("tasks", [])
        if task.get("status") == "queued"
        and not task.get("thread_id")
        and dependencies_satisfied(task, registry)
    ]
    selected = eligible[:available]
    return {
        "active_count": active_count,
        "available_slots": available,
        "selected": [
            {
                "task_id": task["task_id"],
                "thread_title": task["thread_title"],
                "task_packet_path": task["task_packet_path"],
                "handoff_path": task["handoff_path"],
            }
            for task in selected
        ],
        "queued_remaining": len([task for task in registry.get("tasks", []) if task.get("status") == "queued"]) - len(selected),
    }


def bind_thread(
    project_root: str,
    task_id: str,
    thread_id: str,
    thread_title: str = "",
    host_id: str = "",
    confirmed: bool = False,
) -> dict[str, Any]:
    paths, registry = load_registry(project_root)
    task = find_task(registry, task_id)
    if not thread_id:
        raise RegistryError("thread_id is required")
    duplicate = next((item for item in registry["tasks"] if item.get("thread_id") == thread_id and item["task_id"] != task_id), None)
    if duplicate:
        raise RegistryError(f"thread_id already bound to {duplicate['task_id']}")
    if task.get("thread_id") == thread_id:
        return {"action": "already_bound", "task": task}
    if task.get("thread_id"):
        raise RegistryError(f"task {task_id} already has a different thread_id")
    if task.get("status") != "queued":
        raise RegistryError(f"task {task_id} must be queued before binding")
    if not dependencies_satisfied(task, registry) and not confirmed:
        raise RegistryError(f"task {task_id} dependencies are not accepted; use --confirmed only for an explicitly approved adoption")
    active_count = sum(item.get("status") in OCCUPIED_STATUSES for item in registry["tasks"])
    if active_count >= registry.get("max_active", MAX_ACTIVE_HARD_LIMIT):
        raise RegistryError("active child-thread limit reached")
    task["thread_id"] = thread_id
    task["host_id"] = host_id or None
    task["thread_title"] = thread_title or task["thread_title"]
    task["status"] = "active"
    task["updated_at"] = now_iso()
    registry["updated_at"] = task["updated_at"]
    write_json(paths["registry"], registry)
    return {"action": "thread_bound", "task": task}


def update_status(project_root: str, task_id: str, status: str, stale_reason: str = "") -> dict[str, Any]:
    if status not in VALID_STATUSES:
        raise RegistryError(f"invalid status: {status}")
    paths, registry = load_registry(project_root)
    task = find_task(registry, task_id)
    old = task["status"]
    if status != old and status not in TRANSITIONS[old]:
        raise RegistryError(f"invalid transition: {old} -> {status}")
    if status == "archived" and old not in {"accepted", "stale"}:
        raise RegistryError("archive only after acceptance or stale retirement")
    if status == "stale" and not stale_reason:
        raise RegistryError("stale status requires --stale-reason")
    task["status"] = status
    task["stale_reason"] = stale_reason or (task.get("stale_reason") if status == "stale" else None)
    task["updated_at"] = now_iso()
    registry["updated_at"] = task["updated_at"]
    write_json(paths["registry"], registry)
    return {"action": "status_updated", "from": old, "to": status, "task": task}


def sync_handoff(project_root: str, task_id: str) -> dict[str, Any]:
    paths, registry = load_registry(project_root)
    task = find_task(registry, task_id)
    handoff_path = resolve_inside(paths["root"], task["handoff_path"], "handoff_path")
    handoff = read_json(handoff_path)
    if handoff.get("task_id") != task_id:
        raise RegistryError("handoff task_id mismatch")
    if handoff.get("status") not in CHILD_HANDOFF_STATUSES:
        raise RegistryError("handoff status must be active, waiting_user, blocked, or ready_for_review")
    if handoff.get("status") == "ready_for_review" and not str(handoff.get("summary", "")).strip():
        raise RegistryError("ready_for_review handoff requires summary")
    if task.get("thread_id") and handoff.get("thread_id") not in {"", task["thread_id"]}:
        raise RegistryError("handoff thread_id mismatch")
    deliverables = handoff.get("deliverables", [])
    if not isinstance(deliverables, list):
        raise RegistryError("handoff deliverables must be a list")
    for item in deliverables:
        candidate = item if isinstance(item, str) else item.get("path") or item.get("file_path") if isinstance(item, dict) else None
        if candidate:
            resolve_inside(paths["root"], candidate, "handoff deliverable")
    target_status = "waiting_user" if handoff.get("needs_main_decision") else handoff["status"]
    old = task["status"]
    if target_status != old and target_status not in TRANSITIONS[old]:
        raise RegistryError(f"handoff cannot transition task: {old} -> {target_status}")
    task["status"] = target_status
    task["handoff_summary"] = str(handoff.get("summary", ""))
    task["handoff_updated_at"] = handoff.get("updated_at") or now_iso()
    task["updated_at"] = now_iso()
    registry["updated_at"] = task["updated_at"]
    write_json(paths["registry"], registry)
    return {"action": "handoff_synced", "task": task, "handoff": handoff}


def mark_stale(project_root: str, task_ids: list[str], context_version: int, reason: str) -> dict[str, Any]:
    if not reason.strip():
        raise RegistryError("reason is required")
    paths, registry = load_registry(project_root)
    current_version = int(registry["context"]["version"])
    if context_version < current_version:
        raise RegistryError("context_version cannot move backwards")
    updated: list[str] = []
    queued_refreshed: list[str] = []
    skipped_archived: list[str] = []
    timestamp = now_iso()
    for task_id in task_ids:
        task = find_task(registry, task_id)
        task["context_version"] = context_version
        packet_path = resolve_inside(paths["root"], task["task_packet_path"], "task_packet_path")
        packet = read_json(packet_path)
        packet["global_context_version"] = context_version
        write_json(packet_path, packet)
        if task["status"] == "queued":
            queued_refreshed.append(task_id)
        elif task["status"] == "archived":
            skipped_archived.append(task_id)
        else:
            task["status"] = "stale"
            task["stale_reason"] = reason
            updated.append(task_id)
        task["updated_at"] = timestamp
    registry["context"]["version"] = context_version
    registry["context"]["updated_at"] = timestamp
    registry["updated_at"] = timestamp
    write_json(paths["registry"], registry)
    return {"action": "context_applied", "stale": updated, "queued_refreshed": queued_refreshed, "skipped_archived": skipped_archived}


def summary(project_root: str) -> dict[str, Any]:
    _, registry = load_registry(project_root)
    counts = Counter(task.get("status") for task in registry.get("tasks", []))
    return {
        "project_id": registry["project_id"],
        "project_root": registry["project_root"],
        "hub": registry.get("hub"),
        "context_version": registry["context"]["version"],
        "max_active": registry["max_active"],
        "counts": {status: counts.get(status, 0) for status in sorted(VALID_STATUSES)},
        "tasks": [
            {
                "task_id": task["task_id"],
                "title": task["title"],
                "status": task["status"],
                "dependencies": task.get("dependencies", []),
                "thread_id": task.get("thread_id"),
                "handoff_summary": task.get("handoff_summary", ""),
                "stale_reason": task.get("stale_reason"),
            }
            for task in registry.get("tasks", [])
        ],
    }


def validate_registry(project_root: str) -> dict[str, Any]:
    paths, registry = load_registry(project_root)
    errors: list[str] = []
    if registry.get("schema_version") != SCHEMA_VERSION:
        errors.append("unsupported schema_version")
    if registry.get("container_mode") != CONTAINER_MODE:
        errors.append("container_mode mismatch")
    if not 1 <= int(registry.get("max_active", 0)) <= MAX_ACTIVE_HARD_LIMIT:
        errors.append("max_active must be 1..4")
    ids = [task.get("task_id") for task in registry.get("tasks", [])]
    if len(ids) != len(set(ids)):
        errors.append("duplicate task IDs")
    thread_ids = [task.get("thread_id") for task in registry.get("tasks", []) if task.get("thread_id")]
    if len(thread_ids) != len(set(thread_ids)):
        errors.append("duplicate thread IDs")
    hub = registry.get("hub", {})
    if not isinstance(hub, dict):
        errors.append("hub must be an object")
    elif hub.get("thread_id") and hub.get("thread_id") in thread_ids:
        errors.append("hub thread ID duplicates a child thread ID")
    if sum(task.get("status") in OCCUPIED_STATUSES for task in registry.get("tasks", [])) > registry.get("max_active", 0):
        errors.append("active thread limit exceeded")
    try:
        validate_dependencies(registry.get("tasks", []))
    except RegistryError as exc:
        errors.append(str(exc))
    for task in registry.get("tasks", []):
        if task.get("status") not in VALID_STATUSES:
            errors.append(f"{task.get('task_id')}: invalid status")
        for field in ["task_workspace", "task_packet_path", "handoff_path"]:
            try:
                resolve_inside(paths["root"], task.get(field, ""), f"{task.get('task_id')}.{field}")
            except RegistryError as exc:
                errors.append(str(exc))
    if not paths["context"].is_file():
        errors.append("missing project-context.md")
    manifest = read_json(paths["manifest"])
    pointer = manifest.get("current", {}).get("thread_registry") if isinstance(manifest.get("current", {}), dict) else None
    if pointer != rel_text(REGISTRY_REL):
        errors.append("project-manifest thread_registry pointer mismatch")
    if errors:
        raise RegistryError("; ".join(errors))
    return {"valid": True, "task_count": len(registry.get("tasks", [])), "registry_path": str(paths["registry"])}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage project-scoped Codex thread task state.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--project-root", required=True)
    init.add_argument("--project-id", required=True)
    init.add_argument("--project-path", required=True)
    init.add_argument("--project-name", default="")
    init.add_argument("--max-active", type=int, default=MAX_ACTIVE_HARD_LIMIT)
    init.add_argument("--dry-run", action="store_true")

    register = sub.add_parser("register-plan")
    register.add_argument("--project-root", required=True)
    register.add_argument("--input", required=True)

    batch = sub.add_parser("next-batch")
    batch.add_argument("--project-root", required=True)
    batch.add_argument("--limit", type=int)

    hub = sub.add_parser("bind-hub")
    hub.add_argument("--project-root", required=True)
    hub.add_argument("--thread-id", required=True)
    hub.add_argument("--thread-title", default="")
    hub.add_argument("--host-id", default="")
    hub.add_argument("--pinned", action="store_true")

    bind = sub.add_parser("bind-thread")
    bind.add_argument("--project-root", required=True)
    bind.add_argument("--task-id", required=True)
    bind.add_argument("--thread-id", required=True)
    bind.add_argument("--thread-title", default="")
    bind.add_argument("--host-id", default="")

    adopt = sub.add_parser("adopt")
    adopt.add_argument("--project-root", required=True)
    adopt.add_argument("--task-id", required=True)
    adopt.add_argument("--thread-id", required=True)
    adopt.add_argument("--thread-title", default="")
    adopt.add_argument("--host-id", default="")
    adopt.add_argument("--confirmed", action="store_true", required=True)

    update = sub.add_parser("update")
    update.add_argument("--project-root", required=True)
    update.add_argument("--task-id", required=True)
    update.add_argument("--status", required=True)
    update.add_argument("--stale-reason", default="")

    sync = sub.add_parser("sync-handoff")
    sync.add_argument("--project-root", required=True)
    sync.add_argument("--task-id", required=True)

    stale = sub.add_parser("mark-stale")
    stale.add_argument("--project-root", required=True)
    stale.add_argument("--task-ids", nargs="+", required=True)
    stale.add_argument("--context-version", type=int, required=True)
    stale.add_argument("--reason", required=True)

    status = sub.add_parser("summary")
    status.add_argument("--project-root", required=True)

    validate = sub.add_parser("validate")
    validate.add_argument("--project-root", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        if args.command == "init":
            result = init_registry(args.project_root, args.project_id, args.project_path, args.project_name, args.max_active, args.dry_run)
        elif args.command == "register-plan":
            result = register_plan(args.project_root, args.input)
        elif args.command == "next-batch":
            result = next_batch(args.project_root, args.limit)
        elif args.command == "bind-hub":
            result = bind_hub(args.project_root, args.thread_id, args.thread_title, args.host_id, args.pinned)
        elif args.command == "bind-thread":
            result = bind_thread(args.project_root, args.task_id, args.thread_id, args.thread_title, args.host_id)
        elif args.command == "adopt":
            result = bind_thread(args.project_root, args.task_id, args.thread_id, args.thread_title, args.host_id, confirmed=True)
        elif args.command == "update":
            result = update_status(args.project_root, args.task_id, args.status, args.stale_reason)
        elif args.command == "sync-handoff":
            result = sync_handoff(args.project_root, args.task_id)
        elif args.command == "mark-stale":
            result = mark_stale(args.project_root, args.task_ids, args.context_version, args.reason)
        elif args.command == "summary":
            result = summary(args.project_root)
        elif args.command == "validate":
            result = validate_registry(args.project_root)
        else:
            raise RegistryError(f"unknown command: {args.command}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (RegistryError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
