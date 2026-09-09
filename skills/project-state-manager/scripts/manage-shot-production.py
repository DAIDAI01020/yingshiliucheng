from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path


STATUSES = [
    "planned", "continuity_locked", "prompt_ready", "image_generated", "image_approved",
    "video_submitted", "video_generated", "qc_passed", "accepted", "blocked", "stale",
]
FLOW = STATUSES[:9]
APPROVAL_ORDER = {"anchor": 0, "hero": 1, "coverage": 2, "insert": 3, "bridge": 4}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage canonical shot production state for film/short-drama projects.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ["init", "audit", "summary", "next-batch"]:
        item = sub.add_parser(name)
        item.add_argument("--project-root", required=True, type=Path)
        if name == "next-batch":
            item.add_argument("--limit", type=int, default=4)
            item.add_argument("--from-status", default="prompt_ready")
    upsert = sub.add_parser("upsert")
    upsert.add_argument("--project-root", required=True, type=Path)
    upsert.add_argument("--input", required=True, type=Path)
    transition = sub.add_parser("transition")
    transition.add_argument("--project-root", required=True, type=Path)
    transition.add_argument("--shot-id", required=True)
    transition.add_argument("--status", required=True, choices=STATUSES)
    transition.add_argument("--artifact", action="append", default=[], help="key=absolute_or_project_relative_path")
    transition.add_argument("--qc-decision")
    transition.add_argument("--blocker")
    transition.add_argument("--resume", action="store_true")
    return parser.parse_args()


def registry_path(project_root: Path) -> Path:
    return project_root.resolve() / "production" / "shot-production-registry.json"


def default_registry(project_root: Path) -> dict:
    return {
        "schema_version": 1,
        "project_root": str(project_root.resolve()),
        "updated_at": now(),
        "shots": [],
    }


def read_registry(project_root: Path) -> dict:
    path = registry_path(project_root)
    if not path.is_file():
        return default_registry(project_root)
    data = json.loads(path.read_text(encoding="utf-8"))
    if Path(data.get("project_root", "")).resolve() != project_root.resolve():
        raise ValueError("Registry project_root does not match the requested project root.")
    return data


def atomic_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def is_inside(project_root: Path, value: str) -> bool:
    if not value:
        return True
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = project_root / candidate
    try:
        candidate.resolve().relative_to(project_root.resolve())
        return True
    except ValueError:
        return False


def normalize_packet(project_root: Path, packet: dict) -> dict:
    shot_id = str(packet.get("shot_id") or "").strip()
    if not shot_id:
        raise ValueError("shot_id is required.")
    status = packet.get("status", "planned")
    if status not in STATUSES:
        raise ValueError(f"Unsupported status: {status}")
    artifacts = packet.get("artifacts") or {}
    outside = [f"{key}:{value}" for key, value in artifacts.items() if value and not is_inside(project_root, str(value))]
    if outside:
        raise ValueError(f"Artifact path outside project_root: {', '.join(outside)}")
    return {
        "schema_version": 1,
        "shot_id": shot_id,
        "episode_id": str(packet.get("episode_id") or ""),
        "scene_id": str(packet.get("scene_id") or ""),
        "order": int(packet.get("order") or 0),
        "status": status,
        "approval_class": str(packet.get("approval_class") or "coverage"),
        "risk_level": str(packet.get("risk_level") or "medium"),
        "narrative_function": str(packet.get("narrative_function") or ""),
        "coverage_role": str(packet.get("coverage_role") or ""),
        "previous_shot_id": str(packet.get("previous_shot_id") or ""),
        "dependencies": sorted(set(str(item) for item in packet.get("dependencies", []) if item)),
        "continuity_in": packet.get("continuity_in") or {},
        "continuity_delta": packet.get("continuity_delta") or {},
        "continuity_out": packet.get("continuity_out") or {},
        "artifacts": artifacts,
        "platform_plan": packet.get("platform_plan") or {},
        "qc_decision": str(packet.get("qc_decision") or ""),
        "blocker": str(packet.get("blocker") or ""),
        "updated_at": now(),
    }


def dependency_cycles(shots: list[dict]) -> list[list[str]]:
    graph = {shot["shot_id"]: shot.get("dependencies", []) for shot in shots}
    cycles: list[list[str]] = []
    active: list[str] = []
    visited: set[str] = set()

    def walk(node: str) -> None:
        if node in active:
            cycles.append(active[active.index(node):] + [node])
            return
        if node in visited:
            return
        active.append(node)
        for child in graph.get(node, []):
            if child in graph:
                walk(child)
        active.pop()
        visited.add(node)

    for node in graph:
        walk(node)
    return cycles


def audit(registry: dict, project_root: Path) -> dict:
    shots = registry.get("shots", [])
    ids = [shot.get("shot_id") for shot in shots]
    known = set(ids)
    errors: list[str] = []
    warnings: list[str] = []
    if len(ids) != len(known):
        errors.append("duplicate_shot_id")
    for shot in shots:
        if shot.get("status") not in STATUSES:
            errors.append(f"{shot.get('shot_id')}:invalid_status")
        for dependency in shot.get("dependencies", []):
            if dependency not in known:
                errors.append(f"{shot.get('shot_id')}:missing_dependency:{dependency}")
        previous = shot.get("previous_shot_id")
        if previous and previous not in known:
            errors.append(f"{shot.get('shot_id')}:missing_previous_shot:{previous}")
        inherits = (shot.get("continuity_in") or {}).get("inherits_from")
        if previous and inherits != previous:
            warnings.append(f"{shot.get('shot_id')}:continuity_in_not_bound_to_previous_shot")
        for key, value in (shot.get("artifacts") or {}).items():
            if value and not is_inside(project_root, str(value)):
                errors.append(f"{shot.get('shot_id')}:artifact_outside_root:{key}")
    for cycle in dependency_cycles(shots):
        errors.append(f"dependency_cycle:{'->'.join(cycle)}")
    return {"valid": not errors, "read_only": True, "shot_count": len(shots), "errors": errors, "warnings": warnings}


def next_batch(registry: dict, from_status: str, limit: int) -> list[dict]:
    shots = registry.get("shots", [])
    accepted = {shot["shot_id"] for shot in shots if shot.get("status") in {"qc_passed", "accepted"}}
    ready = [
        shot for shot in shots
        if shot.get("status") == from_status and all(item in accepted for item in shot.get("dependencies", []))
    ]
    risk_order = {"high": 0, "medium": 1, "low": 2}
    ready.sort(key=lambda shot: (
        APPROVAL_ORDER.get(shot.get("approval_class"), 9),
        risk_order.get(shot.get("risk_level"), 9),
        shot.get("order", 0),
        shot.get("shot_id", ""),
    ))
    return ready[:max(1, min(limit, 20))]


def parse_artifacts(items: list[str], project_root: Path) -> dict:
    result: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Invalid --artifact, expected key=path: {item}")
        key, value = item.split("=", 1)
        if not is_inside(project_root, value):
            raise ValueError(f"Artifact path outside project_root: {value}")
        result[key] = value
    return result


def main() -> int:
    args = parse_args()
    project_root = args.project_root.resolve()
    if args.command == "init":
        registry = read_registry(project_root)
        atomic_write(registry_path(project_root), registry)
        print(json.dumps({"registry": str(registry_path(project_root)), "created": True}, ensure_ascii=False, indent=2))
        return 0
    registry = read_registry(project_root)
    if args.command == "upsert":
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        packets = payload if isinstance(payload, list) else payload.get("shots", [payload])
        normalized = [normalize_packet(project_root, packet) for packet in packets]
        by_id = {shot["shot_id"]: shot for shot in registry.get("shots", [])}
        for shot in normalized:
            by_id[shot["shot_id"]] = {**by_id.get(shot["shot_id"], {}), **shot}
        registry["shots"] = sorted(by_id.values(), key=lambda shot: (shot.get("episode_id", ""), shot.get("scene_id", ""), shot.get("order", 0), shot["shot_id"]))
        registry["updated_at"] = now()
        result = audit(registry, project_root)
        if not result["valid"]:
            raise ValueError("; ".join(result["errors"]))
        atomic_write(registry_path(project_root), registry)
        print(json.dumps({"registry": str(registry_path(project_root)), "upserted": [shot["shot_id"] for shot in normalized], **result}, ensure_ascii=False, indent=2))
        return 0
    if args.command == "transition":
        shot = next((item for item in registry.get("shots", []) if item.get("shot_id") == args.shot_id), None)
        if not shot:
            raise ValueError(f"Unknown shot_id: {args.shot_id}")
        current = shot.get("status", "planned")
        target = args.status
        if target not in {"blocked", "stale"}:
            if current in {"blocked", "stale"} and not args.resume:
                raise ValueError("Leaving blocked/stale requires --resume.")
            if current in FLOW and FLOW.index(target) > FLOW.index(current) + 1:
                raise ValueError(f"Cannot skip production state from {current} to {target}.")
            if current in FLOW and target in FLOW and FLOW.index(target) < FLOW.index(current) and not args.resume:
                raise ValueError("Backward transition requires --resume.")
        shot["status"] = target
        shot["artifacts"] = {**(shot.get("artifacts") or {}), **parse_artifacts(args.artifact, project_root)}
        if args.qc_decision is not None:
            shot["qc_decision"] = args.qc_decision
        shot["blocker"] = args.blocker or (shot.get("blocker", "") if target == "blocked" else "")
        shot["updated_at"] = now()
        registry["updated_at"] = now()
        atomic_write(registry_path(project_root), registry)
        print(json.dumps({"shot_id": args.shot_id, "previous_status": current, "status": target, "registry": str(registry_path(project_root))}, ensure_ascii=False, indent=2))
        return 0
    if args.command == "audit":
        print(json.dumps(audit(registry, project_root), ensure_ascii=False, indent=2))
        return 0
    if args.command == "next-batch":
        if args.from_status not in STATUSES:
            raise ValueError(f"Unsupported --from-status: {args.from_status}")
        batch = next_batch(registry, args.from_status, args.limit)
        print(json.dumps({"from_status": args.from_status, "count": len(batch), "shots": batch}, ensure_ascii=False, indent=2))
        return 0
    counts = {status: 0 for status in STATUSES}
    for shot in registry.get("shots", []):
        counts[shot.get("status", "planned")] = counts.get(shot.get("status", "planned"), 0) + 1
    print(json.dumps({"shot_count": len(registry.get("shots", [])), "status_counts": counts, "next_prompt_batch": next_batch(registry, "continuity_locked", 4), "next_image_batch": next_batch(registry, "prompt_ready", 4)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=os.sys.stderr)
        raise SystemExit(1)
