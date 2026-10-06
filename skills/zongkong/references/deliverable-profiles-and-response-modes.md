# Deliverable Profiles And Response Modes

Use this reference to select task-specific prompt requirements, user-visible output, and QC depth. Choose one primary profile. Add a secondary profile only when the deliverable genuinely combines two functions, such as a photographic product KV.

## Contents

- Deliverable profiles
- Conditional gates
- Response modes
- QC modes
- Prompt visibility

## Deliverable Profiles

| Profile | Required accuracy | Apply only when relevant | Do not require by default |
| --- | --- | --- | --- |
| `three_d_asset` | source/version, scale/units, geometry, materials, editability, dependencies and export requirements | deformation topology, UV/baking, destination import tests | image-prompt audit, render camera for model-only work, exact dimensions inferred from one image |
| `three_d_render` | scene/camera, reference/style, engine, color management, dimensions, dependencies, actual readable output | alpha, passes, compositor, multiple ratios | AI provider prompt/generation gates, animation fields for a still |
| `three_d_animation` | editable scene/rig, fps/range, action/camera timing, cache dependencies, complete frame evidence and playback | simulation, sound, export/encoding | universal breath tail, assumed AI platform, image sequences counted as movies |
| `live_action_people` | visible subject, performance state, scene, composition, motivated light, color/material, identity continuity, realism risks | camera/lens/depth, mother-library application, skin/hand controls | typography, product geometry, stage-safe zones |
| `product_structure` | exact structure, proportions, material, color, logo/text policy, placement, reflections | camera/light when photographic; motion physics for video | skin realism, hook audit, breath tail |
| `commercial_kv` | claim/hook, first-read hierarchy, composition, negative space, title/logo/sponsor-safe zones, ratio | product or live-action extension; reference system when aesthetic continuity matters | shot audit, breath tail, full scene map for one master KV |
| `graphic_abstract` | shape language, layering, palette, density, rhythm, edge quality, forbidden style drift | stage/LED safe areas when displayed live | camera brand, focal length, skin realism, mother-library cinematography |
| `typography_asset` | exact glyphs, legibility, extrusion/bevel/material when 3D, transparency, clean edges | layout-safe placement and reference lettering roles | scene map, shot audit, skin realism, breath tail |
| `led_stage` | screen ratio, center safe area, performer/presenter safety, distance readability, extension behavior | photographic or graphic sub-profile as needed | character continuity or hook audit unless narrative characters actually recur |
| `local_edit` | base-image/video lock, named target region, exact delta, reference roles, do-not-inherit, blend/integration | subject/product-specific identity or structure locks | new global style, full-frame redesign, unrelated formal gates |
| `storyboard_frame` | shot function, visible beat, spatial layout, continuity, composition/camera language, light/material, ratio | live-action/product/graphic risk controls selected by content | fixed camera brand/aperture when they do not improve the frame |
| `video_i2v` | source authority, must-preserve lock, subject action, camera behavior, environment/light change if any, ending behavior, duration/ratio, default `no_music_allow_sfx` policy | positive audio instructions only when platform/task supports or requests them; breath only when motivated | full image-style restatement |
| `video_multi_shot` | per-shot duration, framing, action, camera, transition/edit motivation, continuity, ending state, default `no_music_allow_sfx` policy | native/reference audio roles and platform reference maps | single-beat one-action rule applied to the whole sequence |
| `archive_review` | source asset, review target, decision, provenance, next owner | QC fields matching the reviewed asset | prompt, style, generation, or folder gates not needed for the review |

## Conditional Gates

```text
mother-library/reference system -> only formal visual work that needs an aesthetic system
style lock -> only approved variables that must remain stable across multiple outputs or regeneration
scene map -> only multi-scene/location-specific work
shot audit -> only dramatic or multi-shot edit logic
photographic realism -> only photographic/live-action execution
camera system/focal/aperture -> only when camera language materially controls the visible result
audio policy -> only when the platform/task can use audio or the user specifies audio intent
music policy -> `no_music_allow_sfx` is the video-prompt default; explicit music or full silence overrides it
breath tail -> only when ending_behavior is breath_light or breath_heavy
```

## Response Modes

```text
direct
Show only the requested prompt, generated artifact, concise decision, or final path. Hide route packets, audits, and internal tables.

compact
Show the result plus one short routing/audit note and only the fields needed for the user's next action.

diagnostic
Show the route packet, applicable gates, missing fields, owners, platform compilation changes, and state handoff. Use only when requested or when a blocker must be explained.
```

Downstream skills inherit `response_mode`. They must not replace a direct answer with a default table merely because they have a formal internal packet.

## QC Modes

```text
none
No automatic QC. Use for prompt-only work, successful built-in image generation that must end with the image, and disposable previews unless the user asks for review.

light_deferred
Run a separate compact QC pass after the artifact exists. Never append it after a built-in image result in the same response.

formal
Run deliverable-specific QC, preserve failure attribution, write state, and create a generation observation.
```

## Prompt Visibility

Keep these internal unless `response_mode: diagnostic`:

```text
zongkong_route_packet
director_contribution_packet
mother_library_application_packet
image_prompt_source_packet
video_prompt_source_packet
audited_prompt_packet
generation_ready_packet
generation_observation
```

For `direct`, show only the final copyable prompt or generated artifact. For `compact`, add at most one sentence describing an assumption or platform-preserving change.
