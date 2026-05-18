# 工作流说明

## 总体链路

```text
brief / 稿子 / 分镜
-> $yingshisheji
-> PPT 提案内容
-> Excel 执行表格
-> Banana/OpenAI 提示词
-> $project-state-manager 建立项目状态
-> generation-job.json
-> $image-generation-controller 出图或 dry-run
-> images / prompts / logs
-> $image-review-board 审片面板
-> $revision-director 修改与重出
```

## 项目状态层

长项目、多轮修改、批量出图时，优先使用 `$project-state-manager`：

```text
project-manifest.json  项目当前状态
asset-index.json       图片、提示词、日志、审片面板、版本状态
generation-job.json    Banana/OpenAI 统一出图任务
```

默认项目结构：

```text
H:\yingshi\projects\{projectSlug}\
  project-manifest.json
  asset-index.json
  generation-jobs\
  generation-runs\
  review\
  revision-logs\
```

## 出图执行

提示词阶段不调用真实 API。只有用户明确指定 Banana 或 OpenAI 出图时，才由 `$image-generation-controller` 调用底层生成器。

```text
用 Banana 出图并整理
用 OpenAI 出图并整理
先测一下这批图能不能出
```

dry-run 不扣费；真实出图需要本机环境变量：

```text
OPENROUTER_API_KEY
OPENAI_API_KEY
```

## 审片与修改

出图后生成：

```text
review/review-board.md
```

审片面板采用左提示词、右图片的结构。修改时可直接引用版本：

```text
改 S03_banana_v01，背景更干净，人物保持不变
```

修改优先从 `asset-index.json` 定位原图、原提示词和对应版本。

