from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create objective technical QC evidence for generated images.")
    parser.add_argument("--image", action="append", required=True, type=Path)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--profile", default="storyboard_frame")
    return parser.parse_args()


def average_hash(image: Image.Image, size: int = 16) -> str:
    pixels = list(ImageOps.grayscale(image).resize((size, size)).getdata())
    mean = sum(pixels) / len(pixels)
    bits = "".join("1" if value >= mean else "0" for value in pixels)
    return f"{int(bits, 2):0{size * size // 4}x}"


def hash_distance(left: str, right: str) -> int:
    return (int(left, 16) ^ int(right, 16)).bit_count()


def statistics(image: Image.Image) -> dict:
    gray = ImageOps.grayscale(image)
    histogram = gray.histogram()
    total = max(1, sum(histogram))
    dark = sum(histogram[:4]) / total
    bright = sum(histogram[252:]) / total
    mean = sum(index * count for index, count in enumerate(histogram)) / total
    variance = sum(((index - mean) ** 2) * count for index, count in enumerate(histogram)) / total
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edge_histogram = edges.histogram()
    edge_mean = sum(index * count for index, count in enumerate(edge_histogram)) / total
    alpha_coverage = None
    if "A" in image.getbands():
        alpha = image.getchannel("A")
        alpha_coverage = sum(1 for value in alpha.getdata() if value < 255) / total
    return {
        "luma_mean": round(mean, 3),
        "luma_stddev": round(math.sqrt(variance), 3),
        "near_black_ratio": round(dark, 5),
        "near_white_ratio": round(bright, 5),
        "edge_energy": round(edge_mean, 3),
        "alpha_nonopaque_ratio": None if alpha_coverage is None else round(alpha_coverage, 5),
    }


def inspect_image(image_path: Path, profile: str, reference_hash: str | None) -> dict:
    resolved = image_path.resolve()
    if not resolved.is_file():
        raise FileNotFoundError(resolved)
    with Image.open(resolved) as source:
        source.load()
        image = ImageOps.exif_transpose(source).copy()
        width, height = image.size
        digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
        image_hash = average_hash(image)
        stats = statistics(image)
        warnings: list[str] = []
        if max(width, height) < 1280:
            warnings.append("low_resolution_for_formal_delivery")
        if stats["near_black_ratio"] > 0.35:
            warnings.append("large_near_black_area_check_intent")
        if stats["near_white_ratio"] > 0.35:
            warnings.append("large_near_white_area_check_intent")
        if stats["edge_energy"] < 2:
            warnings.append("very_low_edge_energy_possible_blur_or_flat_frame")
        if profile == "typography_asset" and "A" not in image.getbands():
            warnings.append("typography_asset_has_no_alpha_channel")
        return {
            "path": str(resolved),
            "sha256": digest,
            "format": source.format,
            "mode": image.mode,
            "width": width,
            "height": height,
            "aspect_ratio": round(width / height, 6),
            "bytes": resolved.stat().st_size,
            "average_hash": image_hash,
            "reference_hash_distance": hash_distance(image_hash, reference_hash) if reference_hash else None,
            "technical_metrics": stats,
            "warnings": warnings,
        }


def build_contact_sheet(items: list[dict], output: Path) -> None:
    thumb_w, thumb_h = 480, 300
    rows = math.ceil(len(items) / 2)
    sheet = Image.new("RGB", (thumb_w * 2, rows * (thumb_h + 44)), "#16191f")
    draw = ImageDraw.Draw(sheet)
    for index, item in enumerate(items):
        with Image.open(item["path"]) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
            image.thumbnail((thumb_w - 20, thumb_h - 20))
            x = (index % 2) * thumb_w + (thumb_w - image.width) // 2
            y = (index // 2) * (thumb_h + 44) + (thumb_h - image.height) // 2
            sheet.paste(image, (x, y))
        label_y = (index // 2) * (thumb_h + 44) + thumb_h + 4
        draw.text(((index % 2) * thumb_w + 10, label_y), f"{Path(item['path']).name}  {item['width']}x{item['height']}", fill="white")
    sheet.save(output, quality=90)


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    reference_hash = None
    if args.reference:
        with Image.open(args.reference.resolve()) as reference:
            reference_hash = average_hash(ImageOps.exif_transpose(reference))
    items = [inspect_image(image, args.profile, reference_hash) for image in args.image]
    contact_sheet = args.output_dir / "image-qc-contact-sheet.jpg"
    build_contact_sheet(items, contact_sheet)
    report = {
        "schema_version": 1,
        "evidence_type": "technical_image_qc",
        "profile": args.profile,
        "semantic_qc_required": True,
        "reference": str(args.reference.resolve()) if args.reference else None,
        "images": items,
        "contact_sheet": str(contact_sheet.resolve()),
        "scope_note": "Objective technical evidence only; it does not decide composition, identity, continuity, text correctness, or aesthetic quality.",
    }
    report_path = args.output_dir / "technical-image-qc.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(report_path.resolve()), "contact_sheet": str(contact_sheet.resolve()), "image_count": len(items)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
