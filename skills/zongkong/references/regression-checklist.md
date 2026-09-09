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

28. `把12部分稿件放在一个总项目下，拆到不同聊天`
    - Route to `$project-thread-orchestrator` only after a director-level semantic split and one user confirmation.
    - Every child must use the same saved Codex `projectId`, local environment, and project root.
    - Create at most four child chats; keep the remainder queued until slots and dependencies allow.
    - Never use a fork, projectless thread, different project, or worktree.

29. `只是一条连续短稿，但字很多`
    - Do not split merely by length.
    - Keep it in one chat when deliverable, references, approval path, and revision ownership remain coherent.

30. `总项目的人物锁修改了，同步分聊天`
    - List affected registered child tasks and ask for one confirmation.
    - Broadcast only a versioned context delta to confirmed affected thread IDs.
    - Mark affected existing results stale; refresh queued packets without marking them stale; preserve unaffected tasks.

31. `把以前的几个聊天直接并入总控`
    - List same-project candidates first and require explicit task binding confirmation.
    - Do not import raw history or trust a result until the adopted child emits a standard handoff.

32. `给品牌片找更多电影参考`
    - Route through `film-prestige-visual-library.md` and the shared cinematography layer.
    - Select one primary reference, at most two problem-specific secondary references, and one cinematography anchor.
    - Return mechanism translation and `do_not_copy`; final prompts must not contain a film/director/cinematographer name dump.

33. `做发布会产品KV找案例`
    - Route through `kv-key-art-case-library.md`, then `$kv-director` retains composition/style authority.
    - Select one primary case mechanism and at most two supporting mechanisms; preserve product truth, title/logo safe area, crop behavior, and screen extensions.
    - Do not copy an exact campaign layout, logo, product, type system, or studio signature treatment.

34. `纯排版标题资产，不要强塞电影参考`
    - Route to `$type-png-director` and the applicable typography/layout anchor.
    - Do not force film, cinematography, or KV case references unless cinematic base art is separately requested.

35. `去ShotDeck给这支品牌片找镜头参考`
    - Treat ShotDeck as a shot-level research interface, not automatic proof that every indexed title belongs in the mother library.
    - Start from project function and craft attributes; default to `Core A`, and use `Specialist B` only for a named gap.
    - If authenticated ShotDeck access was not actually inspected, return `shotdeck_status: search_recipe_only`; never invent shot links or a deck.

36. `这部电影很有名，直接放进母库`
    - Reject fame-only admission. Score cinematography distinction, shot retrievability, transferability, functional coverage, craft evidence, and anti-copy safety.
    - Keep sub-threshold or unverified titles out of formal recommendations; duplicate mechanisms are rejected even when the title is celebrated.

37. `两个skill都说自己负责出图，随便选一个`
    - Resolve ownership from `capability-registry.json`; do not improvise a second owner.
    - New Banana work routes to `$banana-image-generator`, built-in image work to `$builtin-imagegen-director`, and the legacy `$image-generation-controller` remains internal compatibility only.
    - Supporting skills may add prompt, state, review, or QC inputs but must not silently replace the execution owner.

38. `完整跑一遍工作流测试，但不要改开学第一课原文件`
    - Run the disposable E2E fixture for formal gates, dry-run image ingest, repeated-ingest idempotency, QC feedback proposals, manual video handoff reuse, dashboard output, and capability ownership.
    - Audit `H:\开学第一课` only through read-only project audit and dashboard `--check-only`.
    - Hash protected manifest/index/registry files before and after; any change is a test failure.

39. `同一批 Banana 付费任务重复执行，或者执行中断后继续`
    - Compute the same idempotency key and reuse a completed run instead of paying twice.
    - Require explicit generation confirmation before a new paid submission.
    - Never auto-retry an uncertain/failed paid job; explicit resume runs only recorded failed shot IDs.

40. `直接调用即梦 CLI 出视频；CLI 不在时也继续`
    - Inspect live CLI help and credits/session before submission, persist `submit_id`, and recover through `query_result`.
    - When the official CLI is unavailable, emit a truthful `jimeng-manual` handoff; never claim that a video was generated.
    - A submitted/querying task is not success until a validated downloaded output exists.

41. `自动审这张图和这段视频`
    - Produce deterministic technical evidence and a contact sheet first.
    - Keep story intent, acting, brand accuracy, and music-versus-SFX judgment with semantic QC; scripts must not invent those decisions.

42. `短剧十几个镜头直接一起出图出视频`
    - Initialize the shot production registry, validate dependencies, and schedule anchor/hero shots before coverage.
    - Prevent illegal transition skips, especially video submission before image approval.
    - Preserve continuation inheritance and project-root path containment.

43. `一张主 KV 自动适配横竖方三个比例`
    - Approve one master composition, compute deterministic crops and safe-area overlays, and create previews.
    - `--check-only` must write nothing.
    - Ratios that cannot contain the locked subject/brand zones require manual recomposition, not independent redesign.

44. `根据生成历史自动换到表现更好的平台`
    - Aggregate project-scoped evidence by platform/model and expose it as a proposal.
    - Never silently switch the user's explicit or current platform and never turn project evidence into an unsupported global rule.

45. `用即梦 Seedance 2.5 做一条30秒完整短片`
    - Preserve `platform_target:jimeng` and `model_target:seedance_2_5`; do not silently apply the model to generic Jimeng work.
    - Organize connected events into stages with one main change and one observable ending state per stage.
    - Treat time ranges as pacing budgets, not frame-accurate edit points.

46. `我上传二十多份人物、商品、动作、场景和声音参考，一起做视频`
    - Map every asset to a named entity/property plus its `do_not_inherit` boundary, then group references by type and call only needed assets per scene.
    - Do not make all uploaded references appear simultaneously and do not rely on image labels to infer roles.
    - Validate documented count/duration limits before approval while treating current platform help as execution authority.

47. `编辑原视频，只换4到7秒右墙灯光，其他都不动`
    - Declare the source video as the unique edit master, define one exact delta and bounded time/region, and preserve all non-target content and timeline relationships.
    - Reject ratio or duration overrides because video edit inherits those values from the source.
    - Do not promise pixel-identical preservation.

48. `向前/向后延长视频`
    - Bind the correct source boundary, camera/light/sound/motion trend, and explicitly prevent later assets from appearing early in forward extension.
    - Preserve the source ratio and set only a live-supported extension duration.

49. `用首帧、尾帧和多张关键帧控制视频`
    - Map first and end frames separately, require compatible aspect ratios, and make intermediate frames ordered visible states.
    - Other reference images may provide attributes but must not replace the anchor-frame compositions.

50. `即梦2.5不要音乐，可以有人声、环境声和动作音效`
    - Keep `music_policy:no_music_allow_sfx` and compile the Seedance sound syntax only where it adds control.
    - Do not suppress requested dialogue, ambience, Foley, machinery, footsteps, or impacts.

51. `这条提示词内容已经定了，只改成可灵格式`
    - Use `prompt_task:platform_compile` and `source_prompt_state:complete`.
    - Route directly to `$prompt-platform-auditor`; do not reconstruct the image or motion concept through a semantic owner.
    - Keep `speed_mode:prompt_only`; do not create project state, QC, or generation.

52. `这条出图提示词构图不成立，帮我重写并适配 Banana`
    - Use `prompt_task:prompt_diagnose` or `targeted_rewrite` with `source_prompt_state:creatively_incomplete`.
    - Route the composition repair to the applicable semantic image-prompt owner, then compile for Banana.
    - Do not let `$prompt-platform-auditor` invent the missing composition.

53. `精简这条提示词，不改变画面内容，也不要生成`
    - Preserve the locked semantic source and use `prompt_task:targeted_rewrite`.
    - Route wording-only compaction to `$prompt-platform-auditor` when a platform is named; otherwise use the applicable semantic owner without changing meaning.
    - Return only the rewritten prompt and do not generate.

54. `直接生成，不要展示提示词`
    - Use `prompt_task:none` at the user-facing routing layer and route to the selected execution owner.
    - Keep any prompt construction internal unless semantic repair is blocking.
    - Do not print the prompt before or after a successful generation result.

55. `用Image 2.5直接出一张电影关键帧`
    - Use `platform_target:built_in_image` and `model_target:gpt_image_2_5`, then route through `$builtin-imagegen-director`.
    - Load the dedicated GPT Image 2.5 prompt branch and lead with the exact frozen moment before style language.
    - Do not claim that Flare or Sunburst was selected unless the live execution surface exposes it.

56. `Image 2.5只换人物衣服，脸、姿势、背景和光线都不动`
    - Use one precision-edit delta and an explicit preservation lock for identity, pose, framing, background, light, and non-target elements.
    - Assign every clothing or identity reference a numbered role and a `do_not_inherit` boundary.
    - Do not promise pixel-identical preservation; use the latest accepted result for the next edit and change one meaningful element per turn.

57. `用Image 2.5做KV，标题必须准确且只出现一次`
    - Quote the exact copy, state occurrence count, position, hierarchy, font character, and no-extra-text control.
    - Keep product geometry, focal hierarchy, negative space, and title/logo-safe zones in the semantic source.
    - Keep model, quality, size, background, and output format outside the visual prompt.

58. `新项目只说image，但旧项目锁定了GPT Image 2`
    - New generic built-in work uses the migrated `model_target:gpt_image_2_5` default.
    - Continuation of the pinned legacy project preserves `model_target:gpt_image_2` until the user explicitly asks to migrate.
    - Never treat the platform migration as permission to switch Banana, Midjourney, Jimeng, or another established route.

59. `Image 2.5生成透明背景产品PNG`
    - Request an isolated centered product with clean alpha edges in prompt semantics and set transparency/output format separately on the execution surface.
    - Reject a drawn checkerboard as transparency and inspect hair/glass/shadows/labels/edge fringing when applicable.
    - Do not promise native transparency unless the selected live execution surface exposes it.

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
classifies prompt_task independently from speed_mode
routes a complete supplied prompt directly to platform compilation when only platform wording changes
routes semantic/directorial repairs to the deliverable-specific prompt owner before platform compilation
keeps direct-generation prompts internal when the user asks not to show them
inherits deliverable_profile/response_mode/qc_mode
uses ending_behavior/audio_mode conditionally and defaults music_policy to no_music_allow_sfx
keeps platform policy in prompt-platform-auditor references
normalizes packet fields to snake_case at the state boundary
requires idempotency and explicit confirmation for new paid submissions
recovers submitted video tasks by submit_id before any resubmission
keeps technical QC evidence separate from semantic/directorial judgment
uses a legal per-shot production state chain for formal multi-shot execution
derives multi-ratio KV renditions from one approved master composition
keeps Seedance 2.5 as an explicit model_target under the selected Jimeng or Ark execution surface
maps each Seedance 2.5 reference to a named role instead of uploading an undifferentiated asset pile
uses one observable state change and ending state per long-video stage
respects source-locked ratio/duration behavior for edit, anchor-frame, and extension tasks
keeps GPT Image 2.5 as a model_target under built_in_image and preserves pinned legacy image models
uses one-delta precision edits, numbered reference roles, exact-text controls, and parameter separation for GPT Image 2.5
does not claim Flare/Sunburst selection when the built-in execution surface hides the submodel
```

## Structural Checks

```text
all modified SKILL.md files stay under 500 lines
every reference file is linked directly from SKILL.md
detailed route tables have one source of truth
all named skill references resolve to an installed skill folder
capability registry gives every reusable capability one owner and keeps compatibility wrappers out of implicit user-facing routes
frontmatter contains only name and description
agents/openai.yaml matches the speed-mode and visibility behavior in SKILL.md
zongkong agents/openai.yaml names execution_intent, prompt_task, speed_mode, deliverable_profile, prompt_only visibility, and the platform compiler
internal compatibility skills disable implicit invocation in both capability-registry.json and their agents/openai.yaml
thread orchestration uses one projectId, one root, clean create_thread packets, and no fork
thread registry tests cover max-four queue, dependencies, stale broadcasts, path guards, and handoffs
```

## Executable Contract Validation

Run after changing the orchestration, prompt, style-lock, QC, state, or folder boundaries:

```powershell
python C:\Users\admin\.codex\skills\zongkong\scripts\validate_workflow_contracts.py
python C:\Users\admin\.codex\skills\zongkong\scripts\run_e2e_workflow_tests.py --compat-project-root "H:\开学第一课"
```

The script checks core line limits, required packet fields, direct reference links, named-skill resolution, removed blanket rules, style-lock/auditor order, platform-policy ownership, and configurable project-root language.
