---
name: project-state-manager
description: Manage project-level state for film AI workflows, including project-manifest.json, asset-index.json, and generation-job.json. Use when creating a new project workspace, tracking generation runs, locating image/prompt versions, or keeping Banana, built-in imagegen, Midjourney, Jimeng, Kling, and Seedance outputs connected to review boards and revisions.
---

# Project State Manager

## Core role

Keep the workflow state in one project-level source of truth. This skill manages:

- `project-manifest.json`: current project status, latest jobs, latest generation runs, and review-board links.
- `asset-index.json`: image, prompt, log, review-board, version, and asset-state records.
- `generation-job.json`: Banana-specific executable job format used by `$banana-image-generator`.
- `generation-ready.json`: generic approved execution record for built-in imagegen, Banana, Midjourney, Jimeng, Kling, Seedance/Ark, and manual handoffs.
- `style-lock.json`: current approved project style variables used by prompt directors.
- `project-intake.json`, `scene-map.md`, `shot-audit.md`, `prompt-audit.md`, and `generation-ready.json`: reusable formal short-drama state gates.
- Same-scene continuity locks and continuity reference boards for short-drama coverage work.
- `generation-observations.jsonl`: QC evidence tied to source assets/prompts for targeted future fixes.

## P0 Core State Layer

For formal projects, `$project-state-manager` is the state and traceability layer. It does not make creative decisions, write prompts, audit prompts, or choose references. It stores or locates the approved outputs from the owning skills.

## Route Authority Boundary

Inherit `$zongkong` route decisions when a `zongkong_route_packet` is present.

This skill owns state persistence and lookup. It does not choose project tier, change `speed_mode`, invent creative decisions, approve prompts, generate media, or downgrade formal gates.

If an owning packet is missing, return `missing_fields` and `route_back_to` instead of creating creative content to fill the state. Store approved outputs from the owning skills; do not become the owner of those decisions.

Track these packets when present:

```text
project_intake_packet -> project-manifest.json
upstream_handoff_packet -> project-manifest.json / references / prompts metadata
mother_library_application_packet -> style-lock.json / scene-map.md / generation-ready.json metadata
scene_continuity_lock / background_continuity_lock / dialogue_coverage_packet -> references/scene-map.md / references/shot-audit.md
short_drama_scene_continuity_board -> asset-index.json / references/scene-map.md metadata
style_lock_packet -> style-lock.json
audited_prompt_packet -> prompts / generation-jobs metadata
generation_ready_packet -> generation-jobs / video-runs metadata
qc_feedback_packet -> asset-index.json / revision-logs
generation_observation -> generation-observations.jsonl / asset-index.json metadata
```

Normalize skill packet fields to snake_case. Convert script responses such as `missingFields` and `routeBackTo` at this boundary into `missing_fields` and `route_back_to`; do not pass mixed naming downstream.

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

If a scene contains 大景/全景、正反打、过肩、对视、反应镜头 and these fields are missing, the project is not generation-ready for batch same-scene image/video work.

Use this before formal batch generation:

```powershell
node .\scripts\manage-project-state.mjs check --project-root {project_root} --stage generation
```

The check returns:

```text
ready
missingFields
routeBackTo
currentState
```

If `ready` is false, route back to the named owner skill. Do not let prompt or generation skills fill missing state decisions from memory.

## Project Root Authority

Use `project_folder_contract.project_root` and `output_path_rule` as the authority. If a new project root, output path, or messy folder needs to be decided, route to `$project-folder-director` first. Do not impose a drive from this skill.

Use this structure for new managed projects:

```text
{project_root}\
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
    generation-observations.jsonl
  briefs\
  prompts\
    prompt-audit.md
  references\
    scene-map.md
    shot-audit.md
    continuity-boards\
```

Generator task folders live under `{project_root}\generation-runs\{timestamp}_{tool}\` when a managed job has a project root. Preserve legacy paths for existing jobs; do not force migration.

## Banana Execution Job

Use this shape:

```json
{
  "projectName": "",
  "projectRoot": "",
  "tool": "banana",
  "mode": "dry-run",
  "promptMode": "quality",
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

This restriction applies only to `generation-job.json` consumed by the current Banana script. It is not the generic cross-platform execution schema.

For all tools, preserve the generic record:

```text
generation_ready_packet
asset_or_shot_id:
platform_target:
deliverable_profile:
execution_mode: built_in / api / external_manual
approved_prompt_source:
reference_roles:
output_path_rule:
response_mode:
qc_mode:
music_policy: no_music_allow_sfx / music_requested / full_silence（video only）
manual_execution:
```

For legacy video packets without `music_policy`, normalize to `no_music_allow_sfx` unless the approved prompt or user instruction explicitly requests music or full silence. Preserve the selected policy through prompt audit, generation-ready state, run manifest, asset ingest, and QC.

For Banana jobs, default `promptMode` is `quality` so every storyboard shot uses its full self-contained prompt. Use `compact` only when the user explicitly asks for `省 token`, a fast test, or compact execution; keep `image_size: 2K` unless the user requests otherwise.

## Script usage

```powershell
node .\scripts\manage-project-state.mjs init --project-name "项目名"
node .\scripts\manage-project-state.mjs init --project-name "短剧项目名" --workflow short-drama --route storyboard-execution
node .\scripts\manage-project-state.mjs check --project-root {project_root} --stage generation
node .\scripts\manage-project-state.mjs create-job --project-root {project_root} --tool banana --input {input_json} --mode dry-run
node .\scripts\manage-project-state.mjs ingest --project-root {project_root} --generation-log {generation_log} --review-board {review_board}
node .\scripts\manage-project-state.mjs ingest-video --project-root {project_root} --run-manifest {run_manifest}
node .\scripts\manage-project-state.mjs find-asset --project-root {project_root} --handle S01_banana_v01
```

For manual or external Jimeng / Kling / Kling O1 / Kling VIDEO 3.0 Omni runs, `ingest-video` may ingest a handoff `run_manifest.json` with:

```text
provider / target_tool / target_model
shot / version
prompt.source
reference_roles
first_frame_or_image_refs
audio_policy
music_policy
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
- Keep generation observations tied to source asset, source prompt, platform, deliverable profile, and attempted fix. Promote repeated evidence deliberately; never let state storage invent a new global rule.
- Do not delete old asset records. Mark old or unused outputs as `废稿` only when instructed.
- `asset-index.json` is the first place to locate an existing generated image or prompt for revision.
- For short-drama same-scene work, `asset-index.json` should record any `short_drama_scene_continuity_board` as a reusable reference asset linked to its `scene_id`.
- For legacy runs without a project root, do not force migration; ingest them only when the user asks or when a generation job includes `projectRoot`.
- If duplicate shot/tool/version handles exist, return the newest record first and keep all records for traceability.

