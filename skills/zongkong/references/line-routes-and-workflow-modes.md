# Line Routes And Workflow Modes

Use this reference when `$zongkong` has to choose the main creative line, detailed workflow mode, or specialist director route.

## Contents

- Two main lines
- Commercial/promo route
- Short-drama/story route
- Short-drama speed routes
- Workflow modes
- Image-storyboard splitting
- Project-folder workflow

## Two Main Lines

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

Default route for full formal cinematic/multi-scene development. Use the shorter profile-specific KV, typography, graphic, LED, product, image, or video route when the deliverable does not need every stage:

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
-> hook audit owned by short-drama-episode-writer when the opening/episode requires it
-> character continuity owned by short-drama-character-bible when recurring characters apply
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

Formal short-drama production gates are conditional and have explicit owners:

```text
hook audit -> short-drama-episode-writer
character continuity -> short-drama-character-bible
scene/background continuity -> short-drama-scene-director
shot logic -> shot-language-auditor
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

Apply these gates only when relevant. Do not require a new hook audit for an isolated scene that does not include the episode opening, and do not require character continuity when no character recurs.

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
| 方案转KV模式 | 已有方案、已有PPT、创意已通过，下一步做主KV/大屏KV | preserve approved proposal -> `$kv-director` proposal_to_kv_packet -> `$kv-image-prompt-director` -> `$prompt-platform-auditor` -> image/layout tool |
| 短剧完整开发模式 | 从0开发短剧、人物、分集、对白 | full short-drama development route |
| 短剧执行模式 | 已有稿子/分镜/视觉方案，要求提示词、出图、出视频 | compressed short-drama execution route |
| 短剧快速测试模式 | 单张图、单镜头、人物动起来、先试效果 | lightweight style-lock route |
| Image故事板独立工作流模式 | image故事板、广告故事板、TVC广告、产品广告、品牌广告、节目宣传、活动开场、品牌片、整张喂即梦/Seedance/Kling、人物道具场景设定板、人物动线机位图、production design storyboard board | `$image-storyboard-workflow` -> `$image-storyboard-director` director_scene_breakdown + image_storyboard_design_packet(s) -> `$scene-board-image-prompter` one prompt per board_unit -> built-in imagegen one image per passed board_unit |
| TVC大段/商业段落整理变体 | 每一大段故事板、章节 beat 整理、剧情包装广告故事板、已有长脚本要先整理大段 | `$image-storyboard-workflow` large_segment_board -> optional `$storyboard-planner` segment lock -> `$image-storyboard-director` director_scene_breakdown + image_storyboard_design_packet(s) -> `$scene-board-image-prompter` one prompt per board_unit -> built-in imagegen one image per passed board_unit |
| 分镜模式 | 分镜、镜头表、执行表 | `$storyboard-planner` / `$short-drama-scene-director` |
| 故事板宫格出图模式 | 已有人物、道具、场景、人物位置、机位、镜头beat，要用内置 image 出一张 production design storyboard board | `$image-storyboard-workflow` -> `$scene-board-image-prompter` -> built-in imagegen |
| 同场戏连续性参考板模式 | 同场戏背景锁、背景连续性参考板、正反打背景控制板、对视/过肩参考板、短剧场景控制板 | `$image-storyboard-workflow` same_scene_continuity_board -> `$short-drama-scene-director` scene_continuity_lock -> `$scene-board-image-prompter` short_drama_scene_continuity_board -> built-in imagegen |
| 商业KV模式 | 品牌KV、活动KV、发布会KV、产品KV、产品主视觉、节目主视觉、LED主视觉、key visual、主视觉、banner system | `$kv-director` -> `$kv-image-prompt-director` -> `$prompt-platform-auditor` -> image tool / layout tool |
| 海报/key art模式 | 海报、人物海报、短剧人物海报、短剧封面、电影海报、film key art、社媒封面、缩略图、poster-like narrative cover | `$poster-director` -> `$frame-vision-director` -> `$prompt-platform-auditor` -> image tool / layout tool |
| 字体PNG资产模式 | 参考字体、仿照字体、3D字体、艺术字、标题字、立体字、透明PNG文字、type PNG、title treatment | `$type-png-director` -> `$prompt-platform-auditor` -> image/layout tool |
| 出图模式 | 静帧/关键帧提示词、需要先完成画面导演判断、正式批量出图 | generic prompt_only: `$frame-vision-director`；named-platform prompt_only: `$frame-vision-director` -> lightweight `$prompt-platform-auditor` -> direct prompt；quick_test requiring direction: same source/compile route -> image tool；formal_managed: source packet -> platform audit -> generation-ready -> image tool。若用户明确要求直接用某平台生成，按 tool-routing reference 的 direct-generation route；“重出”继承当前项目平台与 route。 |
| 视频模式 | 出视频、图动起来、一镜到底、可灵/Omini提示词 | `$ai-video-prompt-director` always owns motion semantics；named-platform prompt_only/quick_test uses lightweight `$prompt-platform-auditor` compilation without formal state；formal_managed uses full applicable audit -> generation-ready -> video tool |
| 产品AI视频测试模式 | 产品图动起来、产品视频重绘、山地/车辆/机械动作测试、即梦产品视频、连续反馈修片 | `$product-video-revision-director` when revising feedback -> `$ai-video-prompt-director` -> optional lightweight audit for quick_test / formal audit for formal_managed -> video tool |
| 审片修订模式 | QC、客户反馈、重出建议 | `$image-qc-director` / `$video-qc-director` / `$revision-director` |
| 归档模式 | 整理素材、找版本、交付 | `$asset-librarian` / `$project-state-manager` |

Image故事板导演拆分规则：

```text
`$image-storyboard-director` must actively split story material into real directing units before board design. Split by scene function, location/set geography, camera axis, blocking/movement path, prop interaction, and emotional turns. Duration is advisory only; do not hard-cut by a fixed second count, and do not compress several directing units into one board.
Image故事板 includes TVC ads, product ads, brand ads, program promos, event openers, brand films, commercial story scenes, standalone production boards, and same-scene continuity boards. If `board_unit_count > 1`, default to `multi_board_series`: one design packet, one precheck, one prompt, and one output image per board_unit. A single master overview board is allowed only when explicitly requested and cannot replace the split narrative boards.
Generation is allowed only after `image_storyboard_workflow_packet`, `director_scene_breakdown`, `image_storyboard_design_packet`, and `$scene-board-image-prompter` `pre_generation_check: passed` exist. If any are missing, route back instead of calling imagegen.
```

Project folder workflow rule:

```text
New project / continue project / scattered files / output path confusion / "do not put files in the main folder" -> `$project-folder-director` -> `$project-state-manager` / `$asset-librarian`.
`$project-folder-director` creates the folder contract and output path rule; `$asset-librarian` inventories assets after files are already in the right project root.
```
