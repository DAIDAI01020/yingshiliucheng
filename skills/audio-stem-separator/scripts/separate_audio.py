"""Cinematic three-stem adapter for a separately installed MSST backend."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1048576), b""):
            value.update(block)
    return value.hexdigest()


def probe(path, ffprobe="ffprobe", stream=0):
    raw = subprocess.run([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                         capture_output=True, text=True, encoding="utf-8", check=True)
    data = json.loads(raw.stdout)
    audios = [s for s in data["streams"] if s["codec_type"] == "audio"]
    if stream < 0 or stream >= len(audios):
        raise ValueError("Selected audio stream does not exist.")
    selected = audios[stream]
    duration = float(selected.get("duration", data.get("format", {}).get("duration", 0)))
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("Cannot verify audio duration.")
    origin = float(data.get("format", {}).get("start_time", 0))
    return {"duration": duration, "channels": int(selected["channels"]), "sample_rate": int(selected["sample_rate"]),
            "source_offset": float(selected.get("start_time", origin)) - origin, "stream_index": selected["index"]}


def model_config(path):
    import yaml
    config = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    labels = config.get("training", {}).get("instruments", [])
    canonical = lambda names: {"sfx" if n == "effects" else n for n in names}
    if len(labels) != 3 or canonical(labels) != {"speech", "music", "sfx"}:
        raise ValueError("Model must declare exactly speech, music and sfx/effects; vocals/instrumental is not sufficient.")
    architectural = config.get("kwargs", {}).get("stems")
    if architectural and canonical(architectural) != canonical(labels):
        raise ValueError("Model architecture and output stem labels disagree.")
    rate = int(config.get("audio", {}).get("sample_rate", 0))
    if rate < 8000 or rate > 192000:
        raise ValueError("Missing or unsupported model sample rate.")
    return labels, rate


def backend_profile_path():
    explicit = os.environ.get("AUDIO_STEM_BACKEND_PROFILE")
    if explicit:
        return Path(explicit)
    codex_root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    return codex_root / "tools/audio-separation/backend.json"


def resolve_backend(args):
    """Reuse a persistent local installation; never install or download implicitly."""
    profile_path = Path(args.backend_profile) if getattr(args, "backend_profile", None) else backend_profile_path()
    profile = {}
    if profile_path.is_file():
        profile = json.loads(profile_path.read_text(encoding="utf-8-sig"))
        if not isinstance(profile, dict) or profile.get("version") != 1:
            raise ValueError("Unsupported audio backend profile: " + str(profile_path))
        for key in ("backend_root", "backend_python", "config", "checkpoint"):
            value = profile.get(key)
            if value is not None and (not isinstance(value, str) or not Path(value).is_absolute()):
                raise ValueError("Backend profile needs an absolute path for " + key)
            if not getattr(args, key, None):
                setattr(args, key, value)
        for key in ("config", "checkpoint"):
            expected = profile.get(key + "_sha256")
            selected = getattr(args, key, None)
            if expected and selected and profile.get(key) and Path(selected).resolve() == Path(profile[key]).resolve():
                if Path(selected).is_file() and digest(selected) != expected:
                    raise ValueError(key + " hash differs from the registered local model; inspect it before repair, do not redownload automatically.")
    elif getattr(args, "backend_profile", None) or os.environ.get("AUDIO_STEM_BACKEND_PROFILE"):
        raise ValueError("Explicit backend profile does not exist: " + str(profile_path))
    args.model_type = getattr(args, "model_type", None) or profile.get("model_type", "bandit_v2")
    if args.model_type not in ("bandit", "bandit_v2"):
        raise ValueError("Unsupported cinematic model type in backend profile.")
    return str(profile_path) if profile else None


def doctor(args):
    profile = resolve_backend(args)
    fields = {"backend_root": args.backend_root, "backend_python": args.backend_python,
              "config": args.config, "checkpoint": args.checkpoint}
    missing = []
    for name, value in fields.items():
        target = Path(value) if value else None
        if target is None or (not target.is_dir() if name == "backend_root" else not target.is_file()):
            missing.append(name)
        elif name == "checkpoint" and target.stat().st_size == 0:
            missing.append(name)
    if args.backend_root and not (Path(args.backend_root) / "inference.py").is_file():
        missing.append("inference.py")
    for name in ("ffmpeg", "ffprobe"):
        if not shutil.which(getattr(args, name)):
            missing.append(name)
    if args.config and Path(args.config).is_file():
        model_config(args.config)
    return {"configured": not missing, "missing": missing, "inference_verified": False,
            "backend_profile": profile, "local_paths": fields, "downloads_performed": False,
            "semantic_targets": ["speech", "music", "sfx"]}


def verify(input_path, stems, ffmpeg="ffmpeg", ffprobe="ffprobe", stream=0):
    if set(stems) != {"speech", "music", "sfx"}:
        raise ValueError("All three explicit stems are required.")
    if len({Path(p).resolve() for p in stems.values()}) != 3:
        raise ValueError("Three separate output files are required.")
    source = probe(input_path, ffprobe, stream)
    output = {}
    for role, file in stems.items():
        file = Path(file)
        if not file.is_file() or not file.stat().st_size:
            raise ValueError(f"Missing {role} output.")
        evidence = probe(file, ffprobe)
        if abs(evidence["duration"] - source["duration"]) > .02:
            raise ValueError(f"{role} duration differs from the selected source.")
        if evidence["channels"] != source["channels"]:
            raise ValueError(f"{role} channels differ from the working mix.")
        subprocess.run([ffmpeg, "-v", "error", "-xerror", "-nostdin", "-i", str(file), "-map", "0:a:0",
                        "-f", "null", "-"], check=True, capture_output=True)
        output[role] = {**evidence, "file": str(file.resolve()), "sha256": digest(file)}
    if len({v["sample_rate"] for v in output.values()}) != 1:
        raise ValueError("Stem sample rates do not match.")
    return {"technical_status": "verified", "listening_status": "not_reviewed", "source": source, "stems": output}


def separate(args):
    readiness = doctor(args)
    if not readiness["configured"]:
        raise ValueError("Separation backend not ready: " + ", ".join(readiness["missing"]))
    original = Path(args.input).resolve()
    source = probe(original, args.ffprobe, args.audio_stream)
    if source["channels"] > 2:
        raise ValueError("Multichannel source requires an explicit downmix plan; adapter supports mono/stereo.")
    labels, rate = model_config(args.config)
    root = Path(args.output_dir).resolve()
    if root.exists():
        raise ValueError("Use a new output directory; preserve previous runs.")
    backend = Path(args.backend_root).resolve()
    python = str(Path(args.backend_python).resolve())
    root.mkdir(parents=True)
    record = {"status": "running", "source": str(original), "source_sha256": digest(original),
              "source_audio_stream": args.audio_stream, "source_audio_offset": source["source_offset"],
              "model_type": args.model_type, "config_sha256": digest(args.config), "checkpoint_sha256": digest(args.checkpoint),
              "backend_profile": readiness["backend_profile"], "local_model_reused": True,
              "inference_script_sha256": digest(backend / "inference.py"), "listening_status": "not_reviewed"}
    manifest = root / "separation-manifest.json"
    def save():
        manifest.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    save()
    try:
        inputs = root / "inputs"
        inputs.mkdir()
        mix = inputs / "mix.wav"
        subprocess.run([args.ffmpeg, "-v", "error", "-nostdin", "-n", "-i", str(original), "-map", f"0:a:{args.audio_stream}",
                        "-vn", "-af", "asetpts=PTS-STARTPTS,aresample=async=1:first_pts=0", "-ac", "2", "-ar", str(rate),
                        "-c:a", "pcm_f32le", str(mix)], check=True, capture_output=True)
        command = [python, str(backend / "inference.py"), "--model_type", args.model_type,
                   "--config_path", str(Path(args.config).resolve()), "--start_check_point", str(Path(args.checkpoint).resolve()),
                   "--input_folder", str(inputs), "--store_dir", str(root / "raw"), "--pcm_type", "FLOAT",
                   "--filename_template", "{instr}"]
        if args.force_cpu:
            command.append("--force_cpu")
        with (root / "inference.log").open("wb") as log:
            subprocess.run(command, cwd=backend, check=True, stdout=log, stderr=subprocess.STDOUT)
        stems = {}
        for label in labels:
            role = "sfx" if label == "effects" else label
            raw = root / "raw" / f"{label}.wav"
            if not raw.is_file():
                raise ValueError(f"Backend did not produce {label}.wav; inspect version/output contract.")
            target = root / f"{role}.wav"
            subprocess.run([args.ffmpeg, "-v", "error", "-nostdin", "-n", "-i", str(raw),
                            "-ar", "48000", "-c:a", "pcm_f32le", str(target)], check=True, capture_output=True)
            stems[role] = target
        evidence = verify(mix, stems, args.ffmpeg, args.ffprobe)
        if (digest(original) != record["source_sha256"] or digest(args.config) != record["config_sha256"]
                or digest(args.checkpoint) != record["checkpoint_sha256"]):
            raise ValueError("Source or model inputs changed during separation; do not accept this run.")
        record.update(technical_status=evidence["technical_status"], stems=evidence["stems"],
                      working_mix=evidence["source"], status="separated", manifest=str(manifest))
        save()
        return record
    except BaseException:
        record["status"] = "incomplete"
        save()
        raise


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["doctor", "separate", "verify"])
    p.add_argument("--input")
    p.add_argument("--output-dir")
    for name in ("speech", "music", "sfx"):
        p.add_argument("--" + name)
    for name, env in [("backend-root", "MSST_ROOT"), ("backend-python", "MSST_PYTHON"), ("config", "MSST_CONFIG"), ("checkpoint", "MSST_CHECKPOINT")]:
        p.add_argument("--" + name, default=os.environ.get(env))
    p.add_argument("--backend-profile", help="Persistent local backend JSON; defaults to CODEX_HOME/tools/audio-separation/backend.json")
    p.add_argument("--model-type", choices=["bandit", "bandit_v2"], default=os.environ.get("MSST_MODEL_TYPE"))
    p.add_argument("--audio-stream", type=int, default=0)
    p.add_argument("--force-cpu", action="store_true")
    p.add_argument("--ffmpeg", default="ffmpeg")
    p.add_argument("--ffprobe", default="ffprobe")
    return p


def main():
    args = parser().parse_args()
    if args.command == "doctor":
        return doctor(args)
    if not args.input or not Path(args.input).is_file():
        raise ValueError("An existing --input is required.")
    if args.command == "verify":
        if not all([args.speech, args.music, args.sfx]):
            raise ValueError("Supply speech, music and sfx outputs explicitly.")
        return verify(args.input, {k: getattr(args, k) for k in ("speech", "music", "sfx")}, args.ffmpeg, args.ffprobe, args.audio_stream)
    if not args.output_dir:
        raise ValueError("A new --output-dir is required.")
    return separate(args)


if __name__ == "__main__":
    try:
        print(json.dumps(main(), ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, ImportError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
