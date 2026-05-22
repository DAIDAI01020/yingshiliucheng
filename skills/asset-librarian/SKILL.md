---
name: asset-librarian
description: Asset librarian for film AI workflows. Use when organizing project folders, naming files, tracking generated images, videos, reference images, prompt files, logs, selected frames, rejects, regeneration versions, and delivery assets for TVC, brand film, program promo, event opener, LED visual, or AI image/video projects.
---

# Asset Librarian

## Core Role

Keep project assets clean, traceable, and usable.

Track:

- Where files belong.
- Which version is current.
- Which image/video is selected.
- Which output is rejected.
- Which reference image is bound to which shot.
- Which prompt generated which asset.

For managed projects, treat `asset-index.json` from `$project-state-manager` as the source of truth.

## Default Folder Structure

Use this structure unless the user already has a project structure:

```text
项目名/
  01_brief/
  02_ppt_proposal/
  03_excel_execution/
  04_prompts/
  05_generated_images/
  06_selected_frames/
  07_video_prompts/
  08_generated_videos/
  09_review_boards/
  10_revision_logs/
  11_delivery/
```

Managed workflow folders:

```text
H:\yingshi\projects\{projectSlug}\
  project-manifest.json
  asset-index.json
  generation-jobs\
  generation-runs\
  video-runs\
  review\
  revision-logs\
  briefs\
  prompts\
  references\
```

## Naming Rules

Generated images:

```text
S01_imagegen_v01.png
S01_banana_v01.png
S01_banana_v02.png
S01_mj_v01.png
S03A_banana_v01.png
```

Generated videos:

```text
S01_seedance_v01.mp4
S01_kling_v01.mp4
S01_jimeng_v01.mp4
```

Prompt files:

```text
S01_banana_v01_prompt.txt
S01_banana_v01_prompt.json
S01_seedance_v01_prompt.txt
```

## Asset States

| 资产状态 | 含义 |
| --- | --- |
| 候选 | 可供选择，未定稿 |
| 入选 | 进入 PPT、首帧、视频或交付 |
| 待重出 | 方向保留，需要重新生成 |
| 待修图 | 图片可用但需要后期修正 |
| 待修片 | 视频可用但需要剪辑/补帧/调色/后期 |
| 废稿 | 不再使用，但保留记录 |

## Reference Binding

Every reference image should have a role:

| 角色 | 用途 |
| --- | --- |
| character | 人物身份/造型 |
| product | 产品/道具结构 |
| scene | 场景空间 |
| style | 风格/摄影/光线 |
| composition | 构图关系 |
| material | 材质细节 |
| motion | 动作/姿态 |

Do not leave references as unnamed loose files when they affect generation.

## Output

### 素材资产清单

| 资产ID | 镜号 | 版本 | 类型 | 工具/来源 | 文件路径 | 提示词TXT | 提示词JSON/Manifest | 审片面板路径 | 资产状态 | 绑定参考图 | 用途 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

### 项目目录建议

| 文件夹 | 用途 | 命名规则 |
| --- | --- | --- |

## Rules

- Never delete older generated versions in the plan. Mark them as `废稿` if unused.
- Tie every generated image/video to a shot number and version.
- Tie every reference image to a shot number or role.
- If the user asks for final delivery, identify selected assets and missing assets first.
- Align with `Sheet 7 出图生成记录` and video run manifests.
- When `asset-index.json` exists, read or update it before producing a manual asset table.

