---
name: blender-production-director
description: Create, revise, inspect and deliver Blender 3D projects under zongkong, covering modeling, materials, lighting, cameras, rigging, animation, geometry nodes, simulation, rendering and compositing. Use for explicit Blender work, existing .blend files or editable 3D deliverables. A 3D-looking AI image alone does not select Blender.
---

# Blender 三维制作导演

Own Blender scene design and execution from references or existing projects through editable assets, rendered images, animation and delivery. Follow the actual request: planning stays planning; a material edit preserves the rest of the scene; full production continues to verified artifacts.

## Position Under Zongkong

- Inherit the project, brief, approved style, shot IDs, output contract and scoped authorization. Do not reopen creative development for an established scene.
- `$zongkong` owns routing. This skill owns Blender technical and artistic implementation. `$project-folder-director` owns managed paths; `$project-state-manager` owns shared state; `$asset-librarian` owns delivery indexing.
- Reuse commercial, KV, typography or LED direction. Editable 3D lettering, objects or explicit Blender animation selects this branch; “3D风格图片” alone stays on the selected image route.
- Reuse `$image-qc-director` and `$video-qc-director` for output review. This skill additionally checks scene dependencies, geometry, rigs, caches and rendering evidence.
- Pure Blender work does not require `$prompt-platform-auditor`, AI generation-ready gates or video-provider submission. Transfer a rendered frame into AI video only when requested.

## Read Only The Relevant Module

| Task | Reference |
| --- | --- |
| Products, props, environments, lettering, UV and shaders | [Modeling and materials](references/modeling-materials.md) |
| Camera/object animation, rigging, geometry nodes and simulation | [Animation and simulation](references/animation-simulation.md) |
| Composition, lighting, engines, color, passes and delivery QC | [Lighting, rendering and delivery](references/lighting-render-delivery.md) |
| Environment detection, scripts, inspection, versioned builds and resumable renders | [Execution tools](references/execution.md) |
| Input/output packets, ownership and managed state | [Handoff contract](references/handoff-contract.md) |

## Modes And Entry Points

`blender_mode: plan / preview / production` is local to this skill; keep Zongkong's `speed_mode` separate.

- **Plan**: assess references, assets, precision, delivery and production approach. Do not build/render merely because a plan mentions it. Read-only environment inspection is allowed when useful.
- **Preview**: use a small scene, representative frame, clay render or short animation to answer the visual question. Save reusable editable work when requested; no formal registry merely for a preview.
- **Production**: implement requested assets/shots, verify dependencies and settings, render within scope, review and deliver. Reuse approvals; do not insert confirmation at every stage.

Enter at new scene, existing .blend, asset import, material/light edit, animation, render-only, compositing, troubleshooting or export. Completed phases are inputs, not work to repeat.

Pure Blender tasks use `workflow_mode: blender_production`, `platform_target: blender`, `prompt_task: none`. A Blender step within an existing commercial/KV/short-drama workflow preserves that workflow and creative profile; add a `blender_task_packet`. `model_target` is not the Blender version field.

## First Useful Action

1. Read the task/assets; identify deliverables, reference roles and what must remain unchanged.
2. For execution, run the environment doctor. Do not assume a connector, plugin, GPU or engine is available. Explicit `--blender` or `BLENDER_EXECUTABLE` overrides discovery.
3. Inspect existing .blend in an isolated process. Use the saved file; do not claim access to unsaved UI edits. Preserve the source and write a new version.
4. Resolve blocking decisions only: exact dimensions require measurements; visual approximation can proceed with stated assumptions. Ask for a source only when ambiguous candidates would change the result.
5. Write a task-specific script or use the existing scene, inspect representative results, then carry the authorized scope through to actual artifacts.

## Production Rules

- Match silhouette, proportions, materials, lighting and composition to the intended use. More polygons/samples or photorealism are not universal quality criteria.
- Preserve editable geometry/modifiers, named materials, collections, cameras and controls where useful. Bake/triangulate export copies only as the destination requires.
- Use stable object/shot IDs and versioned .blend files. Local revisions change the target and necessary dependencies, not the entire direction.
- Record relevant units, scale, fps, frames, output size, engine and color management. Inherit existing settings unless the requested change requires otherwise.
- Estimate render cost from representative frames; distinguish startup, frame rendering, baking, compositing and encoding. Estimates are not guarantees.
- Existing authorized scope proceeds without repeated approval. New paid assets/cloud rendering/publishing need authorization covering those actions.
- A single-view reconstruction is not dimensionally exact. Character rigs, hair and complex simulations need their own visual/motion verification before production-ready claims.
- Verify simulation cache range/version and dependencies. Do not silently remove effects or substitute missing assets.

## Evidence And Recovery

Scene saved, technical render success, visual QC and client selection are separate states. Scripts and planned filenames are not finished assets.

The runner reopens saved .blend files, decodes rendered images and records frame evidence. Resume requires matching scene content, external dependencies, Blender version, runner code and settings. Changed inputs start a new run; do not mix old/new frames. Preserve completed frames after interruption.

Embedded Blender script auto-execution is disabled by the runner. A broken script-dependent rig needs dependency investigation and a separately reviewed execution path; never silently enable it.

## Tools And Verification

Run from this skill directory using host Python:

```powershell
python scripts/blender_task.py doctor
python scripts/blender_task.py inspect --blend "PATH/scene.blend"
python scripts/blender_task.py build --project-root "PATH/project" --script "PATH/task.py" --output "PATH/project/scenes/scene_v002.blend"
python scripts/blender_task.py render --project-root "PATH/project" --blend "PATH/project/scenes/scene_v002.blend" --frames 1,12,24 --output-dir "PATH/project/render-runs/preview-v002"
python scripts/blender_task.py status --output-dir "PATH/project/render-runs/preview-v002"
```

Options, limits and acceptance fixtures are in [execution tools](references/execution.md). The helpers do not fabricate arbitrary geometry from prose: the director writes the task-specific Blender script and checks its result.

Run `python -m unittest discover -s tests`. Live Blender tests skip when unavailable; passing host-side tests does not prove Blender execution.

## Completion

Return requested media and editable .blend/export, concise verification and remaining limitations. Image sequences need explicit fps/frame range and must not be called encoded videos. Show scripts only when requested or useful for reuse/debugging.

For managed delivery pass verified files/evidence through the [handoff contract](references/handoff-contract.md). Render manifests are local job evidence linked from shared state, not a second project registry.
