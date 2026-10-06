"""Host-side Blender execution and frame-evidence tracking. Standard library only."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

BRIDGE = Path(__file__).with_name("blender_bridge.py")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def contained(root, target):
    root, target = Path(root).resolve(), Path(target).resolve()
    if not target.is_relative_to(root) or target == root:
        raise ValueError("Output must be inside the selected project root.")
    return target


def frames(value):
    result = set()
    for part in value.split(","):
        bits = part.strip().split(":")
        if len(bits) == 1:
            result.add(int(bits[0]))
        elif len(bits) == 2:
            start, end = map(int, bits)
            if end < start or end - start > 10000:
                raise ValueError("Invalid or excessive frame range.")
            result.update(range(start, end + 1))
        else:
            raise ValueError("Frames must be comma-separated integers or inclusive start:end ranges.")
    if not result or min(result) < 0 or len(result) > 10000:
        raise ValueError("Request 1 to 10000 nonnegative frames per run.")
    return sorted(result)


def discover(explicit=None):
    chosen = explicit or os.environ.get("BLENDER_EXECUTABLE")
    if chosen:
        candidate = Path(chosen).expanduser()
        if not candidate.is_file():
            raise ValueError("Configured Blender executable does not exist.")
        return str(candidate.resolve())
    found = shutil.which("blender")
    if found:
        return found
    candidates = []
    for key in ("ProgramFiles", "ProgramFiles(x86)"):
        if os.environ.get(key):
            candidates.extend(Path(os.environ[key]).glob("Blender Foundation/Blender*/blender.exe"))
    for candidate in (Path("/Applications/Blender.app/Contents/MacOS/Blender"),):
        if candidate.is_file():
            candidates.append(candidate)
    return str(sorted(candidates)[-1]) if candidates else None


def doctor(explicit=None):
    executable = discover(explicit)
    if not executable:
        return {"available": False, "reason": "Blender not found; supply --blender or BLENDER_EXECUTABLE."}
    result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=30)
    if result.returncode or not result.stdout.startswith("Blender "):
        raise RuntimeError("Executable did not return a Blender version.")
    return {"available": True, "executable": executable, "version": result.stdout.splitlines()[0]}


def invoke(executable, payload, blend=None, timeout=300, log_path=None):
    # Fresh process protects the user's open Blender session. Auto-run is disabled.
    with tempfile.TemporaryDirectory(prefix="blender-request-") as temp:
        request = Path(temp) / "request.json"
        report = Path(temp) / "report.json"
        save_json(request, {**payload, "report": str(report)})
        cmd = [executable, "--background", "--factory-startup", "--disable-autoexec"]
        if blend:
            cmd.append(str(Path(blend).resolve()))
        cmd.extend(["--python-exit-code", "1", "--python", str(BRIDGE), "--", str(request)])
        destination = Path(log_path) if log_path else Path(temp) / "blender.log"
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("wb") as log:
            result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=timeout)
        if result.returncode or not report.is_file():
            raise RuntimeError(f"Blender action failed; log: {destination}" if log_path else "Blender action failed; no verified result.")
        data = read_json(report)
        if data.get("ok") is not True:
            raise RuntimeError("Blender did not verify the action.")
        return data


def dependency_hashes(paths):
    files = set()
    for item in paths:
        p = Path(item).resolve()
        if not p.exists():
            raise ValueError(f"Missing dependency: {p}")
        if p.is_dir():
            files.update(x.resolve() for x in p.rglob("*") if x.is_file())
        else:
            files.add(p)
    if len(files) > 20000:
        raise ValueError("Dependency set exceeds 20000 files; partition the production run.")
    return {str(p): digest(p) for p in sorted(files)}


def fingerprint(scene, dependencies, settings, version):
    record = {"scene": digest(scene), "dependencies": dependency_hashes(dependencies),
              "settings": settings, "blender_version": version,
              "runner": digest(__file__), "bridge": digest(BRIDGE)}
    return hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()


def frame_valid(record, root):
    try:
        p = contained(root, record["file"])
        return (record.get("decoded") is True and p.is_file() and p.stat().st_size > 0
                and digest(p) == record["sha256"])
    except (KeyError, ValueError, OSError):
        return False


def status(output_dir):
    root = Path(output_dir).resolve()
    manifest = read_json(root / "render-manifest.json")
    valid = [f for f in manifest["frames"] if frame_valid(manifest.get("outputs", {}).get(str(f), {}), root)]
    complete = len(valid) == len(manifest["frames"]) and manifest.get("status") == "rendered"
    return {"status": "rendered" if complete else "incomplete", "verified_frames": valid,
            "missing_or_invalid_frames": sorted(set(manifest["frames"]) - set(valid)),
            "recorded_status": manifest.get("status"), "active_lock": (root / ".render.lock").exists(),
            "manifest": str(root / "render-manifest.json"), "visual_qc_status": "not_reviewed"}


@contextlib.contextmanager
def run_lock(root):
    lock = root / ".render.lock"
    try:
        descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
    except FileExistsError:
        raise ValueError("Render lock exists. Check its process before removing a stale lock.")
    try:
        with os.fdopen(descriptor, "w") as stream:
            json.dump({"pid": os.getpid(), "created_at": time.time()}, stream)
        yield
    finally:
        lock.unlink(missing_ok=True)


def build(args, environment):
    target = contained(args.project_root, args.output)
    if target.suffix.lower() != ".blend" or target.exists():
        raise ValueError("Build requires a new .blend output; preserve existing versions.")
    if not Path(args.script).is_file():
        raise ValueError("Task script does not exist.")
    if args.blend and not Path(args.blend).is_file():
        raise ValueError("Source .blend does not exist.")
    target.parent.mkdir(parents=True, exist_ok=True)
    invoke(environment["executable"], {"action": "build", "script": str(Path(args.script).resolve()),
           "output": str(target), "project_root": str(Path(args.project_root).resolve())}, args.blend,
           args.timeout, str(target) + ".build.log")
    inspection = invoke(environment["executable"], {"action": "inspect"}, target, args.timeout)
    save_json(str(target) + ".inspection.json", inspection)
    return {"status": "scene_saved", "blend": str(target), "reopened": True,
            "inspection": inspection, "visual_qc_status": "not_reviewed"}


def render(args, environment):
    root = contained(args.project_root, args.output_dir)
    source = Path(args.blend).resolve()
    if not source.is_file():
        raise ValueError("Source .blend does not exist.")
    requested = frames(args.frames)
    settings = {"frames": requested, "scene": args.scene, "engine": args.engine,
                "scale": args.scale, "format": args.format}
    inspection = invoke(environment["executable"], {"action": "inspect", "scene": args.scene}, source, args.timeout)
    if inspection["missing_dependencies"] or inspection["file_output_nodes"]:
        raise ValueError("Resolve missing dependencies or compositor File Output nodes before rendering.")
    if inspection["unresolved_dependencies"]:
        raise ValueError("Sequence/tiled assets require a dedicated validated dependency/render workflow.")
    dependencies = inspection["dependencies"] + (args.dependency or [])
    identity = fingerprint(source, dependencies, settings, environment["version"])
    manifest_path = root / "render-manifest.json"
    if manifest_path.exists():
        if not args.resume:
            raise ValueError("Run already exists; use --resume for unchanged inputs or a new output directory.")
        manifest = read_json(manifest_path)
        if manifest["fingerprint"] != identity or manifest.get("status") == "invalidated":
            raise ValueError("Scene, dependencies, settings or runtime changed; use a new output directory.")
    else:
        if root.exists() and any(root.iterdir()):
            raise ValueError("New render run requires an empty output directory.")
        manifest = {"schema_version": 1, "fingerprint": identity, "source_blend": str(source),
                    "settings": settings, "frames": requested, "outputs": {},
                    "environment": environment, "status": "planned"}
    root.mkdir(parents=True, exist_ok=True)
    with run_lock(root):
        if manifest_path.exists():
            manifest = read_json(manifest_path)
            if manifest["fingerprint"] != identity or manifest.get("status") == "invalidated":
                raise ValueError("Concurrent run changed identity; use a new output directory.")
        manifest["status"] = "rendering"
        save_json(manifest_path, manifest)
        # Invalidate any previous completion handoff before a repair attempt.
        save_json(root / "generation-log.json", {"tool": "blender", "outputDir": str(root), "status": "incomplete", "shots": []})
        save_json(root / "scene-inspection.json", inspection)
        try:
            for frame in requested:
                if frame_valid(manifest["outputs"].get(str(frame), {}), root):
                    continue
                extension = "png" if args.format == "PNG" else "exr"
                target = contained(root, root / "frames" / f"frame_{frame:06d}_{uuid.uuid4().hex[:8]}.{extension}")
                result = invoke(environment["executable"], {"action": "render", **settings,
                                "frame": frame, "output": str(target)}, source, args.timeout,
                                contained(root, root / f"frame_{frame:06d}.log"))
                if result.get("decoded") is not True or not target.is_file() or not target.stat().st_size:
                    raise RuntimeError("Missing or undecodable rendered output.")
                manifest["outputs"][str(frame)] = {**result, "file": str(target), "sha256": digest(target)}
                save_json(manifest_path, manifest)
            if fingerprint(source, dependencies, settings, environment["version"]) != identity:
                manifest["status"] = "invalidated"
                raise RuntimeError("Inputs changed during rendering; output set must not be accepted.")
            manifest["status"] = "rendered"
        except BaseException:
            if manifest["status"] != "invalidated":
                manifest["status"] = "incomplete"
            save_json(manifest_path, manifest)
            raise
        save_json(manifest_path, manifest)
        save_json(root / "generation-log.json", {"tool": "blender", "outputDir": str(root), "shots": [
            {"shot": f"FRAME{f:06d}", "status": "success", "tool": "blender", "filePath": manifest["outputs"][str(f)]["file"]}
            for f in requested]})
    return status(root)


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["doctor", "inspect", "build", "render", "status"])
    p.add_argument("--blender")
    p.add_argument("--blend")
    p.add_argument("--project-root")
    p.add_argument("--script")
    p.add_argument("--output")
    p.add_argument("--output-dir")
    p.add_argument("--scene")
    p.add_argument("--engine")
    p.add_argument("--frames", default="1")
    p.add_argument("--scale", type=int, default=100)
    p.add_argument("--format", choices=["PNG", "OPEN_EXR"], default="PNG")
    p.add_argument("--dependency", action="append")
    p.add_argument("--resume", action="store_true")
    p.add_argument("--timeout", type=int, default=1800)
    return p


def main():
    args = parser().parse_args()
    required = {"inspect": ["blend"], "build": ["project_root", "script", "output"],
                "render": ["project_root", "blend", "output_dir"], "status": ["output_dir"]}
    for field in required.get(args.command, []):
        if not getattr(args, field):
            raise ValueError(f"Missing --{field.replace('_', '-')}")
    if not 1 <= args.scale <= 100 or args.timeout <= 0:
        raise ValueError("Scale must be 1..100 and timeout positive.")
    if args.command == "status":
        return status(args.output_dir)
    environment = doctor(args.blender)
    if args.command == "doctor":
        return environment
    if not environment["available"]:
        raise RuntimeError(environment["reason"])
    if args.command == "inspect":
        if not Path(args.blend).is_file():
            raise ValueError("Source .blend does not exist.")
        return invoke(environment["executable"], {"action": "inspect", "scene": args.scene}, args.blend, args.timeout)
    return build(args, environment) if args.command == "build" else render(args, environment)


if __name__ == "__main__":
    try:
        print(json.dumps(main(), ensure_ascii=False, indent=2))
    except (ValueError, OSError, RuntimeError, subprocess.SubprocessError, KeyError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
