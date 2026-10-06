# Execution Tools

## Environment And Scope

Use host Python for `scripts/blender_task.py`; the bridge runs with Blender's bundled Python and `bpy`. No pip package or connector is needed for this route. An explicit `--blender PATH` or `BLENDER_EXECUTABLE` wins over PATH/common-directory discovery. Multiple installations require the project's selected version, not an automatic upgrade.

`doctor` reports executable/version only; GPU usability and scene compatibility require inspection/test rendering. If Blender is missing, complete available planning/code checks, retain the skill and state that real execution is unverified. Do not invent a successful render or install a different application silently.

The runner uses separate background processes with factory startup and embedded script auto-run disabled. It neither reads unsaved UI edits nor connects to an open Blender session. User-preference plugins/GPU configuration may not be present; task scripts must establish the required settings explicitly. A reviewed interactive/MCP route may be used if actually available.

Task scripts run trusted Python with user filesystem access; this is not a sandbox. Read them before execution, scope writes to project output, and do not execute code embedded in untrusted reference files. No automatic paid assets, downloads or external rendering.

## Inspect

```powershell
python scripts/blender_task.py inspect --blend "PATH/project/scenes/master.blend"
```

Returns scene/camera, objects/material slots, mesh counts, frames/fps, engine/color settings and discovered external images/fonts/libraries/sounds. No saved scene mutation. Inspect selects the named `--scene` when supplied; a missing name is an error.

This is an inventory, not a complete model-quality or dependency audit. Cache/plugin/sequencer inputs need task-specific review. Sequence/tiled textures are flagged and refused by the general renderer, since one-file hashing would be insufficient. Use an expanded, validated dependency workflow for those scenes.

## Build Or Revise

Write a task-specific Python script that imports `bpy` and performs the approved scene changes. `OUTPUT_BLEND` and `PROJECT_ROOT` are available as globals; **leave saving to the runner**. Do not render, write unrelated files or reset a loaded scene unless the task requires it.

```powershell
python scripts/blender_task.py build --project-root "PATH/project" --script "PATH/project/scripts/task.py" --output "PATH/project/scenes/asset_v001.blend"
python scripts/blender_task.py build --project-root "PATH/project" --blend "PATH/project/scenes/asset_v001.blend" --script "PATH/project/scripts/material_revision.py" --output "PATH/project/scenes/asset_v002.blend"
```

The output must be a new project-contained .blend. The source remains unchanged by the bridge; the runner then reopens the saved output in another process and writes an inspection sidecar. A task script itself is trusted code, so review its source-preservation behavior too.

## Render And Resume

```powershell
python scripts/blender_task.py render --project-root "PATH/project" --blend "PATH/project/scenes/asset_v002.blend" --frames 1:24 --scale 25 --output-dir "PATH/project/render-runs/preview-v002"
python scripts/blender_task.py render --project-root "PATH/project" --blend "PATH/project/scenes/asset_v002.blend" --frames 1:24 --scale 25 --output-dir "PATH/project/render-runs/preview-v002" --resume
python scripts/blender_task.py status --output-dir "PATH/project/render-runs/preview-v002"
```

- Frames support comma-separated integers and inclusive `start:end`. Use bounded ranges; large projects should be partitioned into shots/ranges. Each frame launches a separate process: robust isolation, with measurable startup overhead.
- `--scene` selects a scene. `--engine` explicitly overrides the saved engine; omission inherits it. `--scale` is output percentage (default 100). `--format PNG|OPEN_EXR` writes a single-layer image; other passes/formats need custom execution.
- `--timeout` limits each Blender process (default 1800 seconds), not the entire job. Long render tasks can use the host's normal session mechanism; this script does not schedule background monitoring.
- Repeat `--dependency PATH` for reviewed external cache files/directories not discoverable by inspection. All referenced files are content-hashed; inventory cache completeness before rendering. Do not put render outputs inside an input dependency directory.
- A run signature covers scene bytes, discovered/explicit dependencies, version, runner code and settings. New settings/assets use a new directory. Resume verifies output hashes and decoded evidence; missing/corrupt frames get new attempt filenames without overwriting old media.
- A lock prevents concurrent writers. After abrupt termination inspect its recorded PID and actual process before explicitly removing a stale lock; never remove an active lock automatically.
- Compositor File Output nodes are refused. Cropped-border outputs also require a dedicated crop-aware workflow. Configure a versioned scene or task-specific runner instead of silently disabling scene behavior.

The runner outputs `render-manifest.json`, scene inspection, per-frame logs, verified frame images and (after full completion) an image-compatible `generation-log.json`. Saved scene render settings are not overwritten. Rendered does not mean visually approved.

## Real Acceptance Test

```powershell
python -m unittest discover -s tests -v
```

Host tests cover containment, evidence, changed dependencies, interrupted resume and source preservation. `test_live_blender.py` builds a small product scene, material/lighting, object animation and geometry nodes, renders two tiny frames, verifies resume, then creates a material-only revision and checks the source hash. It skips explicitly if Blender is unavailable. It does not validate production-quality facial rigs, fluid simulation or all export formats.

After connecting Blender, supplement that smoke test with the user's real product still, assembly motion, stage/procedural animation and existing-project revision. Review actual images/playback; passing script assertions is insufficient aesthetic validation.

## API Sources

Resolve details against the installed version; development docs are not a pinned runtime contract.

- [Blender command-line reference](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html)
- [Window/file operators](https://docs.blender.org/api/current/bpy.ops.wm.html)
- [Render operators](https://docs.blender.org/api/current/bpy.ops.render.html)
- [Image loading](https://docs.blender.org/api/current/bpy.types.BlendDataImages.html)
