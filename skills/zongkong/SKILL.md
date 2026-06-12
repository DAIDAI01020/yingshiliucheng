---
name: zongkong
description: Top-level production orchestrator for all local AI creative workflows. Use at the start of a new conversation, new project, or ambiguous request to decide project setup, project tier, workflow mode, skill routing, image/video generation route, prompt platform audit, QC, asset management, and next action across film, promo, short-drama, image, video, and workflow tasks.
---

# Zongkong

## Core Role

`$zongkong` is the highest-level entry skill. It sits above all film, short-drama, image, video, and asset skills.

It decides:

- Project tier: formal, quick, or misc.
- Project folder: create or reuse.
- Workflow mode: proposal, short drama, storyboard, commercial KV, poster/key art, typography PNG asset, image, video, review, archive.
- Main route: commercial/promo line or short-drama/story line.
- Required director skills.
- Whether prompt work is needed before generation.
- Whether platform audit is needed before execution.
- Whether QC, review board, or asset indexing is needed after generation.

Keep the workflow fast. Do not turn every task into a long ceremony.

## Project Tiers

| Tier | Use case | Default handling |
| --- | --- | --- |
| 正式项目 | 客户项目、片名明确、长期制作、成组镜头、交付需求 | 建独立项目目录，建立风格圣经，记录资产和版本 |
| 快速项目 | 主题明确但规模小，少量图/视频或快速提案 | 可建轻量项目目录，保留关键 prompt 和输出路径 |
| 杂项目/_misc | 测试模型、单图、临时视频、随手试 prompt | 放入 `H:\yingshi\projects\_misc\`，轻量 QC |

Project paths:

```text
Formal/quick: H:\yingshi\projects\{projectSlug}\
Misc: H:\yingshi\projects\_misc\
```

Project folder contract:

```text
Before creating files for a new project, continuing a managed project, or running any generation that writes multiple files, route through `$project-folder-director` to produce `project_folder_contract` and `output_path_rule`.
Do not let downstream director, prompt, image, video, or layout skills write project files directly into `H:\yingshi\`.
For quick/misc work that creates more than one file, use `H:\yingshi\projects\_misc\{YYYYMMDD}_{shortSlug}\` instead of dumping files into the workspace root.
If user says files are messy, outputs are scattered, or asks to organize a project folder, use `$project-folder-director` first; it must produce a visible move plan before `$asset-librarian` or `$project-state-manager` ingest.
```

Ask only if project tier is blocking:

```text
这是正式项目，还是先放到杂项目测试池？
```

## Speed / Quality Routing

Before routing to downstream skills, classify the speed mode. Preserve quality by using the right amount of workflow, not by forcing the heaviest route every time.

```text
prompt_only: user only needs one copyable prompt, Kling/Omini/Jimeng wording, a single-shot motion instruction, or a quick rewrite. Route directly to the prompt director. Do not require project state, mother-library packets, platform audit, manifest, or QC.
quick_test: user wants to test one image/video/shot, try a model, or preview motion. Keep necessary reference-role, subject-preservation, platform-risk, and audio constraints. Use lightweight platform checking only when it prevents obvious failure.
formal_managed: user explicitly says formal project, batch, delivery, project-state ingest, style-lock inheritance, manifest, QC, client asset, or continuing a managed project. Use full state, mother-library, style-lock, audit, generation record, and QC.
```

Default triggers:

```text
"给我可灵提示词" / "Omini提示词" / "单镜头" / "先试一下" / "只要提示词" -> prompt_only or quick_test.
"批量" / "正式项目" / "交付" / "入项目状态" / "写manifest" / "做QC" / "继续项目目录" -> formal_managed.
When unclear, prefer the lighter mode and say that formal gates can be added if this is a batch/managed deliverable.
```

Quality floor:

```text
prompt_only must still include subject action, camera movement, ending frame, key forbidden items, and audio policy.
quick_test must still protect reference-image roles, subject/product structure, first-frame fidelity, and platform-specific failure risks.
formal_managed must pass project-intake / style-lock / scene-map / shot-audit / prompt-audit / generation-ready.
```

## Route Output Contract

Before any long explanation or downstream handoff, `$zongkong` must output or preserve a compact `zongkong_route_packet`. This packet is mandatory for all speed modes. `project_intake_packet` is attached only for `formal_managed` work or when the user explicitly asks for formal state.

```text
zongkong_route_packet
speed_mode: prompt_only / quick_test / formal_managed
project_tier: formal / quick / misc / undecided
workflow_mode: proposal / short_drama / storyboard / commercial_kv / poster_key_art / typography_png_asset / image / video / product_ai_video / review / archive
main_line: commercial_promo / short_drama_story / other
platform_target: built_in_image / Banana / Banana Pro / Jimeng / Kling / Kling O1 / Kling VIDEO 3.0 Omni / Seedance / Ark / Midjourney / layout / none
next_skill:
missing_fields:
route_reason:
```

Fast-path handling:

```text
prompt_only -> output zongkong_route_packet, route directly to the prompt owner, and do not create project_intake_packet, platform audit, manifest, QC, or project state unless the user asks.
quick_test -> output zongkong_route_packet, keep the route marked quick_test, use only constraints needed for this test, and do not backfill formal state gates before the test.
formal_managed -> output zongkong_route_packet, then create or check project_intake_packet and required upstream state before prompt writing or generation.
```

## P0 Workflow Contract Gate

For `formal_managed` projects, `$zongkong` must create or check a `project_intake_packet` before routing to prompt writing or generation. Do not create this packet for `prompt_only` or `quick_test` work unless the user explicitly asks for formal project state.

```text
project_intake_packet
project_tier: formal / quick / misc
project_folder_contract:
output_path_rule:
workflow_mode: proposal / short_drama / storyboard / commercial_kv / poster_key_art / typography_png_asset / image / video / product_ai_video / review / archive
deliverable_type:
main_line: commercial_promo / short_drama_story / other
reference_source: user_reference_image / user_named_reference / mother_library_recommendation / existing_project_lock / none
mother_library_route:
platform_target: built_in_image / Banana / Banana Pro / Jimeng / Kling / Kling O1 / Kling VIDEO 3.0 Omni / Seedance / Ark / Midjourney / layout
required_upstream:
available_upstream:
missing_fields:
next_skill:
quick_test_flag: true / false
speed_mode: prompt_only / quick_test / formal_managed
```

Hard rule:

```text
formal_managed + missing_fields -> route back to next_skill
quick_test -> may continue when quick_test_flag is true; skipped formal upstream fields are not blockers for the test
formal_managed generation -> allowed only after audited_prompt_packet and generation_ready_packet exist
prompt_only -> no project_intake_packet or audit required unless the user asks
project_tier: formal alone does not trigger full gates; speed_mode: formal_managed does
```

`$zongkong` does not ask downstream prompt or generation skills to fill missing reference, scene, shot, style-lock, platform, or state decisions.

For managed formal short-drama projects, `$zongkong` must use `$project-state-manager` as the state gate before prompt writing, regeneration, or execution:

```text
Route through `$project-state-manager` to initialize/check state. If a direct command is required, resolve `scripts\manage-project-state.mjs` from the `$project-state-manager` skill directory, not from `$zongkong` or the workspace root.
```

If `check` returns `ready: false`, route to `routeBackTo` and preserve `missingFields`. Do not continue from memory or from a single project's old prompt notes.

## Two Main Lines

Route work into one of two main lines:

```text
商业宣传线：品牌片 / 宣传片 / TVC / 活动开场 / LED / 节目包装 / 社媒切条
剧情短剧线：短剧 / 微短剧 / 竖屏剧情 / 横屏剧情短片 / 连续分集
```

Do not use the same reference logic for both. Commercial/promo work and short drama have different aesthetics, structure, and success criteria.

## Commercial / Promo Line

Use for:

```text
品牌片、企业宣传片、城市宣传片、招商片、TVC、产品广告、
活动开场片、发布会开场、LED大屏、节目包装、社媒切条
```

Default route:

```text
brief-analyzer
-> concept-director
-> yingshisheji
-> specialist director
-> style-reference-director（先定项目级/章节级参考风格）
-> reference-visual-library（商业/宣传片母库）
-> reference-aesthetic-director（商业/宣传片参考）
-> scene-style-map-director（按章节/场景/地点分配视觉策略）
-> style-bible-director
-> script-writer / storyboard-planner
-> pitch-deck-director
-> frame-vision-director / ai-video-prompt-director
-> prompt-platform-auditor
-> generation tool
-> image-qc-director / asset-librarian
```

Specialist director routing:

| Intent | Route |
| --- | --- |
| 企业/城市/品牌宣传片 | `$brand-film-director` |
| 产品广告/TVC | `$tvc-director` |
| 活动/发布会/晚会开场 | `$event-opener-director` |
| LED大屏/舞美视觉 | `$led-screen-director` |
| 节目/综艺/栏目包装 | `$program-promo-director` |
| 社媒切条/预热视频 | `$social-cutdown-director` |

P1 handoff rule:

```text
Specialist directors do not produce final image/video prompts by themselves.
For formal projects they output or preserve upstream_handoff_packet, including upstream_source, reference route, scene/story function, platform target, missing_fields, and route_back_to.
Downstream prompt directors inherit the handoff instead of inventing concept, reference, style, or shot logic.
```

Commercial/promo reference logic:

```text
Top TVC, Apple, Nike/Wieden+Kennedy, Mercedes/Porsche/BMW,
BBC/Netflix documentary, Guinness Surfer, Honda Cog,
Moment Factory, Es Devlin, Olympic-scale stage visuals,
top brand manifesto films, engineering/city documentaries.
```

Commercial/promo success criteria:

```text
品牌主张清楚
客户表达可讲
产品/工程/城市可信
视觉记忆点强
空间规模准确
节奏和落版明确
PPT可整理
```

## Short Drama / Story Line

Use for:

```text
短剧、微短剧、竖屏剧情、横屏剧情短片、连续分集、
人物关系戏、悬疑案件、家庭伦理、都市情感、复仇爽剧
```

Default route for full development:

```text
short-drama-director
-> short-drama-concept-writer
-> short-drama-character-bible
-> short-drama-episode-writer
-> short-drama-dialogue-doctor
-> short-drama-scene-director
-> style-reference-director（先定全剧/场戏参考风格）
-> reference-visual-library（电影/精品剧母库）
-> reference-aesthetic-director（电影/精品剧参考）
-> scene-style-map-director（按场戏/地点/时间/情绪分配视觉策略）
-> shot-language-auditor（审核景别递进、机位焦段和剪辑动机）
-> style-bible-director
-> project-style-lock（锁定固定风格变量和提示词 schema）
-> frame-vision-director / ai-video-prompt-director
-> prompt-platform-auditor
-> generation tool
-> image-qc-director / asset-librarian
```

Short-drama reference hard rule:

```text
If the user provides reference images:
reference-image-style-matcher
-> style-reference-director
-> scene-style-map-director

Reference images are not copied as style. First analyze the image, then match it to the closest mother-library visual mechanism.
```

If the user gives no reference images, formal short-drama projects must still receive:

```text
1 primary short-drama mother-library reference system
1 shared-elite-cinematography anchor
mother-library translation: light direction + space relation + lens psychology + composition blocking + material touch + performance state + AI risk control
```

## Short Drama Speed Routes

Do not run the full short-drama pipeline every time. Choose one of three routes by input state.

| Route | Use when | Required route |
| --- | --- | --- |
| 完整开发模式 | 用户要从概念/人物/分集/剧本开始开发，或正式项目尚无角色/风格/场戏结构 | `short-drama-director -> concept/character/episode/dialogue -> short-drama-scene-director -> reference/style/scene map -> shot-language-auditor -> style-bible -> project-style-lock -> prompts` |
| 已有分镜执行模式 | 用户已经给剧本、分镜、视觉方案、人物参考，目标是出提示词/出图/出视频 | `short-drama-scene-director -> reference-image-style-matcher(if refs) -> scene-style-map-director -> shot-language-auditor -> project-style-lock(reuse or create) -> frame/video prompt -> platform audit` |
| 快速测试模式 | 用户只想测一张图、一个镜头、一个人物动起来，或明确说先试效果 | `reuse project-style-lock if available -> lightweight reference-image-style-matcher(if refs) -> frame/video prompt -> optional lightweight platform check -> generation/prompt` |

Routing rules:

```text
正式短剧默认用 project-state-manager init --workflow short-drama --route storyboard-execution 建立通用状态层。
正式短剧批量生成前必须通过 project-state-manager check --stage generation。
已有稿子/分镜时，不重新跑 concept、episode、dialogue。
已有 project-style-lock 时，不重新定全剧风格，只做场戏或镜头局部变化。
单图/单视频测试放快速测试模式，除非用户明确要求正式流程。
正式批量出图/出视频必须至少经过 scene-style-map、shot-language-auditor、project-style-lock、prompt-platform-auditor。
快速测试可以轻量化，但不能把测试结果直接升级为正式批量风格；正式批量前必须补 project-style-lock、scene-style-map、shot-language-auditor、prompt-platform-auditor。
```

If the user only says "继续出图" or "重出", assume the current route and current style lock from project state; do not restart the full pipeline.

Short-drama reference logic:

```text
Global top cinema, elite cinematography, prestige series,
realist crime/family/emotional/suspense films,
Fincher, Deakins, Villeneuve, Cuarón, Park Chan-wook,
Kore-eda, Bong Joon-ho, Wong Kar-wai,
Mindhunter, True Detective, The Night Of.
```

Short-drama success criteria:

```text
人物关系清楚
角色连续稳定
表演空间可信
场戏调度有张力
悬念和反转成立
每场戏有独立光线/地点/焦段
AI角色一致性可控
```

## Workflow Modes

| Mode | Trigger | Main route |
| --- | --- | --- |
| 方案模式 | 方案、创意、PPT、客户提案 | commercial/promo line or short-drama concept line |
| 短剧完整开发模式 | 从0开发短剧、人物、分集、对白 | full short-drama development route |
| 短剧执行模式 | 已有稿子/分镜/视觉方案，要求提示词、出图、出视频 | compressed short-drama execution route |
| 短剧快速测试模式 | 单张图、单镜头、人物动起来、先试效果 | lightweight style-lock route |
| TVC大段故事板测试模式 | TVC广告、产品广告、剧情包装广告，每一大段故事板，直接给 image 出故事板 | existing director/prompt outputs -> `$storyboard-planner` segment lock -> `$scene-board-image-prompter` -> built-in imagegen |
| 分镜模式 | 分镜、镜头表、执行表 | `$storyboard-planner` / `$short-drama-scene-director` |
| 故事板宫格出图模式 | 已有人物、道具、场景、人物位置、机位、镜头beat，要用内置 image 出一张 production design storyboard board | `$scene-board-image-prompter` -> built-in imagegen |
| 同场戏连续性参考板模式 | 同场戏背景锁、背景连续性参考板、正反打背景控制板、对视/过肩参考板、短剧场景控制板 | `$short-drama-scene-director` scene_continuity_lock -> `$scene-board-image-prompter` short_drama_scene_continuity_board -> built-in imagegen |
| 商业KV模式 | 品牌KV、活动KV、发布会KV、产品KV、产品主视觉、节目主视觉、LED主视觉、key visual、主视觉、banner system | `$kv-director` -> `$kv-image-prompt-director` -> `$prompt-platform-auditor` -> image tool / layout tool |
| 海报/key art模式 | 海报、人物海报、短剧人物海报、短剧封面、电影海报、film key art、社媒封面、缩略图、poster-like narrative cover | `$poster-director` -> `$frame-vision-director` -> `$prompt-platform-auditor` -> image tool / layout tool |
| 字体PNG资产模式 | 参考字体、仿照字体、3D字体、艺术字、标题字、立体字、透明PNG文字、type PNG、title treatment | `$type-png-director` -> `$prompt-platform-auditor` -> image/layout tool |
| 出图模式 | 静帧、关键帧、出图、重出 | prompt_only/quick_test: `$frame-vision-director` -> optional lightweight audit -> image tool；formal_managed: `$frame-vision-director` -> `$prompt-platform-auditor` -> image tool |
| 视频模式 | 出视频、图动起来、一镜到底、可灵/Omini提示词 | prompt_only: `$ai-video-prompt-director` 直接给可复制提示词；quick_test: `$ai-video-prompt-director` -> optional lightweight audit -> video tool；formal_managed: `$ai-video-prompt-director` -> `$prompt-platform-auditor` -> video tool |
| 产品AI视频测试模式 | 产品图动起来、产品视频重绘、山地/车辆/机械动作测试、即梦产品视频、连续反馈修片 | `$product-video-revision-director` when revising feedback -> `$ai-video-prompt-director` -> optional lightweight audit for quick_test / formal audit for formal_managed -> video tool |
| 审片修订模式 | QC、客户反馈、重出建议 | `$image-qc-director` / `$video-qc-director` / `$revision-director` |
| 归档模式 | 整理素材、找版本、交付 | `$asset-librarian` / `$project-state-manager` |

Project folder workflow rule:

```text
New project / continue project / scattered files / output path confusion / "do not put files in the main folder" -> `$project-folder-director` -> `$project-state-manager` / `$asset-librarian`.
`$project-folder-director` creates the folder contract and output path rule; `$asset-librarian` inventories assets after files are already in the right project root.
```

## Reference Library Rule

For formal projects, route through `$style-reference-director` before `$reference-visual-library` and `$reference-aesthetic-director`.

If the user provides reference images, route through `$reference-image-style-matcher` before `$style-reference-director`.

```text
reference images
-> reference-image-style-matcher（视觉解析 + 母库反向匹配）
-> style-reference-director
-> scene-style-map-director
-> frame/video prompt
-> prompt-platform-auditor
```

When no reference image is provided, do not leave the visual route generic. Actively recommend a mother-library route and a cinematography anchor appropriate to the main line, then translate them into executable prompt language.

| Main line | Library route |
| --- | --- |
| 商业宣传线 | `commercial-promo-library.md` + mandatory `shared-elite-cinematography.md` |
| 剧情短剧线 | `short-drama-story-library.md` + mandatory `shared-elite-cinematography.md` |

`$style-reference-director` is the task-facing reference style entry. The library supplies curated sources. `$reference-aesthetic-director` translates the chosen reference into visual principles, style bible input, and AI risks.

Strong mother-library application rule:

```text
Formal projects must output or preserve mother_library_application_packet.
The mother library controls project DNA, scene function, shot execution, and platform risk.
Do not leave it as a passive reference name list.
```

Required fields:

```text
library_route
project_function
primary_reference_family
cinematography_anchor
borrowed_mechanisms
scene_function_rules
do_not_copy
forbidden_drift
prompt_inheritance
```

Hard rule:

```text
Formal image/video work must first output project-level and scene/chapter-level style references.
For formal image/video work, the shared elite cinematography layer is mandatory.
Every reference decision must include one project reference family and one cinematography anchor.
Every formal short-drama reference decision must include mother-library translation:
光线方向、空间关系、焦段心理效果、构图调度、材质触感、人物表演状态、AI风险控制。
Formal image/video prompts without mother_library_application_packet or an equivalent scene-function application rule must route back to style-reference-director / scene-style-map-director / project-style-lock.
```

Scene style mapping rule:

```text
When the user provides a script, storyboard, shot list, reference images, or asks for different scene/location styles,
route through `$scene-style-map-director` before final image/video prompts.
It decides what changes per scene while protecting the unified project DNA.
```

## Prompt and Generation Rule

Image/video generators are execution tools. They do not decide the aesthetic.

Generation is an execution validation step, not the creative exploration center.

## No Lazy Routing Rule

Do not let any formal project jump directly from brief, script, storyboard, reference image, or user taste words to final prompts or generation.

Before any formal route, check `project_intake_packet`. If it is missing, create it first. If `missing_fields` is not empty, route back to the owner named in `next_skill`.

Fast-path exception:

```text
prompt_only is not formal generation. Do not require project_intake_packet, mother_library_application_packet, prompt-platform-auditor, generation_ready_packet, manifest, or QC.
quick_test may continue with missing formal upstream fields when it is clearly marked quick_test and keeps only the constraints needed for this test.
Only formal_managed uses the full No Lazy Routing gate.
```

Before routing formal_managed prompt writing or generation, `$zongkong` must check required upstream outputs:

```text
project-state-manager check result for managed formal short-drama projects
reference / mother-library decision
reference-image-style-matcher result when reference images are used
scene-style-map-director scene map for multi-scene work
shot-language-auditor approval for short-drama or dramatic multi-shot work
project-style-lock for formal project prompt batches
prompt-platform-auditor decision before any execution controller or generation tool
```

If any upstream output is missing, route back to the skill that owns it. Do not ask a downstream skill to invent the missing decision.

Quick/test work may be lightweight, but it must be marked `quick/test` and must not be treated as formal batch execution until the missing upstream outputs are completed.

Formal projects must not use repeated image generation to discover the style. Director decisions, reference matching, scene logic, shot language, style lock, and platform audit must happen before generation.

For short-drama or dramatic multi-shot work, shot logic is mandatory before prompts:

```text
shot-language-auditor
-> frame-vision-director / ai-video-prompt-director
```

Do not output random shot lists. Each shot must have a function, a motivated shot-size change, and a cut/transition reason.

Before formal_managed generation:

1. Check whether a complete prompt exists.
2. If missing, route to the correct director/prompt skill.
3. For formal projects, check whether a current `$project-style-lock` exists after style approval.
4. For short-drama or dramatic multi-shot work, check whether `$shot-language-auditor` has approved the shot logic.
5. Route the completed prompt to `$prompt-platform-auditor`.
6. Use only the audited execution prompt for generation.

For quick_test generation, use a one-pass lightweight platform check only when it protects the effect or avoids obvious platform failure. For prompt_only, do not run platform audit unless the user asks.

Execution controllers may run only from `generation_ready_packet` or an equivalent managed job that contains `final_prompt`, `audit_status`, `target_tool`, `source_lock`, `reference_roles`, and `output_path_rule`. Video execution must also contain `first_frame_or_image_refs` or an approved public URL/local relay path.

Hard rule:

```text
Formal project prompts must not re-invent style wording every turn.
Use project-style-lock as the stable visual DNA, then vary only scene-specific camera, light, composition, and action.
Do not run Banana/MJ/imagegen/Jimeng/Seedance as a substitute for missing director decisions.
Formal image generation defaults to built-in imagegen or Banana/Banana Pro.
Do not use Jimeng as the default formal image route; reserve Jimeng mainly for image-to-video or video prompt handoff unless the user explicitly asks for Jimeng images.
```

Commercial KV / Poster rule:

```text
Commercial KV, poster, and key-art work are not ordinary keyframe generation.
`$kv-director` is the commercial/event KV specialist under `$zongkong`, not a top-level orchestrator.
`$poster-director` is a specialist director under `$zongkong`, not a top-level orchestrator.
`$zongkong` must decide project tier, main line, upstream style/reference requirements, and whether commercial KV or poster/key-art mode is needed before calling either skill.
Route commercial, brand, launch, product, program, event, conference, gala, LED, stage-screen, campaign, key visual, main visual, and banner system requests through `$kv-director` before `$kv-image-prompt-director`.
Route narrative posters, short-drama character posters, 短剧人物海报, film posters, suspense case posters, covers, thumbnails, social covers, and poster-like key art through `$poster-director` before `$frame-vision-director`.
KV/poster generation should usually create no-text base art, character/product/background/object assets, and title-safe or logo-safe layouts; final readable title, slogan, logo, cast names, sponsor marks, QR code, and legal text are added in post layout.
If the user asks to generate stylized title text, 3D type, lettering inspired by a font, or transparent PNG text assets, route that typography asset request to `$type-png-director`; do not ask KV/poster image prompts to generate production text inside the base art.
```

Formal generation gate:

```text
project-style-lock exists
shot has function / shot size / camera angle / focal length / composition / light / color / material / negative prompt
mother-library translation mechanism is present
anti-AI photographic realism is present: real skin texture / fabric wrinkles / life traces / dust or worn objects / real light source / original light ratio / no over-sharpening / no beauty smoothing / no fake HDR
reference image roles are explicit when references are used
prompt-platform-auditor decision is 通过 or 保效精简后通过
short-drama shot logic has passed shot-language-auditor when applicable
```

Video prompt gate for Jimeng / Seedance:

```text
First frame controls image style.
Text controls only one subject action, one camera movement, one subtle environment/light change, and one clear ending frame.
Every short-drama shot defaults to a light breath tail; every segment/scene/emotional-beat ending defaults to a heavier 1-2 second breath tail unless the user asks for hard cut, beat cut, flash cut, or shock point.
```

Product AI video test route / 产品AI视频测试路线:

```text
产品结构参考
-> 场景/比例参考
-> 动作参考
-> 单镜头/多镜头判断
-> ai-video-prompt-director 即梦执行提示词
-> prompt-platform-auditor 即梦平台审查
-> 结果反馈归因：动作错 / 机位错 / 比例错 / 风格AI / 天气假
```

For product image-to-video, vehicle motion, mountain/off-road scenes, mechanical movement, or video redraw tests, default to execution-stable prompts:

```text
one shot
one action
timed action stages
explicit reference image roles
locked product structure and proportions
Jimeng platform audit before generation
```

Platform audit decisions:

| Decision | Action |
| --- | --- |
| 通过 | Generate directly |
| 保效精简后通过 | Use the compact execution prompt |
| 打回重写 | Send back to prompt director |
| 建议拆分 | Split before generation |

Hard rule:

```text
平台审核不是单纯压缩。优先级是：效果保住 > 画面准确 > 平台稳定 > 文字精简。
```

## Tool Routing

| User intent | Route |
| --- | --- |
| 新建工程 / 继续工程 / 项目根目录 / 输出路径 / 文件散落 / 目录混乱 / 不要放总文件夹 / 整理工程但先不移动 | `$project-folder-director` -> `$project-state-manager` / `$asset-librarian` |
| 品牌KV / 活动KV / 发布会KV / 产品KV / 产品主视觉 / 节目主视觉 / LED主视觉 / key visual / 主视觉 / banner system | `$kv-director` -> `$kv-image-prompt-director` -> `$prompt-platform-auditor` -> image/layout tool |
| 海报 / 人物海报 / 短剧人物海报 / 短剧封面 / 电影海报 / film key art / 社媒封面 / 缩略图 / poster-like narrative cover | `$poster-director` -> `$frame-vision-director` -> `$prompt-platform-auditor` -> image/layout tool |
| 参考字体 / 仿照字体 / 3D字体 / 艺术字 / 标题字 / 立体字 / 透明PNG文字 / type PNG / title treatment | `$type-png-director` -> `$prompt-platform-auditor` -> image/layout tool |
| image / image-2 / ChatGPT Image / 内置最新模型 / 直接生成一张 | `$builtin-imagegen-director` + built-in imagegen |
| TVC广告故事板测试 / 每一大段故事板 / 剧情包装广告故事板 / 直接给image出故事板 | quick_test: existing director/prompt outputs -> `$storyboard-planner` tvc_segment_storyboard_lock -> `$scene-board-image-prompter` -> built-in imagegen |
| TVC逐镜出图提示词 / 每个小分镜提示词 / 单独小分镜 image | quick_test: `$storyboard-planner` tvc_shot_prompt_handoff -> `$frame-vision-director` tvc_shot_image_prompt_packet -> image tool；formal_managed only when the user says 批量 / 客户交付 / QC / 入项目状态 |
| 故事板宫格 / 场戏控制板 / production design storyboard board / 人物道具环境机位板 | `$scene-board-image-prompter` -> built-in imagegen |
| 同场戏背景锁 / 背景连续性参考板 / 正反打背景控制板 / 对视过肩参考板 / short-drama continuity board | `$short-drama-scene-director` scene_continuity_lock -> `$scene-board-image-prompter` short_drama_scene_continuity_board -> built-in imagegen |
| Banana / Banana Pro / 重出 / 继续出 / 省token | `$banana-image-generator` / `$image-generation-controller` |
| MJ / Midjourney / Legnext | `$midjourney` |
| 出视频 / 让图动起来 / Seedance / Ark | quick_test: `$ai-video-prompt-director` -> optional lightweight audit -> video tool；formal_managed: `$ai-video-prompt-director` -> `$prompt-platform-auditor` -> `$video-generation-controller` / `$seedance-2-video` |
| 即梦/可灵/Omini提示词 | prompt_only: `$ai-video-prompt-director` 直接输出可复制提示词；formal_managed 才追加 `$prompt-platform-auditor` |
| 可灵 O1 / VIDEO 3.0 Omni 多参考、元素、视频参考、局部编辑、原生音频 | prompt_only/quick_test: `$ai-video-prompt-director` 做最小 reference role map 并给提示词；formal_managed: `$project-state-manager` reference role map / `$scene-board-image-prompter` board cells -> `$ai-video-prompt-director` -> `$prompt-platform-auditor` -> `$video-generation-controller` manual handoff / run manifest -> `$video-qc-director` |
| 产品视频重绘 / 产品图动起来 / 山地车辆动作 / 机械动作测试 / 连续反馈修片 | `$product-video-revision-director` -> `$ai-video-prompt-director` -> optional lightweight audit for quick_test / formal audit for formal_managed |
| 审片/判断图片能不能用 | `$image-qc-director` |
| 审片/判断视频能不能用 / 动作错 / 脸漂 / 主体重绘 / 天气假 | `$video-qc-director` |
| 对比图和提示词 | `$image-review-board` |
| 客户反馈转修改 | `$client-feedback-interpreter` -> `$revision-director` |
| 同步 workflow | `$workflow-sync-manager` |

Formal image routing rule:

```text
内置 imagegen and Banana/Banana Pro are the default image routes for formal projects.
Jimeng is not a default formal image route. Use it for video/image-to-video prompts unless explicitly requested for still-image generation.
```

Formal video platform selection:

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

Video platform packet rule:

```text
Before any formal video generation or external handoff, `$zongkong` must require a `video_platform_prompt_packet` or equivalent fields:
target_platform, task_type, first_frame_or_reference, reference_roles, subject_action, camera_movement, environment_or_light_change, ending_frame, duration, ratio, audio_policy, style_lock_compact, forbidden_items.
manual_execution: external_platform, upload_roles, copyable_prompt, expected_output_path, status.

For O1/Omni, also require `kling_omni_reference_role_map`.
For Seedance/Ark, require public reference URL or approved relay path when images are used.
For Jimeng image-to-video, first frame is the style authority and the prompt text controls motion only.
```

## Post-Generation Rule

After generation:

| Project tier | Handling |
| --- | --- |
| 正式项目 | review board -> image/video QC -> asset-index |
| 快速项目 | preview/path -> short QC -> key record |
| 杂项目 | preview/path -> one-line judgment |

QC decisions:

```text
可用 / 可小修 / 定向重出 / 提示词需重写 / 前置导演判断错误
```

Regeneration rule:

```text
普通生成失败只定向修正：构图、人物、手、文字、光线、平台味、风格漂移。
只有“前置导演判断错误”才回到风格参考、场戏地图或 project-style-lock。
Do not rewrite the whole project style because one generated image failed.
```

Asset states:

```text
候选 / 入选 / 待重出 / 待修图 / 待修片 / 废稿
```

## Guardrails

- Do not print API keys or tokens.
- Do not commit, push, or sync workflow changes unless the user explicitly asks.
- Do not delete generated outputs unless the user explicitly asks.
- Before changing workflow, skills, agents, project templates, or state scripts, explain the intended change, affected files/skills, formal-vs-quick impact, complexity risk, and rollback/scope-down path, then wait for user confirmation unless the user has explicitly requested that exact implementation in the current turn.
- Prefer improving a specific agent behavior first, such as Kling video prompts, mother-library routing, image prompts, QC, or regeneration advice. Be conservative with global zongkong rules, state gates, templates, and scripts.
- Keep formal projects and quick tests separate: formal projects may use full state/mother-library/style-lock/audit/QC; quick tests must stay lightweight and must not be blocked by formal batch gates.
- Do not route built-in image requests to removed OpenAI API scripts.
- Do not route MJ requests through Banana or built-in imagegen.
- Do not route Banana tasks through MJ.
- Prefer execution when the user asks for action; ask only when missing information blocks the task.
