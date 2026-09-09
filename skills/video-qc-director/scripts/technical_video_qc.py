from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract objective technical QC evidence from a generated video.")
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--reference-first-frame", type=Path)
    parser.add_argument("--samples", type=int, default=9)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--ffprobe", default="ffprobe")
    return parser.parse_args()


def run(command: list[str], allow_failure: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)
    if result.returncode != 0 and not allow_failure:
        raise RuntimeError((result.stderr or result.stdout).strip() or "Command failed")
    return result


def ffprobe(video: Path, executable: str) -> dict:
    result = run([executable, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(video)])
    return json.loads(result.stdout)


def parse_fraction(value: str | None) -> float | None:
    if not value:
        return None
    if "/" in value:
        left, right = value.split("/", 1)
        return float(left) / float(right) if float(right) else None
    return float(value)


def average_hash(image_path: Path, size: int = 16) -> str:
    with Image.open(image_path) as image:
        pixels = list(ImageOps.grayscale(ImageOps.exif_transpose(image)).resize((size, size)).getdata())
    mean = sum(pixels) / len(pixels)
    bits = "".join("1" if value >= mean else "0" for value in pixels)
    return f"{int(bits, 2):0{size * size // 4}x}"


def hash_distance(left: str, right: str) -> int:
    return (int(left, 16) ^ int(right, 16)).bit_count()


def extract_samples(video: Path, output_dir: Path, duration: float, count: int, ffmpeg_exe: str) -> list[Path]:
    frame_dir = output_dir / "sample-frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    count = max(3, min(count, 20))
    points = [0.0] if duration <= 0 else [duration * index / (count - 1) for index in range(count)]
    frames: list[Path] = []
    for index, point in enumerate(points):
        output = frame_dir / f"frame_{index + 1:02d}_{point:.3f}s.jpg"
        result = run([
            ffmpeg_exe, "-hide_banner", "-loglevel", "error", "-y",
            "-ss", f"{point:.3f}", "-i", str(video), "-frames:v", "1", "-q:v", "2", str(output),
        ], allow_failure=True)
        if result.returncode == 0 and output.is_file():
            frames.append(output)
    return frames


def build_contact_sheet(frames: list[Path], output: Path) -> None:
    cell_w, cell_h, label_h = 400, 225, 28
    columns = 3
    rows = math.ceil(len(frames) / columns)
    sheet = Image.new("RGB", (cell_w * columns, (cell_h + label_h) * rows), "#11151b")
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(frames):
        with Image.open(frame) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
            image.thumbnail((cell_w, cell_h))
            x = (index % columns) * cell_w + (cell_w - image.width) // 2
            y = (index // columns) * (cell_h + label_h) + (cell_h - image.height) // 2
            sheet.paste(image, (x, y))
        draw.text(((index % columns) * cell_w + 8, (index // columns) * (cell_h + label_h) + cell_h + 5), frame.stem, fill="white")
    sheet.save(output, quality=90)


def filter_evidence(video: Path, ffmpeg_exe: str) -> dict:
    result = run([
        ffmpeg_exe, "-hide_banner", "-i", str(video),
        "-vf", "blackdetect=d=0.2:pix_th=0.10,freezedetect=n=-50dB:d=0.5",
        "-af", "volumedetect", "-f", "null", "-",
    ], allow_failure=True)
    text = f"{result.stdout}\n{result.stderr}"
    black = [
        {"start": float(a), "end": float(b), "duration": float(c)}
        for a, b, c in re.findall(r"black_start:([0-9.]+)\s+black_end:([0-9.]+)\s+black_duration:([0-9.]+)", text)
    ]
    freeze_starts = [float(value) for value in re.findall(r"freeze_start:\s*([0-9.]+)", text)]
    freeze_ends = [float(value) for value in re.findall(r"freeze_end:\s*([0-9.]+)", text)]
    mean_volume = re.search(r"mean_volume:\s*(-?[0-9.]+) dB", text)
    max_volume = re.search(r"max_volume:\s*(-?[0-9.]+) dB", text)
    return {
        "black_intervals": black,
        "freeze_starts": freeze_starts,
        "freeze_ends": freeze_ends,
        "audio_mean_db": float(mean_volume.group(1)) if mean_volume else None,
        "audio_max_db": float(max_volume.group(1)) if max_volume else None,
        "detector_exit_code": result.returncode,
    }


def main() -> int:
    args = parse_args()
    video = args.video.resolve()
    if not video.is_file():
        raise FileNotFoundError(video)
    if not shutil.which(args.ffmpeg) and not Path(args.ffmpeg).is_file():
        raise FileNotFoundError(f"ffmpeg not found: {args.ffmpeg}")
    if not shutil.which(args.ffprobe) and not Path(args.ffprobe).is_file():
        raise FileNotFoundError(f"ffprobe not found: {args.ffprobe}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    probe = ffprobe(video, args.ffprobe)
    format_data = probe.get("format", {})
    streams = probe.get("streams", [])
    video_stream = next((stream for stream in streams if stream.get("codec_type") == "video"), {})
    audio_streams = [stream for stream in streams if stream.get("codec_type") == "audio"]
    duration = float(format_data.get("duration") or video_stream.get("duration") or 0)
    frames = extract_samples(video, args.output_dir, duration, args.samples, args.ffmpeg)
    if not frames:
        raise RuntimeError("No sample frames could be extracted.")
    contact_sheet = args.output_dir / "video-qc-contact-sheet.jpg"
    build_contact_sheet(frames, contact_sheet)
    first_hash_distance = None
    if args.reference_first_frame:
        first_hash_distance = hash_distance(average_hash(args.reference_first_frame.resolve()), average_hash(frames[0]))
    evidence = filter_evidence(video, args.ffmpeg)
    warnings: list[str] = []
    if duration <= 0:
        warnings.append("duration_unavailable")
    if video_stream.get("width", 0) < 720 or video_stream.get("height", 0) < 720:
        warnings.append("low_resolution_for_formal_delivery")
    if evidence["black_intervals"]:
        warnings.append("black_frames_detected_review_edit_intent")
    if evidence["freeze_starts"]:
        warnings.append("freeze_detected_review_hold_intent")
    report = {
        "schema_version": 1,
        "evidence_type": "technical_video_qc",
        "video": str(video),
        "duration_seconds": duration,
        "container": format_data.get("format_name"),
        "bytes": int(format_data.get("size") or video.stat().st_size),
        "video_stream": {
            "codec": video_stream.get("codec_name"),
            "width": video_stream.get("width"),
            "height": video_stream.get("height"),
            "fps": parse_fraction(video_stream.get("avg_frame_rate")),
            "frame_count": int(video_stream["nb_frames"]) if str(video_stream.get("nb_frames", "")).isdigit() else None,
            "pixel_format": video_stream.get("pix_fmt"),
        },
        "audio_streams": [
            {"codec": stream.get("codec_name"), "sample_rate": stream.get("sample_rate"), "channels": stream.get("channels")}
            for stream in audio_streams
        ],
        "audio_track_present": bool(audio_streams),
        "music_vs_sfx_semantic_review_required": bool(audio_streams),
        "first_frame_reference_hash_distance": first_hash_distance,
        "detectors": evidence,
        "sample_frames": [str(frame.resolve()) for frame in frames],
        "contact_sheet": str(contact_sheet.resolve()),
        "warnings": warnings,
        "scope_note": "Objective technical evidence only. Music/SFX identity, character drift, motion quality, continuity, and aesthetic approval remain semantic QC decisions.",
    }
    report_path = args.output_dir / "technical-video-qc.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(report_path.resolve()), "contact_sheet": str(contact_sheet.resolve()), "sample_count": len(frames), "warnings": warnings}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
