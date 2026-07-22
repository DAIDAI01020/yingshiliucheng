# Reference Library Rules

Use this reference when `$zongkong` has identified formal visual work that needs a project-level aesthetic system, scene-level style references, mother-library translation, or reference-image role analysis. Do not require this route for typography, archive, review-only work, or simple product/layout tasks that already have a complete approved visual specification.

## Formal Reference Route

For formal projects that require a reference system, route through `$style-reference-director` before `$reference-visual-library` and `$reference-aesthetic-director`.

If the user provides reference images, route through `$reference-image-style-matcher` before `$style-reference-director`.

```text
reference images
-> reference-image-style-matcher（视觉解析 + 母库反向匹配）
-> style-reference-director
-> scene-style-map-director
-> frame/video prompt
-> prompt-platform-auditor
```

When no reference image is provided and a formal aesthetic system is needed, do not leave the visual route generic. Actively recommend a mother-library route and an appropriate visual anchor, then translate them into executable prompt language.

When the user mentions ShotDeck or asks to find film frames, treat ShotDeck as a shot-level research interface, not a prestige badge. Use the `film-prestige-visual-library.md` admission gate and curated tiers. If the user's authenticated ShotDeck session is available and they ask for direct research, search by shot function and craft attributes; otherwise return a `shotdeck_search_recipe`. Never fabricate a searched frame, deck, or ShotDeck URL.

| Main line | Library route |
| --- | --- |
| 商业宣传线 | `commercial-promo-library.md` + `shared-elite-cinematography.md` when cinematic/live-action execution applies |
| 电影化品牌片 / 正式叙事 / 历史 / 城市 / 人文 / 类型氛围 | `film-prestige-visual-library.md` + `shared-elite-cinematography.md` |
| 剧情短剧线 | `short-drama-story-library.md` + mandatory `shared-elite-cinematography.md` for formal cinematic short drama |
| 商业KV / 产品KV / 发布会KV / 活动主视觉 / 节目KV | `kv-key-art-case-library.md` -> `$kv-director` composition/style system |

KV routing boundary:

```text
kv-key-art-case-library = proven case mechanism and source trace
kv-director = communication hierarchy, kv_composition_mode, style family, title/logo safe area, crop and extension authority
film-prestige-visual-library = optional cinematic base-art world when the KV genuinely needs live-action/narrative imagery
```

Pure typography, graphic-only layout, exact-title assets, and abstract LED visuals must not be forced through film references. Use `$type-png-director`, `$kv-director`, or `$led-screen-director` with the applicable typography/composition/material/stage anchor. A cinematic reference layer is added only when the base art is genuinely cinematic or live action.

`$style-reference-director` is the task-facing reference style entry. The library supplies curated sources. `$reference-aesthetic-director` translates the chosen reference into visual principles, style bible input, and AI risks.

## Mother-Library Application

Formal projects that use a mother-library/reference system must output or preserve `mother_library_application_packet`.

The mother library controls project DNA, scene function, shot execution, and platform risk. Do not leave it as a passive reference name list.

Required fields:

```text
library_route
reference_selection_mode
project_function
primary_reference_family
cinematography_anchor
borrowed_mechanisms
scene_function_rules
do_not_copy
forbidden_drift
prompt_inheritance
shotdeck_status
shotdeck_search_recipe
```

Hard rule:

```text
Formal multi-scene image/video work must first output project-level and scene/chapter-level style references.
For formal cinematic/live-action work, the shared elite cinematography layer is mandatory. Do not force it onto typography, pure graphic design, abstract LED visuals, or tasks governed by product/material/layout references.
Every reference decision must include one project reference family and the appropriate anchor type: cinematography, composition, material/product, typography, or stage/space.
Every selected reference system must use one primary reference and at most two secondary references; each secondary reference must solve a named scene, communication, or deliverable problem.
Every formal short-drama reference decision must include mother-library translation:
光线方向、空间关系、焦段心理效果、构图调度、材质触感、人物表演状态、AI风险控制。
When the route declares a mother-library/reference system applicable, formal image/video prompts without `mother_library_application_packet` or an equivalent task/scene application rule must route back to style-reference-director / scene-style-map-director / project-style-lock.
Final image/video prompts must contain the translated visual mechanisms, not a dump of film titles, directors, cinematographers, studios, campaigns, or protected layouts.
```

## Scene Style Mapping

When the user provides multi-scene material or asks for different scene/location styles, route through `$scene-style-map-director` before final image/video prompts. A single isolated asset does not require a scene map merely because it has one reference image.

`$scene-style-map-director` decides what changes per scene while protecting the unified project DNA.
