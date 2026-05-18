---
name: asset-librarian
description: Asset librarian for film AI workflows. Use when organizing project folders, naming files, tracking generated images, reference images, prompt files, logs, selected frames, rejects, regeneration versions, and delivery assets for TVC, brand film, program promo, event opener, LED visual, or AI image/video projects.
---

# Asset Librarian

## Core role

Keep the project assets clean, traceable, and usable. Track where files belong, which version is current, which image is selected, which is rejected, and which reference image is bound to which shot.

For managed projects, treat `asset-index.json` from `$project-state-manager` as the source of truth for generated image paths, prompt files, review-board paths, selected frames, rejects, and regeneration versions.

## Default folder structure

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
  08_revision_logs/
```

Generated images should keep tool and version:

```text
S01_banana_v01.png
S01_banana_v02.png
S01_openai_v01.png
S03A_banana_v01.png
```

For generator task folders, separate image files and records:

```text
任务时间/
  images/
    S01_banana_v01.png
    S02_openai_v01.png
  prompts/
    S01_banana_v01_prompt.txt
    S01_banana_v01_prompt.json
  logs/
    generation-log.json
  review/
    review-board.md
```

## Asset states

| 资产状态 | 含义 |
| --- | --- |
| 候选 | 可供选择，未定稿 |
| 入选 | 进入PPT、首帧或交付 |
| 废稿 | 不再使用，但保留记录 |
| 待重出 | 方向保留，需要重新生成 |
| 待修图 | 可用但需要后期修正 |

## Output

### 素材资产清单

| 资产ID | 镜号 | 版本 | 类型 | 工具/来源 | 文件路径 | 提示词TXT | 提示词JSON | 审片面板路径 | 资产状态 | 绑定参考图 | 用途 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

### 项目目录建议

| 文件夹 | 用途 | 命名规则 |
| --- | --- | --- |

## Rules

- Never delete older generated versions in the plan. Mark them as `废稿` if unused.
- Tie every generated image to a shot number and version.
- Tie every reference image to a shot number or a role: product, character, scene, style, composition.
- If the user asks for final delivery, identify selected assets and missing assets first.
- Align with `Sheet 7 出图生成记录`.
- When `asset-index.json` exists, read or update it before producing a manual asset table.
