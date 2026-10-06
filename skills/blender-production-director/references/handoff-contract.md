# Blender Task And Result Handoff

## Task Packet

Internal; populate applicable fields only, without asking users to fill a form.

```text
blender_task_packet
task_id / shot_ids
execution_intent: plan / generate / revise / review / status / archive
blender_mode: plan / preview / production
project_root / source_blend / source_version
deliverables: editable_scene / model_export / still / image_sequence / movie / passes
must_preserve / requested_delta / reference_roles / approved_style_source
dimensions_and_units / precision: measured / inferred / artistic
objects_or_collections / camera / scene
fps / frames / output_size / engine / color_management
dependencies / cache_version / dependency_review / output_paths / render_scope
```

Keep the existing `speed_mode` for project weight. Pure 3D may use `deliverable_profile: three_d_asset / three_d_render / three_d_animation`; existing product/KV/stage/shot profiles remain valid. Plan intent is not prompt_only.

## Result Packet

```text
blender_result_packet
task_id / shot_ids / source_blend / output_blend / blender_version / engine
scene_inspection / render_manifest / generation_log
verified_files / missing_files / dependencies / caches
technical_status / visual_qc_status / selection_status
next_action / unresolved_limitations
```

Link local scene/render evidence into existing state through `$project-state-manager`; preserve unrelated fields and avoid a competing asset index.

The runner's `generation-log.json` supports image ingest: each verified frame has tool `blender`, a frame-specific shot ID, actual file path and success status. Map production shot IDs when appropriate. An image sequence is not a completed video; only encode/validate an actual movie before video-manifest ingest.

Hand editable .blend/export metadata to `$asset-librarian` and the state owner. Existing image/video ingest commands are not universal 3D ingesters; never disguise .blend as an image.

## Evidence States

- `planned`: decisions/scripts only.
- `scene_saved`: saved .blend reopens; quality may remain unreviewed.
- `rendering` / `incomplete`: some frames may exist.
- `rendered`: all requested frames decode at expected dimensions and match recorded evidence.
- `qc_passed`: actual visual/motion review passed, stored separately.
- `selected` / `delivered`: explicit selection / verified requested package.

Changed camera/material/animation/cache invalidates affected downstream outputs, not every creative decision. Preserve selected prior versions. New input fingerprints require a new run; matching runs reuse only verified frames.
