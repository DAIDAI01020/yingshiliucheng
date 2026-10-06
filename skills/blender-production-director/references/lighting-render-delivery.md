# Lighting, Rendering, Compositing And Delivery

## Look Development

Start with purpose, hierarchy, material visibility, palette and reference lighting. Product light reveals form/finish; stage work respects screen geometry/viewing distance; stylized work follows its own approved language.

Choose camera perspective, depth and motion blur for the shot. Preserve cameras when only material/light edits are requested. Check composition for each delivered ratio.

Record color management and intended viewing/export transform. Keep scene-linear/HDR compositing data distinct from display-ready output; avoid applying display transforms twice.

## Engine And Budget

Inspect engine/device availability and scene requirements. Choose Eevee/Cycles according to effect support, visual target and measured speed. Do not silently switch engine or CPU/GPU after failure; API/engine names vary by version.

Test representative frames including expensive materials, volumes and blur. Set final resolution, fps, frames, samples, denoising, passes and transparency from the deliverable.

For longer animation prefer resumable image sequences, followed by encoding. Distinguish rendering estimates from baking/compositing/encoding time.

## Passes And Compositing

Specify needed beauty, alpha, depth, normals, masks or lighting passes. Verify names and alpha interpretation in actual files. Use appropriate scene-linear formats for downstream compositing.

Inspect compositor/sequencer output paths. The bundled simple renderer refuses compositor File Output nodes; redirect/disable them in a versioned scene or use an explicitly scoped compositor runner. It writes PNG or single-layer OpenEXR. Multilayer passes, movie encoding and advanced compositing need task-specific scripts and validation.

## Review

| Deliverable | Evidence |
| --- | --- |
| Editable scene | Reopen .blend; inspect units, expected objects/cameras, materials, dependencies, editability |
| Still | Decode file, verify dimensions/transparency/color; inspect geometry, composition, material and light |
| Animation | Expected frames/fps/duration; preview playback for motion, intersections and flicker |
| Simulation | Cache version/range and representative playback without unintended reset |
| Export | Open/reimport and check geometry, scale, texture links and animation |
| Package | Selected versions, accessible resources, final media, editable source and usage notes |

Technical decoding is not visual approval. Contact sheets do not prove complete animation/audio quality. Keep uninspected aspects explicit.

## Delivery

Provide requested artifacts and dependencies. Packing resources may omit fonts, caches, linked scenes or licensed assets; verify before saying fully packed.

For AI continuation label frames/depth/masks with shot IDs, dimensions and reference roles. The downstream owner handles platform prompts and execution authorization.

LED work uses actual canvas/screen layouts. AE screen-split parameters belong to `$aedaping`; Blender owns scene/camera/render implementation.
