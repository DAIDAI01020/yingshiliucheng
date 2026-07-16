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

```text
explicit platform
> continue current project platform/route
> direct generation request
> prompt-only request
> formal batch/delivery request
> generic image/video wording
```

“直接用 image 出图” means execute through the built-in image route. “给我出图提示词” means route to the image prompt owner. “重出/继续出” inherits the current project platform; it is not a new generic-platform decision.

## Tool Routing

| User intent | Route |
| --- | --- |
| 新建工程 / 继续工程 / 项目根目录 / 输出路径 / 文件散落 / 目录混乱 / 不要放总文件夹 / 整理工程但先不移动 | `$project-folder-director` -> `$project-state-manager` / `$asset-librarian` |
| 品牌KV / 活动KV / 发布会KV / 产品KV / 产品主视觉 / 节目主视觉 / LED主视觉 / key visual / 主视觉 / banner system | `$kv-director` -> `$kv-image-prompt-director` -> `$prompt-platform-auditor` -> image/layout tool |
| 已有方案/PPT/创意方向，下一步做KV或大屏KV | preserve approved proposal -> `$kv-director` proposal_to_kv_packet -> large-screen experience packet when needed -> `$kv-image-prompt-director` -> `$prompt-platform-auditor` -> image/layout tool |
| 海报 / 人物海报 / 短剧人物海报 / 短剧封面 / 电影海报 / film key art / 社媒封面 / 缩略图 / poster-like narrative cover | `$poster-director` -> `$frame-vision-director` -> `$prompt-platform-auditor` -> image/layout tool |
| 参考字体 / 仿照字体 / 3D字体 / 艺术字 / 标题字 / 立体字 / 透明PNG文字 / type PNG / title treatment | `$type-png-director` -> `$prompt-platform-auditor` -> image/layout tool |
| image / image-2 / ChatGPT Image / 内置最新模型 / 直接生成一张 / 直接用 image 出图 | quick_test by default: `$builtin-imagegen-director` `direct_image_preflight_check` -> built-in imagegen；successful generation ends with the image result；`qc_mode:none` stops, `light_deferred/formal` reviews separately；formal_managed only when batch/delivery/state requirements are explicit |
| image故事板 / 直接给image出故事板 / 广告故事板 / TVC广告故事板 / 产品广告故事板 / 品牌广告故事板 / 节目宣传故事板 / 活动开场故事板 / 整张喂即梦/Seedance/Kling / 人物道具环境机位板 / 角色道具场景设定板 / production design storyboard board | quick_test: `$image-storyboard-workflow` -> `$image-storyboard-director` director_scene_breakdown + image_storyboard_design_packet(s) -> `$scene-board-image-prompter` one prompt per board_unit -> built-in imagegen one image per passed board_unit |
| 每一大段故事板 / 章节 beat 整理 / 剧情包装广告故事板 | quick_test: `$image-storyboard-workflow` large_segment_board -> optional `$storyboard-planner` tvc_segment_storyboard_lock -> `$image-storyboard-director` director_scene_breakdown + image_storyboard_design_packet(s) -> `$scene-board-image-prompter` one prompt per board_unit -> built-in imagegen one image per passed board_unit |
| TVC逐镜出图提示词 / 每个小分镜提示词 / 单独小分镜 image | quick_test: `$image-storyboard-workflow` -> `$storyboard-planner` tvc_shot_prompt_handoff -> `$frame-vision-director` tvc_shot_image_prompt_packet -> image tool；formal_managed only when the user says 批量 / 客户交付 / QC / 入项目状态 |
| 故事板宫格 / 场戏控制板 | `$image-storyboard-workflow` -> `$scene-board-image-prompter` -> built-in imagegen |
| 同场戏背景锁 / 背景连续性参考板 / 正反打背景控制板 / 对视过肩参考板 / short-drama continuity board | `$image-storyboard-workflow` -> `$short-drama-scene-director` scene_continuity_lock -> `$scene-board-image-prompter` short_drama_scene_continuity_board -> built-in imagegen |
| Banana / Banana Pro / 用Banana出图 / Banana批量出图 / Banana重出 / 继续Banana出图 / 省token | `$banana-image-generator` |
| MJ / Midjourney / Legnext | `$midjourney` |
| 出视频 / 让图动起来 / Seedance / Ark | quick_test: `$ai-video-prompt-director` -> optional lightweight audit -> video tool；formal_managed: `$ai-video-prompt-director` -> `$prompt-platform-auditor` -> `$video-generation-controller` / `$seedance-2-video` |
| 即梦/可灵/Omini提示词 | prompt_only: `$ai-video-prompt-director` source packet -> `$prompt-platform-auditor` lightweight platform compilation -> direct copyable prompt；no project intake/QC/state；formal_managed uses the full applicable audit/state handoff |
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
```

## Formal Video Platform Selection

```text
Jimeng:
Use for first-frame image-to-video, quick motion tests, short controlled actions, and external/manual platform execution. Best when the first frame already carries the look.

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
Before any formal video generation or external handoff, `$zongkong` must require a `video_prompt_source_packet` plus an approved `audited_prompt_packet`, or equivalent fields:
platform_target, task_type, complexity_mode, source_authority, must_preserve, reference_roles, do_not_inherit, subject_action_or_beats, camera_behavior, environment_or_light_change, ending_behavior, duration, ratio, audio_mode when applicable, style_lock_compact, risk_profile.
manual_execution: external_platform, upload_roles, copyable_prompt, expected_output_path, status.

For O1/Omni, also require `kling_omni_reference_role_map`.
For Seedance/Ark, require public reference URL or approved relay path when images are used.
For Jimeng image-to-video, first frame is the style authority and prompt text focuses on motion and ending behavior.
```

Apply the first-frame rule only when a first-frame/image-to-video task actually exists. Text-to-video and approved start/end-frame tasks use their own fields. Ending behavior, audio mode, and multi-reference behavior are shot/task decisions owned by `$ai-video-prompt-director` and compiled by `$prompt-platform-auditor`; they are not global defaults.
