# 影视 AI 工作流 Skills

这是一个给 Codex 使用的影视 AI 制作工作流 skill 库。

它不是单一出图工具，而是一套“总控 → 导演 → 风格 → 提示词 → 生成 → QC → 资产管理”的影视制作流程。

## 总入口

日常优先使用：

```text
$zongkong
```

`$zongkong` 是最高总控，负责判断项目分级、工作模式、文件夹、工具路线和下一步动作。

影视创作主入口：

```text
$yingshisheji
```

`$yingshisheji` 是影视导演层，负责审美判断、叙事判断、风格推荐、客户表达、分镜逻辑和提示词方向。

## 核心链路

```text
$zongkong
-> 项目分级 / 工作模式 / 文件夹
-> $yingshisheji 导演判断
-> $reference-aesthetic-director 顶级参考审美转译
-> $style-bible-director 统一风格圣经
-> $frame-vision-director 静帧提示词
-> 内置 imagegen / Banana / Midjourney 出图
-> $image-review-board + $image-qc-director 审片
-> $ai-video-prompt-director 视频提示词
-> $video-generation-controller / $seedance-2-video 出视频
-> $revision-director 修改重出
-> $asset-librarian / $project-state-manager 资产归档
```

## 项目分级

| 层级 | 使用场景 | 默认处理 |
| --- | --- | --- |
| 正式项目 | 有客户、片名、长期制作目标、成组镜头或交付需求 | 建独立项目文件夹，建立风格圣经，记录资产和版本 |
| 快速项目 | 有明确主题但只做少量图/视频或快速提案 | 可建轻量项目文件夹，保留关键 prompt 和输出路径 |
| 杂项目/_misc | 测试模型、单张图、临时视频、随手试 prompt | 放入 `H:\yingshi\projects\_misc\`，只做轻量 QC |

## 主要目录

```text
skills/
  zongkong/
  yingshisheji/
  reference-aesthetic-director/
  short-drama-director/
  short-drama-concept-writer/
  short-drama-character-bible/
  short-drama-episode-writer/
  short-drama-dialogue-doctor/
  short-drama-scene-director/
  style-bible-director/
  frame-vision-director/
  ai-video-prompt-director/
  image-generation-controller/
  video-generation-controller/
  builtin-imagegen-director/
  banana-image-generator/
  midjourney/
  seedance-2-video/
  image-review-board/
  image-qc-director/
  project-state-manager/
  asset-librarian/
  production-manager/

projects/
  {projectSlug}/
    project-manifest.json
    asset-index.json
    generation-jobs/
    generation-runs/
    video-runs/
    review/
    revision-logs/
    briefs/
    prompts/
    references/
  _misc/
    临时测试、模型验证、随手出图、生视频小样
```

## 出图路线

- 内置 imagegen：用户说 `image / image-2 / ChatGPT Image / 内置最新模型 / 先看效果` 时使用。
- Banana：用户明确说 `Banana 出图 / 重出 / 继续出 / 省 token` 时使用，默认 `2K + compact prompt`。
- Midjourney：用户明确说 `MJ / Midjourney / Legnext` 时使用。
- OpenAI API 出图路线已移除，不再使用 `OPENAI_API_KEY` 做图片生成。

出图前必须先有完整提示词。正式项目没有提示词时，先经过 `$yingshisheji` / `$reference-aesthetic-director` / `$style-bible-director` / `$frame-vision-director` 补齐。

## 视频路线

- 默认使用 Seedance/Ark。
- 优先使用公网图片 URL。
- 本地图中转只在需要时启用。
- 一镜到底请求必须先做视频可行性判断。

## 生成后收口

生成后按项目等级处理：

- 正式项目：review board + QC + asset-index 记录。
- 快速项目：预览/路径 + 简短 QC + 关键记录。
- 杂项目：预览/路径 + 一句判断。

QC 判断统一为：

```text
可用 / 可小修 / 建议重出 / 提示词需重写
```

资产状态统一为：

```text
候选 / 入选 / 待重出 / 待修图 / 待修片 / 废稿
```

## 不同步内容

以下内容默认不进入仓库同步：

- `outputs/`
- `projects/` 中的大体积生成内容
- 临时 input JSON
- 生成图片、视频、音频
- API key、token、本地环境变量、私密配置

不要把真实 key 写入 skill、prompt、manifest、日志、README 或 Git。
