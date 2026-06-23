---
name: project-state-manager
description: Manage project-level state for film AI workflows, including project-manifest.json, asset-index.json, and generation-job.json. Use when creating a new project workspace, tracking generation runs, locating image/prompt versions, or keeping Banana, built-in imagegen, Midjourney, Jimeng, Kling, and Seedance outputs connected to review boards and revisions.
---

# Project State Manager

## Core role

Keep the workflow state in one project-level source of truth. This skill manages:

- `project-manifest.json`: current project status, latest jobs, latest generation runs, and review-board links.
- `asset-index.json`: image, prompt, log, review-board, version, and asset-state records.
- `generation-job.json`: one unified job format that `$image-generation-controller` can use for logged Banana generation.
- `style-lock.json`: current approved project style variables used by prompt directors.
- `project-intake.json`, `hook-audit.md`, `character-continuity.md`, `scene-map.md`, `shot-audit.md`, `prompt-audit.md`, and `generation-ready.json`: reusable formal short-drama state gates.

## P0 Core State Layer

For formal projects, `$project-state-manager` is the state and traceability layer. It does not make creative decisions, write prompts, audit prompts, or choose references. It stores or locates the approved outputs from the owning skills.

Track these packets when present:

```text
project_intake_packet -> project-manifest.json
short_drama_hook_packet -> references/hook-audit.md / generation-ready.json metadata
character_continuity_packet -> references/character-continuity.md / style-lock.json / generation-ready.json metadata
upstream_handoff_packet -> project-manifest.json / references / prompts metadata
mother_library_application_packet -> style-lock.json / scene-map.md / generation-ready.json metadata
director_contribution_packet -> character-continuity.md / style-lock.json / scene-map.md / shot-audit.md / prompt-audit.md / generation-ready.json metadata
visual_helpfulness_targets -> character-continuity.md / style-lock.json / scene-map.md / shot-audit.md metadata
visual_helpfulness_check -> prompt-audit.md / generation-ready.json metadata
scene_continuity_lock / background_continuity_lock / dialogue_coverage_packet -> references/scene-map.md / references/shot-audit.md
short_drama_scene_continuity_board -> asset-index.json / references/scene-map.md metadata
style_lock_packet -> style-lock.json
audited_prompt_packet -> prompts / generation-jobs metadata
generation_ready_packet -> generation-jobs / video-runs metadata
qc_feedback_packet -> asset-index.json / revision-logs
```

Required state lookups before revision or regeneration:

```text
current style-lock source
approved/audited prompt source
first frame or reference image source
generation run and output path
QC decision and failure type
client/user feedback revision source
```

If the project state lacks the needed asset, prompt, first frame, or audit record, return `missing_fields` and route back to the owner. Do not infer state from memory when a managed project has an index.

## Short-Drama State Workflow

For reusable short-drama projects, initialize the project with:

```powershell
node .\scripts\manage-project-state.mjs init --project-name "项目名" --workflow short-drama --route storyboard-execution
```

Supported routes:

```text
storyboard-execution
full-development
quick-test
```

Default route is `storyboard-execution` because most formal short-drama work starts from an existing script, storyboard, character setup, or reference images.

Formal short-drama projects use a strong generation gate:

```text
project-intake -> mother-library-application -> style-lock -> scene-map -> shot-audit -> prompt-audit -> generation-ready
```

Optimized formal short-drama projects use this stronger gate:

```text
project-intake -> hook-audit -> character-continuity -> mother-library-application -> director-contribution -> visual-helpfulness -> style-lock -> scene-map -> shot-audit -> prompt-audit -> generation-ready
```

`hook-audit` protects the first 3-8 seconds, conflict entry, information gap, payoff/cliffhanger, and AI execution risk. `character-continuity` protects recurring character face, hair, costume, age/body, performance state, relationship state, reference roles, generation anchor, and forbidden drift.

`director-contribution` preserves what each upstream director added: mother-library route, scene function, shot-language logic, character/product continuity, and prompt director translation. `visual-helpfulness` proves the final prompt's kept words protect or improve visible subject, composition, camera, light, material, motion, continuity, or concrete platform risks.

For formal same-scene coverage, `scene-map.md` must preserve:

```text
scene_continuity_lock
background_continuity_lock
dialogue_coverage_packet
camera_axis
screen_direction
background_side_map
prop_anchor
continuity_reference_board asset id/path when generated
```

If a scene contains master wide, reverse angles, over-shoulder, eye contact, reaction shots, interrogation, confrontation, or table/office/living-room dialogue and these fields are missing, the project is not generation-ready for batch same-scene image/video work.

Use this before formal batch generation:

```powershell
node .\scripts\manage-project-state.mjs check --project-root H:\yingshi\projects\project --stage generation
```

The check returns:

```text
ready
missingFields
routeBackTo
currentState
```

If `ready` is false, route back to the named owner skill. Do not let prompt or generation skills fill missing state decisions from memory.

## Default project root

Use this structure for new managed projects:

```text
H:\yingshi\projects\{projectSlug}\
  project-manifest.json
  asset-index.json
  project-intake.json
  style-lock.json
  generation-jobs\
    generation-ready.json
  generation-runs\
  video-runs\
  review\
  revision-logs\
    qc-feedback.md
  briefs\
  prompts\
    prompt-audit.md
  references\
    hook-audit.md
    character-continuity.md
    scene-map.md
    shot-audit.md
    continuity-boards\
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
node .\scripts\manage-project-state.mjs init --project-name "短剧项目名" --workflow short-drama --route storyboard-execution
node .\scripts\manage-project-state.mjs check --project-root H:\yingshi\projects\project --stage generation
node .\scripts\manage-project-state.mjs create-job --project-root H:\yingshi\projects\project --tool banana --input H:\yingshi\input.json --mode dry-run
node .\scripts\manage-project-state.mjs ingest --project-root H:\yingshi\projects\project --generation-log H:\...\logs\generation-log.json --review-board H:\...\review\review-board.md
node .\scripts\manage-project-state.mjs ingest-video --project-root H:\yingshi\projects\project --run-manifest H:\...\run_manifest.json
node .\scripts\manage-project-state.mjs find-asset --project-root H:\yingshi\projects\project --handle S01_banana_v01
```

For manual or external Jimeng / Kling / Kling O1 / Kling VIDEO 3.0 Omni runs, `ingest-video` may ingest a handoff `run_manifest.json` with:

```text
provider / target_tool / target_model
shot / version
prompt.source
reference_roles
first_frame_or_image_refs
audio_policy
outputs.video（optional before manual execution）
task.status: manual_handoff / succeeded / failed
```

When `outputs.video` is empty and status is `manual_handoff`, the asset state is `待执行`. When a video path is present and status is `succeeded`, the asset state is `候选`.

## Rules

- Do not store API keys in project state files.
- Store only approved visual variables in `style-lock.json`; do not store private reference URLs or temporary generation URLs.
- Store prompt audit status as metadata only; do not change the audited prompt text inside project-state-manager.
- Store first-frame/public relay provenance without storing private upload tokens.
- Keep QC and revision decisions tied to the source generated asset and source prompt.
- Do not delete old asset records. Mark old or unused outputs as `废稿` only when instructed.
- `asset-index.json` is the first place to locate an existing generated image or prompt for revision.
- For short-drama same-scene work, `asset-index.json` should record any `short_drama_scene_continuity_board` as a reusable reference asset linked to its `scene_id`.
- For legacy runs without a project root, do not force migration; ingest them only when the user asks or when a generation job includes `projectRoot`.
- If duplicate shot/tool/version handles exist, return the newest record first and keep all records for traceability.

