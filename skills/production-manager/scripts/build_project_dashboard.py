from __future__ import annotations

import argparse
import html
import json
import os
import runpy
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


OCCUPIED = {"active", "waiting_user", "blocked", "ready_for_review"}
THREAD_STATUSES = {"queued", "active", "waiting_user", "blocked", "ready_for_review", "accepted", "stale", "archived"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a read-only summary or static project production dashboard.")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args()


def load_json(path: Path, default):
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    rows: list[dict] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL {path}:{line_number}: {exc}") from exc
    return rows


def inside(root: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def manifest_value(manifest: dict, snake: str, camel: str, default=None):
    return manifest.get(snake, manifest.get(camel, default))


def summarize(project_root: Path) -> dict:
    root = project_root.resolve()
    manifest_path = root / "project-manifest.json"
    asset_index_path = root / "asset-index.json"
    manifest = load_json(manifest_path, {})
    asset_index = load_json(asset_index_path, {"assets": []})
    current = manifest.get("current", {})
    workflow = manifest.get("workflow", {})
    registry_pointer = (
        current.get("thread_registry")
        or current.get("threadRegistry")
        or workflow.get("thread_orchestration", {}).get("registry")
        or ""
    )
    warnings: list[str] = []
    registry = {}
    registry_path = root / registry_pointer if registry_pointer else None
    if registry_path:
        if not inside(root, registry_path):
            warnings.append("线程注册表路径越出项目根目录")
        elif registry_path.is_file():
            registry = load_json(registry_path, {})
        else:
            warnings.append("项目清单声明了线程注册表，但文件不存在")

    tasks = registry.get("tasks", [])
    thread_status = Counter(task.get("status", "unknown") for task in tasks)
    invalid_status = sorted(status for status in thread_status if status not in THREAD_STATUSES)
    if invalid_status:
        warnings.append(f"存在非法线程状态：{', '.join(invalid_status)}")
    occupied = sum(thread_status.get(status, 0) for status in OCCUPIED)
    max_active = int(registry.get("max_active") or workflow.get("thread_orchestration", {}).get("max_active") or 4)
    if occupied > max_active:
        warnings.append(f"活动任务 {occupied} 超过并发上限 {max_active}")

    assets = asset_index.get("assets", []) if isinstance(asset_index.get("assets", []), list) else []
    asset_states = Counter(asset.get("asset_state", asset.get("assetState", "未标注")) for asset in assets)
    asset_types = Counter(asset.get("type", "unknown") for asset in assets)
    generation_runs = manifest.get("generation_runs", manifest.get("generationRuns", [])) or []
    video_runs = manifest.get("video_runs", manifest.get("videoRuns", [])) or []
    all_runs = [*generation_runs, *video_runs]
    failed_runs = [run for run in all_runs if str(run.get("status", "")).lower() in {"failed", "失败", "部分失败", "partial"} or run.get("failedCount", run.get("failed_count", 0))]

    observations_path = root / "revision-logs" / "generation-observations.jsonl"
    feedback_path = root / "revision-logs" / "generation-feedback-summary.json"
    ledger_path = root / "revision-logs" / "generation-run-ledger.jsonl"
    shot_registry_path = root / "production" / "shot-production-registry.json"
    observations = load_jsonl(observations_path)
    feedback = load_json(feedback_path, {})
    ledger = load_jsonl(ledger_path)
    shot_registry = load_json(shot_registry_path, {"shots": []})
    shots = shot_registry.get("shots", []) if isinstance(shot_registry.get("shots", []), list) else []
    shot_status = Counter(shot.get("status", "unknown") for shot in shots)
    shot_classes = Counter(shot.get("approval_class", "unknown") for shot in shots)
    shot_helpers = runpy.run_path(str(Path(__file__).resolve().parents[2] / "project-state-manager" / "scripts" / "manage-shot-production.py"))
    shot_audit = shot_helpers["audit"](shot_registry, root)
    warnings.extend(shot_audit["errors"])
    ready_images = shot_helpers["next_batch"](shot_registry, "prompt_ready", 4) if shot_audit["valid"] else []
    latest_ledger_by_key: dict[str, dict] = {}
    for event in ledger:
        if event.get("idempotency_key"):
            latest_ledger_by_key[event["idempotency_key"]] = event
    ledger_status = Counter(event.get("status", "unknown") for event in latest_ledger_by_key.values())

    total_elapsed = sum(float(event.get("metrics", {}).get("elapsed_seconds") or 0) for event in latest_ledger_by_key.values())
    total_credits = sum(float(event.get("metrics", {}).get("credits_used") or 0) for event in latest_ledger_by_key.values())
    total_cost = sum(float(event.get("metrics", {}).get("estimated_cost") or 0) for event in latest_ledger_by_key.values())

    next_actions: list[str] = []
    if thread_status.get("blocked"):
        next_actions.append(f"处理 {thread_status['blocked']} 个阻塞分任务")
    if thread_status.get("waiting_user"):
        next_actions.append(f"确认 {thread_status['waiting_user']} 个等待用户输入的分任务")
    if thread_status.get("ready_for_review"):
        next_actions.append(f"审核并验收 {thread_status['ready_for_review']} 个待审分任务")
    if thread_status.get("stale"):
        next_actions.append(f"根据最新全局设定刷新 {thread_status['stale']} 个过期结果")
    if failed_runs or ledger_status.get("partial") or ledger_status.get("failed"):
        next_actions.append("仅恢复失败生成项，保留成功结果并检查积分/幂等状态")
    proposals = feedback.get("promotion_proposals", [])
    if shot_status.get("blocked"):
        next_actions.append(f"处理 {shot_status['blocked']} 个被阻塞镜头，保留已通过镜头")
    if shot_status.get("stale"):
        next_actions.append(f"复核 {shot_status['stale']} 个受上游修改影响的镜头，旧文件保留待比对")
    if shot_status.get("continuity_locked"):
        next_actions.append(f"优先完成 {shot_status['continuity_locked']} 个已锁连续性的镜头提示词")
    if ready_images:
        next_actions.append("下一批具备参考条件的出图镜头：" + "、".join(shot["shot_id"] for shot in ready_images))
    elif shot_status.get("prompt_ready"):
        next_actions.append("待出图镜头仍有依赖或状态问题，先完成对应参考和检查")
    if proposals:
        next_actions.append(f"人工审核 {len(proposals)} 条基于重复证据的规则升级建议")
    if not next_actions:
        next_actions.append("继续执行当前已批准任务；生成后记录QC观察和运行指标")

    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "read_only_summary": True,
        "project": {
            "name": manifest_value(manifest, "project_name", "projectName", manifest.get("project", root.name)),
            "root": str(root),
            "manifest": str(manifest_path),
            "asset_index": str(asset_index_path),
            "thread_registry": str(registry_path) if registry_path else "",
            "context_version": registry.get("context", {}).get("version"),
        },
        "threads": {
            "total": len(tasks),
            "status_counts": dict(sorted(thread_status.items())),
            "occupied": occupied,
            "max_active": max_active,
            "tasks": [
                {
                    "task_id": task.get("task_id", ""),
                    "title": task.get("title", ""),
                    "owning_skill": task.get("owning_skill", ""),
                    "status": task.get("status", ""),
                    "dependencies": task.get("dependencies", []),
                    "context_version": task.get("context_version"),
                    "handoff_summary": task.get("handoff_summary", ""),
                    "stale_reason": task.get("stale_reason"),
                }
                for task in tasks
            ],
        },
        "assets": {"total": len(assets), "state_counts": dict(sorted(asset_states.items())), "type_counts": dict(sorted(asset_types.items()))},
        "runs": {
            "image_runs": len(generation_runs),
            "video_runs": len(video_runs),
            "failed_or_partial": len(failed_runs),
            "ledger_status_counts": dict(sorted(ledger_status.items())),
            "elapsed_seconds": round(total_elapsed, 3),
            "credits_used": round(total_credits, 4),
            "estimated_cost": round(total_cost, 4),
        },
        "feedback": {
            "observation_count": len(observations),
            "promotion_proposal_count": len(proposals),
            "summary_path": str(feedback_path) if feedback_path.is_file() else "",
        },
        "shots": {
            "total": len(shots),
            "registry": str(shot_registry_path) if shot_registry_path.is_file() else "",
            "status_counts": dict(sorted(shot_status.items())),
            "approval_class_counts": dict(sorted(shot_classes.items())),
            "next_image_batch": [shot["shot_id"] for shot in ready_images],
            "items": [{key: shot.get(key, "") for key in ["shot_id", "ratio", "camera_id", "camera_reference_shot_id", "status", "stale_reason"]} for shot in shots],
        },
        "warnings": warnings,
        "next_actions": next_actions[:5],
    }


def rows(mapping: dict) -> str:
    return "".join(f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(str(value))}</td></tr>" for key, value in mapping.items()) or "<tr><td colspan='2'>暂无</td></tr>"


def render_html(data: dict) -> str:
    shot_rows = "".join("<tr>" + "".join(f"<td>{html.escape(str(shot[key]))}</td>" for key in
        ["shot_id", "ratio", "camera_id", "camera_reference_shot_id", "status", "stale_reason"]) + "</tr>"
        for shot in data["shots"].get("items", [])) or "<tr><td colspan='6'>暂无登记镜头</td></tr>"
    task_rows = "".join(
        "<tr>"
        f"<td>{html.escape(str(task['task_id']))}</td>"
        f"<td>{html.escape(str(task['title']))}</td>"
        f"<td>{html.escape(str(task['owning_skill']))}</td>"
        f"<td><span class='status'>{html.escape(str(task['status']))}</span></td>"
        f"<td>{html.escape(str(task['handoff_summary'] or task['stale_reason'] or ''))}</td>"
        "</tr>"
        for task in data["threads"]["tasks"]
    ) or "<tr><td colspan='5'>没有注册分任务</td></tr>"
    actions = "".join(f"<li>{html.escape(action)}</li>" for action in data["next_actions"])
    warnings = "".join(f"<li>{html.escape(item)}</li>" for item in data["warnings"]) or "<li>无结构警告</li>"
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(str(data['project']['name']))} · 制作控制台</title>
<style>
body{{font-family:Segoe UI,Microsoft YaHei,sans-serif;background:#0b1020;color:#e8edf7;margin:0;padding:24px}}main{{max-width:1280px;margin:auto}}h1{{margin:0 0 6px}}.muted{{color:#9eabc4}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:20px 0}}.card{{background:#141b30;border:1px solid #26304a;border-radius:12px;padding:16px}}.value{{font-size:28px;font-weight:700}}table{{width:100%;border-collapse:collapse;background:#141b30}}th,td{{padding:10px;border-bottom:1px solid #26304a;text-align:left;vertical-align:top}}th{{color:#a9b8d4}}.status{{padding:3px 8px;border-radius:999px;background:#253455}}section{{margin:24px 0}}li{{margin:7px 0}}code{{color:#9ed0ff}}</style></head>
<body><main><h1>{html.escape(str(data['project']['name']))}</h1><div class="muted">生成时间：{html.escape(data['generated_at'])}<br>项目根：<code>{html.escape(data['project']['root'])}</code></div>
<div class="grid">
<div class="card"><div class="muted">分任务</div><div class="value">{data['threads']['total']}</div><div>{data['threads']['occupied']} / {data['threads']['max_active']} 占用并发</div></div>
<div class="card"><div class="muted">资产</div><div class="value">{data['assets']['total']}</div><div>图像/视频/提示词统一追踪</div></div>
<div class="card"><div class="muted">生成运行</div><div class="value">{data['runs']['image_runs'] + data['runs']['video_runs']}</div><div>{data['runs']['failed_or_partial']} 个失败或部分失败</div></div>
<div class="card"><div class="muted">反馈证据</div><div class="value">{data['feedback']['observation_count']}</div><div>{data['feedback']['promotion_proposal_count']} 条待确认升级建议</div></div>
<div class="card"><div class="muted">镜头生产状态</div><div class="value">{data['shots']['total']}</div><div>连续性、首帧、视频与QC串联</div></div>
</div>
<section><h2>分任务状态</h2><table><thead><tr><th>ID</th><th>任务</th><th>负责人</th><th>状态</th><th>交接/原因</th></tr></thead><tbody>{task_rows}</tbody></table></section>
<section class="grid"><div class="card"><h2>任务状态统计</h2><table>{rows(data['threads']['status_counts'])}</table></div><div class="card"><h2>资产状态统计</h2><table>{rows(data['assets']['state_counts'])}</table></div><div class="card"><h2>镜头状态</h2><table>{rows(data['shots']['status_counts'])}</table></div><div class="card"><h2>运行账本</h2><table>{rows(data['runs']['ledger_status_counts'])}</table></div></section>
<section><h2>镜头画幅与参考关系</h2><table><thead><tr><th>镜头</th><th>画幅</th><th>机位</th><th>参考镜头</th><th>状态</th><th>待复核原因</th></tr></thead><tbody>{shot_rows}</tbody></table></section>
<section class="grid"><div class="card"><h2>下一步</h2><ol>{actions}</ol></div><div class="card"><h2>结构警告</h2><ul>{warnings}</ul></div></section>
</main></body></html>"""


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(content, encoding="utf-8")
    os.replace(temp, path)


def main() -> int:
    args = parse_args()
    data = summarize(args.project_root)
    if args.check_only:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    output_dir = (args.output_dir or args.project_root / "00_project_control" / "dashboard").resolve()
    json_path = output_dir / "project-dashboard.json"
    html_path = output_dir / "project-dashboard.html"
    atomic_write(json_path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    atomic_write(html_path, render_html(data))
    print(json.dumps({"project_root": str(args.project_root.resolve()), "dashboard_json": str(json_path), "dashboard_html": str(html_path), "warnings": data["warnings"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"PROJECT DASHBOARD: FAIL\n- {exc}", file=sys.stderr)
        sys.exit(1)
