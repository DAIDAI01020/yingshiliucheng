# Dynamic screen design and delivery

Read for animated event KV, standby loops, countdowns, chapter transitions, multi-screen motion or procedural visuals. `kv-director` retains visual identity/composition; `led-screen-director` owns screen motion constraints; `event-opener-director` owns ceremony timing and the stage handoff. Use existing execution skills/tools only when available and appropriate.

## Pick the actual deliverable

| Request | Design and execution judgment |
| --- | --- |
| Static main visual / backdrop | Complete the still composition; no animation setup is required |
| Ambient standby loop | Limited motion, stable title/presenter areas, repeatable time cycle |
| Countdown | Deterministic digits and timing; readable holds, final trigger and landing state |
| Opening / reveal film | Authored progression and a known landing for host, lighting or product cue |
| Chapter or award package | Shared type/motion identity with replaceable exact names and copy |
| Real-time interactive visual | Separate live project/runtime, input mapping and fallback playback; a rendered movie is not an interactive system |

Do not translate every screen into a moving AI image. Exact text/timing can use an available AE or programmatic animation route; three-dimensional materials, camera movement and simulation can use `blender-production-director`; authored AI visual motion goes through `ai-video-prompt-director` and the chosen execution platform. Remotion/p5.js are optional approaches, not assumed installed capabilities. Never silently substitute a browser demo for the requested video or an editable AE project.

## Motion handoff

Extend the existing `upstream_handoff_packet` with a `motion_design` object only when motion is requested. Include applicable fields; omit real-time fields for a rendered loop:

```text
purpose: standby_loop / countdown / reveal / chapter / live_interactive
source_kv_and_revision:
canvas_pixels_and_screen_map:
fps / total_frames:
timebase: authored timeline / audio beats / show-control cue
layers: static copy / hero / ambient / transition
motion_hierarchy: dominant movement, supporting movement, protected quiet zones
timing_beats: start frame, end frame, observable action, landing state
loop_period_and_seam_rule:
multi_screen_phase_and_shared_coordinates:
ending_hold_and_stage_cue:
execution_route_and_availability:
delivery: format, codec, alpha requirement, filenames, playback constraints
live_input_and_fallback: when relevant
```

Use the source project's physical canvas, not a default 16:9 or 9:16. For arbitrary widths and irregular screens, animate one shared virtual world or explicitly coordinated modules before delivery splitting. Keep joins, masks and camera sightlines from the screen owner. `aedaping` owns its supported rectangular/row AE split calculations; complex mapping requires the actual map and suitable tooling.

## Controlled procedural motion

Describe motion through visible behaviour rather than tool names: broad streams converging, sparse particles orbiting a fixed symbol, a surface growing along one path, or slow material light changes. Define scale, density, speed and contrast against the screen's viewing distance. Preserve low-motion zones behind titles and live subjects. Do not import the upstream viewer's branding, controls or UI into screen content.

If using a procedural backend, retain the seed, parameter values, source revision and time origin. A seed makes the initial system reproducible; it does **not** guarantee a seamless loop. Design a periodic state or an explicitly authored transition. Particles need matched lifecycle/state at the boundary, not simply a matching colour at the first and last frame. A forward/backward playback loop is a deliberate motion choice, not an automatic fix for every simulation.

For rendered animation, derive motion from frame number and the project's fixed FPS. Avoid wall-clock timing or uncontrolled random values during capture. If several screens share a pattern, sample common coordinates/time rather than independently randomizing each screen. Separate exact title layers from ambient movement so copy revisions need not regenerate the visual world.

## Countdown and ceremony timing

Specify the display interval for each numeral and whether zero is shown. For example, a 10-second countdown at 25 FPS can use frames `[0,25)` for 10 through `[225,250)` for 1, with the reveal starting at frame 250; any reveal/hold extends the deliverable beyond those 250 frames. This is an example, not a fixed preset. Use the actual FPS and agreed event cue; check boundaries for duplicate or missing digits.

Define whether audio is absent, ambient/SFX, music-driven or synchronized to a supplied track. Keep the user's existing music policy. A visual beat plan alone does not establish synchronization to venue lighting or show control; record the operator's cue and actual playback arrangement. The ending must allow the host, product or next segment to take over rather than drifting into an arbitrary fade.

## Verify before delivery

- Preview the complete motion and representative beginning/middle/end frames. Inspect actual text, gradients, clipping and presenter-safe areas; still-frame approval is not motion approval.
- For a loop, play at least two consecutive cycles and inspect position, velocity, brightness and any audio seam. Compare time `T` with time `0`; the last encoded frame at `T - 1/FPS` need not be identical to the first. Avoid a duplicated endpoint that produces a visible pause.
- For multi-screen delivery, review a combined stage/map preview and each exported piece. Check common frame counts/FPS, timing, missing areas and visible joins. Geometry assumptions must be resolved for final delivery.
- Check decoded dimensions, duration/frame count, codec and any requested alpha against the playback specification. Browser smoothness does not prove final export performance or venue compatibility.
- Review high-frequency patterns, abrupt luminance changes and camera readability using the existing screen rules. Final camera/LED behaviour needs venue or representative hardware testing; software previews cannot certify it.

Deliver the requested rendered media and/or editable source, along with concise playback/split notes. Label previews, final renders and live projects accurately. Keep accepted stills and unaffected variants during revision; changing a countdown numeral or sponsor line should not automatically rebuild the background.

## Source ideas and limits

Reviewed 2026-10-14; independently integrated methods, not a bundled runtime:

- [Anthropic algorithmic-art](https://github.com/anthropics/skills/tree/main/skills/algorithmic-art): seeded procedural variation and adjustable visual parameters. Adapt its exploration to screen scale; its HTML viewer alone is not a venue-ready loop.
- [Remotion Skills](https://github.com/remotion-dev/skills): composition, preview and rendering as distinct production operations. Use current official instructions only if that backend is selected and available; installing a workflow rule does not install Remotion or verify its output.

The timing, loop, multi-screen and stage-cue rules above are local production adaptations. Do not represent upstream repository stars as evidence of LED deployment quality.
