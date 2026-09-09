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

from PIL import Image


SKILLS_ROOT = Path(__file__).resolve().parents[2]
STATE_SCRIPT = SKILLS_ROOT / "project-state-manager" / "scripts" / "manage-project-state.mjs"
IMAGE_CONTROLLER = SKILLS_ROOT / "image-generation-controller" / "scripts" / "run-image-generation.mjs"
BANANA_GENERATOR = SKILLS_ROOT / "banana-image-generator" / "scripts" / "generate-banana-images.mjs"
VIDEO_CONTROLLER = SKILLS_ROOT / "video-generation-controller" / "scripts" / "run-video-generation.mjs"
DREAMINA_RUNNER = SKILLS_ROOT / "dreamina-cli" / "scripts" / "dreamina_runner.mjs"
SHOT_REGISTRY = SKILLS_ROOT / "project-state-manager" / "scripts" / "manage-shot-production.py"
KV_RENDITION = SKILLS_ROOT / "kv-director" / "scripts" / "build_kv_rendition_matrix.py"
IMAGE_TECHNICAL_QC = SKILLS_ROOT / "image-qc-director" / "scripts" / "technical_image_qc.py"
VIDEO_TECHNICAL_QC = SKILLS_ROOT / "video-qc-director" / "scripts" / "technical_video_qc.py"
SEEDANCE_25_AUDIT = SKILLS_ROOT / "prompt-platform-auditor" / "scripts" / "audit_seedance_25_packet.py"
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


def run_execution_extension_e2e(root: Path, project_root: Path, node: str, image_job: Path, prompt_path: Path) -> dict:
    direct_banana_dir = root / "banana-direct-dry-run"
    banana = run([
        node, str(BANANA_GENERATOR), "--input", str(image_job),
        "--project-root", str(project_root), "--output-dir", str(direct_banana_dir), "--dry-run",
    ])
    if banana.get("status") != "dry-run" or len(banana.get("shots", [])) != 2 or not banana.get("idempotencyKey"):
        raise AssertionError("Direct Banana dry-run did not preserve shots and idempotency metadata.")
    run([
        node, str(BANANA_GENERATOR), "--input", str(image_job),
        "--project-root", str(project_root), "--output-dir", str(root / "banana-paid-block"),
    ], expect=1)

    shot_input = root / "shots.json"
    write_json(shot_input, {"shots": [
        {"shot_id": "S10", "order": 10, "status": "continuity_locked", "approval_class": "coverage", "risk_level": "low"},
        {"shot_id": "S08", "order": 8, "status": "continuity_locked", "approval_class": "anchor", "risk_level": "high"},
        {"shot_id": "S09", "order": 9, "status": "continuity_locked", "approval_class": "hero", "risk_level": "medium", "previous_shot_id": "S08", "continuity_in": {"inherits_from": "S08"}},
    ]})
    run([sys.executable, str(SHOT_REGISTRY), "init", "--project-root", str(project_root)])
    run([sys.executable, str(SHOT_REGISTRY), "upsert", "--project-root", str(project_root), "--input", str(shot_input)])
    shot_batch = run([sys.executable, str(SHOT_REGISTRY), "next-batch", "--project-root", str(project_root), "--from-status", "continuity_locked", "--limit", "3"])
    if [shot["shot_id"] for shot in shot_batch.get("shots", [])] != ["S08", "S09", "S10"]:
        raise AssertionError("Shot scheduler did not prioritize anchor/hero before coverage.")
    run([sys.executable, str(SHOT_REGISTRY), "transition", "--project-root", str(project_root), "--shot-id", "S08", "--status", "video_submitted"], expect=1)
    shot_audit = run([sys.executable, str(SHOT_REGISTRY), "audit", "--project-root", str(project_root)])
    if shot_audit.get("valid") is not True:
        raise AssertionError(f"Shot production registry audit failed: {shot_audit}")

    master_image = root / "kv-master.png"
    Image.new("RGB", (1600, 900), (42, 56, 76)).save(master_image)
    image_qc = run([sys.executable, str(IMAGE_TECHNICAL_QC), "--image", str(master_image), "--output-dir", str(root / "image-qc")])
    if image_qc.get("image_count") != 1 or not Path(image_qc["contact_sheet"]).is_file():
        raise AssertionError("Technical image QC did not create evidence and contact sheet.")

    kv_plan = json.loads((SKILLS_ROOT / "kv-director" / "templates" / "kv-rendition-plan-template.json").read_text(encoding="utf-8"))
    kv_plan["master_image"] = str(master_image)
    kv_input = root / "kv-plan.json"
    write_json(kv_input, kv_plan)
    kv_check_dir = root / "kv-check-only-must-not-exist"
    kv_check = run([sys.executable, str(KV_RENDITION), "--input", str(kv_input), "--output-dir", str(kv_check_dir), "--check-only"])
    if kv_check_dir.exists() or kv_check.get("check_only") is not True:
        raise AssertionError("KV --check-only wrote files or did not report check-only mode.")
    kv_output = root / "kv-renditions"
    kv_result = run([sys.executable, str(KV_RENDITION), "--input", str(kv_input), "--output-dir", str(kv_output)])
    kv_matrix = json.loads(Path(kv_result["matrix"]).read_text(encoding="utf-8"))
    if len(kv_matrix.get("renditions", [])) != 4 or len(list(kv_output.glob("*_safe-area.svg"))) != 4:
        raise AssertionError("KV rendition matrix did not create all four safe-area variants.")

    seedance_packet = root / "seedance-2.5-valid.json"
    write_json(seedance_packet, {
        "model_target": "seedance_2_5",
        "platform_target": "jimeng",
        "task_mode": "reference_to_video",
        "duration": 30,
        "music_policy": "no_music_allow_sfx",
        "references": [
            {"id": "@图片1", "kind": "image", "entity": "人物A", "use": "五官、发型和服装", "do_not_use": "背景", "width": 1080, "height": 1920},
            {"id": "@视频1", "kind": "video", "entity": "人物A", "use": "动作路径和节奏", "do_not_use": "人物身份和场景", "duration_seconds": 10},
            {"id": "@音频1", "kind": "audio", "entity": "人物A", "use": "音色和指定台词", "do_not_use": "画面身份", "duration_seconds": 5},
        ],
        "stages": [
            {"label": "阶段一", "time_range": "0-10秒", "start_state": "人物在门外", "main_change": "人物推门进入", "ending_state": "人物站在门内"},
            {"label": "阶段二", "time_range": "10-20秒", "start_state": "承接门内站位", "main_change": "人物取出盒子", "ending_state": "盒子位于桌面中央"},
            {"label": "阶段三", "time_range": "20-30秒", "start_state": "盒子位于桌面中央", "main_change": "人物打开盒子", "ending_state": "镜头稳定在盒内物品"},
        ],
    })
    seedance_valid = run([sys.executable, str(SEEDANCE_25_AUDIT), "--input", str(seedance_packet)])
    if seedance_valid.get("valid") is not True or seedance_valid.get("reference_total") != 3:
        raise AssertionError(f"Valid Seedance 2.5 packet did not pass: {seedance_valid}")
    seedance_invalid_packet = root / "seedance-2.5-invalid-edit.json"
    write_json(seedance_invalid_packet, {
        "model_target": "seedance_2_5",
        "platform_target": "jimeng",
        "task_mode": "video_edit",
        "music_policy": "no_music_allow_sfx",
        "edit_master": "@视频1",
        "edit_scope": "4-7秒右侧墙面",
        "must_preserve": ["人物、动作、构图、镜头和声音"],
        "parameter_overrides": {"ratio": "9:16", "duration": 12},
        "references": [{"id": "@视频1", "kind": "video", "entity": "唯一母版", "use": "原始画面和时间线", "duration_seconds": 10}],
    })
    seedance_invalid = run([sys.executable, str(SEEDANCE_25_AUDIT), "--input", str(seedance_invalid_packet)], expect=1)
    if seedance_invalid.get("valid") is not False or not {"task_mode_forbids_ratio_override", "video_edit_forbids_duration_override"}.issubset(set(seedance_invalid.get("errors", []))):
        raise AssertionError("Seedance 2.5 locked-parameter audit did not reject edit overrides.")

    fake_cli = root / "fake-dreamina.mjs"
    fake_cli.write_text(
        "import fs from 'node:fs';\n"
        "import path from 'node:path';\n"
        "const a=process.argv.slice(2), c=a[0]||'';\n"
        "const val=n=>{const p=a.find(x=>x.startsWith('--'+n+'='));return p?p.slice(n.length+3):''};\n"
        "if(c==='-h'){console.log('user_credit image2video query_result');}\n"
        "else if(a.includes('-h')){console.log('--prompt --negative_prompt --image --duration --ratio --resolution --poll --download_dir --submit_id');}\n"
        "else if(c==='user_credit'){console.log(JSON.stringify({available_credits:100}));}\n"
        "else if(c==='image2video'){console.log(JSON.stringify({submit_id:'fake-task-001',gen_status:'querying'}));}\n"
        "else if(c==='query_result'){const d=val('download_dir');fs.mkdirSync(d,{recursive:true});const f=path.join(d,'fake-result.mp4');fs.writeFileSync(f,'fixture');console.log(JSON.stringify({submit_id:'fake-task-001',gen_status:'success',output_paths:[f]}));}\n"
        "else{process.exitCode=2;}\n",
        encoding="utf-8",
    )
    live_command = [
        node, str(VIDEO_CONTROLLER), "--provider", "jimeng-cli", "--project-root", str(project_root),
        "--shot", "S11", "--prompt-file", str(prompt_path), "--image-file", str(master_image),
        "--duration", "5", "--ratio", "16:9", "--generation-confirmation", "approved",
        "--dreamina-cli-script", str(fake_cli),
    ]
    submitted = run(live_command)
    if submitted.get("dreamina", {}).get("gen_status") != "querying" or submitted.get("ledgerEvent", {}).get("status") != "submitted":
        raise AssertionError("Dreamina adapter did not persist the submitted/querying state.")
    recovered = run(live_command + ["--submit-id", "fake-task-001", "--idempotency-key", submitted["idempotencyKey"]])
    if recovered.get("recovered") is not True or recovered.get("dreamina", {}).get("gen_status") != "success" or not Path(recovered["video"]).is_file():
        raise AssertionError("Dreamina recovery did not reuse submit_id and validate the downloaded output path.")

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise AssertionError("ffmpeg is required for the technical video QC E2E test.")
    test_video = root / "technical-qc-fixture.mp4"
    run([
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", "color=c=black:s=640x360:d=1",
        "-f", "lavfi", "-i", "sine=frequency=800:duration=1",
        "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(test_video),
    ])
    video_qc = run([sys.executable, str(VIDEO_TECHNICAL_QC), "--video", str(test_video), "--output-dir", str(root / "video-qc"), "--samples", "4"])
    video_report = json.loads(Path(video_qc["report"]).read_text(encoding="utf-8"))
    if video_report.get("audio_track_present") is not True or video_report.get("music_vs_sfx_semantic_review_required") is not True:
        raise AssertionError("Technical video QC did not preserve music-vs-SFX as a semantic review decision.")

    return {
        "banana_paid_preflight_blocked": True,
        "shot_order": [shot["shot_id"] for shot in shot_batch["shots"]],
        "image_qc": True,
        "video_qc": True,
        "kv_renditions": len(kv_matrix["renditions"]),
        "seedance_25_prompt_audit": True,
        "dreamina_submit_recover": True,
    }


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

    execution_extensions = run_execution_extension_e2e(root, project_root, node, image_job, prompt_path)

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
        "execution_extensions": execution_extensions,
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
