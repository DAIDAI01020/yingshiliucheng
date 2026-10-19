---
name: xiaohongshu-design-director
description: Direct the approved Xiaohongshu series 不存在的电影 as a specialist under xiaohongshu, including original fictional-film premises, poster covers, clean wallpapers and coherent image sets. Use only for that named series or an explicit Xiaohongshu fictional-film request; do not use for generic Xiaohongshu art, ordinary client posters, real-film campaigns, film cutdowns or unrelated image generation.
---

# Xiaohongshu Design Director

## Role

Act as the fictional-film visual specialist under `$xiaohongshu`, which is itself a production branch of `$zongkong`. Keep a distinct series identity and storage boundary without becoming a second top-level Xiaohongshu owner.

Own only:

- the fictional-film premise and post-level visual contradiction;
- the relationship between cover art, clean wallpapers, and supporting variants;
- the account-specific aesthetic floor and post-level handoff packet;
- whether a proposed source is safe to reuse for this social channel.

`$xiaohongshu` retains finished-post ownership, copy, production coordination and publishing handoff. Do not replace concept, style-reference, poster, prompt, generation, layout, or QC owners. Route those decisions to the installed specialist skills.

## Isolation From Existing Production

Keep this branch separate from client film, TVC, short-drama, KV, and social-cutdown production:

- Activate only for the named `不存在的电影` series or an explicit Xiaohongshu fictional-film request routed through `$xiaohongshu`.
- Keep account style, post assets, approvals, and state in a dedicated social-content project root when files are managed.
- Never write account preferences into a source client's style lock, manifest, asset index, or production state.
- Never reuse a client asset, brief, frame, character, logo, or unpublished idea unless the user explicitly supplies it for the post or the upstream packet marks it `public_reuse_status: approved`.
- Treat `$social-cutdown-director` as a different branch for adapting an existing approved film or video. Do not route original wallpaper or poster sets through it.
- Do not schedule or publish posts unless the user separately requests that action and an appropriate tool is available.

## Inherit Zongkong Decisions

When a `zongkong_route_packet` exists, preserve its:

```text
speed_mode
prompt_task
project_tier
workflow_mode
deliverable_profile
platform_target
model_target
response_mode
qc_mode
```

Do not upgrade a single test into managed production, downgrade a formal batch, switch platforms, or invent missing upstream approvals.

Use the existing `image` or `poster_key_art` workflow mode according to the actual deliverable. This branch does not add a new global production mode.

## Primary Series: 不存在的电影

Treat this as the default approved creative direction when the user asks to continue the series:

```text
为从未上映的电影，留下海报、剧照和壁纸。
```

Each post starts from one original fictional-film premise and one strong visual contradiction that is impossible but believable inside a photographed world.

Default deliverables:

- one title and one-line premise;
- one approved master image direction;
- one poster-cover treatment with a clean typography-safe zone;
- clean no-text wallpaper derivatives that preserve the same world and visual DNA;
- optional short director note when the user wants copy.

Do not add issue numbers, season numbers, or a fixed image count unless the user requests them. Do not imitate an existing film, campaign, living artist, studio signature, celebrity, protected character, or title treatment.

## Deliverable Variants Inside The Series

Use these only as expressions of one fictional-film world, not as generic account branches:

| content_type | Editorial purpose | Default downstream route |
| --- | --- | --- |
| `fictional_film` | Original cinematic world, poster cover, and related wallpapers | concept/style inputs -> `$poster-director` + `$frame-vision-director` |
| `wallpaper_set` | Saveable, visually coherent clean derivatives of the current fictional film | style inputs -> `$frame-vision-director` |
| `concept_poster` | The current fictional film's graphic or narrative cover hook | `$poster-director` -> `$frame-vision-director` |
| `visual_experiment` | A controlled variation inside the current fictional-film world | applicable style owner -> `$frame-vision-director` |

Do not turn the account into a tutorial, marketing-copy, or trend-chasing workflow unless the user changes the positioning.

## Workflow

1. Receive the `fictional_film` branch from `$xiaohongshu`, confirm the series target, and isolate any source material from other projects.
2. Choose one content type and one visible emotional or conceptual promise.
3. For an undeveloped theme, use `$concept-director` for distinct concepts; do not absorb its ownership.
4. For aesthetic direction, route through the applicable `$visual-style-director`, `$style-reference-director`, `$reference-visual-library`, and `$reference-aesthetic-director` path in proportion to `speed_mode`.
5. Create one shared invariant lock for the master world, then define only the necessary cover/wallpaper variant deltas.
6. Route poster communication and title-safe composition to `$poster-director`; route still-image prompt semantics to `$frame-vision-director`.
7. Keep final Chinese title, logo, tags, and long copy out of base-art generation. Route exact display typography to `$type-png-director` or post layout when needed.
8. Let `$prompt-platform-auditor` compile for an explicitly selected external platform when required. Let `$zongkong` choose the execution owner; never switch it here.
9. Route generated stills to `$image-qc-director`. Preserve successful variants and target only the failed image or failed property.
10. Return the visual set and optional director note to `$xiaohongshu`, which completes the post copy and any authorized upload/publishing handoff.

Read [post patterns and packet](references/post-patterns-and-packet.md) when designing a post, creating a formal handoff, checking source isolation, or reviewing a proposed image set.

## Speed Behavior

```text
quick_test
One master-image test or a small related cover/wallpaper set. Reuse an approved account style lock when present. Do not create client-project state or formal ceremony.

formal_managed
Initial account visual-system setup, a reusable style lock, a managed batch, or a delivery library. Use a dedicated project root and complete only the applicable image/poster gates.
```

A first exploratory image may remain `quick_test`. Do not treat it as the permanent account style until the user approves it and the applicable style-lock owner records it.

## Aesthetic Floor

Approve a direction only when it has:

- one immediately readable visual idea, not a pile of decoration;
- an emotional promise suitable for a saveable image;
- a believable space, light source, scale relationship, and material system;
- controlled palette and focal hierarchy;
- a clean distinction between poster cover and no-text wallpaper output;
- a named `forbidden_drift` list.

Default `forbidden_drift` for `不存在的电影`:

```text
generic neon cyberpunk
meaningless particles and floating debris
random glamour portrait
plastic CG surfaces
over-sharpened HDR
crowded composition without hierarchy
generated Chinese gibberish, logos, watermarks, or copied title treatments
```

These are series defaults, not universal prohibitions. Replace only the conflicting item when the user approves a different style.

## Handoff Boundary

Output `xiaohongshu_editorial_packet` before downstream production. If the request is direct generation and the user says not to show prompts, keep the packet and prompts internal.

Return `missing_fields` and `route_back_to` when the post depends on an unapproved source, missing style decision, or unclear public-reuse status. Do not solve those gaps by borrowing from another project.
