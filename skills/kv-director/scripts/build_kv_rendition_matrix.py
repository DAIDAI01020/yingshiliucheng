from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build deterministic KV crop/safe-area renditions from one approved master composition.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args()


def bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def validate_box(box: dict, label: str) -> dict:
    result = {key: bounded(box.get(key, 0)) for key in ["x", "y", "w", "h"]}
    if result["w"] <= 0 or result["h"] <= 0 or result["x"] + result["w"] > 1.000001 or result["y"] + result["h"] > 1.000001:
        raise ValueError(f"Invalid normalized box for {label}: {box}")
    return result


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def crop_for_ratio(width: int, height: int, target_ratio: float, focus: dict, subject: dict | None) -> tuple[int, int, int, int, list[str]]:
    source_ratio = width / height
    warnings: list[str] = []
    if source_ratio >= target_ratio:
        crop_h = height
        crop_w = round(height * target_ratio)
    else:
        crop_w = width
        crop_h = round(width / target_ratio)
    center_x = bounded(focus.get("x", 0.5)) * width
    center_y = bounded(focus.get("y", 0.5)) * height
    left = clamp(center_x - crop_w / 2, 0, width - crop_w)
    top = clamp(center_y - crop_h / 2, 0, height - crop_h)
    if subject:
        subject_left = subject["x"] * width
        subject_top = subject["y"] * height
        subject_right = (subject["x"] + subject["w"]) * width
        subject_bottom = (subject["y"] + subject["h"]) * height
        if subject_right - subject_left > crop_w or subject_bottom - subject_top > crop_h:
            warnings.append("subject_box_larger_than_crop_manual_recomposition_required")
        else:
            left_min = max(0, subject_right - crop_w)
            left_max = min(width - crop_w, subject_left)
            top_min = max(0, subject_bottom - crop_h)
            top_max = min(height - crop_h, subject_top)
            if left_min <= left_max:
                left = clamp(left, left_min, left_max)
            if top_min <= top_max:
                top = clamp(top, top_min, top_max)
    return round(left), round(top), round(left + crop_w), round(top + crop_h), warnings


def pixel_box(box: dict, width: int, height: int) -> dict:
    return {
        "x": round(box["x"] * width),
        "y": round(box["y"] * height),
        "w": round(box["w"] * width),
        "h": round(box["h"] * height),
    }


def svg_overlay(rendition: dict, zones: dict[str, dict], output: Path) -> None:
    width, height = rendition["width"], rendition["height"]
    colors = {"title_zone": "#00d9ff", "logo_zone": "#ffe066", "sponsor_zone": "#ff5c8a", "performer_safe_zone": "#8aff80"}
    rects = []
    for name, box in zones.items():
        pixels = pixel_box(box, width, height)
        color = colors.get(name, "#ffffff")
        rects.append(f'<rect x="{pixels["x"]}" y="{pixels["y"]}" width="{pixels["w"]}" height="{pixels["h"]}" fill="none" stroke="{color}" stroke-width="4" stroke-dasharray="14 8"/>')
        rects.append(f'<text x="{pixels["x"] + 8}" y="{pixels["y"] + 24}" fill="{color}" font-family="Arial" font-size="22">{name}</text>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="#111827" fill-opacity="0.08"/>{"".join(rects)}</svg>\n'
    output.write_text(svg, encoding="utf-8")


def preview(image: Image.Image, crop: tuple[int, int, int, int], rendition: dict, zones: dict[str, dict], output: Path) -> None:
    target = image.crop(crop).resize((rendition["width"], rendition["height"]), Image.Resampling.LANCZOS).convert("RGB")
    draw = ImageDraw.Draw(target, "RGBA")
    colors = {"title_zone": (0, 217, 255, 220), "logo_zone": (255, 224, 102, 220), "sponsor_zone": (255, 92, 138, 220), "performer_safe_zone": (138, 255, 128, 220)}
    for name, box in zones.items():
        pixels = pixel_box(box, rendition["width"], rendition["height"])
        xy = [pixels["x"], pixels["y"], pixels["x"] + pixels["w"], pixels["y"] + pixels["h"]]
        color = colors.get(name, (255, 255, 255, 220))
        draw.rectangle(xy, outline=color, width=max(3, round(min(rendition["width"], rendition["height"]) / 250)))
        draw.text((xy[0] + 8, xy[1] + 8), name, fill=color)
    target.thumbnail((1200, 1200))
    target.save(output, quality=90)


def main() -> int:
    args = parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    renditions = data.get("renditions") or []
    if not renditions:
        raise ValueError("Input must include at least one rendition.")
    focus = data.get("focus_point") or {"x": 0.5, "y": 0.5}
    subject = validate_box(data["subject_box"], "subject_box") if data.get("subject_box") else None
    master_path = Path(data["master_image"]).resolve() if data.get("master_image") else None
    master_image = None
    source_width = int(data.get("master_width") or 0)
    source_height = int(data.get("master_height") or 0)
    if master_path:
        if not master_path.is_file():
            raise FileNotFoundError(master_path)
        master_image = ImageOps.exif_transpose(Image.open(master_path)).copy()
        source_width, source_height = master_image.size
    if source_width <= 0 or source_height <= 0:
        raise ValueError("Provide master_image or positive master_width/master_height.")
    if not args.check_only:
        args.output_dir.mkdir(parents=True, exist_ok=True)
    matrix = []
    for item in renditions:
        rendition = {"id": str(item["id"]), "width": int(item["width"]), "height": int(item["height"])}
        if rendition["width"] <= 0 or rendition["height"] <= 0:
            raise ValueError(f"Invalid rendition dimensions: {rendition}")
        zones = {name: validate_box(item[name], name) for name in ["title_zone", "logo_zone", "sponsor_zone", "performer_safe_zone"] if item.get(name)}
        crop, warnings = None, []
        crop = crop_for_ratio(source_width, source_height, rendition["width"] / rendition["height"], focus, subject)
        left, top, right, bottom, warnings = crop
        overlay_path = args.output_dir / f"{rendition['id']}_safe-area.svg"
        preview_path = args.output_dir / f"{rendition['id']}_preview.jpg"
        if not args.check_only:
            svg_overlay(rendition, zones, overlay_path)
            if master_image:
                preview(master_image, (left, top, right, bottom), rendition, zones, preview_path)
        matrix.append({
            **rendition,
            "ratio": round(rendition["width"] / rendition["height"], 6),
            "source_crop_pixels": {"left": left, "top": top, "right": right, "bottom": bottom},
            "source_crop_normalized": {"x": round(left / source_width, 6), "y": round(top / source_height, 6), "w": round((right - left) / source_width, 6), "h": round((bottom - top) / source_height, 6)},
            "safe_areas_normalized": zones,
            "safe_areas_pixels": {name: pixel_box(box, rendition["width"], rendition["height"]) for name, box in zones.items()},
            "overlay_svg": str(overlay_path.resolve()) if not args.check_only else None,
            "preview": str(preview_path.resolve()) if master_image and not args.check_only else None,
            "warnings": warnings,
        })
    report = {
        "schema_version": 1,
        "kv_id": data.get("kv_id", "KV"),
        "master_image": str(master_path) if master_path else None,
        "master_size": {"width": source_width, "height": source_height},
        "focus_point": focus,
        "subject_box": subject,
        "renditions": matrix,
        "approval_rule": "Approve the master composition first. Crop previews may derive variants; a warning requires manual recomposition instead of independent style regeneration.",
    }
    report_path = args.output_dir / "kv-rendition-matrix.json"
    if not args.check_only:
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"valid": True, "check_only": args.check_only, "matrix": str(report_path.resolve()) if not args.check_only else report}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
