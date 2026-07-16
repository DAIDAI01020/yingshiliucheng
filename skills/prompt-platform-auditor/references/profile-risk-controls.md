# Deliverable Profile Risk Controls

Use the primary `deliverable_profile` to select required fields and the smallest useful risk set. Three to eight targeted controls are normally enough.

## Contents

- Image profiles
- Video profiles
- Risk selection

## Image Profiles

### `live_action_people`

Require visible subject/performance, scene, composition, motivated light, color/material, identity continuity, and ratio. Add camera/depth only when useful. Select risks such as face drift, plastic skin, hand failure, wardrobe drift, fake depth, over-sharpening, or background melt according to the frame.

### `product_structure`

Require structure, proportions, scale, material, color, logo/text policy, placement, and reflections. Select risks such as geometry drift, new parts, logo displacement, wrong material, scale change, or uncontrolled reflections.

### `commercial_kv`

Require first-read hierarchy, primary composition, brand/product/event relationship, negative space, title/logo/sponsor-safe zones, ratio, and extension behavior when requested. Select risks such as template composition, crowded title area, fake readable text, logo hallucination, hierarchy loss, or extension crop failure.

### `graphic_abstract`

Require shape language, layers, palette, density, rhythm, edge/material finish, and forbidden style drift. Select risks such as accidental objects, muddy layers, color drift, noisy density, weak silhouette, or unintended typography. Do not add skin/hand/camera realism controls.

### `typography_asset`

Require exact text/glyph source, letterform, legibility, 3D construction when relevant, transparent/isolated background, edge quality, and layout use. Select risks such as misspelling, fake glyphs, extra letters, merged strokes, dirty alpha, poster background, logo, or watermark.

### `led_stage`

Require screen geometry, ratio, center safe area, stage/performer relation, distance readability, and extension/loop behavior. Select risks such as edge overload, center obstruction, scale mismatch, tiny unreadable details, seams, or presenter collision.

### `local_edit`

Require base lock, named target region, exact delta, integration, and non-target preservation. Select risks such as full-frame repaint, camera shift, light/color change, wrong subject replacement, halo edges, or reference contamination.

### `storyboard_frame`

Require shot function, visible beat, space, continuity, composition/camera language, light/material, ratio, and only the content-specific risk subset from another profile.

## Video Profiles

### `video_i2v`

Require source authority, must-preserve lock, complexity mode, action/beat process, camera behavior, ending behavior, duration/ratio, optional environment/light change, applicable audio mode, `music_policy`, and targeted drift controls.

Select risks such as identity/structure drift, jump cut, scene repaint, camera instability, action incompleteness, light jumping, background melt, or platform-template motion.

### `video_multi_shot`

Require per-shot duration, framing, action, camera, transition/edit motivation, continuity, ending state, reference roles, `music_policy`, and audio ownership when applicable.

Select risks such as reference-role conflict, continuity drift, unmotivated cuts, timing overload, identity merge, wrong background side, or audio mismatch.

## Risk Selection

Use positive preservation when it directly describes what must remain visible. Use negative controls for concrete failure types. Do not paste a universal anti-AI block into every prompt.

Promote a risk into a project-level base only when it is intrinsic to the deliverable or repeated QC evidence justifies it.
