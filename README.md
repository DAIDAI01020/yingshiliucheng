# 影视 AI 工作流 Agent

给 Codex 使用的影视、短剧、KV、海报、图像与视频制作 skill 库。日常从 `$zongkong` 进入：总控判断当前需求，只调用本次需要的专业能力，不要求每个任务走完整制作链。

## 三种工作方式

| 模式 | 常见说法 | 执行边界 |
| --- | --- | --- |
| `prompt_only` | 给我提示词、改一下这段词 | 输出可复制提示词，不生成、不建无关项目状态 |
| `quick_test` | 先看效果、直接出两张机位图 | 一次必要检查，逐张返回独立结果；失败只重试允许重试的失败项 |
| `formal_managed` | 正式项目、批量镜头、客户交付 | 使用适用的参考、风格与连续性锁，记录任务、素材、版本和审片结果 |

单张临时测试不必建立项目文件夹。需要落盘时由项目目录规则确定位置，不把本机盘符硬编码到另一台电脑。

## 按交付物路由

| 需求 | 主要负责能力 |
| --- | --- |
| 影视提案、广告、品牌片 | `yingshisheji` 和对应专项导演 |
| 短剧 | `short-drama-director`，按需进入人物、分集、场景、镜头与对白能力 |
| 商业或活动 KV | `kv-director` → `kv-image-prompt-director` |
| 电影/短剧海报 | `poster-director` |
| 一般静帧或改图 | `frame-vision-director` |
| 独立故事板设定板 | `image-storyboard-workflow` |
| 视频提示词 | `ai-video-prompt-director` |
| 平台编译与审查 | `prompt-platform-auditor` |
| 多部分项目、上下文隔离 | `project-thread-orchestrator` |

正式创作按需参考精选影视、TVC、KV 和 key-art 母库，把参考转成构图、光线、色彩、材质等可执行控制；不以随意罗列片名代替设计。已有确认稿、风格或参考时沿用有效决定，不从头重复开发。

## 出图与改图

- 内置 imagegen：内置出图、Image 2.5、快速预览或明确选用内置能力的正式项目。
- Banana：明确选择 Banana / Banana Pro / Nano Banana / OpenRouter 时使用。
- Midjourney：明确选择 MJ / Midjourney / Legnext 时使用。
- 提示词分支与工具实际模型分开记录；工具不暴露模型选择时，不声称选中了某个子模型或旧模型。
- 需要归档不等于需要换平台。只能登记真实返回且已验证的本地文件；只有内联结果时标记待捕获。
- 换机位锁定场景中的物体、位置和光源，允许透视、遮挡和取景改变；局部改图才锁定不受修改影响的画面区域。

每张独立出图都有自己的精简完整提示词。两张机位图不会合成一张拼图，除非用户明确要求对比板。

## 视频制作

先完成当前镜头所需的首帧/参考与动作提示词，再按明确选择的平台执行：即梦 CLI 走 `dreamina-cli`，火山 Ark 走 `seedance-2-video`；不在两者之间自动切换。只写提示词不会自动发起付费生成。

默认音频约束：不要音乐、不要配乐，可以有符合画面的环境声和动作音效；对白按镜头要求保留。用户明确要求音乐时，以本次要求为准。

正式任务记录平台任务 ID；提交结果不确定时先查询恢复，不直接重新付费提交。一镜到底、长动作链和连续多镜头按适用的可行性与连续性规则检查。

## 总项目与分任务

长稿件按叙事和交付需求动态拆分，用户确认后创建分任务。所有任务使用同一总项目、同一本地根目录；每个分任务有独立任务包和工作目录。最多同时运行 4 个，依赖完成后启动后续队列，不复制总控完整历史。

用户说“汇总进度 / 继续项目 / 同步分聊天”时读取交接结果。全局约束版本化，确认后只向受影响任务广播；不默认开启后台轮询。

项目目录规范由 `project-folder-director` 管理；线程注册表与状态由 `project-state-manager` 配合编排能力管理。

## 审片与交付

- `formal_managed`：技术证据、适用的语义 QC、资产与状态回写。
- `quick_test + qc_mode:none`：显示结果后停止。
- `quick_test + qc_mode:light_deferred`：后续独立审片步骤按需检查。
- 内置出图成功后以图片收口，不在同一生成回复后追加 QC 文字。

QC 结论统一为：`可用 / 可小修 / 定向重出 / 提示词需重写 / 前置导演判断错误`。局部失败优先局部修正，不自动重写整个项目。

## 另一台电脑更新

源码仓库：[GitHub · yingshiliucheng](https://github.com/DAIDAI01020/yingshiliucheng)。`skills/` 是可安装技能源码；克隆或拉取仓库并不等于已更新 Codex 的本地 skills。

可把这段要求交给另一台电脑上的 Codex：

```text
从 https://github.com/DAIDAI01020/yingshiliucheng 更新影视 Agent。
先核对仓库 remote 与本地修改：已有仓库只对正确的 GitHub remote 做安全快进更新，
不强推、不丢弃本地修改、不假定 origin 一定是 GitHub。
比较仓库 skills 与当前 Codex skills，备份将被替换的文件；
有独立本地修改先说明差异，无冲突再同步并校验。
不要复制 API key、账户配置、项目素材或会话历史。
最后报告源码版本、实际安装位置和验证结果。
```

真实密钥只保存在本机专用密钥配置中，不写入提示词、skill、清单、日志或 Git。项目素材、生成媒体和临时输入不进入源码发布范围。

## 维护验证

```powershell
python -X utf8 skills/zongkong/scripts/validate_workflow_contracts.py
python -X utf8 skills/zongkong/scripts/run_e2e_workflow_tests.py
node --test skills/workflow-sync-manager/scripts/sync-workflow.test.mjs
```

发布由 `workflow-sync-manager` 处理：使用明确文件白名单，保留白名单外用户暂存内容，检查密钥和远端分歧；远端哈希验证后才报告已推送。没有变更时不制造重复日志或提交。
