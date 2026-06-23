#!/usr/bin/env python3
"""Split one source video into row/column video-wall tiles with FFmpeg."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path


def parse_size(value: str) -> tuple[int, int]:
    text = value.lower().replace(" ", "")
    if "x" not in text:
        raise argparse.ArgumentTypeError("size must look like WIDTHxHEIGHT, for example 1920x1080")
    width, height = text.split("x", 1)
    try:
        width_i = int(width)
        height_i = int(height)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("size must contain integer pixels") from exc
    if width_i <= 0 or height_i <= 0:
        raise argparse.ArgumentTypeError("size values must be positive")
    return width_i, height_i


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Required tool not found in PATH: {name}")


def ffprobe_video(path: Path) -> dict:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,r_frame_rate,duration",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    streams = data.get("streams") or []
    if not streams:
        raise SystemExit(f"No video stream found: {path}")
    return streams[0]


def build_tile_command(args: argparse.Namespace, tile: dict, scale_filter: str | None) -> list[str]:
    filters = []
    if scale_filter:
        filters.append(scale_filter)
    filters.append(f"crop={tile['width']}:{tile['height']}:{tile['x']}:{tile['y']}")
    if args.fps:
        filters.append(f"fps={args.fps}")

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(args.input),
        "-map",
        "0:v:0",
        "-vf",
        ",".join(filters),
        "-c:v",
        args.codec,
        "-preset",
        args.preset,
        "-crf",
        str(args.crf),
        "-pix_fmt",
        args.pix_fmt,
    ]

    if args.audio == "none":
        command.append("-an")
    elif args.audio == "first" and not (tile["row"] == 1 and tile["col"] == 1):
        command.append("-an")
    elif args.audio in {"first", "all"}:
        command.extend(["-map", "0:a?", "-c:a", "copy"])

    command.append(str(tile["file"]))
    return command


def write_manifests(output_dir: Path, manifest: dict) -> None:
    json_path = output_dir / "manifest.json"
    csv_path = output_dir / "manifest.csv"
    json_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    fields = ["file", "row", "col", "x", "y", "width", "height"]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for tile in manifest["tiles"]:
            writer.writerow({field: tile[field] for field in fields})


def main() -> int:
    parser = argparse.ArgumentParser(description="Split a video into tiled screen outputs.")
    parser.add_argument("input", type=Path, help="source video")
    parser.add_argument("--rows", type=int, required=True, help="number of screen rows")
    parser.add_argument("--cols", type=int, required=True, help="number of screen columns")
    parser.add_argument("--screen-size", type=parse_size, help="per-screen output size, such as 1920x1080")
    parser.add_argument("--output-dir", type=Path, help="directory for tile outputs")
    parser.add_argument("--prefix", help="output filename prefix")
    parser.add_argument("--codec", default="libx264", help="FFmpeg video codec")
    parser.add_argument("--crf", type=int, default=18, help="quality value for CRF codecs")
    parser.add_argument("--preset", default="medium", help="FFmpeg encoder preset")
    parser.add_argument("--pix-fmt", default="yuv420p", help="output pixel format")
    parser.add_argument("--fps", type=float, help="force output frame rate")
    parser.add_argument("--audio", choices=["none", "first", "all"], default="none", help="audio handling")
    parser.add_argument("--dry-run", action="store_true", help="print commands and write manifests only")
    args = parser.parse_args()

    if args.rows <= 0 or args.cols <= 0:
        raise SystemExit("--rows and --cols must be positive")
    if not args.input.exists():
        raise SystemExit(f"Input does not exist: {args.input}")

    require_tool("ffmpeg")
    require_tool("ffprobe")

    stream = ffprobe_video(args.input)
    source_w = int(stream["width"])
    source_h = int(stream["height"])

    if args.screen_size:
        tile_w, tile_h = args.screen_size
        canvas_w = tile_w * args.cols
        canvas_h = tile_h * args.rows
        scale_filter = f"scale={canvas_w}:{canvas_h}:flags=lanczos"
    else:
        tile_w = source_w // args.cols
        tile_h = source_h // args.rows
        canvas_w = tile_w * args.cols
        canvas_h = tile_h * args.rows
        scale_filter = None
        if canvas_w != source_w or canvas_h != source_h:
            scale_filter = f"scale={canvas_w}:{canvas_h}:flags=lanczos"
            print(
                f"Warning: source {source_w}x{source_h} is not evenly divisible by "
                f"{args.cols}x{args.rows}; scaling to {canvas_w}x{canvas_h}.",
                file=sys.stderr,
            )

    output_dir = args.output_dir or args.input.with_suffix("")
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.prefix or args.input.stem

    tiles = []
    for row in range(1, args.rows + 1):
        for col in range(1, args.cols + 1):
            filename = f"{prefix}_r{row:02d}_c{col:02d}.mp4"
            tiles.append(
                {
                    "file": str(output_dir / filename),
                    "row": row,
                    "col": col,
                    "x": (col - 1) * tile_w,
                    "y": (row - 1) * tile_h,
                    "width": tile_w,
                    "height": tile_h,
                }
            )

    manifest = {
        "source": str(args.input),
        "source_width": source_w,
        "source_height": source_h,
        "canvas_width": canvas_w,
        "canvas_height": canvas_h,
        "rows": args.rows,
        "cols": args.cols,
        "tile_width": tile_w,
        "tile_height": tile_h,
        "tiles": tiles,
    }
    write_manifests(output_dir, manifest)

    for tile in tiles:
        command = build_tile_command(args, {**tile, "file": Path(tile["file"])}, scale_filter)
        print(" ".join(command))
        if not args.dry_run:
            subprocess.run(command, check=True)

    print(f"Wrote {len(tiles)} tile entries to {output_dir / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
