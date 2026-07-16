#!/usr/bin/env python3
"""Create a safe simple folder plan for loose AI project files.

Default mode is dry-run. Use --apply only after user approval.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}
VIDEO_EXT = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
DOC_EXT = {".doc", ".docx", ".pdf", ".ppt", ".pptx", ".xls", ".xlsx", ".csv", ".md", ".txt"}
ARCHIVE_EXT = {".zip", ".rar", ".7z"}

DEFAULT_DIRS = [
    "00_inbox",
    "docs",
    "images",
    "videos",
    "prompts",
    "references",
    "review",
    "delivery",
    "archive",
]

SKIP_DIR_NAMES = {
    ".git",
    "skills",
    "projects",
    "outputs",
    "sync-logs",
    "handoff",
    "node_modules",
    "__pycache__",
}

WORKSPACE_ROOT_FILE_NAMES = {
    ".gitignore",
    ".gitattributes",
    "README.md",
    "WORKFLOW.md",
}


def norm_text(value: str) -> str:
    return value.lower().replace(" ", "_").replace("-", "_")


def contains_any(text: str, patterns: list[str]) -> bool:
    return any(pattern in text for pattern in patterns)


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def classify_file(path: Path) -> str:
    full = norm_text(path.name)
    ext = path.suffix.lower()

    if contains_any(full, ["prompt", "提示词", "_input", "run_manifest", "generation_job", "generation_ready"]):
        return "prompts"

    if contains_any(full, ["delivery", "deliver", "交付"]):
        return "delivery"

    if ext in ARCHIVE_EXT:
        return "references"

    if ext in IMAGE_EXT:
        return "images"

    if ext in VIDEO_EXT:
        return "videos"

    if ext in DOC_EXT:
        return "docs"

    if ext == ".json":
        return "prompts" if contains_any(full, ["banana", "midjourney", "mj", "imagegen", "seedance", "kling", "jimeng", "openai"]) else "docs"

    return "00_inbox"


def is_workspace_root(source_dir: Path) -> bool:
    return (source_dir / ".git").exists() or ((source_dir / "skills").exists() and (source_dir / "projects").exists())


def iter_candidate_files(source_dir: Path, project_root: Path, recursive: bool) -> list[Path]:
    iterator = source_dir.rglob("*") if recursive else source_dir.iterdir()
    files: list[Path] = []
    protect_workspace_files = is_workspace_root(source_dir)
    for item in iterator:
        if item.is_dir():
            continue
        if protect_workspace_files and item.parent.resolve() == source_dir.resolve() and item.name in WORKSPACE_ROOT_FILE_NAMES:
            continue
        if is_relative_to(item, project_root):
            continue
        if any(part in SKIP_DIR_NAMES for part in item.parts):
            continue
        files.append(item)
    return sorted(files, key=lambda p: str(p).lower())


def unique_target(path: Path, reserved: set[Path]) -> Path:
    candidate = path
    index = 1
    while candidate.exists() or candidate in reserved:
        candidate = path.with_name(f"{path.stem}_dup{index:02d}{path.suffix}")
        index += 1
    reserved.add(candidate)
    return candidate


def build_plan(source_dir: Path, project_root: Path, recursive: bool) -> dict:
    source_dir = source_dir.resolve()
    project_root = project_root.resolve()
    reserved: set[Path] = set()
    moves = []

    for file_path in iter_candidate_files(source_dir, project_root, recursive):
        rel_target_dir = classify_file(file_path)
        target_dir = project_root / rel_target_dir
        target_path = unique_target(target_dir / file_path.name, reserved)
        moves.append(
            {
                "source": str(file_path),
                "target": str(target_path),
                "targetFolder": rel_target_dir,
                "reason": f"classified as {rel_target_dir}",
            }
        )

    return {
        "projectRoot": str(project_root),
        "sourceDir": str(source_dir),
        "recursive": recursive,
        "defaultDirs": [str(project_root / d) for d in DEFAULT_DIRS],
        "moveCount": len(moves),
        "moves": moves,
        "safety": {
            "dryRunDefault": True,
            "deleteFiles": False,
            "overwriteFiles": False,
            "requiresUserApprovalBeforeApply": True,
        },
    }


def apply_plan(plan: dict) -> None:
    for directory in plan["defaultDirs"]:
        Path(directory).mkdir(parents=True, exist_ok=True)
    for move in plan["moves"]:
        source = Path(move["source"])
        target = Path(move["target"])
        target.parent.mkdir(parents=True, exist_ok=True)
        if not source.exists():
            move["status"] = "skipped_source_missing"
            continue
        if target.exists():
            move["status"] = "skipped_target_exists"
            continue
        shutil.move(str(source), str(target))
        move["status"] = "moved"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan or apply simple project folder organization.")
    parser.add_argument("--source-dir", required=True, help="Folder containing loose files.")
    parser.add_argument("--project-root", required=True, help="Target clean project root.")
    parser.add_argument("--recursive", action="store_true", help="Scan source folder recursively.")
    parser.add_argument("--apply", action="store_true", help="Create folders and move files. Default is dry-run.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dir = Path(args.source_dir)
    project_root = Path(args.project_root)
    if not source_dir.exists() or not source_dir.is_dir():
        raise SystemExit(f"source-dir does not exist or is not a directory: {source_dir}")

    plan = build_plan(source_dir, project_root, args.recursive)
    plan["dryRun"] = not args.apply

    if args.apply:
        apply_plan(plan)

    print(json.dumps(plan, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
