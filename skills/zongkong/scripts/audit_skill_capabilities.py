from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


DEFAULT_SKILLS_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = Path(__file__).resolve().parents[1] / "references" / "capability-registry.json"

EXPECTED_PROMPT_OWNERS = {
    "generic_frame_prompt_semantics": "frame-vision-director",
    "kv_image_prompt_semantics": "kv-image-prompt-director",
    "storyboard_board_prompt_semantics": "scene-board-image-prompter",
    "typography_prompt_semantics": "type-png-director",
    "video_prompt_semantics": "ai-video-prompt-director",
    "platform_prompt_compilation": "prompt-platform-auditor",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit deterministic skill capability ownership.")
    parser.add_argument("--skills-root", type=Path, default=DEFAULT_SKILLS_ROOT)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    failures: list[str] = []
    capabilities = registry.get("capabilities", [])
    internal = registry.get("internal_compatibility_skills", [])
    internal_names = {entry.get("skill") for entry in internal}

    ids = [entry.get("capability_id") for entry in capabilities]
    if not ids or any(not item for item in ids):
        failures.append("Every capability must have a non-empty capability_id.")
    if len(ids) != len(set(ids)):
        failures.append("Duplicate capability_id values found.")

    referenced_skills: set[str] = set()
    owners: dict[str, str] = {}
    for entry in capabilities:
        capability_id = entry.get("capability_id", "")
        owner = entry.get("owner", "")
        supporters = entry.get("supporters", [])
        if not owner:
            failures.append(f"{capability_id}: missing owner")
            continue
        if not isinstance(supporters, list):
            failures.append(f"{capability_id}: supporters must be a list")
            continue
        if owner in supporters:
            failures.append(f"{capability_id}: owner is also listed as supporter")
        if owner in internal_names:
            failures.append(f"{capability_id}: internal compatibility skill cannot own a capability")
        owners[capability_id] = owner
        referenced_skills.add(owner)
        referenced_skills.update(str(item) for item in supporters)

    for entry in internal:
        for key in ["skill", "replacement_owner", "allowed_use"]:
            if not entry.get(key):
                failures.append(f"internal compatibility entry missing {key}")
        referenced_skills.add(str(entry.get("skill", "")))
        referenced_skills.add(str(entry.get("replacement_owner", "")))
        if entry.get("implicit_invocation") is not False:
            failures.append(f"{entry.get('skill')}: internal compatibility skill must disable implicit invocation")

        skill = str(entry.get("skill", ""))
        agent_yaml = args.skills_root / skill / "agents" / "openai.yaml"
        if not agent_yaml.is_file():
            failures.append(f"{skill}: internal compatibility skill is missing agents/openai.yaml")
        elif "allow_implicit_invocation: false" not in agent_yaml.read_text(encoding="utf-8"):
            failures.append(f"{skill}: agents/openai.yaml must disable implicit invocation")

    if "image_prompt_semantics" in owners:
        failures.append("image_prompt_semantics is deprecated; split prompt semantics by deliverable profile")
    for capability_id, expected_owner in EXPECTED_PROMPT_OWNERS.items():
        actual_owner = owners.get(capability_id)
        if actual_owner != expected_owner:
            failures.append(f"{capability_id}: expected owner {expected_owner}, got {actual_owner or 'missing'}")

    for skill in sorted(referenced_skills):
        if not skill:
            continue
        if not (args.skills_root / skill / "SKILL.md").is_file():
            failures.append(f"Missing referenced skill: {skill}")

    result = {
        "valid": not failures,
        "registry": str(args.registry.resolve()),
        "capability_count": len(capabilities),
        "internal_compatibility_count": len(internal),
        "owners": owners,
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
