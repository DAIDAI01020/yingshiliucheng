# 影视 AI 总工作流

## 0. 总原则

这套 workflow 不是单纯的工具集合，而是一套影视 AI 制作流水线。

核心原则：

```text
总控决定路线
导演决定审美与叙事
专项导演决定片种方法
提示词导演负责可生成画面
平台审核负责工具适配与效果保真
生成工具只负责执行
QC/资产层负责收口
```

新增硬原则：

```text
每个导演必须贡献自己负责的判断。
母库必须转译成可见画面机制。
提示词里的每句话必须真的帮助画面。
```

## 0.1 工作 Agent 持续优化规则

后续优化 `H:\yingshi` 影视 AI 工作 agent 时，默认采用“先解释、再确认、后修改”的方式。

改动前必须先说明：

```text
要改哪一个 agent / skill / workflow 文件
为什么要改
影响正式项目还是快速测试
是否会让流程变慢、变复杂
如果不合适如何回退或收缩
```

优化优先级：

```text
优先优化具体 agent 行为：可灵出视频、母库调用、出图提示词、QC、重出建议
慎改全局总控、状态门、项目模板、脚本逻辑
只有当规则对整个正式流程明显有益时，才升级为 workflow 规则
```

正式项目和快速测试必须分开：

```text
正式项目可以走完整状态、母库、风格锁、审核、QC
快速测试只保留必要约束，不强制完整状态门
单镜头 / 单图 / 单条可灵提示词不能被正式流程卡死
```

已有方向可以作为正式 workflow 升级基础；如果某条规则让流程变笨，应收缩到“正式项目专用”，不要压到 quick/test。

## 0.2 质量与速度分层规则

工作流必须先判断速度模式，再决定是否启用完整正式门槛。目标是：正式项目保质量，普通提示词和单镜头测试保速度。

```text
prompt_only：用户只要一条可复制提示词、可灵/Omini/即梦提示词、单镜头动作描述。直接输出，不强制项目状态、母库包、平台审核或 manifest。
quick_test：用户要先试效果、单图、单视频、小样、临时测试。保留必要的画面/动作/参考约束，可做轻量平台检查，但不强制完整状态门。
formal_managed：用户明确说正式项目、批量、交付、入项目状态、继承 style-lock、写 manifest、做 QC 或继续托管项目。启用完整状态、母库、风格锁、审核、生成记录和 QC。
```

默认判断：

```text
单条提示词 / 单镜头 / “给我可灵提示词” / “Omini提示词” / “先试一下” -> prompt_only 或 quick_test
成组镜头 / 客户交付 / 正式项目 / 批量出图出视频 / 要写入项目目录 -> formal_managed
不确定时，先按较轻模式推进，并提示“如果这是正式批量，我再补完整门槛”。
```

质量底线：

```text
prompt_only 也必须保留主体动作、镜头运动、结束画面、关键禁止项和音频规则。
quick_test 也必须保留参考图角色边界、主体结构、画面保真和平台风险控制。
formal_managed 必须走 project-intake / style-lock / scene-map / shot-audit / prompt-audit / generation-ready。
```

## 1. 总入口

所有新项目、新对话、模糊任务先进入：

```text
$zongkong
```

`$zongkong` 判断：

| 判断项 | 结果 |
| --- | --- |
| 项目层级 | 正式项目 / 快速项目 / 杂项目 |
| 项目类型 | 宣传片 / TVC / 活动开场 / LED / 节目包装 / 短剧 / 单图测试 / 视频测试 |
| 当前模式 | 方案 / 分镜 / 出图 / 视频 / 审片修订 / 归档 |
| 是否已有项目目录 | 没有则创建 |
| 是否已有合格提示词 | 没有则先走导演和提示词层 |
| 应该调用哪些 skill | 按下面双主线分流 |

项目目录：

```text
正式/快速项目：H:\yingshi\projects\{projectSlug}\
杂项目：H:\yingshi\projects\_misc\
```

正式短剧项目默认使用项目状态层，不绑定单个专项项目：

```powershell
node .\skills\project-state-manager\scripts\manage-project-state.mjs init --project-name "项目名" --workflow short-drama --route storyboard-execution
node .\skills\project-state-manager\scripts\manage-project-state.mjs check --project-root H:\yingshi\projects\project --stage generation
```

正式/托管/批量生成前 `check` 必须通过；否则按 `routeBackTo` 回到对应 skill。`prompt_only` 和 `quick_test` 不强制状态门，除非用户要求写入正式项目或继续正式批量。

## 2. 双主线结构

当前工作流分成两条主线：

```text
商业宣传线：品牌片 / 宣传片 / TVC / 活动开场 / LED / 节目包装 / 社媒切条
剧情短剧线：短剧 / 微短剧 / 竖屏剧情 / 横屏剧情短片 / 连续分集
```

两条线共享：

```text
reference-image-style-matcher
reference-visual-library
style-reference-director
reference-aesthetic-director
scene-style-map-director
style-bible-director
frame-vision-director
ai-video-prompt-director
prompt-platform-auditor
image-qc-director
asset-librarian
project-state-manager
```

但它们的参考审美、拆解逻辑、PPT表达、镜头方法不同，不能混用一套标准。

## 3. 商业宣传线

适用：

```text
品牌片 / 企业宣传片 / 城市宣传片 / 招商片 / TVC / 产品广告 /
活动开场片 / 发布会开场 / LED大屏 / 节目包装 / 社媒切条
```

标准流程：

```text
brief-analyzer
-> concept-director
-> yingshisheji
-> 专项导演
-> reference-image-style-matcher（如有参考图，先做视觉解析和母库反向匹配）
-> style-reference-director（先定项目级/章节级参考风格）
-> reference-visual-library（商业/宣传片母库 + 必选顶级摄影层）
-> reference-aesthetic-director（商业/宣传片参考 + 摄影锚点转译）
-> scene-style-map-director（按章节/场景/地点分配视觉策略）
-> style-bible-director
-> script-writer / storyboard-planner
-> pitch-deck-director
-> frame-vision-director / ai-video-prompt-director
-> prompt-platform-auditor
-> 生成工具
-> image-qc-director / asset-librarian
```

Image故事板独立工作流路线：

```text
用户提出 image故事板 / 直接给 image 出故事板 / 整张喂即梦或Seedance / 人物道具环境机位板
-> image-storyboard-workflow 产出 image_storyboard_workflow_packet
-> image-storyboard-director 先产出 image_storyboard_design_packet
-> scene-board-image-prompter 做 pre_generation_check
-> pre_generation_check: passed 后才允许内置 imagegen
```

使用场景：

```text
image故事板
直接给 image 出故事板
整张喂即梦/Seedance/Kling
人物道具场景设定板
人物动线机位图
production design storyboard board
```

规则：

```text
默认 quick_test，不强制状态门、母库包、平台审核或 QC。
image-storyboard-workflow 先判断 workflow_variant、source_type、board_type、是否整张喂即梦/Seedance/Kling，以及 video_reference_inherit / video_reference_do_not_inherit。
image故事板覆盖 TVC广告、产品广告、品牌广告、节目宣传、活动开场、品牌片、商业剧情和短剧同场连续性板；不要因为是广告/产品就绕出这个 workflow。
默认 board_type 是 production_design_storyboard_board，不是普通分镜预览。
image-storyboard-director 必须先按真实导演逻辑主动拆场戏/段落/节拍单元，再想清楚人物、服装、道具、场景、人物动线、视线、俯视机位图、节拍执行流、关键帧预览和灯光材质参考。
拆分不按固定秒数硬切，时长只是辅助判断；优先按场景功能、空间地理、机位轴线、人物调度、道具互动和情绪转折拆。
一张板只服务一个可执行场戏或短节拍单元；不能把完整剧情、多个转折或多个空间轴线都塞进一张图。
如果 director_scene_breakdown 产生多个 board_unit，默认输出 multi_board_series：每个 board_unit 单独 image_storyboard_design_packet、单独 pre_generation_check、单独内置 image prompt、单独一张图。只有用户明确要“总览板/只要一张 master board”时，才允许单张 overview，并且不能替代分段叙事板。
scene-board-image-prompter 只把 image_storyboard_design_packet 翻译成内置 imagegen 提示词，不重新设计人物道具场景。
出图前必须通过 pre_generation_check：必须有 director_scene_breakdown、image_storyboard_design_packet、明确 board_unit、九个板块、连续性控制和视频参考继承边界。检查不通过就打回对应 skill，不允许直接出图。
整张板必须能防止多角色视频生成中的位置不对、视线不对、人物消失、道具消失和空间漂移。
如果用户要求“每个小分镜提示词 / 单独小分镜出图 / 逐镜出图提示词”，再从 image_storyboard_design_packet 的 shot_preview_list 切到 frame-vision-director 输出逐镜自包含 image prompt。
```

TVC / 产品广告 / 商业宣传 image故事板路线：

```text
已有导演/提示词输出
-> image-storyboard-workflow 判断 source_type: tvc / product_demo / program_promo / event_opener / brand_film / other_commercial
-> 可选 storyboard-planner 轻整理大段 beat（仅当用户明确要大段/章节 beat 整理）
-> image-storyboard-director 按真实导演逻辑拆 board_unit，并补齐人物/道具/产品/场景/动线/机位设定包
-> scene-board-image-prompter 为每个 board_unit 单独 precheck 和提示词
-> 内置 imagegen 为每个通过 precheck 的 board_unit 单独出图
```

使用场景：

```text
TVC广告故事板测试
产品广告故事板
品牌广告故事板
剧情包装广告故事板
每一大段故事板
```

规则：

```text
只有用户明确要 TVC大段、每一大段、章节 beat 整理或剧情包装广告故事板时，才走 storyboard-planner。
TVC大段板也必须保留人物、道具、产品、场景、人物动线、机位图和关键节拍，不再只做普通分镜预览。
多段广告/产品流程默认多张板，不能把产品揭示、使用证明、情绪反应和品牌落点全部压进一张图。
```

专项导演选择：

| 项目类型 | 专项导演 |
| --- | --- |
| 企业/城市/品牌宣传片 | `$brand-film-director` |
| 产品广告/TVC | `$tvc-director` |
| 活动/发布会/晚会开场 | `$event-opener-director` |
| LED大屏/舞美视觉 | `$led-screen-director` |
| 节目/综艺/栏目包装 | `$program-promo-director` |
| 社媒切条/预热视频 | `$social-cutdown-director` |

商业宣传线的审美参考优先级：

```text
顶级TVC
Apple / Nike / Wieden+Kennedy
Mercedes / Porsche / BMW premium film
BBC / Netflix premium documentary
Guinness Surfer / Honda Cog
Moment Factory / Es Devlin / Olympic-scale stage visuals
顶级品牌宣言片、工程纪录片、城市影像
```

商业宣传线关注：

```text
品牌主张
客户可理解表达
产品/工程/城市可信度
视觉记忆点
空间规模
节奏与落版
PPT可讲述性
```

默认输出可以包括：

```text
需求拆解
创意概念
视觉参考体系
风格圣经
脚本/旁白
分镜表
关键帧提示词
视频提示词
PPT页面结构
生成记录与QC
```

### 3.1 商业 KV / 主视觉模式

商业 KV 不是普通关键帧，也不是随便生成一张“主KV”。当用户说品牌KV、活动KV、发布会KV、产品KV、节目主视觉、LED主视觉、key visual、主视觉、banner system 时，必须走：

```text
$zongkong
-> $kv-director
-> $kv-image-prompt-director
-> $prompt-platform-auditor
-> image tool / Canva / Photoshop / manual layout
```

如果已有通过的方案、PPT或创意方向，不重新跑概念开发：

```text
approved proposal
-> proposal_to_kv_packet
-> $kv-director 把方案压缩为单一传播层级、视觉钩子、构图系统和资产拆分
-> 主KV / 大屏KV分别设计
```

`$kv-director` 必须先决定：

```text
kv_type
proposal_to_kv_packet（已有方案时必需）
kv_composition_style_packet（所有KV必需）
kv_composition_mode
composition_reference_source
reference_mechanism_translation
master_kv_layout_spec
led_screen_layout_spec
large_screen_experience_packet（大屏/LED/舞台KV必需）
safe_area_map
extension_crop_map
asset_split
post_typography_plan
```

其中 `kv_composition_style_packet` 是 KV 导演的核心能力，必须先于大屏适配完成：第一眼焦点、主体层级、视线动线、画面平衡、景深结构、负空间、标题关系、裁切逻辑、主构图母型、主风格机制、辅助风格、色彩、材质、光线、摄影/图形比例、画面密度、反模板规则和禁止漂移。

主KV和大屏KV必须分开判断：

```text
主KV：主体层级、标题/logo/sponsor留白、负空间、裁切边界、多比例延展。
大屏KV / LED：屏幕比例、中心安全区、主持人/表演安全区、远距可读性、侧翼延展、边缘不可放关键信息。
```

所有KV必须先读取 `skills/kv-director/references/kv-composition-style-library.md` 完成通用构图与风格系统。大屏KV再读取 `large-screen-kv-experience-library.md` 做物理屏适配，检查舞台占位、观众与摄像机双重可读性、摩尔纹/频闪/亮度风险、主屏与侧屏分工；不能让屏幕规格反过来替代KV的构图与风格判断，也不能把16:9主KV直接拉宽当作超宽大屏设计。

允许参考 Pinterest、Behance、Dribbble、官方品牌/活动页面、舞美/LED设计案例，但只能提炼构图机制，不能照搬具体设计、logo、字体、赞助商布局、名人肖像或专属视觉系统。

KV 出图提示词必须生成无字底图或分层资产；可读标题、slogan、logo、赞助商、日期、地点、二维码、法务信息由后期排版添加。

## 4. 剧情短剧线

适用：

```text
短剧 / 微短剧 / 竖屏剧情 / 横屏剧情短片 / 连续分集 /
人物关系戏 / 悬疑案件 / 家庭伦理 / 都市情感 / 复仇爽剧
```

完整开发流程：

```text
project-state-manager（正式短剧先建/查通用状态层）
short-drama-director
-> short-drama-concept-writer
-> short-drama-character-bible
-> short-drama-episode-writer
-> short-drama-dialogue-doctor
-> short-drama-scene-director
-> reference-image-style-matcher（如有参考图，先做视觉解析和母库反向匹配）
-> style-reference-director（先定全剧/场戏参考风格）
-> reference-visual-library（电影/精品剧母库 + 必选顶级摄影层）
-> reference-aesthetic-director（电影/精品剧参考 + 摄影锚点转译）
-> scene-style-map-director（按场戏/地点/时间/情绪分配视觉策略）
-> shot-language-auditor（审核景别递进、机位焦段、剪辑动机）
-> style-bible-director
-> project-style-lock（锁定固定风格变量和提示词 schema）
-> frame-vision-director / ai-video-prompt-director
-> prompt-platform-auditor
-> 生成工具
-> image-qc-director / asset-librarian
```

短剧三档路由：

| 路由 | 使用场景 | 流程 |
| --- | --- | --- |
| 完整开发模式 | 从概念、人物、分集、剧本开始，或正式项目尚未建立角色/风格/场戏结构 | `short-drama-director -> concept/character/episode/dialogue -> scene/style/shot/style-lock -> prompts` |
| 已有分镜执行模式 | 已经有稿子、分镜、视觉方案、人物参考，目标是出提示词、出图、出视频 | `short-drama-scene-director -> reference-image-style-matcher(if refs) -> scene-style-map-director -> shot-language-auditor -> project-style-lock -> frame/video prompt -> prompt-platform-auditor` |
| 快速测试模式 | 单张图、单镜头、人物动起来、先试效果 | `reuse project-style-lock if available -> lightweight reference match(if refs) -> frame/video prompt -> optional lightweight platform check -> generation/prompt` |

默认新短剧项目采用“已有分镜执行模式”，除非用户明确要求从零开发或只做快速测试。

效率规则：

```text
正式短剧先查 project-state-manager 的 workflow/gates。
已有稿子/分镜时，不重新跑概念、分集、对白。
已有 project-style-lock 时，不重新定全剧风格。
单图/单视频测试不走完整开发流程。
正式批量出图/出视频至少保留：project-intake、style-lock、scene-map、shot-audit、prompt-audit、generation-ready。
```

短剧线的审美参考优先级：

```text
全球顶级电影
顶级摄影体系
精品剧集
现实主义犯罪/家庭/情感/悬疑作者电影
Fincher / Deakins / Villeneuve / Cuarón / Park Chan-wook /
Kore-eda / Bong Joon-ho / Wong Kar-wai / Mindhunter / True Detective
```

短剧线关注：

```text
人物关系
角色连续性
表演空间
场戏调度
情绪张力
悬念与反转
每场戏不同地点/光线/焦段
AI角色一致性
```

短剧出图前必须先有：

```text
全剧统一风格DNA
角色圣经
场戏合并表
每场戏视觉参考
参考图角色说明
AI生成风险
```

## 5. 顶级摄影层硬规则

正式项目的出图和出视频不允许只调用类型母库。必须同时调用：

```text
reference-image-style-matcher 先把参考图拆解并反向匹配母库
style-reference-director 先定项目级和场戏/章节级参考风格
reference-visual-library 类型母库
+ shared-elite-cinematography.md 顶级摄影层
-> reference-aesthetic-director 转译
-> scene-style-map-director 分配每场戏风格机制
-> style-bible-director 固化
```

执行要求：

```text
每个项目必须有一个主参考体系
每个项目必须有一个摄影/导演视觉锚点
每条最终图片提示词必须自带摄影、镜头、光线、色彩、材质、构图
每条最终视频提示词必须保留核心摄影锚点，但压缩为平台能执行的短句
```

## 5.1 母库强应用规则

母库不只是“参考片单”，而是正式项目的审美和执行约束来源。正式项目必须把母库转成：

```text
mother_library_application_packet
```

这个包至少包含：

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

作用层级：

```text
项目级：决定真实度、摄影纪律、色彩边界、材质可信度、禁止漂移
场戏级：决定每场的光源、空间关系、焦段心理、构图调度、表演状态
镜头级：只继承可见机制，不把长片单、导演名、摄影师名塞进最终提示词
```

硬规则：

```text
正式出图/出视频如果没有 mother_library_application_packet 或等效的场戏母库应用规则，不能进入最终提示词和生成；必须回到 style-reference-director / scene-style-map-director / project-style-lock 补齐。
```

## 5.2 导演贡献链与画面有效性

正式项目不能让一个提示词 agent 代替所有导演判断。每个相关导演必须留下可继承贡献：

```text
zongkong：路线、速度模式、主线、目标平台
style-reference-director / reference-visual-library：母库应用包、主参考体系、顶级摄影锚点
reference-image-style-matcher：参考图角色和不继承边界
scene-style-map-director：场戏功能、光线、空间、焦段、构图、材质、表演状态
shot-language-auditor：镜头功能、景别递进、剪辑动机、轴线/视线/连续性
character-continuity / character-bible：人物脸、发型、服装、关系状态、表演锚点
project-style-lock：稳定视觉DNA和禁止漂移
frame-vision-director / ai-video-prompt-director：把上游判断转成平台可执行画面词
prompt-platform-auditor：保住效果、检查画面有效性、做平台压缩
```

正式项目 handoff / audit / generation-ready 中应保留：

```text
director_contribution_packet
visual_helpfulness_check
mother_library_application_packet
```

画面有效性检查：

```text
提示词中每个保留词必须能回答：它会让画面哪一部分更准确、更稳定或更好看？
有效词：主体、道具、服装、场景、构图、前中后景、机位、焦段、景深、光线、色彩、材质、动作、结束画面、参考图角色、连续性、平台风险控制。
无效词：高级感、电影感、大片感、真实感、克制、压抑、氛围拉满、质感拉满，除非立刻转译为可见机制。
```

参考顶级影视创作方式时，不学习“堆名词”，而学习他们如何用镜头、光线、空间、材质和表演讲故事。AI 提示词应像给摄影指导和执行平台的合并 brief：清楚、可见、可拍、可审核。

## 6. 提示词与平台审核

提示词由导演层生成，但不能直接等于平台执行稿。

出图/出视频是执行验证环节，不是创意探索中心。正式项目不能靠反复生成来找风格。

```text
frame-vision-director 写静帧提示词
ai-video-prompt-director 写视频提示词
prompt-platform-auditor 审核并改写为平台执行版
```

速度分层审核规则：

```text
prompt_only：不强制调用 prompt-platform-auditor，提示词导演直接给可复制版本。
quick_test：只做一遍轻量平台检查；如果提示词已经清楚稳定，可以直接给执行版。
formal_managed：必须通过 prompt-platform-auditor，并保留审核结果、最终提示词和生成记录。
```

审核优先级：

```text
效果保住 > 画面准确 > 平台稳定 > 文字精简
```

平台审核新增检查：

```text
visual_helpfulness_check：每个保留词是否真的影响画面、动作、光线、材质、构图、连续性或风险控制。
director_contribution_check：母库、场戏、镜头语言、角色/产品连续性是否被保留，是否被提示词压缩时误删。
```

正式项目生成前门槛：

```text
已有 project-style-lock
已有 mother_library_application_packet
已有 director_contribution_packet
已有 visual_helpfulness_check
镜头有功能、景别、机位、焦段、构图、光线、色彩、材质、负面词
参考图角色明确
短剧镜头已通过 shot-language-auditor
平台执行提示词通过 prompt-platform-auditor
```

平台审核结果：

| 结果 | 含义 |
| --- | --- |
| 通过 | 可直接复制执行 |
| 保效精简后通过 | 已压缩，但保留核心效果 |
| 打回重写 | 提示词结构不适合平台或会丢效果 |
| 建议拆分 | 视频/一镜到底太复杂，需要拆段 |

关键规则：

```text
每条图片提示词都必须自带完整风格，不写“同上”
Banana / Banana Pro 故事分镜默认用完整详细提示词：每个分镜单独写清统一风格DNA、摄影机/影像系统、镜头焦段、光圈/景深、景别、机位、构图、光线、色彩、材质、连续性、比例和负面项
只有用户明确说省token、快速测试或 compact，Banana 才使用 compactPrompt；compact 也不能删掉本镜头的相机、光线、构图和连续性
Banana 与内置 image 是两条独立 skill 路线，互不代办、互不自动回退；泛称“出图/重出/继续出”时继承当前项目已锁定的平台，未锁定且会影响执行方式时先由总控确定平台
视频提示词必须单主体动作、单镜头运动
即梦视频优先短执行版
Banana局部替换必须先锁定原图
参考图必须说明角色
平台审核不能只压缩，必须保住画面效果
```

## 7. 生成工具分工

| 工具 | 使用场景 |
| --- | --- |
| 内置 imagegen | `$builtin-imagegen-director`；会话内快速看效果、单张概念图、内置最新模型，不使用 Banana API，也不承诺 Banana 日志 |
| Banana / Banana Pro | `$banana-image-generator`；OpenRouter 直出、批量关键帧、逐镜重出、文件与失败日志，默认完整质量提示词 |
| Midjourney | MJ/Legnext 独立路线，风格探索或高质视觉方向 |
| Seedance/Ark | 直接视频生成，优先公网图URL |
| 即梦/可灵 | 视频提示词执行或外部平台手动执行 |

OpenAI API 出图路线已移除，不作为默认路线。

## 8. 生成后收口

生成后进入：

```text
image-qc-director
-> image-review-board
-> revision-director
-> asset-librarian / project-state-manager
```

QC判断：

```text
可用 / 可小修 / 定向重出 / 提示词需重写 / 前置导演判断错误
```

QC问题归因：

```text
生成偶发问题 -> 定向重出
提示词表达问题 -> frame-vision-director
平台适配问题 -> prompt-platform-auditor
风格锁问题 -> project-style-lock / style-bible-director
前置导演判断问题 -> style-reference / scene-style-map / shot-language-auditor
```

资产状态：

```text
候选 / 入选 / 待重出 / 待修图 / 待修片 / 废稿
```

版本命名示例：

```text
S03_banana_v01
S03_imagegen_v01
S03_mj_v01
S03_seedance_v01
```

## 9. 不同步内容

默认不提交、不同步：

```text
outputs/
projects/
生成图片、视频、音频
临时公网URL
API key / token / .env / secrets
*_input.json
```

workflow 源码同步范围：

```text
skills/
README.md
WORKFLOW.md
.gitignore
sync-logs/
```
