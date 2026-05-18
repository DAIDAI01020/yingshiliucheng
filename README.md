# 影视 AI 工作流 Skills

这是一个用于 Codex 的影视化 AI 制作工作流 skill 库，主入口是 `$yingshisheji`。

覆盖内容包括 TVC、品牌片、电视节目宣传片、发布会/晚会开场、大屏视觉、LED 舞美视觉，以及 AI 出图、审片、修改和项目状态管理。

## 主入口

日常使用优先调用：

```text
$yingshisheji
```

真实出图链路由 `$image-generation-controller` 统一调度，项目级状态由 `$project-state-manager` 管理。

## 目录

```text
skills/
  yingshisheji/
  project-state-manager/
  image-generation-controller/
  image-review-board/
  banana-image-generator/
  openai-image-generator/
  ...
```

## 本地生成内容

以下内容默认不进入仓库：

- `outputs/`
- `projects/`
- 生成图片、视频、音频
- 临时 input JSON
- API key、本地环境变量、日志

API key 只应保存在本机环境变量中，例如 `OPENROUTER_API_KEY` 和 `OPENAI_API_KEY`。

## 跨设备使用

在新电脑上 clone 仓库后，把需要使用的 skill 同步或复制到 Codex 全局 skills 目录：

```text
C:\Users\admin\.codex\skills\
```

Mac 上对应为用户目录下的 Codex skills 目录，具体路径以 Codex 当前环境为准。

