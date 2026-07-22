from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SKILLS_ROOT = Path(__file__).resolve().parents[2]
STATE_SCRIPT = SKILLS_ROOT / "project-state-manager" / "scripts" / "manage-project-state.mjs"
IMAGE_CONTROLLER = SKILLS_ROOT / "image-generation-controller" / "scripts" / "run-image-generation.mjs"
VIDEO_CONTROLLER = SKILLS_ROOT / "video-generation-controller" / "scripts" / "run-video-generation.mjs"
DASHBOARD_SCRIPT = SKILLS_ROOT / "production-manager" / "scripts" / "build_project_dashboard.py"
CAPABILITY_AUDIT = SKILLS_ROOT / "zongkong" / "scripts" / "audit_skill_capabilities.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run non-destructive film-agent end-to-end workflow tests.")
    parser.add_argument("--compat-project-root", type=Path)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--node", type=Path, help="Node.js executable when node is not on PATH.")
    return parser.parse_args()


def run(command: list[str], cwd: Path | None = None, expect: int = 0) -> dict:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=False,
        env=env,
    )
    if result.returncode != expect:
        raise AssertionError(
            f"Command failed ({result.returncode}, expected {expect}): {' '.join(command)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    text = result.stdout.strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"Command returned non-JSON output: {' '.join(command)}\n{text}") from exc


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def hash_files(paths: list[Path]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in paths:
        if path.is_file():
            hashes[str(path.resolve())] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def approve_short_drama_gate(project_root: Path) -> None:
    write_json(project_root / "project-intake.json", {
        "project_intake_packet": {
            "project_tier": "formal",
            "main_line": "short_drama_story",
            "missing_fields": [],
        }
    })
    write_json(project_root / "style-lock.json", {
        "style_lock_packet": {
            "status": "approved",
            "style_id": "e2e_style_v1",
            "master_style_sentence": "restrained cinematic realism",
            "mother_library_application_packet": {"library_route": "film-prestige-visual-library"},
            "upstream_source": "e2e-fixture",
        }
    })
    (project_root / "references" / "scene-map.md").write_text("status: approved\n", encoding="utf-8")
    (project_root / "references" / "shot-audit.md").write_text("status: passed\n", encoding="utf-8")
    (project_root / "prompts" / "prompt-audit.md").write_text("status: 通过\n", encoding="utf-8")
    write_json(project_root / "generation-jobs" / "generation-ready.json", {
        "generation_ready_packet": {
            "target_tool": "banana",
            "deliverable_profile": "storyboard_frame",
            "final_prompt": "A restrained cinematic medium close-up.",
            "audit_status": "approved",
        }
    })


def run_temp_e2e(root: Path, node: str) -> dict:
    project_root = root / "agent-e2e-project"
    init = run([
        node, str(STATE_SCRIPT), "init",
        "--project-name", "Agent E2E",
        "--project-root", str(project_root),
        "--workflow", "short-drama",
        "--route", "storyboard-execution",
        "--project-tier", "formal",
    ])
    initial_check = run([node, str(STATE_SCRIPT), "check", "--project-root", str(project_root), "--stage", "generation"])
    if initial_check.get("ready") is not False:
        raise AssertionError("Fresh formal project unexpectedly passed the generation gate.")

    approve_short_drama_gate(project_root)
    ready_check = run([node, str(STATE_SCRIPT), "check", "--project-root", str(project_root), "--stage", "generation"])
    if ready_check.get("ready") is not True:
        raise AssertionError(f"Approved formal fixture did not pass: {ready_check}")

    image_job = project_root / "generation-jobs" / "e2e-image-job.json"
    write_json(image_job, {
        "projectName": "Agent E2E",
        "projectRoot": str(project_root),
        "tool": "banana",
        "mode": "dry-run",
        "promptMode": "quality",
        "deliverable_profile": "storyboard_frame",
        "shots": [
            {"shot": "S01", "prompt": "cinematic medium close-up, motivated window light", "negativePrompt": "plastic skin", "ratio": "16:9", "references": []},
            {"shot": "S02", "prompt": "cinematic close-up, restrained performance", "negativePrompt": "poster pose", "ratio": "16:9", "references": []},
        ],
    })
    image_result = run([node, str(IMAGE_CONTROLLER), "--job", str(image_job), "--dry-run"])
    if image_result.get("shotCount") != 2:
        raise AssertionError("Image dry-run did not preserve both fixture shots.")
    run([
        node, str(STATE_SCRIPT), "ingest",
        "--project-root", str(project_root),
        "--generation-log", image_result["generationLog"],
        "--review-board", image_result["reviewBoard"],
        "--generation-job", str(image_job),
    ])
    manifest = json.loads((project_root / "project-manifest.json").read_text(encoding="utf-8"))
    if len(manifest.get("generationRuns", [])) != 1:
        raise AssertionError("Repeated image ingest created a duplicate generation run.")

    asset_index = json.loads((project_root / "asset-index.json").read_text(encoding="utf-8"))
    asset_id = asset_index["assets"][0]["assetId"]
    for index, outcome in enumerate(["improved", "improved", "unchanged"], 1):
        observation_path = root / f"observation-{index}.json"
        write_json(observation_path, {
            "observation_id": f"obs_e2e_{index}",
            "asset_id": asset_id,
            "source_prompt": str(image_job),
            "platform": "banana",
            "model": "fixture-model",
            "deliverable_profile": "storyboard_frame",
            "qc_decision": "定向重出",
            "failure_type": "plastic_skin",
            "attempted_fix": "reduce beauty smoothing and preserve skin texture",
            "outcome": outcome,
            "metrics": {"elapsed_seconds": index, "credits_used": 0, "estimated_cost": 0},
        })
        run([node, str(STATE_SCRIPT), "record-observation", "--project-root", str(project_root), "--input", str(observation_path)])
    feedback = run([node, str(STATE_SCRIPT), "summarize-feedback", "--project-root", str(project_root), "--minimum-evidence", "3"])
    if feedback.get("observation_count") != 3 or len(feedback.get("promotion_proposals", [])) != 1:
        raise AssertionError("Feedback evidence did not produce exactly one human-confirmed promotion proposal.")

    prompt_path = project_root / "prompts" / "S03_video.txt"
    prompt_path.write_text("人物缓慢抬头，镜头轻微推近。不要背景音乐，允许同步环境声。", encoding="utf-8")
    roles_path = project_root / "prompts" / "S03_roles.json"
    write_json(roles_path, [{"reference": "S03_first_frame.png", "role": "first_frame"}])
    first_frame = project_root / "references" / "S03_first_frame.png"
    first_frame.write_bytes(b"fixture")
    video_command = [
        node, str(VIDEO_CONTROLLER), "--provider", "kling-omni",
        "--project-root", str(project_root), "--shot", "S03",
        "--prompt-file", str(prompt_path), "--image-file", str(first_frame),
        "--reference-roles", str(roles_path), "--task-type", "multi_shot_storyboard",
        "--duration", "10", "--ratio", "9:16",
    ]
    video_first = run(video_command)
    video_second = run(video_command)
    if not video_first.get("runManifest") or video_second.get("reused") is not True:
        raise AssertionError("Manual video handoff idempotency did not reuse the existing manifest.")

    dashboard_dir = root / "dashboard"
    dashboard = run([sys.executable, str(DASHBOARD_SCRIPT), "--project-root", str(project_root), "--output-dir", str(dashboard_dir)])
    if not Path(dashboard["dashboard_html"]).is_file() or not Path(dashboard["dashboard_json"]).is_file():
        raise AssertionError("Dashboard files were not created.")
    dashboard_data = json.loads(Path(dashboard["dashboard_json"]).read_text(encoding="utf-8"))
    if dashboard_data["feedback"]["observation_count"] != 3:
        raise AssertionError("Dashboard did not include feedback evidence.")

    audit = run([node, str(STATE_SCRIPT), "audit", "--project-root", str(project_root)])
    if audit.get("valid") is not True or audit.get("read_only") is not True:
        raise AssertionError(f"Temporary project audit failed: {audit}")

    capability = run([sys.executable, str(CAPABILITY_AUDIT)])
    if capability.get("valid") is not True:
        raise AssertionError(f"Capability audit failed: {capability}")

    return {
        "project_root": str(project_root),
        "initial_gate_blocked": True,
        "approved_gate_passed": True,
        "image_dry_run_shots": image_result.get("shotCount"),
        "image_ingest_idempotent": True,
        "feedback_observations": feedback.get("observation_count"),
        "promotion_proposals": len(feedback.get("promotion_proposals", [])),
        "video_handoff_reused": True,
        "dashboard_html": dashboard["dashboard_html"],
        "capabilities": capability.get("capability_count"),
    }


def run_compatibility_audit(project_root: Path, node: str) -> dict:
    paths = [
        project_root / "project-manifest.json",
        project_root / "asset-index.json",
        project_root / "00_project_control" / "thread-registry.json",
    ]
    before = hash_files(paths)
    audit = run([node, str(STATE_SCRIPT), "audit", "--project-root", str(project_root)])
    dashboard = run([sys.executable, str(DASHBOARD_SCRIPT), "--project-root", str(project_root), "--check-only"])
    after = hash_files(paths)
    if before != after:
        raise AssertionError("Compatibility audit modified protected project files.")
    if audit.get("valid") is not True:
        raise AssertionError(f"Compatibility project failed audit: {audit}")
    return {
        "project_root": str(project_root.resolve()),
        "files_unchanged": True,
        "task_count": audit.get("task_count"),
        "asset_count": audit.get("asset_count"),
        "dashboard_thread_total": dashboard.get("threads", {}).get("total"),
        "warnings": audit.get("warnings", []),
    }


def main() -> int:
    args = parse_args()
    node = str(args.node.resolve()) if args.node else shutil.which("node")
    if not node:
        raise AssertionError("Node.js is required for workflow E2E tests.")
    temp_root = Path(tempfile.mkdtemp(prefix="film-agent-e2e-"))
    try:
        result = {
            "status": "PASS",
            "temporary_e2e": run_temp_e2e(temp_root, node),
            "compatibility_audit": run_compatibility_audit(args.compat_project_root.resolve(), node) if args.compat_project_root else None,
            "temp_retained": bool(args.keep_temp),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    finally:
        if not args.keep_temp:
            shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssertionError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)
