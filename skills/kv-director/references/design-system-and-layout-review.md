# Design system and layout review

Use for poster/KV art direction, typography relationships, competing directions and multi-size design. This reference supplements the existing composition library; it does not add another approval stage. The active director owns the design: `poster-director` for narrative key art, `kv-director` for commercial/event visuals. LED constraints remain with the existing large-screen experience rules and `led-screen-director`.

## Turn an idea into visible decisions

Express the visual thesis briefly: **message → one visible metaphor → composition → type/image relationship**. For a complete brief, proceed with its direction. When alternatives would help, compare genuinely different arrangements using the same copy and assets; colour swaps alone are not different concepts. Do not require a separate manifesto document or a new choice after the user has already chosen.

Example for an event about connection:

| Direction | Visible construction | Why choose it / trade-off |
| --- | --- | --- |
| Converging paths | A few broad paths merge into one structure; title occupies the open field | Clear collective movement; avoid generic network particles |
| Shared structure | Distinct materials support one monumental object | Strong physical metaphor; needs convincing contact and scale |
| Typographic relationship | Two word groups share a visual axis, with one restrained image accent | Strong title recognition; depends on exact typography execution |

Keep the chosen metaphor specific to this event/story. Do not make every technology brief a glowing sphere, every cultural brief an ink landscape, or every premium brief a gold-on-black composition.

## Specify typography as part of the layout

Use the existing `post_typography_plan` rather than creating a parallel packet. Record the applicable details:

- Exact supplied title, subtitle, date, attribution and logo assets; distinguish final copy from placeholders.
- Title line breaks and alignment, intended glyph weight/width, primary/secondary size relationship, spacing, and the title's relationship to the image mass.
- Chinese glyph coverage, punctuation/Latin/numeral consistency, and whether an available font needs substitution. Preview the actual words: Latin samples cannot establish Chinese fit.
- Intended editable deliverable: layout file, HTML/SVG typography composition, or separate title asset when requested. A flattened PNG is not an editable layout or a layered PSD.

Reserve type zones while designing the base art. Use supplied logos and deterministic final typesetting when exact wording matters; keep the existing generated-text rules and the user's explicit choice. Separate stylized lettering belongs to `type-png-director`. Avoid arbitrary font-count, percentage or web-body-size rules when the physical display or brief calls for another solution.

## Separate fixed identity from flexible composition

Preserve the approved visual hook, palette relationships, material/light logic, typography identity and brand assets across a series. Allow subject scale, grouping, line breaks and negative-space distribution to change with aspect ratio. A coherent series need not repeat one rigid layout.

Use existing `extension_crop_map` and `kv_rendition_matrix` for KV variants. For each requested rendition record **crop / recompose / regenerate affected asset**, protected content, copy zones and actual pixel dimensions. If a crop cuts the visual metaphor or the title's counterweight, recompose instead of stretching or shrinking the whole master. Do not generate variants the user did not request.

For a stage, inherit the actual screen/presenter masks; do not import a social-ad CTA corner or a universal central 70–80% safe zone. A side-screen live feed, presenter silhouette, floor or scenic gap changes the composition. Commercial web readability rules are not proof of LED/camera readability.

## Review the rendered composition

Review the actual requested deliverable, not only its prompt or empty text boxes:

| View | Check |
| --- | --- |
| Full canvas | First-read, title/image balance, purposeful negative space, required copy and brand fidelity |
| Small preview | Does the intended message remain legible without explaining it? Do small accents become distracting noise? |
| Intended delivery size | Glyphs, line breaks, clipping, visible seams, raster sharpness and font substitution |
| Series side by side | Shared identity, useful compositional variation, no accidental colour or type drift |
| Stage mockup when relevant | Presenter/product occlusion, screen gaps, distant read and camera framing |

Distinguish base-art QC from finished-layout QC. A correct image can still have a broken title layout; a well-typeset title cannot rescue a missing visual hook. Record the specific defect and route to the owner: concept/composition → director; asset defect → image QC/prompt owner; lettering → typography owner; spacing/copy → layout; screen geometry → LED/AE split owner. Fix the affected layer and preserve accepted work.

For a still-image request, do not introduce animation/rendering infrastructure. For an image-only brief, do not make an HTML poster mandatory. HTML/CSS can be a deterministic layout option when the user needs editable type and the renderer is available; visual inspection of its actual export is still required.

## Source ideas and limits

Reviewed 2026-10-14. Independent synthesis of transferable methods, without copying upstream implementation:

- [Anthropic canvas-design](https://github.com/anthropics/skills/tree/main/skills/canvas-design): deliberate composition, form, colour, typography and a refinement pass. Adopt specific visual decisions; do not inherit mandatory long philosophy files, a fixed minimal-text aesthetic, or repeated claims of craftsmanship.
- [UI UX Pro Max banner-design](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/.claude/skills/banner-design): distinguish art directions, use explicit dimensions and brand assets, separate generated art from exact layout, inspect exports. Its social/web banner conventions do not define stage-screen engineering.

Repository popularity guided research, not quality approval. These skill instructions are integrated locally; this does not install either full upstream bundle or certify a new renderer.
