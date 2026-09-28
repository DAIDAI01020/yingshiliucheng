---
name: style-bible-director
description: Consolidate approved film and visual decisions into a coherent style bible and continuity rules. Use when a project needs a visual system, scene variations, character or product continuity, or targeted style revisions before project-style-lock freezes execution variables.
---

# Style Bible Director

## Role And Boundary

Consolidate the project's visual system from relevant director decisions. The reference owner chooses reference mechanisms; the scene owner defines scene variations; this skill resolves their visual continuity; `$project-style-lock` freezes approved variables for execution. Do not recreate decisions already sufficient for the task.

Inherit `zongkong_route_packet` and use the [stage handoff contract](../zongkong/references/stage-handoff-contract.md) for multi-stage work. A bible may be drafted before approval; only approved decisions become an approved style lock. Do not require a downstream platform audit or completed lock in order to draft the bible.

Reuse an applicable existing bible for added shots, revisions, or QC. Do not create one for prompt-only work or an isolated preview unless requested. Keep specialist judgments internal when the user only requests the final artifact.

## Applicable Content

Use only rows relevant to the deliverable:

| Layer | Content | Applies when |
| --- | --- | --- |
| Core | style_id/version, source/status, visual intent, palette, composition, material, permitted variation, forbidden drift | Every bible |
| References | selected mechanisms, source evidence, mother_library_application_packet, do_not_copy | A reference system is used |
| Live action | motivated light, camera distance, lens/depth, skin/fabric realism | Photographic people/scenes |
| Product | geometry, scale, material finish, color, brand/text policy | Product accuracy matters |
| Graphic/KV/type | shapes, hierarchy, density, exact text policy, title/logo safe zones | Graphic, typography, or KV work |
| Stage | screen geometry, viewing distance, performer-safe zones, edge behavior | LED/stage work |
| Continuity | character/product/prop identity, space, reference roles, chapter variations | Multiple related outputs |
| Motion | source of approved motion/ending decisions, stable visual constraints | Video deliverables only |

Do not add skin texture, wear, dust, camera brands, film references, or audio fields merely to fill a template. Clean products and stylized images keep their intended materials and rendering. Preserve photographic detail only where it is actually part of the approved look.

For formal work preserve `director_contribution_packet` and `visual_helpfulness_targets` as compact owned contributions and visible controls, not a repeated record of every director in the library.

## Project Style Lock Handoff

Hand off the approved core plus applicable extensions:

```text
upstream_source
status: draft / approved
style_id
version
deliverable_profile
master_style_sentence
palette_and_contrast
composition_or_layout_rule
material_or_surface_rule
reference_roles
do_not_inherit
allowed_variation
forbidden_drift
director_contribution_packet
visual_helpfulness_targets
profile_extension
mother_library_application_packet: when applicable
```

`$project-style-lock` owns its exact schema. Preserve existing compatible field names when continuing old projects; do not migrate old state merely for formatting. Legacy `anti_ai_realism_rule` applies only to photographic content. Legacy `jimeng_seedance_motion_rule` and `breath_tail_rule` carry explicitly chosen motion and ending decisions, not universal defaults.

The scene/shot owner supplies edit intent; `$ai-video-prompt-director` owns `complexity_mode`, `ending_behavior`, and motion feasibility; `$prompt-platform-auditor` compiles those choices. Do not impose one action, one camera move, or a breath tail across an entire staged or multi-shot video. Audio and platform capabilities are not style-bible decisions.

## Continuity Review

- Preserve invariant identity, product structure, palette, materials, and reference roles.
- Permit scene-specific light, focal distance, blocking, and palette variation explicitly allowed by the project. Continuity does not mean identical compositions.
- Preserve source-space geography under a camera change; do not demand that objects stay at identical image coordinates.
- Check that the prompt expresses applicable visible controls without relying on “同上”.
- Keep typography, brand marks, screen safety, and exact-text requirements where relevant.
- Separate a failed output from a faulty global rule; inspect the prompt/reference inheritance before recommending a style change.

## Revision And Output

| Change | Action |
| --- | --- |
| One image/shot issue | Protect the bible; target that artifact |
| Scripted chapter/time variation | Define a bounded scene variation |
| Repeated relevant drift | Diagnose evidence and propose a targeted rule change |
| Explicit global style change | Revise the bible, identify affected dependencies, then update approved locks |

Return the requested style table, changed rules, and any real unresolved choice. Do not mark a new proposal approved by default or regenerate images merely because a style rule was edited. Keep former versions available for traceability.
