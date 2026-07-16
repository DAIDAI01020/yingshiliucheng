---
name: project-folder-director
description: Simple project folder structure director for AI film and visual workflows. Use when Codex or zongkong creates a new project, continues an existing project, decides output paths, prevents files from being dumped into the workspace root, classifies loose docs/images/videos/prompts, or prepares a safe folder cleanup plan before moving assets.
---

# Project Folder Director

## Core Role

Keep each project inside one clean project root with a simple folder structure.

This skill owns:

- project root selection and slug naming.
- simple folder contract for new and existing projects.
- output path rules for docs, images, videos, prompts, references, review, and delivery.
- loose-file classification and safe move plans.
- handoff to `$project-state-manager` and `$asset-librarian`.

It does not make creative decisions, write prompts, generate images/videos, delete files, or silently move user files.

## Route Authority Boundary

Inherit `$zongkong` route decisions when a `zongkong_route_packet` is present.

This skill owns folder contracts, output path rules, loose-file classification, and move plans. It does not choose creative route, change `speed_mode`, decide formal generation readiness, rewrite state, or manage asset quality.

If project tier, project slug, move approval, or state owner is unclear, output `missing_fields` and route back instead of silently creating or moving project material.

## Hard Rules

- Resolve `projects_root` from, in order: an existing project contract, an explicit user/configured root, or `{current_workspace_root}\projects`.
- Never place project outputs directly under the workspace root unless the user explicitly asks for a temporary one-off file.
- Formal and quick projects must use `{projects_root}\{projectSlug}\`.
- Misc tests use `{projects_root}\_misc\{date_or_slug}\` when more than one managed file may be created.
- Before a tool writes files, produce an `output_path_rule`.
- Never move, rename, overwrite, or delete existing files without a visible move plan and user approval.
- If a target file exists, keep both files and propose a suffix such as `_dup01`; do not overwrite.
- Keep the folder tree broad. Do not over-sort into many subfolders unless the user asks.

## Standard Project Tree

Use this simple default tree:

```text
{projects_root}\{projectSlug}\
  project-manifest.json
  asset-index.json
  00_inbox\
  docs\
  images\
  videos\
  prompts\
  references\
  review\
  delivery\
  archive\
```

Folder meanings:

```text
docs        Word/PDF/Markdown/TXT/Excel/PPT/source docs/storyboards/reports
images      PNG/JPG/WebP/TIFF, including generated images, contact sheets, reference grids, poster/KV drafts
videos      MP4/MOV/AVI/MKV/WebM
prompts     prompt text, input JSON, run manifests, generation-ready files
references  packed reference material, archives, downloaded reference packages
review      review notes, comparison boards if the user wants them separate
delivery    final handoff files
archive     retained old material only when the user asks to archive
00_inbox    unknown or ambiguous files
```

Managed state files from `$project-state-manager` can still live in the project root. Do not create deep state folders unless that tool needs them.

## Workflow

### 1. Create or Reuse Project Root

Infer `projectSlug` from the project name when possible:

```text
开学第一课2026 -> kaixue-diyike-2026
品牌发布会KV -> brand-launch-kv
短剧《失踪的丈夫》 -> shizong-de-zhangfu
```

Output:

```text
project_folder_contract
project_name:
project_slug:
projects_root:
project_root:
project_tier: formal / quick / misc
workflow_mode:
must_create_dirs: docs / images / videos / prompts / references / review / delivery / archive / 00_inbox
state_owner: project-state-manager / none
asset_owner: asset-librarian
```

### 2. Assign Output Path Rules

Every downstream prompt or generation handoff must include an `output_path_rule`.

```text
documents/reports/storyboards -> docs\
still images/contact sheets/reference grids/generated images -> images\
videos -> videos\
prompt files/input JSON/run manifests -> prompts\
reference packages/archives -> references\
final handoff files -> delivery\
unknown files -> 00_inbox\
```

Example:

```text
output_path_rule
project_root: {projects_root}\kaixue-diyike-2026
docs_output_dir: {project_root}\docs
image_output_dir: {project_root}\images
video_output_dir: {project_root}\videos
prompt_output_dir: {project_root}\prompts
do_not_write_to: {current_workspace_root}
```

### 3. Classify Loose Files

When a user says files are messy, first inspect and produce a plan. Do not move yet.

Use `scripts/plan_project_folder.py`:

```powershell
python C:\Users\admin\.codex\skills\project-folder-director\scripts\plan_project_folder.py `
  --source-dir "{source_dir}" `
  --project-root "{project_root}"
```

Apply only after user approval:

```powershell
python C:\Users\admin\.codex\skills\project-folder-director\scripts\plan_project_folder.py `
  --source-dir "{source_dir}" `
  --project-root "{project_root}" `
  --apply
```

Simple classification:

```text
docs: .doc .docx .pdf .md .txt .ppt .pptx .xls .xlsx .csv
images: .png .jpg .jpeg .webp .tif .tiff .bmp
videos: .mp4 .mov .avi .mkv .webm
prompts: prompt / 提示词 / *_input.json / run_manifest / generation_job / generation_ready
references: .zip .rar .7z and obvious reference packages
delivery: only files explicitly named delivery / deliver / 交付
00_inbox: unknown
```

### 4. Handoff

For new managed projects:

```text
$project-folder-director
-> $project-state-manager init
-> downstream creative/prompt/generation skill
```

For messy existing folders:

```text
$project-folder-director move_plan
-> user approval
-> apply move plan
-> $asset-librarian asset table
```

For quick prompt-only tasks, do not force a formal project tree. If the request creates files, place them in:

```text
{projects_root}\_misc\{YYYYMMDD}_{short_slug}\
```

## Required Output

When this skill is used, return this compact packet:

```text
project_folder_contract
project_name:
project_slug:
projects_root:
project_root:
project_tier:
workflow_mode:
folder_status: new / exists / needs_repair / loose_files_detected
must_create_dirs:
output_path_rule:
loose_file_plan:
requires_user_approval_before_move: true / false
next_skill:
```

If the user only wants the skill/rules updated, do not organize real files.
