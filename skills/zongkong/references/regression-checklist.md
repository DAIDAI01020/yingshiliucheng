# Regression Checklist

Use this checklist after editing `$zongkong` or downstream route boundaries.

## Contents

- Smoke scenarios
- Boundary checks
- Structural checks
- Executable contract validation

## Smoke Scenarios

1. `直接用 image 出图`
   - Expected route: `quick_test` or `prompt_only` as appropriate.
   - Must perform `direct_image_preflight_check`.
   - Must generate through `$builtin-imagegen-director`.
   - On success, must end with the generated image result; run QC only in a later turn or separate review workflow.

2. `只要即梦提示词`
   - Expected route: `prompt_only`.
   - Must preserve compressed style/reference/platform judgment.
   - Must not create project intake, manifest, QC, or asset index unless requested.

3. `正式短剧批量出图`
   - Expected route: `formal_managed`.
   - Must require project state, scene map, shot audit, project style lock, prompt platform audit, and generation-ready packet.
   - Must not downgrade to `quick_test`.

4. `formal_managed but missing style lock`
   - Must output `missing_fields`.
   - Must route back to `project-style-lock` or the owning upstream style skill.
   - Must not let prompt or generation skills invent a new style.

5. `QC says generated image failed`
   - Must classify failure cause.
   - Ordinary generation problems get targeted regeneration.
   - Only style-lock or director-logic failures route upstream.

6. `Kling O1 / Omni multi-reference prompt`
   - `prompt_only` / `quick_test`: minimal reference role map is enough.
   - `formal_managed`: require reference role map, platform audit, and manual handoff / run manifest.

7. `files are scattered`
   - Route to `$project-folder-director` first.
   - Do not move/delete files without a visible plan and user approval.

8. `给我一条静帧出图提示词`
   - Expected route: `prompt_only`.
   - Route to the applicable image prompt owner, not directly to imagegen.
   - Must not require video-only fields such as ending frame or audio policy.

9. `做一套正式发布会抽象LED主视觉`
   - Expected route: `formal_managed`, `commercial_kv`, or the appropriate LED/KV route.
   - Must require screen/layout-safe constraints and applicable reference/style decisions.
   - Must not force skin texture, dust, worn objects, hook audit, or character continuity.

10. `正式生成透明背景3D标题字PNG`
    - Expected route: `formal_managed`, `typography_png_asset`.
    - Require glyph accuracy, legibility, transparency, edge quality, platform audit, and managed output path.
    - Must not require scene map, shot audit, mother-library cinematography, or photoreal live-action controls by default.

11. `继续用Banana重出上一张`
    - Preserve the current Banana platform, approved prompt source, reference roles, style lock, and output path.
    - Do not route to built-in imagegen or restart style development.

12. `正式短剧批量出图，但没有角色连续性锁`
    - Expected route: `formal_managed`.
    - `missing_fields` must identify character continuity.
    - `route_back_to` must be `$short-drama-character-bible`.

13. `正式短剧开场没有hook audit`
    - `route_back_to` must be `$short-drama-episode-writer`.
    - Must not route the missing hook to a prompt or generation skill.

14. `一个无人物的正式产品单图`
    - Require the applicable product structure/material/composition gate.
    - Must not require hook audit, character continuity, scene map, or shot audit.

15. `出图` with no platform, no current state, and no direct/prompt wording
   - Infer from nearby context when safe.
   - Clarify only if platform choice materially changes execution or output storage.
   - Never silently switch platforms after a route is established.

16. `保持这个空间不变，用 image 出两个机位：右下低机位、右上高机位`
    - Expected route: one built-in imagegen `quick_test`, not `formal_managed`.
    - Must create one shared invariant lock and two variant deltas.
    - Must perform one preflight and one orchestration turn without repeated route narration or project-folder setup.
    - Must return two separate requested image outputs rather than merging the two camera views into one image unless the user asks for a comparison board.

17. `两个 quick_test 变体中一个生成失败`
    - Preserve any successful image result.
    - Retry only the failed variant, once, and only for `transient_service` or `empty_result`.
    - After the retry limit, return a concise per-variant failure result and stop; do not enter an open-ended retry loop.

18. `正式生成抽象图形LED主视觉`
    - `deliverable_profile: graphic_abstract` or `led_stage` with the applicable secondary profile.
    - Require shape/palette/density/screen-safe/distance-readability controls.
    - Must not require camera brand, focal length, aperture, skin realism, or mother-library cinematography by default.

19. `给我一条内置Image的人物关键帧提示词`
    - `speed_mode: prompt_only`, `response_mode: direct`, no project state or QC.
    - `$frame-vision-director` creates the semantic source; `$prompt-platform-auditor` performs lightweight built-in compilation.
    - User sees only the final copyable prompt.

20. `即梦图生视频，结尾硬切，不要气口，平台不生成音频`
    - `deliverable_profile: video_i2v`, `ending_behavior: hard_cut`, `audio_mode: unsupported`, `music_policy: no_music_allow_sfx`.
    - Must not append breath wording. The negative prompt must still reject music while allowing synchronized natural ambience and physical SFX.

21. `可灵Omni生成4镜连续场景`
    - `complexity_mode: multi_shot`.
    - Require per-shot duration, framing, action, camera behavior, transition motivation, ending state, and reference roles.
    - Must not reject merely because the entire sequence has more than one action or camera move.

22. `正式产品单图，平台为Banana`
    - Style lock may use `product_structure` extension without mother-library, skin realism, scene map, shot audit, breath, or audio fields.
    - Platform target comes from `$zongkong`; style lock must not require a prior prompt audit.

23. `内置image快速出图成功`
    - `qc_mode:none` ends with the image result.
    - `qc_mode:light_deferred` schedules/recommends a separate QC pass; never appends QC after the image in the same response.

24. `同类产品结构漂移连续出现两次`
    - Write two linked `generation_observation` records.
    - A repeated relevant failure may be promoted to the product risk profile or style lock after confirmation.
    - A single failure must not rewrite the project style.

25. `给我一条视频提示词，没有说明音频`
    - Default `music_policy: no_music_allow_sfx`.
    - `negative_or_forbidden` must include `不要背景音乐、配乐、歌曲或人声演唱；允许与画面动作同步的自然环境声和物理音效。`

26. `视频需要史诗配乐和环境音效`
    - Explicit music overrides the default with `music_policy: music_requested`.
    - Preserve the requested score and omit the default no-music negative.

27. `视频完全静音`
    - Use `music_policy: full_silence` and `audio_mode: none`.
    - Prohibit all audio and do not say that sound effects are allowed.

## Boundary Checks

For any downstream skill touched by a change, confirm:

```text
inherits zongkong_route_packet when present
does not change speed_mode/project_tier/workflow_mode/formal gates
does not downgrade formal_managed to quick_test
does not invent missing upstream decisions outside its domain
returns missing_fields + route_back_to when blocked
requires only gates applicable to the deliverable
preserves explicit/current platform over generic trigger words
inherits deliverable_profile/response_mode/qc_mode
uses ending_behavior/audio_mode conditionally and defaults music_policy to no_music_allow_sfx
keeps platform policy in prompt-platform-auditor references
normalizes packet fields to snake_case at the state boundary
```

## Structural Checks

```text
all modified SKILL.md files stay under 500 lines
every reference file is linked directly from SKILL.md
detailed route tables have one source of truth
all named skill references resolve to an installed skill folder
frontmatter contains only name and description
agents/openai.yaml matches the speed-mode and visibility behavior in SKILL.md
```

## Executable Contract Validation

Run after changing the orchestration, prompt, style-lock, QC, state, or folder boundaries:

```powershell
python C:\Users\admin\.codex\skills\zongkong\scripts\validate_workflow_contracts.py
```

The script checks core line limits, required packet fields, direct reference links, named-skill resolution, removed blanket rules, style-lock/auditor order, platform-policy ownership, and configurable project-root language.
