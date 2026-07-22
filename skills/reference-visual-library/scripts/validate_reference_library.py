from __future__ import annotations

import re
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_DIR / "references"


def table_rows(path: Path, prefix: str, expected_columns: int) -> list[list[str]]:
    text = path.read_text(encoding="utf-8")
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not line.startswith(f"| {prefix}-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != expected_columns:
            raise AssertionError(
                f"{path.name}: {cells[0]} has {len(cells)} columns; expected {expected_columns}"
            )
        if any(not cell for cell in cells):
            raise AssertionError(f"{path.name}: {cells[0]} has an empty required cell")
        rows.append(cells)
    return rows


def validate_ids(rows: list[list[str]], prefix: str) -> None:
    ids = [row[0] for row in rows]
    if len(ids) != len(set(ids)):
        raise AssertionError(f"{prefix}: duplicate IDs found")
    expected = [f"{prefix}-{index:03d}" for index in range(1, len(rows) + 1)]
    if ids != expected:
        raise AssertionError(f"{prefix}: IDs must be contiguous and ordered")


def validate_skill_contract() -> None:
    skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    required = [
        "references/film-prestige-visual-library.md",
        "references/kv-key-art-case-library.md",
        "reference_selection_mode",
        "one to two secondary systems",
        "pure typography, graphic-only KV, or abstract LED work",
        "ShotDeck-First Film Research",
        "shotdeck_search_recipe",
    ]
    for token in required:
        if token not in skill_text:
            raise AssertionError(f"SKILL.md missing contract token: {token}")

    yaml_text = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    for pattern in [
        r"(?m)^interface:\s*$",
        r"(?m)^\s{2}display_name:\s*\"[^\"]+\"\s*$",
        r"(?m)^\s{2}short_description:\s*\"[^\"]+\"\s*$",
        r"(?m)^\s{2}default_prompt:\s*\"[^\"]*\$reference-visual-library[^\"]*\"\s*$",
    ]:
        if not re.search(pattern, yaml_text):
            raise AssertionError(f"agents/openai.yaml missing pattern: {pattern}")


def main() -> int:
    film_path = REFERENCES / "film-prestige-visual-library.md"
    kv_path = REFERENCES / "kv-key-art-case-library.md"

    film_rows = table_rows(film_path, "FILM", 8)
    kv_rows = table_rows(kv_path, "KV", 7)
    validate_ids(film_rows, "FILM")
    validate_ids(kv_rows, "KV")

    film_text = film_path.read_text(encoding="utf-8")
    tier_ids: dict[str, list[str]] = {}
    for tier in ["Core A", "Specialist B"]:
        match = re.search(rf"(?m)^\| {re.escape(tier)} \| ([^|]+) \|", film_text)
        if not match:
            raise AssertionError(f"film library missing curated tier: {tier}")
        tier_ids[tier] = re.findall(r"FILM-\d{3}", match.group(1))
    assigned = tier_ids["Core A"] + tier_ids["Specialist B"]
    all_film_ids = [row[0] for row in film_rows]
    if len(assigned) != len(set(assigned)) or set(assigned) != set(all_film_ids):
        raise AssertionError("film tier assignment must cover every entry exactly once")
    if len(tier_ids["Core A"]) < 30:
        raise AssertionError("Core A pool is too small for useful functional coverage")

    for token in [
        "ShotDeck inclusion alone is not an approval badge",
        "cinematography_distinction",
        "shot_level_retrievability",
        "transferability",
        "functional_coverage",
        "craft_evidence",
        "anti_copy_safety",
        "shotdeck_status: inspected / search_recipe_only / not_required",
    ]:
        if token not in film_text:
            raise AssertionError(f"film library missing curation token: {token}")

    if len(film_rows) < 48:
        raise AssertionError(f"film library too small: {len(film_rows)} entries")
    if len(kv_rows) < 36:
        raise AssertionError(f"KV library too small: {len(kv_rows)} entries")

    for row in film_rows:
        reference_id, reference, _, project_function, mechanism, prompt, do_not_copy, source = row
        if len(project_function) < 4 or len(mechanism) < 12 or len(prompt) < 20:
            raise AssertionError(f"{reference_id}: translation fields are too weak")
        if reference.strip("* ").lower() in prompt.lower():
            raise AssertionError(f"{reference_id}: prompt translation repeats the reference title")
        if len(do_not_copy) < 8 or len(source) < 5:
            raise AssertionError(f"{reference_id}: do_not_copy or source trace is too weak")

    for row in kv_rows:
        case_id, _, kv_function, mechanism, prompt, do_not_copy, source = row
        if len(kv_function) < 4 or len(mechanism) < 12 or len(prompt) < 20:
            raise AssertionError(f"{case_id}: translation fields are too weak")
        if len(do_not_copy) < 8 or not source.startswith("["):
            raise AssertionError(f"{case_id}: do_not_copy or official source link is missing")

    validate_skill_contract()
    print("REFERENCE LIBRARY VALIDATION: PASS")
    print(f"- film/prestige entries: {len(film_rows)}")
    print(f"- Core A entries: {len(tier_ids['Core A'])}")
    print(f"- Specialist B entries: {len(tier_ids['Specialist B'])}")
    print(f"- KV/key-art entries: {len(kv_rows)}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssertionError, OSError) as exc:
        print("REFERENCE LIBRARY VALIDATION: FAIL")
        print(f"- {exc}")
        sys.exit(1)
