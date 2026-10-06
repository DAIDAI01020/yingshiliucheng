# Animation, Rigging And Procedural Effects

## Timing And Cameras

Translate the shot into starting state, beats, timing and ending state. Preserve fps/duration and choose interpolation intentionally. Do not impose a universal linear move or breath tail.

Turntables require silhouette/specular checks across the rotation. Exploded/assembly views need meaningful pivots, clear travel directions and a stable final assembly. Camera paths need framing, clipping and roll checks throughout.

Review a low-cost motion preview before expensive output. Contact sheets check poses, not continuous timing; playback must check jerks, intersections, foot sliding, constraint pops and blur.

## Rigs

Inspect controls, rest pose, scale and action ownership before edits. Preserve rig controls/source actions; retarget or bake copies only when needed. Test extreme poses and contacts before extending a shot.

Facial performance, skin/hair and complex cloth contact need close-up/motion validation. Basic rig setup alone is not production-ready performance. Do not enable embedded scripts to make an unknown rig work; establish trusted dependencies separately.

## Geometry Nodes

Use editable nodes for scattering, arrays, procedural forms, growth and motion. Name inputs by production meaning and keep deterministic seeds for repeatable revision.

Check node/socket availability against the installed API. Realize instances only when required. Check bounds, density and memory use in the actual camera; high counts alone are not quality.

## Simulation

Specify solver, scale, collision geometry, preroll/frame range, cache location and dependencies. Test a representative small range before costly baking.

Rigid bodies need collision/mass/contact checks; cloth needs thickness/pinning/collision checks; fluids/volumes need domain, resolution, boundaries and cache-size checks. Bake into a versioned project-contained directory.

Geometry, animation or solver changes invalidate dependent caches. Use new cache/render identities. Isolated frame renders without required baked state do not prove a valid simulation.

The bundled renderer does not bake solvers or enumerate every plugin/cache dependency. Use a task-specific bake script, verify range coverage and include cache directories with `--dependency`.

## Export

Choose FBX/glTF/Alembic/USD or other output according to destination and available exporter. Reimport or test destination playback for axes, units, materials, rig/actions and range. Do not promise Blender shader/constraint equivalence in all formats.

Keep editable .blend as master. A frame sequence needs encoding/playback verification before movie delivery. Sound follows the actual brief, not an invented soundtrack.
