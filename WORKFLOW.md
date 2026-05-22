# 影视 AI 总工作流说明

## 0. 总原则

这套 workflow 的目标是成为专业、实用、稳定的影视 AI 制作流程，而不是工具集合。

核心分工：

```text
$zongkong 管入口、项目、模式、路线
$yingshisheji 管导演审美、叙事、客户表达
$reference-aesthetic-director 管顶级电影/TVC/纪录片/舞台视觉参考转译
$style-bible-director 管统一风格和连续性
$frame-vision-director 管静态关键帧提示词
$ai-video-prompt-director 管视频提示词和可行性判断
生成工具只负责执行
QC/资产层负责收口和版本
```

## 1. 新对话默认启动

新对话或新任务先进入 `$zongkong`。

默认判断：

1. 这是正式项目、快速项目，还是杂项目？
2. 当前工作模式是什么？
3. 是否需要建立项目文件夹？
4. 是否已有合格提示词？
5. 应该交给哪个 skill？

正式项目目录：

```text
H:\yingshi\projects\{projectSlug}\
```

杂项目目录：

```text
H:\yingshi\projects\_misc\
```

## 2. 工作模式

| 模式 | 主任务 | 主要 skill |
| --- | --- | --- |
| 方案模式 | 创意、PPT、客户提案 | `$yingshisheji`、专项导演、`$pitch-deck-director` |
| 短剧模式 | 短剧、微短剧、竖屏剧情、分集、角色对白 | `$short-drama-director` |
| 分镜模式 | 分镜、镜头表、执行表 | `$storyboard-planner` |
| 出图模式 | 静帧、关键帧、重出 | `$style-bible-director`、`$frame-vision-director`、生成工具 |
| 视频模式 | 视频提示词、出视频、一镜到底 | `$ai-video-prompt-director`、视频生成工具 |
| 审片修订模式 | QC、客户反馈、重出建议 | `$image-qc-director`、`$revision-director` |
| 归档模式 | 整理素材、版本、交付 | `$asset-librarian` |

## 3. 短剧场景级视觉导演流程

当用户给出短剧稿子、分镜、人物参考图或影视风格参考时，默认不要直接进入出图提示词。短剧正式流程先走“场景级视觉导演”：

```text
稿件/分镜/参考图
-> short-drama-director 判断项目与输入
-> short-drama-character-bible 建立人物连续性
-> reference-aesthetic-director 转译顶级影视参考
-> style-bible-director 建立全剧统一风格 DNA
-> short-drama-scene-director 按场戏输出视觉参考
-> frame-vision-director 生成静态关键帧提示词
-> ai-video-prompt-director 生成视频提示词与一镜到底判断
-> image/video generation
-> QC 与资产归档
```

短剧出图前必须先有：

```text
全剧统一风格 DNA
场戏合并表
每场戏风格参考/视觉导演设定
角色连续性与参考图角色
AI 风险与负面词
```

每场戏风格参考固定字段：

| 字段 | 说明 |
| --- | --- |
| 场次/场名 | 用地点或剧情功能命名 |
| 覆盖镜头/段落 | 对应原稿镜头或剧情段 |
| 叙事功能 | 报案、怀疑、反转、闪回、认罪、收束等 |
| 地点/时间 | 室内外、日夜、天气、空间属性 |
| 光线/色温 | 每场独立光源逻辑，避免同质化 |
| 色彩/材质 | 墙面、雨水、玻璃、手机、泥土、文件、木材、金属等 |
| 构图/焦段 | 低机位、长焦压缩、门缝、玻璃反射、前景遮挡等 |
| 视觉符号 | 承载剧情的物件或空间符号 |
| 参考审美 | 电影、精品剧、纪录片或 TVC 原则，不照搬画面 |
| 为什么这样设定 | 给客户和执行团队看的画面理由 |
| AI 风险 | 角色漂移、文字乱码、屏幕伪 UI、手部异常、暴力过度等 |

核心原则：

```text
统一的是全剧真实度、人物质感、摄影边界和色彩边界；
变化的是每场戏的地点、光线、焦段、前景遮挡、材质和情绪强度。
```

## 4. 出图前流程

用户说“出图”时，不直接交给生成工具。先判断提示词是否完整。

提示词完整性检查：

```text
主体 / 场景 / 动作 / 构图 / 机位 / 摄影系统 / 镜头焦段 /
光线 / 色彩 / 材质 / 比例 / 负面词 / 参考图角色
```

如果不完整：

```text
正式项目 -> yingshisheji -> reference-aesthetic-director -> style-bible-director -> frame-vision-director
快速项目 -> frame-vision-director 快速补齐
杂项目 -> 简洁补齐后直接生成
```

出图路线：

```text
内置 imagegen：image / image-2 / ChatGPT Image / 内置最新模型
Banana：Banana / Banana Pro / 重出 / 继续出 / 省 token
Midjourney：MJ / Midjourney / Legnext
```

OpenAI API 出图路线已移除。

## 5. 视频前流程

视频提示词生成前先做可行性判断：

```text
是否跨空间
是否跨时间
是否跨主体
景别跳跃是否过大
动作是否过多
是否需要遮挡转场
是否适合一镜到底
```

一镜到底必须写清：

```text
连续镜头
空间路径
目标物锁定
景别变化方式
遮挡/光线/形态匹配衔接
禁止剪切、跳切、突然换景
```

如果难度过高，默认建议“伪一镜到底拆段”，用遮挡、光线、运动方向或形态匹配衔接。

## 6. 生成后收口

生成后按项目等级处理：

```text
正式项目 -> review board -> QC -> asset-index
快速项目 -> 预览/路径 -> 简短 QC -> 关键记录
杂项目 -> 预览/路径 -> 一句判断
```

QC 结论：

```text
可用 / 可小修 / 建议重出 / 提示词需重写
```

资产状态：

```text
候选 / 入选 / 待重出 / 待修图 / 待修片 / 废稿
```

修订优先引用 handle：

```text
S03_banana_v01
S03_imagegen_v01
S03_mj_v01
S03_seedance_v01
```

## 7. 不同步内容

默认不要同步：

- 真实 API key / token
- `outputs/`
- 大体积视频和图片
- 临时公网 URL
- 本地私密配置

同步 skill 变化时使用 `$workflow-sync-manager`，但用户明确说“先不要同步”时，不 commit、不 push。
