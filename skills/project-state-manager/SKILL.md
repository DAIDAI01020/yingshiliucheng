---
name: project-state-manager
description: Manage project-level state for film AI workflows, including project-manifest.json, asset-index.json, and generation-job.json. Use when creating a new project workspace, tracking generation runs, locating image/prompt versions, or keeping Banana, built-in imagegen, Midjourney, and Seedance outputs connected to review boards and revisions.
---

# Project State Manager

## Core role

Keep the workflow state in one project-level source of truth. This skill manages:

- `project-manifest.json`: current project status, latest jobs, latest generation runs, and review-board links.
- `asset-index.json`: image, prompt, log, review-board, version, and asset-state records.
- `generation-job.json`: one unified job format that `$image-generation-controller` can use for logged Banana generation.

## Default project root

Use this structure for new managed projects:

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

Generator task folders live under `generation-runs\{timestamp}_{tool}\` when a `generation-job.json` has `projectRoot`, or under legacy `H:\yingshi\outputs\...` when using old inputs.

## Unified generation job

Use this shape:

```json
{
  "projectName": "",
  "projectRoot": "",
  "tool": "banana",
  "mode": "dry-run",
  "promptMode": "compact",
  "outputDir": "",
  "shots": [
    {
      "shot": "S01",
      "prompt": "",
      "negativePrompt": "",
      "ratio": "16:9",
      "references": []
    }
  ]
}
```

`tool` must be `banana`. `mode` must be `dry-run` or `real-generation`.

For Banana jobs, default `promptMode` is `compact` so the generator can use `compactPrompt` / `bananaCompactPrompt` while keeping `image_size: 2K`.

## Script usage

```powershell
node .\scripts\manage-project-state.mjs init --project-name "项目名"
node .\scripts\manage-project-state.mjs create-job --project-root H:\yingshi\projects\project --tool banana --input H:\yingshi\input.json --mode dry-run
node .\scripts\manage-project-state.mjs ingest --project-root H:\yingshi\projects\project --generation-log H:\...\logs\generation-log.json --review-board H:\...\review\review-board.md
node .\scripts\manage-project-state.mjs ingest-video --project-root H:\yingshi\projects\project --run-manifest H:\...\run_manifest.json
node .\scripts\manage-project-state.mjs find-asset --project-root H:\yingshi\projects\project --handle S01_banana_v01
```

## Rules

- Do not store API keys in project state files.
- Do not delete old asset records. Mark old or unused outputs as `废稿` only when instructed.
- `asset-index.json` is the first place to locate an existing generated image or prompt for revision.
- For legacy runs without a project root, do not force migration; ingest them only when the user asks or when a generation job includes `projectRoot`.
- If duplicate shot/tool/version handles exist, return the newest record first and keep all records for traceability.

