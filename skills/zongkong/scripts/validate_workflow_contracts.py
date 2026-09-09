from __future__ import annotations

import re
import sys
import json
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[2]

CORE_SKILLS = [
    "zongkong",
    "frame-vision-director",
    "openai-image-prompt-director",
    "ai-video-prompt-director",
    "prompt-platform-auditor",
    "project-style-lock",
    "builtin-imagegen-director",
    "image-qc-director",
    "video-qc-director",
    "project-state-manager",
    "project-thread-orchestrator",
    "production-manager",
    "short-drama-director",
    "kv-director",
    "banana-image-generator",
    "project-folder-director",
    "reference-visual-library",
    "kv-image-prompt-director",
    "type-png-director",
    "scene-board-image-prompter",
    "image-generation-controller",
    "video-generation-controller",
    "dreamina-cli",
    "workflow-sync-manager",
]

REQUIRED_BY_SKILL = {
    "zongkong": ["prompt_task", "source_prompt_state", "semantic_create", "platform_compile", "prompt_diagnose", "targeted_rewrite", "deliverable_profile", "response_mode", "qc_mode", "thread_orchestration", "project-thread-orchestrator", "model_target:gpt_image_2_5"],
    "frame-vision-director": ["image_prompt_source_packet", "must_preserve", "must_change", "model_target", "task_mode"],
    "ai-video-prompt-director": ["video_prompt_source_packet", "model_target", "task_mode", "complexity_mode", "reference_asset_map", "stage_plan", "edit_master", "boundary_state", "locked_parameters", "ending_behavior", "audio_mode", "music_policy", "no_music_allow_sfx"],
    "prompt-platform-auditor": ["deliverable_profile", "model_target", "task_mode", "reference_asset_map", "stage_plan", "edit_master", "boundary_state", "locked_parameters", "ending_behavior", "audio_mode", "music_policy", "audited_prompt_packet", "gpt-image-2-5.md", "gpt_image_2_5", "seedance-2-5.md", "audit_seedance_25_packet.py"],
    "builtin-imagegen-director": ["direct_image_preflight_check", "model_target:gpt_image_2_5", "precision edits", "Flare", "Sunburst"],
    "project-style-lock": ["profile_extension", "Never require `$prompt-platform-auditor` as an upstream source"],
    "image-qc-director": ["generation_observation", "qc_mode", "technical_image_qc.py", "semantic"],
    "video-qc-director": ["generation_observation", "ending behavior", "music_policy:no_music_allow_sfx", "technical_video_qc.py", "music versus ambience/SFX"],
    "project-state-manager": ["generation-observations.jsonl", "project_folder_contract.project_root", "thread_registry", "shared_project_shared_root", "shot-production-registry.json", "manage-shot-production.py", "platform_performance"],
    "project-thread-orchestrator": ["thread_split_plan", "shared_project_shared_root", "next-batch", "mark-stale", "sync-handoff", "Never use fork"],
    "short-drama-director": ["Shot Production State Chain", "anchor", "image_approved", "video_submitted", "accepted"],
    "kv-director": ["Master-To-Rendition Gate", "kv_rendition_matrix", "build_kv_rendition_matrix.py", "manual-recomposition"],
    "banana-image-generator": ["generation_confirmation", "idempotency", "--resume", "Do not auto-retry", "project-state"],
    "production-manager": ["分聊天任务看板", "thread_registry", "ready_for_review"],
    "project-folder-director": ["projects_root", "{current_workspace_root}\\projects"],
    "reference-visual-library": ["film-prestige-visual-library.md", "kv-key-art-case-library.md", "reference_selection_mode", "mother_library_application_packet", "ShotDeck-First Film Research", "shotdeck_search_recipe"],
    "kv-image-prompt-director": ["kv_image_prompt_source_packet", "response_mode", "prompt-platform-auditor"],
    "type-png-director": ["type_png_prompt_source_packet", "text_content", "prompt-platform-auditor"],
    "scene-board-image-prompter": ["board_prompt_source_packet", "pre_generation_check", "prompt-platform-auditor"],
    "image-generation-controller": ["idempotency key", "generation_confirmation", "generation-run-ledger.jsonl", "--resume", "--force-new-run"],
    "video-generation-controller": ["idempotency key", "generation_confirmation", "generation-run-ledger.jsonl", "no_music_allow_sfx", "--force-new-run", "dreamina_runner.mjs", "jimeng-manual", "querying"],
    "dreamina-cli": ["submit_id", "user_credit", "idempotency_key", "generation_confirmation", "no_music_allow_sfx", "dreamina_runner.mjs", "live help"],
    "workflow-sync-manager": ["--paths-file", "never force-push automatically", "--remote github", "--tag"],
}

BANNED = {
    "frame-vision-director": [
        "Anti-AI realism is mandatory for image prompts",
        "Final image prompts cannot pass if any of these are missing",
    ],
    "prompt-platform-auditor": [
        "For image prompts, approval requires all mandatory camera fields",
        "For formal image prompts, return `打回重写` if anti-AI photographic realism is missing",
        "Do not add a breath tail or no-music sentence by default",
    ],
    "ai-video-prompt-director": [
        "every copyable video prompt must include",
        "短剧每个镜头默认有轻气口",
        "Do not insert a universal `不要音乐` line",
    ],
    "project-style-lock": [
        "prompt-platform-auditor target platform expectations",
        "every short-drama shot ends with a light breath tail",
    ],
    "project-folder-director": [
        "Formal and quick projects must use `H:\\yingshi",
    ],
}


def read_skill(name: str) -> str:
    path = SKILL_ROOT / name / "SKILL.md"
    if not path.is_file():
        raise AssertionError(f"missing SKILL.md: {path}")
    return path.read_text(encoding="utf-8")


def direct_reference_links(skill_dir: Path, text: str) -> list[Path]:
    links = re.findall(r"\]\((references/[^)#]+)(?:#[^)]+)?\)", text)
    return [skill_dir / link for link in sorted(set(links))]


def validate_agent_yaml(name: str, failures: list[str]) -> None:
    path = SKILL_ROOT / name / "agents" / "openai.yaml"
    if not path.is_file():
        failures.append(f"{name}: missing agents/openai.yaml")
        return
    text = path.read_text(encoding="utf-8")
    required_patterns = [
        r"(?m)^interface:\s*$",
        r'(?m)^\s{2}display_name:\s+"[^"]+"\s*$',
        r'(?m)^\s{2}short_description:\s+"[^"]+"\s*$',
        r'(?m)^\s{2}default_prompt:\s+"[^"]+"\s*$',
    ]
    for pattern in required_patterns:
        if not re.search(pattern, text):
            failures.append(f"{name}: agents/openai.yaml missing pattern {pattern!r}")
    short_match = re.search(r'(?m)^\s{2}short_description:\s+"([^"]+)"\s*$', text)
    if short_match and not 25 <= len(short_match.group(1)) <= 64:
        failures.append(f"{name}: short_description must be 25-64 chars")
    if f"${name}" not in text:
        failures.append(f"{name}: default_prompt must mention ${name}")
    if name == "zongkong":
        for token in [
            "execution_intent", "prompt_task", "speed_mode", "deliverable_profile",
            "$prompt-platform-auditor", "prompt_only", "不创建项目", "当前唯一负责人",
        ]:
            if token not in text:
                failures.append(f"zongkong: agents/openai.yaml missing routing token {token}")


def main() -> int:
    failures: list[str] = []
    texts: dict[str, str] = {}

    for name in CORE_SKILLS:
        try:
            text = read_skill(name)
            texts[name] = text
        except AssertionError as exc:
            failures.append(str(exc))
            continue

        line_count = len(text.splitlines())
        if line_count >= 500:
            failures.append(f"{name}: {line_count} lines, expected < 500")

        frontmatter = re.match(r"^\ufeff?---\s*\n(.*?)\n---", text, re.S)
        if not frontmatter:
            failures.append(f"{name}: invalid frontmatter")
        else:
            keys = re.findall(r"^([A-Za-z_][A-Za-z0-9_-]*):", frontmatter.group(1), re.M)
            if keys != ["name", "description"]:
                failures.append(f"{name}: frontmatter keys must be name, description; got {keys}")

        for token in REQUIRED_BY_SKILL.get(name, []):
            if token not in text:
                failures.append(f"{name}: missing required contract token {token!r}")

        for token in BANNED.get(name, []):
            if token in text:
                failures.append(f"{name}: banned blanket rule remains: {token!r}")

        skill_dir = SKILL_ROOT / name
        for ref in direct_reference_links(skill_dir, text):
            if not ref.is_file():
                failures.append(f"{name}: missing linked reference {ref}")

        validate_agent_yaml(name, failures)

    combined = "\n".join(texts.values())
    for named in sorted(set(re.findall(r"\$([a-z0-9][a-z0-9-]+)", combined))):
        if not (SKILL_ROOT / named / "SKILL.md").is_file():
            failures.append(f"named skill is not installed: {named}")

    auditor = texts.get("prompt-platform-auditor", "")
    for reference in ["image-platforms.md", "gpt-image-2-5.md", "video-platforms.md", "profile-risk-controls.md", "seedance-2-5.md"]:
        if f"references/{reference}" not in auditor:
            failures.append(f"prompt-platform-auditor: reference not linked: {reference}")

    generation_template = SKILL_ROOT / "project-state-manager" / "templates" / "short-drama" / "generation-ready-template.json"
    generation_text = generation_template.read_text(encoding="utf-8") if generation_template.is_file() else ""
    for token in ["video_prompt_source_packet", "ending_behavior", "audio_mode", "music_policy", "no_music_allow_sfx", "deliverable_profile"]:
        if token not in generation_text:
            failures.append(f"generation-ready-template.json: missing {token}")
    for token in ['"video_platform_prompt_packet"', '"audio_policy"']:
        if token in generation_text:
            failures.append(f"generation-ready-template.json: legacy primary field remains {token}")

    state_script = SKILL_ROOT / "project-state-manager" / "scripts" / "manage-project-state.mjs"
    state_text = state_script.read_text(encoding="utf-8") if state_script.is_file() else ""
    for token in ["video_prompt_source_packet", "ending_behavior", "musicPolicy", "deliverable_profile", "requires_mother_library"]:
        if token not in state_text:
            failures.append(f"manage-project-state.mjs: missing compatibility token {token}")
    for token in ["record-observation", "summarize-feedback", "generation-run-ledger.jsonl", "read_only"]:
        if token not in state_text:
            failures.append(f"manage-project-state.mjs: missing reliability token {token}")

    required_runtime_files = [
        SKILL_ROOT / "project-state-manager" / "scripts" / "generation-run-ledger.mjs",
        SKILL_ROOT / "project-state-manager" / "templates" / "generation-observation-template.json",
        SKILL_ROOT / "project-state-manager" / "templates" / "shot-production-packet-template.json",
        SKILL_ROOT / "project-state-manager" / "scripts" / "manage-shot-production.py",
        SKILL_ROOT / "production-manager" / "scripts" / "build_project_dashboard.py",
        SKILL_ROOT / "banana-image-generator" / "scripts" / "generate-banana-images.mjs",
        SKILL_ROOT / "dreamina-cli" / "scripts" / "dreamina_runner.mjs",
        SKILL_ROOT / "image-qc-director" / "scripts" / "technical_image_qc.py",
        SKILL_ROOT / "video-qc-director" / "scripts" / "technical_video_qc.py",
        SKILL_ROOT / "kv-director" / "scripts" / "build_kv_rendition_matrix.py",
        SKILL_ROOT / "kv-director" / "templates" / "kv-rendition-plan-template.json",
        SKILL_ROOT / "prompt-platform-auditor" / "references" / "seedance-2-5.md",
        SKILL_ROOT / "prompt-platform-auditor" / "references" / "gpt-image-2-5.md",
        SKILL_ROOT / "prompt-platform-auditor" / "templates" / "seedance-2-5-prompt-packet.json",
        SKILL_ROOT / "prompt-platform-auditor" / "scripts" / "audit_seedance_25_packet.py",
        SKILL_ROOT / "zongkong" / "scripts" / "audit_skill_capabilities.py",
        SKILL_ROOT / "zongkong" / "scripts" / "run_e2e_workflow_tests.py",
    ]
    for required_file in required_runtime_files:
        if not required_file.is_file():
            failures.append(f"required runtime file missing: {required_file.relative_to(SKILL_ROOT)}")

    thread_template_dir = SKILL_ROOT / "project-state-manager" / "templates" / "thread-orchestration"
    thread_template_names = [
        "thread-registry-template.json",
        "child-task-packet-template.json",
        "handoff-template.json",
        "thread-orchestration.schema.json",
    ]
    for template_name in thread_template_names:
        template_path = thread_template_dir / template_name
        if not template_path.is_file():
            failures.append(f"thread orchestration template missing: {template_name}")
            continue
        template_text = template_path.read_text(encoding="utf-8")
        for token in ["schema_version", "project_root"] if "handoff" not in template_name else ["schema_version", "task_id", "status"]:
            if token not in template_text:
                failures.append(f"{template_name}: missing {token}")

    thread_script = SKILL_ROOT / "project-thread-orchestrator" / "scripts" / "manage_thread_registry.py"
    thread_script_text = thread_script.read_text(encoding="utf-8") if thread_script.is_file() else ""
    for token in ["MAX_ACTIVE_HARD_LIMIT = 4", "register-plan", "next-batch", "bind-hub", "bind-thread", "sync-handoff", "mark-stale", "project-manifest.json"]:
        if token not in thread_script_text:
            failures.append(f"manage_thread_registry.py: missing contract token {token}")

    profile_ref = (SKILL_ROOT / "zongkong" / "references" / "deliverable-profiles-and-response-modes.md").read_text(encoding="utf-8")
    tool_ref = (SKILL_ROOT / "zongkong" / "references" / "tool-routing-and-platforms.md").read_text(encoding="utf-8")
    regression_ref = (SKILL_ROOT / "zongkong" / "references" / "regression-checklist.md").read_text(encoding="utf-8")
    seedance_25_ref = (SKILL_ROOT / "prompt-platform-auditor" / "references" / "seedance-2-5.md").read_text(encoding="utf-8")
    gpt_image_25_ref = (SKILL_ROOT / "prompt-platform-auditor" / "references" / "gpt-image-2-5.md").read_text(encoding="utf-8")
    capability_registry_path = SKILL_ROOT / "zongkong" / "references" / "capability-registry.json"
    capability_registry = json.loads(capability_registry_path.read_text(encoding="utf-8")) if capability_registry_path.is_file() else {}
    capability_ids = [entry.get("capability_id") for entry in capability_registry.get("capabilities", [])]
    capability_owners = [entry.get("owner") for entry in capability_registry.get("capabilities", [])]
    internal_compatibility = capability_registry.get("internal_compatibility_skills", [])
    scenario_contracts = {
        "direct image ends without same-turn QC": all(token in texts["builtin-imagegen-director"] for token in ["qc_mode:none", "do not append a QC line"]),
        "named platform prompt uses lightweight compilation": "lightweight platform compilation" in tool_ref,
        "graphic/LED avoids photographic defaults": all(token in profile_ref for token in ["graphic_abstract", "camera brand, focal length, skin realism, mother-library cinematography", "distance readability"]),
        "typography uses glyph/alpha profile": all(token in profile_ref for token in ["typography_asset", "exact glyphs", "transparency"]),
        "video default rejects music but allows SFX": all(token in texts["ai-video-prompt-director"] for token in ["ending_behavior", "audio_mode", "music_policy", "no_music_allow_sfx", "允许与画面动作同步的自然环境声和物理音效"]),
        "explicit music overrides video default": all(token in texts["prompt-platform-auditor"] for token in ["music_requested", "omit the default no-music line", "preserve the requested score"]),
        "full silence overrides SFX allowance": all(token in texts["prompt-platform-auditor"] for token in ["full_silence", "stronger no-audio negative", "do not claim that sound effects are allowed"]),
        "multi-shot has per-shot contract": all(token in texts["ai-video-prompt-director"] for token in ["complexity_mode", "transition or edit motivation", "Do not apply the single-action rule to the whole sequence"]),
        "style lock precedes platform audit": "Never require `$prompt-platform-auditor` as an upstream source" in texts["project-style-lock"],
        "quick variants preserve partial success": all(token in texts["builtin-imagegen-director"] for token in ["shared_invariant_lock", "retry only the failed variant", "preserve every successful image artifact"]),
        "QC writes reusable observations": all("generation_observation" in texts[name] for name in ["image-qc-director", "video-qc-director", "project-state-manager"]),
        "regression checklist covers new profiles": all(token in regression_ref for token in ["正式生成抽象图形LED主视觉", "结尾硬切，不要气口", "同类产品结构漂移连续出现两次"]),
        "thread orchestration shares project and root": all(token in texts["project-thread-orchestrator"] for token in ["target.type: project", "target.environment.type: local", "projectId", "project_root"]),
        "thread orchestration forbids history forks": all(token in texts["project-thread-orchestrator"] for token in ["Never use fork", "Never copy the hub history"]),
        "regression checklist covers thread isolation": all(token in regression_ref for token in ["把12部分稿件放在一个总项目下", "Create at most four child chats", "人物锁修改了，同步分聊天"]),
        "mother library has film and KV routes": all(token in texts["reference-visual-library"] for token in ["film-prestige-visual-library.md", "kv-key-art-case-library.md", "one to two secondary systems", "do not force it onto pure typography"]),
        "regression checklist covers reference expansion": all(token in regression_ref for token in ["给品牌片找更多电影参考", "做发布会产品KV找案例", "纯排版标题资产，不要强塞电影参考"]),
        "ShotDeck is a curation gate not a fame list": all(token in texts["reference-visual-library"] for token in ["presence alone never qualifies", "Core A", "Specialist B", "shotdeck_status: search_recipe_only"]),
        "regression checklist covers ShotDeck curation": all(token in regression_ref for token in ["去ShotDeck给这支品牌片找镜头参考", "这部电影很有名，直接放进母库", "never invent shot links"]),
        "capability registry is deterministic": bool(capability_ids) and len(capability_ids) == len(set(capability_ids)) and all(capability_owners),
        "legacy image controller is internal only": any(entry.get("skill") == "image-generation-controller" and entry.get("implicit_invocation") is False and entry.get("replacement_owner") == "banana-image-generator" for entry in internal_compatibility),
        "OpenAI image prompt compatibility is explicit only": any(entry.get("skill") == "openai-image-prompt-director" and entry.get("implicit_invocation") is False and entry.get("replacement_owner") == "frame-vision-director" for entry in internal_compatibility),
        "prompt semantic ownership is profile-specific": all(item in set(capability_ids) for item in ["generic_frame_prompt_semantics", "kv_image_prompt_semantics", "storyboard_board_prompt_semantics", "typography_prompt_semantics", "video_prompt_semantics"]),
        "complete prompts compile without semantic reconstruction": all(token in texts["zongkong"] + tool_ref for token in ["platform_compile + complete", "Do not recreate the concept", "`prompt_only` does not create project state, QC, or generation"]),
        "regression checklist covers prompt-task routing": all(token in regression_ref for token in ["内容已经定了，只改成可灵格式", "构图不成立，帮我重写并适配 Banana", "不改变画面内容，也不要生成", "直接生成，不要展示提示词"]),
        "regression checklist covers ownership conflicts": all(token in regression_ref for token in ["两个skill都说自己负责出图", "capability-registry.json", "internal compatibility only"]),
        "regression checklist covers non-destructive E2E": all(token in regression_ref for token in ["完整跑一遍工作流测试", "dashboard `--check-only`", "Hash protected manifest/index/registry files"]),
        "GPT Image 2.5 is the new built-in default": all(token in texts["zongkong"] + tool_ref for token in ["model_target:gpt_image_2_5", "new generic built-in", "pinned to GPT Image 2"]),
        "GPT Image 2.5 prompt reference is scoped": all(token in gpt_image_25_ref for token in ["one to three clear natural-language sentences", "one meaningful edit per turn", "Do not switch a user-selected or project-pinned model silently"]),
        "GPT Image 2.5 separates prompt and parameters": all(token in gpt_image_25_ref for token in ["Keep API parameters outside", "Do not write quality parameters into the visual prompt", "set transparent background separately"]),
        "GPT Image 2.5 keeps precise reference roles": all(token in gpt_image_25_ref for token in ["image 1 -> identity", "do_not_inherit", "Do not infer roles from filenames alone"]),
        "GPT Image 2.5 avoids hidden submodel claims": all(token in texts["builtin-imagegen-director"] + gpt_image_25_ref for token in ["Flare", "Sunburst", "never claim"]),
        "regression checklist covers GPT Image 2.5": all(token in regression_ref for token in ["Image 2.5直接出一张电影关键帧", "只换人物衣服", "标题必须准确且只出现一次", "旧项目锁定了GPT Image 2", "透明背景产品PNG"]),
    }
    scenario_contracts.update({
        "paid generation is idempotent and explicit": all(token in regression_ref for token in ["Banana", "idempotency key", "explicit generation confirmation", "Never auto-retry"]),
        "Dreamina execution recovers instead of resubmitting": all(token in regression_ref for token in ["query_result", "jimeng-manual", "submitted/querying"]),
        "technical QC stays evidence-only": all(token in regression_ref for token in ["technical evidence", "music-versus-SFX", "semantic QC"]),
        "short drama uses legal shot state": all(token in regression_ref for token in ["shot production registry", "anchor/hero", "video submission before image approval"]),
        "KV rendition derives from master": all(token in regression_ref for token in ["one master composition", "safe-area overlays", "--check-only"]),
        "platform evidence never silently switches": all(token in regression_ref for token in ["Aggregate project-scoped evidence", "Never silently switch"]),
        "Seedance 2.5 is model-explicit": all(token in tool_ref + seedance_25_ref for token in ["model_target:seedance_2_5", "Never silently upgrade", "platform_target:jimeng"]),
        "Seedance 2.5 maps multimodal references": all(token in seedance_25_ref for token in ["up to 50 multimodal reference assets", "Bind every asset to a named entity", "called per scene"]),
        "Seedance 2.5 stages long video": all(token in seedance_25_ref + regression_ref for token in ["one main observable state change", "observable ending state", "pacing budgets"]),
        "Seedance 2.5 locks source parameters": all(token in seedance_25_ref for token in ["video edit", "inherited from source video", "inherited from first frame", "extension duration"]),
        "Seedance 2.5 keeps no-music SFX policy": all(token in seedance_25_ref for token in ["music_policy:no_music_allow_sfx", "不要配乐、歌曲或人声演唱", "物理音效"]),
        "regression checklist covers Seedance 2.5": all(token in regression_ref for token in ["30秒完整短片", "二十多份人物、商品、动作、场景和声音参考", "unique edit master", "向前/向后延长视频", "首帧、尾帧和多张关键帧", "不要音乐，可以有人声"]),
    })
    for scenario, passed in scenario_contracts.items():
        if not passed:
            failures.append(f"scenario contract failed: {scenario}")

    reference_texts = []
    for owner in ["zongkong", "prompt-platform-auditor"]:
        reference_texts.extend(path.read_text(encoding="utf-8") for path in (SKILL_ROOT / owner / "references").glob("*.md"))
    all_contract_text = combined + "\n" + "\n".join(reference_texts)
    for named in sorted(set(re.findall(r"\$([a-z0-9][a-z0-9-]+)", all_contract_text))):
        if not (SKILL_ROOT / named / "SKILL.md").is_file():
            failures.append(f"named skill is not installed: {named}")

    if failures:
        print("WORKFLOW CONTRACT VALIDATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("WORKFLOW CONTRACT VALIDATION: PASS")
    for name in CORE_SKILLS:
        print(f"- {name}: {len(texts[name].splitlines())} lines")
    print(f"- scenario contracts: {len(scenario_contracts)} passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
