from __future__ import annotations

import argparse
import json
import os
import tempfile
from fractions import Fraction
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
    invalidate = sub.add_parser("invalidate")
    invalidate.add_argument("--project-root", required=True, type=Path)
    invalidate.add_argument("--shot-id", required=True)
    invalidate.add_argument("--reason", required=True)
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
        "ratio": str(packet.get("ratio") or ""),
        "camera_id": str(packet.get("camera_id") or ""),
        "camera_reference_shot_id": str(packet.get("camera_reference_shot_id") or ""),
        "reference_roles": packet.get("reference_roles") or [],
        "source_evidence": packet.get("source_evidence") or [],
        "frame_selection": packet.get("frame_selection") or {},
        "continuity_in": packet.get("continuity_in") or {},
        "continuity_delta": packet.get("continuity_delta") or {},
        "continuity_out": packet.get("continuity_out") or {},
        "artifacts": artifacts,
        "platform_plan": packet.get("platform_plan") or {},
        "qc_decision": str(packet.get("qc_decision") or ""),
        "blocker": str(packet.get("blocker") or ""),
        "stale_reason": str(packet.get("stale_reason") or ""),
        "status_before_stale": str(packet.get("status_before_stale") or ""),
        "updated_at": now(),
    }


def reference_dependencies(shot: dict) -> set[str]:
    return {value for value in [shot.get("camera_reference_shot_id"),
            (shot.get("continuity_in") or {}).get("inherits_from")] if value}


def all_dependencies(shot: dict) -> set[str]:
    return set(shot.get("dependencies", [])) | reference_dependencies(shot)


def ratio_value(value: str) -> Fraction:
    parts = value.split(":")
    if len(parts) != 2 or not all(item.isdigit() and int(item) > 0 for item in parts):
        raise ValueError(f"Invalid ratio: {value!r}; use positive integers such as 16:9 or 9:16.")
    return Fraction(int(parts[0]), int(parts[1]))


def project_format(project_root: Path) -> dict:
    intake_path = project_root / "project-intake.json"
    if not intake_path.is_file():
        return {}
    intake = json.loads(intake_path.read_text(encoding="utf-8"))
    return (intake.get("project_intake_packet") or {}).get("format_spec") or {}


def invalidate_shots(registry: dict, shot_ids: set[str], reason: str) -> list[str]:
    known = {shot["shot_id"] for shot in registry.get("shots", [])}
    if not shot_ids <= known:
        raise ValueError(f"Unknown shots: {sorted(shot_ids - known)}")
    affected = set(shot_ids)
    while True:
        expanded = affected | {shot["shot_id"] for shot in registry["shots"]
                               if all_dependencies(shot) & affected}
        if expanded == affected:
            break
        affected = expanded
    for shot in registry["shots"]:
        if shot["shot_id"] in affected:
            if shot["status"] != "stale":
                shot["status_before_stale"] = shot["status"]
            shot.update(status="stale", stale_reason=reason, updated_at=now())
            # Retain old artifact paths for review; their status now forbids reuse.
            if shot.get("frame_selection"):
                shot["frame_selection"]["stale"] = True
    return sorted(affected)


def dependency_cycles(shots: list[dict]) -> list[list[str]]:
    graph = {shot["shot_id"]: sorted(all_dependencies(shot)) for shot in shots}
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
    fmt = project_format(project_root)
    allowed_ratios = {ratio_value(value) for value in
                      [fmt.get("master_ratio"), *fmt.get("delivery_ratios", [])] if value}
    if len(ids) != len(known):
        errors.append("duplicate_shot_id")
    for shot in shots:
        if shot.get("status") not in STATUSES:
            errors.append(f"{shot.get('shot_id')}:invalid_status")
        for dependency in all_dependencies(shot):
            if dependency not in known:
                errors.append(f"{shot.get('shot_id')}:missing_dependency:{dependency}")
        ratio = shot.get("ratio")
        if ratio:
            try:
                parsed = ratio_value(ratio)
                if allowed_ratios and parsed not in allowed_ratios:
                    errors.append(f"{shot['shot_id']}:ratio_not_in_project_format:{ratio}")
            except ValueError as error:
                errors.append(f"{shot['shot_id']}:{error}")
        elif fmt:
            errors.append(f"{shot['shot_id']}:missing_ratio")
        else:
            warnings.append(f"{shot['shot_id']}:legacy_ratio_unset")
        selection = shot.get("frame_selection") or {}
        candidates = selection.get("candidates", [])
        candidate_ids = [item.get("candidate_id") for item in candidates]
        if len(candidate_ids) != len(set(candidate_ids)) or any(not item for item in candidate_ids):
            errors.append(f"{shot['shot_id']}:invalid_candidate_ids")
        for candidate in candidates:
            if not candidate.get("path") or not is_inside(project_root, candidate["path"]):
                errors.append(f"{shot['shot_id']}:invalid_candidate_path")
        selected_id = selection.get("selected_candidate_id")
        winner = next((item for item in candidates if item.get("candidate_id") == selected_id), None)
        if selected_id and (not winner or winner.get("qc_decision") != "passed" or not winner.get("evidence")):
            errors.append(f"{shot['shot_id']}:selected_candidate_not_reviewed_pass")
        if selection and shot.get("status") in FLOW[4:]:
            if selection.get("stale") or not winner or not selection.get("reason"):
                errors.append(f"{shot['shot_id']}:frame_selection_missing_or_stale")
            elif winner.get("path") != (shot.get("artifacts") or {}).get("approved_first_frame"):
                errors.append(f"{shot['shot_id']}:selected_frame_artifact_mismatch")
            else:
                frame = project_root / winner["path"]
                if not frame.is_file() or frame.stat().st_size == 0:
                    errors.append(f"{shot['shot_id']}:selected_frame_missing")
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
    reference_ready = {shot["shot_id"] for shot in shots
                       if shot.get("status") in FLOW[4:] and
                       (shot.get("artifacts") or {}).get("approved_first_frame")}
    unusable = {shot["shot_id"] for shot in shots if shot.get("status") in {"blocked", "stale"}}
    ready = [
        shot for shot in shots
        if shot.get("status") == from_status
        and all(item in accepted for item in shot.get("dependencies", []))
        and not (reference_dependencies(shot) & unusable)
        and (from_status in {"planned", "continuity_locked"}
             or not shot.get("camera_reference_shot_id")
             or shot["camera_reference_shot_id"] in reference_ready)
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
        by_id = {shot["shot_id"]: shot for shot in registry.get("shots", [])}
        fmt = project_format(project_root)
        normalized = []
        changed = set()
        input_keys = {"ratio", "camera_id", "camera_reference_shot_id", "reference_roles", "source_evidence",
                      "dependencies", "continuity_in", "continuity_delta", "continuity_out", "narrative_function", "platform_plan"}
        for packet in packets:
            old = by_id.get(packet.get("shot_id"), {})
            if old and packet.get("status", old["status"]) != old["status"]:
                raise ValueError("Use transition to change an existing shot status.")
            merged = {**old, **packet}
            if not merged.get("ratio") and fmt.get("master_ratio"):
                merged["ratio"] = fmt["master_ratio"]
            shot = normalize_packet(project_root, merged)
            if old and any(old.get(key) != shot.get(key) for key in input_keys if key in packet):
                changed.add(shot["shot_id"])
            if old and "artifacts" in packet and any(
                (old.get("artifacts") or {}).get(key) != (shot.get("artifacts") or {}).get(key)
                for key in ["image_prompt", "approved_first_frame"] if key in packet["artifacts"]
            ):
                changed.add(shot["shot_id"])
            normalized.append(shot)
        for shot in normalized:
            by_id[shot["shot_id"]] = {**by_id.get(shot["shot_id"], {}), **shot}
        registry["shots"] = sorted(by_id.values(), key=lambda shot: (shot.get("episode_id", ""), shot.get("scene_id", ""), shot.get("order", 0), shot["shot_id"]))
        registry["updated_at"] = now()
        affected = invalidate_shots(registry, changed, "production_inputs_changed") if changed else []
        result = audit(registry, project_root)
        if not result["valid"]:
            raise ValueError("; ".join(result["errors"]))
        atomic_write(registry_path(project_root), registry)
        print(json.dumps({"registry": str(registry_path(project_root)), "upserted": [shot["shot_id"] for shot in normalized], "invalidated": affected, **result}, ensure_ascii=False, indent=2))
        return 0
    if args.command == "invalidate":
        affected = invalidate_shots(registry, {args.shot_id}, args.reason)
        registry["updated_at"] = now()
        atomic_write(registry_path(project_root), registry)
        print(json.dumps({"invalidated": affected, "artifacts_preserved": True}, ensure_ascii=False, indent=2))
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
            if current == "stale" and target not in FLOW[:3]:
                raise ValueError("Resume stale work at planned, continuity_locked or prompt_ready after reviewing affected inputs.")
        if target == "stale":
            affected = invalidate_shots(registry, {args.shot_id}, args.blocker or "upstream_revision")
        new_artifacts = parse_artifacts(args.artifact, project_root)
        old_artifacts = shot.get("artifacts") or {}
        replaced_input = any(old_artifacts.get(key) and old_artifacts[key] != value
                             for key, value in new_artifacts.items()
                             if key in {"image_prompt", "approved_first_frame"})
        if ("image_prompt" in new_artifacts and old_artifacts.get("image_prompt")
                and new_artifacts["image_prompt"] != old_artifacts["image_prompt"]
                and target in FLOW[3:]):
            raise ValueError("Invalidate the shot and review the revised prompt before retaining generated-image/video status.")
        if replaced_input:
            children = {item["shot_id"] for item in registry["shots"] if args.shot_id in all_dependencies(item)}
            if children:
                invalidate_shots(registry, children, f"reference_replaced:{args.shot_id}")
        shot["status"] = target
        shot["artifacts"] = {**old_artifacts, **new_artifacts}
        if args.qc_decision is not None:
            shot["qc_decision"] = args.qc_decision
        shot["blocker"] = args.blocker or (shot.get("blocker", "") if target == "blocked" else "")
        shot["updated_at"] = now()
        registry["updated_at"] = now()
        result = audit(registry, project_root)
        if not result["valid"]:
            raise ValueError("; ".join(result["errors"]))
        atomic_write(registry_path(project_root), registry)
        print(json.dumps({"shot_id": args.shot_id, "previous_status": current, "status": target, "registry": str(registry_path(project_root))}, ensure_ascii=False, indent=2))
        return 0
    if args.command == "audit":
        print(json.dumps(audit(registry, project_root), ensure_ascii=False, indent=2))
        return 0
    if args.command == "next-batch":
        if args.from_status not in STATUSES:
            raise ValueError(f"Unsupported --from-status: {args.from_status}")
        result = audit(registry, project_root)
        batch = next_batch(registry, args.from_status, args.limit) if result["valid"] else []
        print(json.dumps({"from_status": args.from_status, "count": len(batch), "shots": batch, **result}, ensure_ascii=False, indent=2))
        return 0
    counts = {status: 0 for status in STATUSES}
    for shot in registry.get("shots", []):
        counts[shot.get("status", "planned")] = counts.get(shot.get("status", "planned"), 0) + 1
    result = audit(registry, project_root)
    print(json.dumps({**result, "status_counts": counts,
                      "next_prompt_batch": next_batch(registry, "continuity_locked", 4) if result["valid"] else [],
                      "next_image_batch": next_batch(registry, "prompt_ready", 4) if result["valid"] else []}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=os.sys.stderr)
        raise SystemExit(1)
