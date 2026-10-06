# Tool Routing And Platforms

Use this reference when `$zongkong` has classified the speed mode and needs the detailed execution route or platform selection.

## Contents

- Routing precedence
- Tool routing
- Image/storyboard generation gates
- Image platform boundaries
- Video platform selection
- Managed video handoff packet

## Routing Precedence

Use the independent action, platform/model, and creative-state precedence in [the Zongkong decision order](../SKILL.md#decision-order). Resolve execution intent before matching a platform row below. Platform names, credentials, project tier, and existing assets do not authorize generation by themselves.

“直接用 image 出图” means execute through the built-in image route. “给我出图提示词” means route to the image prompt owner. “重出/继续出” inherits the current project platform; it is not a new generic-platform decision.

## Tool Routing

| User intent | Route |
| --- | --- |
| Blender / 已有.blend / 可编辑三维模型或场景 / 建模材质灯光 / 骨骼动画 / 几何节点 / 三维模拟渲染 | `$blender-production-director` -> actual environment/scene inspection -> applicable 3D modules -> versioned scene and verified outputs；plan stays plan；rendered is not QC-approved；a 3D-looking AI image alone stays on its image route |
| 新建工程 / 继续工程 / 项目根目录 / 输出路径 / 文件散落 / 目录混乱 / 不要放总文件夹 / 整理工程但先不移动 | `$project-folder-director` -> `$project-state-manager` / `$asset-librarian` |
| 大稿件多部分 / 一个总项目拆多个聊天 / 上下文隔离 / 分聊天并行 / 总控汇总 / 同步分聊天 | explicit separate-chat request -> project/root and director split -> `$project-thread-orchestrator` with authorization for the concrete plan -> same-project local child threads (max 4)；reuse existing registered tasks for continuation/status；a split proposal alone creates no chats |
| 品牌KV / 活动KV / 发布会KV / 产品KV / 产品主视觉 / 节目主视觉 / LED主视觉 / key visual / 主视觉 / banner system | `$kv-director` -> `$kv-image-prompt-director` -> `$prompt-platform-auditor` -> image/layout tool |
| 已有方案/PPT/创意方向，下一步做KV或大屏KV | preserve approved proposal -> `$kv-director` proposal_to_kv_packet -> large-screen experience packet when needed -> `$kv-image-prompt-director` -> `$prompt-platform-auditor` -> image/layout tool |
| 海报 / 人物海报 / 短剧人物海报 / 短剧封面 / 电影海报 / film key art / 社媒封面 / 缩略图 / poster-like narrative cover | `$poster-director` -> `$frame-vision-director` -> `$prompt-platform-auditor` -> image/layout tool |
| 参考字体 / 仿照字体 / 3D字体 / 艺术字 / 标题字 / 立体字 / 透明PNG文字 / type PNG / title treatment | `$type-png-director` -> `$prompt-platform-auditor` -> image/layout tool |
| 已有提示词 / 优化提示词 / 改成某平台格式 / 精简但不改变内容 | first classify `source_prompt_state` and `prompt_task`; complete semantics + platform-only adaptation -> `$prompt-platform-auditor` directly；creative/visible/motion repair -> applicable semantic owner -> optional platform compilation；`prompt_only` does not create project state, QC, or generation |
| image / ChatGPT Image / ChatGPT Images 2.5 / GPT Image 2.5 / Image 2.5 / 内置最新模型 / 直接生成一张 / 直接用 image 出图 | new work defaults to `platform_target:built_in_image` + `model_target:gpt_image_2_5`; quick_test by default: `$builtin-imagegen-director` `direct_image_preflight_check` -> Images 2.5 prompt branch -> built-in imagegen；do not claim Flare/Sunburst unless exposed；successful generation ends with the image result；`qc_mode:none` stops, `light_deferred/formal` reviews separately |
| image-2 / GPT Image 2 / 旧版内置Image | preserve `model_target:gpt_image_2` when explicitly requested or inherited; use the built-in route without applying Images 2.5-only assumptions |
| image故事板 / 直接给image出故事板 / 广告故事板 / TVC广告故事板 / 产品广告故事板 / 品牌广告故事板 / 节目宣传故事板 / 活动开场故事板 / 整张喂即梦/Seedance/Kling / 人物道具环境机位板 / 角色道具场景设定板 / production design storyboard board | quick_test: `$image-storyboard-workflow` -> `$image-storyboard-director` director_scene_breakdown + image_storyboard_design_packet(s) -> `$scene-board-image-prompter` one prompt per board_unit -> built-in imagegen one image per passed board_unit |
| 每一大段故事板 / 章节 beat 整理 / 剧情包装广告故事板 | quick_test: `$image-storyboard-workflow` large_segment_board -> optional `$storyboard-planner` tvc_segment_storyboard_lock -> `$image-storyboard-director` director_scene_breakdown + image_storyboard_design_packet(s) -> `$scene-board-image-prompter` one prompt per board_unit -> built-in imagegen one image per passed board_unit |
| TVC逐镜出图提示词 / 每个小分镜提示词 / 单独小分镜 image | quick_test: `$image-storyboard-workflow` -> `$storyboard-planner` tvc_shot_prompt_handoff -> `$frame-vision-director` tvc_shot_image_prompt_packet -> image tool；formal_managed only when the user says 批量 / 客户交付 / QC / 入项目状态 |
| 故事板宫格 / 场戏控制板 | `$image-storyboard-workflow` -> `$scene-board-image-prompter` -> built-in imagegen |
| 同场戏背景锁 / 背景连续性参考板 / 正反打背景控制板 / 对视过肩参考板 / short-drama continuity board | `$image-storyboard-workflow` -> `$short-drama-scene-director` scene_continuity_lock -> `$scene-board-image-prompter` short_drama_scene_continuity_board -> built-in imagegen |
| Banana / Banana Pro / 用Banana出图 / Banana批量出图 / Banana重出 / 继续Banana出图 | generation intent -> `$banana-image-generator`；prompt-only intent -> semantic owner when needed, then `$prompt-platform-auditor`；“省token” alone does not select or change a platform |
| MJ / Midjourney / Legnext | generation intent -> `$midjourney`；prompt-only intent uses its prompt workflow without submission |
| 出视频 / 让图动起来 / Seedance / Ark | quick_test: `$ai-video-prompt-director` -> optional lightweight audit -> video tool；formal_managed: `$ai-video-prompt-director` -> `$prompt-platform-auditor` -> `$video-generation-controller` / `$seedance-2-video` |
| 即梦/可灵/Omini提示词 | prompt_only: `$ai-video-prompt-director` source packet -> `$prompt-platform-auditor` lightweight platform compilation -> direct copyable prompt；no project intake/QC/state；formal_managed uses the full applicable audit/state handoff |
| 可灵 API Key / 配置可灵 API / 可灵 API 连通测试 | `$kling-api` -> private local credential file outside `skills/` and Git -> optional free live authentication check；never treat key setup as paid-generation approval |
| 可灵 O1 / VIDEO 3.0 Omni 多参考、元素、视频参考、局部编辑、原生音频 | prompt_only/quick_test: `$ai-video-prompt-director` 做最小 reference role map 并给提示词；formal_managed: `$project-state-manager` reference role map / `$scene-board-image-prompter` board cells -> `$ai-video-prompt-director` -> `$prompt-platform-auditor` -> `$video-generation-controller` manual handoff / run manifest -> `$video-qc-director` |
| 产品视频重绘 / 产品图动起来 / 山地车辆动作 / 机械动作测试 / 连续反馈修片 | `$product-video-revision-director` -> `$ai-video-prompt-director` -> optional lightweight audit for quick_test / formal audit for formal_managed |
| 审片/判断图片能不能用 | `$image-qc-director` |
| 审片/判断视频能不能用 / 动作错 / 脸漂 / 主体重绘 / 天气假 | `$video-qc-director` |
| 对比图和提示词 | `$image-review-board` |
| 客户反馈转修改 | `$client-feedback-interpreter` -> `$revision-director` |
| 同步 workflow | `$workflow-sync-manager` |

Image故事板出图门槛：

```text
For image故事板 routes, do not call built-in imagegen until `image_storyboard_workflow_packet`, `director_scene_breakdown`, `image_storyboard_design_packet`, and `$scene-board-image-prompter` `pre_generation_check: passed` exist. image故事板 includes TVC ads, product ads, brand ads, program promos, event openers, brand films, commercial story scenes, standalone production boards, and same-scene continuity boards. If `board_unit_count > 1`, default to `multi_board_series`: one design packet, one precheck, one prompt, and one output image per board_unit. Do not collapse multi-board work into one image unless the user explicitly asks for a single master overview board.
```

## Image Routing

Explicit Blender or editable 3D requirements take precedence over generic image/video/3D-text rows. Blender rendering uses its own task and scene checks, not AI image/video prompt gates. Preserve an existing film/KV/stage creative owner while Blender owns scene implementation. Rendering a first frame does not by itself authorize AI-video submission.

Quick multi-variant image rule:

```text
Two to four requested outputs that share one reference/space/style and differ only by a controlled camera, crop, pose, or element change remain one quick_test.
Build one shared_invariant_lock and one variant_delta per output.
Run one preflight and one orchestration turn; use the minimum internal imagegen calls needed to return separate requested images.
Do not create a project folder or repeat route commentary merely because requested_image_count > 1.
Retry a failed variant once only for transient_service or empty_result. Preserve successful variants, report the failed variant concisely, and stop after the retry limit.
```

Formal image routing rule:

```text
内置 imagegen and Banana/Banana Pro are the default image routes for formal projects.
Jimeng is not a default formal image route. Use it for video/image-to-video prompts unless explicitly requested for still-image generation.

Banana and built-in imagegen are separate user-facing skills. Banana routes only to `$banana-image-generator`; image / image-2 / ChatGPT Image / 内置 image routes only to `$builtin-imagegen-director` plus built-in imagegen. Never silently fall back between them. `$image-generation-controller` is only a legacy internal compatibility wrapper.

For new built-in work, `image`, `ChatGPT Image`, and `内置最新模型` use the migrated `model_target:gpt_image_2_5`. A continuation with an explicit or inherited GPT Image 2/older lock remains on that model. The prompt compiler loads `gpt-image-2-5.md` only for the 2.5 branch. Direct built-in execution does not imply that Flare or Sunburst is selectable; API submodel and parameter claims require an execution surface that exposes them.
```

## Formal Video Platform Selection

```text
Jimeng:
Use for first-frame image-to-video, quick motion tests, short controlled actions, and external/manual platform execution. Best when the first frame already carries the look.

Jimeng / Seedance 2.5:
Use only when the user/current project explicitly selects Seedance 2.5. Route semantic motion to `$ai-video-prompt-director`, then `$prompt-platform-auditor` with `model_target:seedance_2_5` and its dedicated platform reference. Use its long-stage, multimodal-reference, local-edit, extension, keyframe, white-model, montage, or transition modes only when that task actually applies.

Seedance / Ark:
Use for formal API-driven video generation, logged batch work, first-frame or first-last-frame generation, public reference URL workflows, and runs that need project-state ingestion.

Kling:
Use for physically continuous single-shot motion when the task is simple and does not need many references.

Kling O1:
Use for strongly referenced single shots, element insertion/replacement, local video edit, start/end frame control, and short controlled motion.

Kling VIDEO 3.0 Omni:
Use for multi-reference continuity, video reference, multi-shot storyboard, native audio, character/element consistency, and professional reference-driven work. Require a reference role map before prompting.
```

Project-managed Jimeng/Kling/Kling O1/Kling VIDEO 3.0 Omni runs are usually external/manual platform executions. Before the user uploads to the platform, write or preserve a `run_manifest.json` handoff through `$video-generation-controller` so the approved prompt, reference roles, audio policy, output path rule, and later downloaded video can be ingested by `$project-state-manager`.

## Video Platform Packet Rule

```text
Before formal AI video generation or external AI-platform handoff, `$zongkong` must require a `video_prompt_source_packet` plus an approved `audited_prompt_packet`, or equivalent fields:
platform_target, model_target when selected, task_type, task_mode when model-specific, complexity_mode, source_authority, must_preserve, reference_roles/reference_asset_map, do_not_inherit, subject_action_or_beats/stage_plan, camera_behavior, environment_or_light_change, ending_behavior, edit/boundary/locked-parameter fields when applicable, duration, ratio, audio_mode when applicable, style_lock_compact, risk_profile.
manual_execution: external_platform, upload_roles, copyable_prompt, expected_output_path, status.

For O1/Omni, also require `kling_omni_reference_role_map`.
For Seedance/Ark, require public reference URL or approved relay path when images are used.
For Jimeng image-to-video, first frame is the style authority and prompt text focuses on motion and ending behavior.
For Seedance 2.5, require its model-specific audit reference and do not pass ratio/duration overrides prohibited by source-locked task modes.
```

Apply the first-frame rule only when a first-frame/image-to-video task actually exists. Text-to-video and approved start/end-frame tasks use their own fields. Ending behavior, audio mode, and multi-reference behavior are shot/task decisions owned by `$ai-video-prompt-director` and compiled by `$prompt-platform-auditor`; they are not global defaults.

## Managed Execution Safety And Recovery

```text
Banana / Banana Pro paid execution
-> `$banana-image-generator` computes an idempotency key before submission
-> require explicit generation confirmation and, when known, a sufficient credit estimate
-> reuse the completed result for the same key
-> never auto-resubmit an uncertain or failed paid job
-> retry only through explicit `--resume`, limited to recorded failed shot IDs
-> ingest the run and outputs into managed project state

Jimeng / Dreamina CLI execution
-> `$video-generation-controller` calls `$dreamina-cli` through the local adapter
-> inspect live CLI help and credits/session before a new paid submission
-> persist `submit_id` and the run manifest as soon as the platform accepts the job
-> use `query_result` recovery for submitted/querying jobs; do not submit again
-> if the official CLI is unavailable, produce a same-platform `jimeng-manual` handoff and state that no video was generated
```

An explicit current generation request or existing approval covering this concrete run satisfies generation confirmation; do not add a duplicate confirmation step. Check its prompt/reference version, requested outputs, platform, and cost scope before reuse. Prompt-only approval, credential setup, and status inspection do not satisfy it.

The controller must never report an external handoff, a queued task, or a `submit_id` as a generated video. A downloaded and validated output path is required for `generated` or `success`.

## Shot Production And KV Rendition Routing

```text
formal multi-shot short drama
-> scene/character/style/shot locks
-> `$project-state-manager` shot production registry
-> anchor and hero shots first
-> image prompt -> image generated -> image approved
-> video submitted -> video generated -> technical QC -> semantic QC -> accepted
-> dependencies and continuation inheritance block illegal skips

approved multi-ratio KV
-> approve one master composition
-> `$kv-director` builds the 16:9 / 9:16 / 4:5 / 1:1 rendition matrix
-> derive crops and safe-area overlays from the master
-> when the subject cannot fit safely, flag manual recomposition
-> do not generate unrelated compositions independently for each ratio
```

## Technical Evidence Before Semantic QC

For saved formal outputs, route images through `$image-qc-director` technical inspection and videos through `$video-qc-director` technical inspection before the director-level semantic judgment. Technical scripts may report dimensions, hashes, clipping, black/frozen frames, audio levels, duration, and contact sheets; they must not decide story intent, performance quality, or whether audio is music versus sound effects.
