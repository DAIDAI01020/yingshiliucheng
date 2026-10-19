# Post Patterns And Packet

Read this reference when `$xiaohongshu-design-director` must turn a theme into a post structure, hand work to existing visual skills, or check isolation and image-set quality.

## Editorial Packet

```text
xiaohongshu_editorial_packet
account_or_series:
content_type: fictional_film / wallpaper_set / concept_poster / visual_experiment
post_goal:
title:
one_line_premise:
audience_emotion:
visual_hook:
master_image_direction:
shared_invariants:
cover_delta:
wallpaper_deltas:
typography_safe_area:
clean_wallpaper_required: true / false
source_project:
public_reuse_status: original / approved / blocked / unknown
allowed_source_assets:
forbidden_source_assets:
style_source:
style_lock:
platform_target:
model_target:
next_skill:
missing_fields:
route_back_to:
```

Use snake_case at a state boundary. Keep the user-facing response compact unless the user asks to inspect the full packet.

## Post Patterns

### Fictional Film

Use one original premise and one visual contradiction. The master image should feel like a frame from a coherent film world rather than an isolated fantasy illustration.

```text
poster cover = same master world + title-safe composition + post typography
clean wallpaper = same master world + no text/logo + crop-safe focal subject
supporting variant = one controlled change in camera, human presence, weather, or color state
```

Do not add issue numbers by default.

### Wallpaper Set

Keep a single emotional and material system across the set. Vary only a small number of visible properties. Do not create unrelated images merely to fill a carousel.

### Concept Poster

Start from communication hierarchy and one visual symbol. Generate no-text base art first; add final readable Chinese copy and logos in layout or through the typography owner.

### Visual Experiment

Name the controlled variable before generation:

```text
color temperature / scale / material / time of day / camera distance / negative space / human presence
```

Keep other approved properties invariant so the experiment has a readable point.

## Source Isolation Check

Before using material from another managed project, require all of:

```text
source_project identified
public_reuse_status: approved
allowed_source_assets listed
forbidden_source_assets listed
client names, faces, logos, unreleased products, scripts, and proprietary references excluded unless explicitly approved
```

If any item is unknown, use an original theme instead or return `missing_fields`. Never copy source-project state into the social-content project.

## Aesthetic Review

Check the set in this order:

1. `visual_hook`: one image idea is readable without explanatory copy.
2. `world_coherence`: cover and wallpapers belong to the same fictional world.
3. `emotional_save_value`: at least one clean image works without typography.
4. `composition`: focal hierarchy, negative space, crop safety, and small-preview clarity are intentional.
5. `light_material_scale`: space, light direction, surfaces, and human scale feel physically coherent for the chosen style.
6. `originality`: no copied film key art, campaign layout, celebrity likeness, signature artist treatment, or protected character.
7. `technical_qc`: no unintended text, watermark, anatomy failure, broken geometry, repeated detail, or plastic artifact.

Use the standard downstream QC decisions:

```text
可用 / 可小修 / 定向重出 / 提示词需重写 / 前置导演判断错误
```

Editorial failure inside the fictional-film world routes back to `$xiaohongshu-design-director`. Finished-post, copy or publishing failure routes to `$xiaohongshu`. Style or concept failure routes to the applicable upstream owner. Image artifact failure routes to targeted regeneration through the current prompt and execution owners.
