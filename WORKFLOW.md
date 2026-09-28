# 影视 AI 总工作流

本文件是整套 Agent 的使用地图。总控负责选路，各专项技能负责自己的判断，执行工具负责真实生成，审片与资产层负责验证和交付。流程按当前交付物选择，不要求每次经过全部环节。

## 规则来源与协作

- 路由、意图、速度模式、继续任务：[总控](skills/zongkong/SKILL.md)。
- 职责归属：[能力登记表](skills/zongkong/references/capability-registry.json)。
- 跨阶段输入、批准证据、依赖与完成标准：[阶段交接规则](skills/zongkong/references/stage-handoff-contract.md)。
- 正式门槛：[适用门槛与负责人](skills/zongkong/references/packets-and-gate-ownership.md)。
- 目录：[项目目录导演](skills/project-folder-director/SKILL.md)；持久状态：[项目状态管理](skills/project-state-manager/SKILL.md)。

本地图不另设第二套门槛、目录或平台默认值。用户当前明确要求优先于历史默认；沿用已经确认且仍适用的决定。影视之外的请求不强制进入制作流程。

## 工作模式

| 当前需要 | 工作方式 | 完成标准 |
| --- | --- | --- |
| 概念、脚本、方案、提示词 | 完成所需内容；已有稿件从相应阶段继续 | 可直接使用的成品内容 |
| 单图、单镜头、小组同源变体 | quick_test，保留必要参考与结构约束 | 实际生成结果及必要的局限说明 |
| 正式批量、客户交付、托管生产 | formal_managed，按交付物启用门槛 | 适用审批、生成证据、QC和状态记录 |
| 审片、查进度、整理素材 | 读取现有证据，按请求检查或整理 | 可核实的判断、清单或交付文件 |

prompt_only 是只交付提示词的任务模式，不触发生成。正式项目内也可以只改一条提示词并继承有效锁；这不更改整个项目的生产模式或平台。少量同源预览图不自动升级为正式批量。

## 制作链路

| 阶段 | 主要负责人 | 实际贡献 |
| --- | --- | --- |
| 需求 | brief-analyzer | 已知事实、目标、限制、待决问题 |
| 概念 | concept-director / short-drama-concept-writer | 核心主张、可见创意、叙事逻辑 |
| 商业统筹 | yingshisheji + 对应专项导演 | 传播目的、片种方法、可执行方向 |
| 短剧统筹 | short-drama-director | 人物、分集、场戏、表演与连续性 |
| 文稿与分镜 | script-writer / storyboard-planner / short-drama-scene-director | 可说出的文稿、镜头功能、时长与空间关系 |
| 参考与风格 | style-reference-director + reference-visual-library | 与用途相符的参考机制及来源 |
| 参考转译与场景 | reference-aesthetic-director / scene-style-map-director | 可见构图、光线、材质和场景变化 |
| 连续性 | style-bible-director → project-style-lock | 先整合规则，再冻结已确认变量 |
| 提示词 | 对应语义负责人 → prompt-platform-auditor | 先表达画面/动作，再适配平台 |
| 生成 | 用户所选平台的执行技能 | 实际提交、恢复、下载和结果证据 |
| 审片与修订 | image-qc-director / video-qc-director → revision-director | 证据、归因、局部修改与版本追踪 |
| 项目与交付 | production-manager / asset-librarian / project-state-manager | 状态、入选版本、文件验证和交付清单 |

从已有有效输入进入相应阶段。已定方案不重新做概念，已定提示词只改平台时直接编译。先起草场景与镜头，再审核并冻结相关决定；不要求场景草稿先具备依赖它才能产出的最终风格锁。

## 专项入口

| 交付物 | 负责人 |
| --- | --- |
| 品牌片、企业或城市片 | brand-film-director |
| 产品广告、TVC | tvc-director |
| 活动开场、发布会、盛典 | event-opener-director |
| LED、异形屏、舞美视觉 | led-screen-director；工程分屏计算交给 aedaping |
| 节目、栏目、综艺宣传 | program-promo-director |
| 社媒改编、切条 | social-cutdown-director |
| 商业、产品、活动KV系统 | kv-director → kv-image-prompt-director |
| 电影、短剧、人物海报 | poster-director → frame-vision-director |
| 标题字、透明字体资产 | type-png-director |
| 独立故事板设定板 | image-storyboard-workflow → image-storyboard-director → scene-board-image-prompter |
| 普通静帧 | frame-vision-director |
| 视频动作、多镜、编辑、延长 | ai-video-prompt-director |
| 客户PPT提案 | pitch-deck-director；实际文件使用可用演示文稿技能 |

故事板按场景功能、空间、调度和转折拆分；每个执行单元独立设计、检查并出图。单张总览不能冒充逐段故事板。普通镜头表不默认变成九宫格设定板。

## 参考、风格与质量

参考库提供经过筛选的来源；风格参考导演选择适用机制，参考审美导演深化转译，场景风格导演分配变化，风格圣经整合连续性，风格锁冻结批准结果。已有足够明确的机制时复用，不重新跑整条参考链。

正式电影化实拍/生成保留适用摄影锚点；纯字体、抽象LED、图形KV和产品结构任务采用字体、构图、舞台或材质规则，不强塞皮肤、灰尘、镜头品牌和电影母库。参考图必须先分清身份、产品、空间、光线、风格等角色及不继承项；仅作产品/身份约束不等于必须反查电影。

参考转译应说明会改变画面什么，不堆片名和导演名。搜索证据、链接、参考图观察与推断分开记录。未查看素材、未检索平台时，不声称完成了匹配或检查。

## 提示词与执行

- 每个可独立执行的提示词包含本次所需的完整信息，不依赖“同上”；无关风格描述和重复表格不进入执行词。
- 静帧只描述冻结画面；视频按 single_beat、staged_action 或 multi_shot 组织动作、镜头和结束状态。
- 结尾按剪辑意图选择停留、气口、硬切、动作出画或循环，不默认每镜追加气口。
- 视频默认不要音乐、配乐、歌曲或人声演唱；允许同步环境声和动作音效，保留要求的对白。明确音乐或完全静音要求优先。
- 平台与实际工具可选择的模型分开记录；不因归档、省token或失败而自动换平台。
- 执行前核对授权范围和已有任务。已提交任务先查询恢复，完成任务复用结果，付费重试遵循执行技能的明确范围。
- 提交ID、手动交接包、预计输出路径均不等于生成完成。部分成功保留成功项，只处理缺失或失败项。

## 审片与修订

技术检查提供分辨率、时长、透明度、音轨等证据；语义审片判断人物、品牌、构图、表演、连续性和声音用途。接触表不能证明整段运动或音频合格，未检项保留为未检。

可用、可小修、定向重出、提示词需重写、前置导演判断错误分别对应不同动作。重复瑕疵先查参考继承、提示词或模型执行；只有证据指向全局决定有误时才提出更新风格。客户说“不高级”不自动授权改全片。

修订保留稳定镜号与原版本，只更新受影响内容和依赖。审片通过、客户入选和最终交付分开记录。内置图片成功回复以原生图片结果收口，后续QC遵循总控规定。

## 项目、分聊天与交付

目录由 project-folder-director 决定，复用已有项目结构，不绑定本机盘符。资产清单与状态由各自负责人维护，不另造一套台账。

默认当前聊天；用户明确要求分聊天时使用同一项目与根目录，确认具体拆分范围后创建干净任务包，最多四个占用中的子任务。已有授权继续有效，创建与广播不重复确认；进度查看不自动发消息、开后台监控或归档聊天。

交付前核对入选版本、实际文件、格式、比例、分辨率、透明度或音频等适用要求。用户要PPTX、表格、文档或PDF时产出实际文件并检查；提纲和路径占位符不算成品。保护历史版本，缺失项明确列出。

## 维护与验证

用户要求优化整套Agent时，检查完整链路、职责边界、规则冲突、源码与本机安装差异；先备份，再合并有效修改。当前请求已经授权的本地实现不重复询问。发布、提交、推送仍按用户授权执行。

从仓库根目录运行：

```powershell
python -X utf8 skills/zongkong/scripts/validate_workflow_contracts.py
python -X utf8 skills/zongkong/scripts/audit_skill_capabilities.py
python -X utf8 skills/zongkong/scripts/run_e2e_workflow_tests.py
python -X utf8 skills/reference-visual-library/scripts/validate_reference_library.py
python -X utf8 -m unittest discover -s skills/zongkong/tests
python -X utf8 -m unittest discover -s skills/project-thread-orchestrator/tests
node --test skills/banana-image-generator/scripts/generate-banana-images.test.mjs skills/project-state-manager/scripts/manage-project-state.test.mjs skills/workflow-sync-manager/scripts/sync-workflow.test.mjs skills/kling-api/scripts/kling_api.test.mjs
```

静态规则检查不等于真实模型行为测试；端到端测试使用临时项目与模拟平台，不发起真实付费生成。真实项目兼容性检查仅在指定时只读执行。

源码发布限 skills、README、WORKFLOW、必要更新记录与仓库规则；生成素材、项目文件、凭据、临时公网URL和会话历史不进入发布范围。
