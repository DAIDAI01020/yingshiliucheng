# 影视 AI 工作流新聊天交接文件

日期：2026-05-25

用途：在新对话中快速恢复当前影视 AI 工作流上下文。此文件只记录 workflow、skill 架构、用户偏好和执行规则，不保存密钥、临时公网地址、生成素材或私密配置。

## 1. 当前总流程

正式项目默认流程：

```text
zongkong
-> style-reference-director
-> reference-visual-library
-> reference-aesthetic-director
-> scene-style-map-director
-> style-bible-director
-> frame-vision-director / ai-video-prompt-director
-> prompt-platform-auditor
-> generation tool
-> image-qc-director / asset-librarian
```

核心逻辑：

```text
先定参考风格
再做场戏/章节视觉分配
再固化风格圣经
再写图片/视频提示词
再做平台审核
最后才出图或出视频
```

## 2. 当前核心新增与关键 Skills

### zongkong

总控入口。新项目、新对话、模糊请求先进入它，判断项目类型、项目层级、工作模式和后续 skill 路由。

### style-reference-director

风格参考入口。正式项目出图/出视频前必须先调用。

职责：

- 读稿子、分镜、参考图、用户给的电影/TVC/短剧风格。
- 输出项目级风格参考表。
- 输出场戏/章节风格参考表。
- 选择主参考体系、辅助参考、顶级摄影锚点。
- 明确不照搬内容和 AI 风险。

它是面向项目的风格参考导演，不是提示词工具。

### reference-visual-library

参考母库。它不是直接面向最终任务的入口，而是给 `style-reference-director` 和 `reference-aesthetic-director` 提供顶级影视、TVC、纪录片、短剧、摄影体系参考。

结构：

```text
commercial-promo-library.md
short-drama-story-library.md
shared-elite-cinematography.md
```

商业宣传线和短剧线参考体系必须分开。

### reference-aesthetic-director

审美转译层。负责把参考风格转译为可执行视觉机制：

```text
镜头
焦段
摄影机
光线
色彩
材质
构图
节奏
AI风险
```

不能只堆片名、导演名或摄影师名。

### scene-style-map-director

场戏/章节视觉分配层。适用于短剧、宣传片、TVC、活动片等多场景项目。

职责：

- 每场戏/章节可以有不同视觉策略。
- 但必须保持全片统一 DNA。
- 输出场戏视觉地图，包含场景功能、参考风格、摄影锚点转译、景别/焦段倾向、光线、色彩、材质、构图/调度、参考图角色和 AI 风险。

### style-bible-director

风格圣经与连续性控制。负责把已选风格固化为后续批量出图/出视频不能乱变的规则。

### frame-vision-director

图片提示词导演。负责静帧、关键帧、Banana、内置 imagegen、即梦图片、MJ 等图片提示词。

硬规则：

```text
每条最终图片提示词必须自带完整风格。
不能写“同上”“延续上条”“同统一风格”。
不能用垃圾模板撑住提示词。
```

### ai-video-prompt-director

视频提示词导演。负责即梦、可灵、Seedance/Ark 视频提示词，一镜到底和伪一镜到底可行性判断。

### prompt-platform-auditor

平台审核层。所有正式提示词生成后，必须经过它审核或改写为平台执行版。

优先级：

```text
效果保住 > 画面准确 > 平台稳定 > 文字精简
```

它不是单纯压缩提示词，而是保证平台能执行且不丢核心效果。

## 3. 出图规则

正式项目不能直接跳到 Banana 或内置出图。

必须先走：

```text
style-reference-director
-> scene-style-map-director
-> style-bible-director
-> frame-vision-director
-> prompt-platform-auditor
```

每条最终图片提示词必须包含：

```text
景别
机位
构图
摄影机/影像系统
镜头焦段
光圈或景深
光线来源和方向
色彩/调色
材质质感
比例
负面词
```

禁止：

```text
只写电影感/高级感/真实感
只堆奥斯卡感/大片感/纪录片感
只堆电影名、导演名、摄影师名
只写 MS / CU / 50mm / f2.8
用 live-action cinematic documentary still 这种模板当主提示词
```

正确提示词必须先描述可见画面，再写摄影锚点转译，再写技术参数和负面词。

## 4. 视频规则

正式视频提示词必须包含：

```text
首帧景别/机位
主体动作
镜头运动
焦段或镜头感
光线方向
色彩边界
材质/空间质感
结束画面
禁止项
时长/比例
```

即梦视频和可灵视频不能写成长篇分镜合集。应优先保证：

```text
一个主体动作
一个镜头运动
一个光线/环境变化
一个清晰首帧
一个清晰结束画面
```

一镜到底必须先判断可行性。如果跨空间、跨时间、跨主体太多，默认建议伪一镜到底，用遮挡、光线、运动方向或形态匹配衔接。

## 5. 用户偏好

### 出图

- Banana / Banana Pro：用户说“Banana 出图 / 重出 / 继续出 / 省额度”时默认快速执行。
- 正式项目如果没有合格提示词，必须先补齐参考风格、场戏视觉和平台审核。
- 内置 image / image-2 / ChatGPT Image / 内置最新模型：指 Codex/ChatGPT 内置图像生成，不走 OpenAI API 出图路线。
- MJ / Midjourney / Legnext：独立路线，不混用 Banana。

### 视频

- Seedance/Ark：用户偏好使用公网图 URL。
- 本地图自动中转可以用，但不是默认优先。
- 视频提示词需要平台审核，尤其是即梦视频需要准确精简。

### 风格审美

- 宣传片/TVC 和短剧是两条不同主线，参考体系不能混用。
- 参考全球顶级电影、精品剧、顶级 TVC、纪录片、舞台/LED 视觉。
- 不以低质量国产网大、廉价短剧、普通企业片作为审美标准。
- 中国文化、历史、地点可以作为内容依据，但视觉纪律仍按顶级影视/TVC标准执行。

## 6. 当前工作流状态

已新增或重点更新的本地 skills：

```text
style-reference-director
scene-style-map-director
reference-visual-library
prompt-platform-auditor
frame-vision-director
ai-video-prompt-director
reference-aesthetic-director
zongkong
```

本地 skill 根目录：

```text
H:\yingshi\skills\
C:\Users\admin\.codex\skills\
```

注意：当前 workflow 文件有未提交修改。不要默认提交或推送。若需要同步 GitLab，必须先运行 secret scan，并排除生成素材、临时文件和密钥。

## 7. 新聊天启动提示

新聊天可以直接复制下面这段：

```text
这是影视 AI 工作流项目。请先读取/遵守本交接文件。

当前核心规则：
1. 正式项目先走 zongkong。
2. 出图/出视频前必须先走 style-reference-director，先定项目级和场戏/章节级参考风格。
3. reference-visual-library 只是母库，不是直接提示词入口。
4. reference-aesthetic-director 负责把参考转译成视觉机制。
5. scene-style-map-director 负责把不同场戏/章节分配不同视觉策略，但保持全片统一 DNA。
6. frame-vision-director 写图片提示词，每条提示词必须自带完整风格，不允许“同上”。
7. prompt-platform-auditor 审核平台适配，禁止垃圾模板提示词。
8. 每条图片提示词必须包含：景别、机位、构图、摄影机/影像系统、焦段、光圈或景深、光线、色彩、材质、比例、负面词。
9. 视频提示词必须包含：首帧景别/机位、主体动作、镜头运动、焦段或镜头感、光线方向、色彩边界、材质/空间质感、结束画面。
10. Banana 出图默认快速执行；但正式项目没合格提示词时必须先补齐参考风格和平台审核。
11. 内置 image/image-2 指 ChatGPT/Codex 内置出图，不走 OpenAI API 出图。
12. Seedance/Ark 视频优先使用公网图 URL。
```

## 8. 不保存内容声明

本交接文件不包含：

```text
API key
上传凭证
临时公网地址
生成图片
生成视频
私密配置
```
