from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


TASK_MODES = {
    "text_to_video", "reference_to_video", "first_frame", "first_end_frames", "multi_keyframe",
    "video_edit", "extend_forward", "extend_backward", "montage", "seamless_transition",
    "coarse_white_model", "fine_white_model",
}
KINDS = {"image", "video", "audio", "text"}
MUSIC_POLICIES = {"no_music_allow_sfx", "music_requested", "full_silence"}
LOCKED_RATIO_MODES = {"video_edit", "extend_forward", "extend_backward", "first_frame", "first_end_frames"}
LOCKED_DURATION_MODES = {"video_edit"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit a structured Seedance 2.5 prompt packet without submitting generation.")
    parser.add_argument("--input", required=True, type=Path)
    return parser.parse_args()


def positive_number(value: object) -> float | None:
    try:
        number = float(value)  # type: ignore[arg-type]
        return number if number > 0 else None
    except (TypeError, ValueError):
        return None


def time_range(value: str) -> tuple[float, float] | None:
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*[-–—]\s*(\d+(?:\.\d+)?)\s*(?:秒|s)?\s*", value or "", re.I)
    if not match:
        return None
    return float(match.group(1)), float(match.group(2))


def main() -> int:
    args = parse_args()
    packet = json.loads(args.input.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

    if packet.get("model_target") != "seedance_2_5":
        errors.append("model_target_must_be_seedance_2_5")
    task_mode = str(packet.get("task_mode") or "")
    if task_mode not in TASK_MODES:
        errors.append("unsupported_or_missing_task_mode")
    if str(packet.get("music_policy") or "") not in MUSIC_POLICIES:
        errors.append("missing_or_invalid_music_policy")

    references = packet.get("references") or []
    if not isinstance(references, list):
        errors.append("references_must_be_an_array")
        references = []
    if len(references) > 50:
        errors.append("reference_total_exceeds_50")
    seen_ids: set[str] = set()
    counts = {kind: 0 for kind in KINDS}
    durations = {"video": 0.0, "audio": 0.0}
    by_id: dict[str, dict] = {}
    for index, item in enumerate(references, 1):
        if not isinstance(item, dict):
            errors.append(f"reference_{index}_must_be_an_object")
            continue
        ref_id = str(item.get("id") or "").strip()
        kind = str(item.get("kind") or "").strip()
        if not ref_id:
            errors.append(f"reference_{index}_missing_id")
        elif ref_id in seen_ids:
            errors.append(f"duplicate_reference_id:{ref_id}")
        else:
            seen_ids.add(ref_id)
            by_id[ref_id] = item
        if kind not in KINDS:
            errors.append(f"{ref_id or index}:invalid_kind")
            continue
        counts[kind] += 1
        if not str(item.get("use") or "").strip():
            errors.append(f"{ref_id or index}:missing_use_role")
        if kind in {"image", "video", "audio"} and not str(item.get("entity") or "").strip():
            warnings.append(f"{ref_id or index}:missing_named_entity_or_sound_owner")
        duration = positive_number(item.get("duration_seconds"))
        if kind in durations and duration:
            durations[kind] += duration
        if kind == "image":
            width = positive_number(item.get("width"))
            height = positive_number(item.get("height"))
            if width and height and max(width, height) > 4096:
                errors.append(f"{ref_id or index}:image_exceeds_4k")

    if counts["image"] > 30:
        errors.append("image_reference_count_exceeds_30")
    if counts["video"] > 10:
        errors.append("video_reference_count_exceeds_10")
    if counts["audio"] > 10:
        errors.append("audio_reference_count_exceeds_10")
    if durations["video"] > 30.0001:
        errors.append("combined_video_reference_duration_exceeds_30_seconds")
    if durations["audio"] > 30.0001:
        errors.append("combined_audio_reference_duration_exceeds_30_seconds")
    if len(references) > 12:
        warnings.append("large_reference_set_requires_grouping_and_per_scene_asset_calls")

    stages = packet.get("stages") or []
    if not isinstance(stages, list):
        errors.append("stages_must_be_an_array")
        stages = []
    duration = positive_number(packet.get("duration"))
    if duration and duration > 30:
        errors.append("requested_duration_exceeds_30_second_documented_ceiling")
    if stages:
        previous_end: float | None = None
        for index, stage in enumerate(stages, 1):
            if not isinstance(stage, dict):
                errors.append(f"stage_{index}_must_be_an_object")
                continue
            if not str(stage.get("main_change") or "").strip():
                errors.append(f"stage_{index}_missing_main_change")
            if not str(stage.get("ending_state") or "").strip():
                errors.append(f"stage_{index}_missing_ending_state")
            raw_range = str(stage.get("time_range") or "")
            parsed = time_range(raw_range) if raw_range else None
            if raw_range and not parsed:
                warnings.append(f"stage_{index}_time_range_not_machine_parseable")
            if parsed:
                start, end = parsed
                if end <= start:
                    errors.append(f"stage_{index}_invalid_time_range")
                if previous_end is not None and abs(start - previous_end) > 0.001:
                    errors.append(f"stage_{index}_time_range_not_contiguous")
                previous_end = end
        if duration and previous_end is not None and abs(previous_end - duration) > 0.001:
            warnings.append("stage_timeline_does_not_end_at_requested_duration")
    elif duration and duration > 20:
        warnings.append("long_multi_event_video_should_use_stages_with_observable_end_states")

    overrides = packet.get("parameter_overrides") or {}
    if not isinstance(overrides, dict):
        errors.append("parameter_overrides_must_be_an_object")
        overrides = {}
    if task_mode in LOCKED_RATIO_MODES and any(key in overrides for key in ["ratio", "aspect_ratio"]):
        errors.append("task_mode_forbids_ratio_override")
    if task_mode in LOCKED_DURATION_MODES and "duration" in overrides:
        errors.append("video_edit_forbids_duration_override")

    edit_master = str(packet.get("edit_master") or "").strip()
    if task_mode in {"video_edit", "extend_forward", "extend_backward"}:
        if not edit_master:
            errors.append("task_mode_requires_edit_master_or_source_video")
        elif edit_master not in by_id:
            errors.append("edit_master_not_found_in_references")
        elif by_id[edit_master].get("kind") != "video":
            errors.append("edit_master_must_reference_video")
    if task_mode == "video_edit":
        if not str(packet.get("edit_scope") or "").strip():
            errors.append("video_edit_requires_bounded_edit_scope")
        if not packet.get("must_preserve"):
            errors.append("video_edit_requires_must_preserve")
    if task_mode in {"extend_forward", "extend_backward"} and not str(packet.get("boundary_state") or "").strip():
        errors.append("extension_requires_boundary_state")

    if task_mode == "first_end_frames":
        anchor_images = [item for item in references if isinstance(item, dict) and item.get("kind") == "image" and any(token in str(item.get("use") or "").lower() for token in ["首帧", "尾帧", "first frame", "end frame", "last frame"])]
        if len(anchor_images) < 2:
            errors.append("first_end_frames_requires_separately_mapped_first_and_end_images")
        ratios = set()
        for item in anchor_images:
            width = positive_number(item.get("width"))
            height = positive_number(item.get("height"))
            if width and height:
                ratios.add(round(width / height, 5))
        if len(ratios) > 1:
            errors.append("first_and_end_frame_aspect_ratios_do_not_match")
    if task_mode == "seamless_transition" and counts["video"] < 2:
        errors.append("seamless_transition_requires_before_and_after_video_references")
    if task_mode in {"coarse_white_model", "fine_white_model"} and counts["video"] < 1:
        errors.append("white_model_task_requires_a_video_reference")

    result = {
        "valid": not errors,
        "model_target": packet.get("model_target"),
        "task_mode": task_mode,
        "reference_counts": counts,
        "reference_total": len(references),
        "video_reference_duration_seconds": round(durations["video"], 3),
        "audio_reference_duration_seconds": round(durations["audio"], 3),
        "errors": errors,
        "warnings": warnings,
        "scope_note": "Prompt-packet audit only. Live Dreamina/Ark model availability, flags, credits, and accepted parameters must still be checked before execution.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
