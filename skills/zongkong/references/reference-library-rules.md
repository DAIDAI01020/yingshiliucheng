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

| Main line | Library route |
| --- | --- |
| 商业宣传线 | `commercial-promo-library.md` + `shared-elite-cinematography.md` when cinematic/live-action execution applies |
| 剧情短剧线 | `short-drama-story-library.md` + mandatory `shared-elite-cinematography.md` for formal cinematic short drama |

`$style-reference-director` is the task-facing reference style entry. The library supplies curated sources. `$reference-aesthetic-director` translates the chosen reference into visual principles, style bible input, and AI risks.

## Mother-Library Application

Formal projects that use a mother-library/reference system must output or preserve `mother_library_application_packet`.

The mother library controls project DNA, scene function, shot execution, and platform risk. Do not leave it as a passive reference name list.

Required fields:

```text
library_route
project_function
primary_reference_family
cinematography_anchor
borrowed_mechanisms
scene_function_rules
do_not_copy
forbidden_drift
prompt_inheritance
```

Hard rule:

```text
Formal multi-scene image/video work must first output project-level and scene/chapter-level style references.
For formal cinematic/live-action work, the shared elite cinematography layer is mandatory. Do not force it onto typography, pure graphic design, abstract LED visuals, or tasks governed by product/material/layout references.
Every reference decision must include one project reference family and the appropriate anchor type: cinematography, composition, material/product, typography, or stage/space.
Every formal short-drama reference decision must include mother-library translation:
光线方向、空间关系、焦段心理效果、构图调度、材质触感、人物表演状态、AI风险控制。
When the route declares a mother-library/reference system applicable, formal image/video prompts without `mother_library_application_packet` or an equivalent task/scene application rule must route back to style-reference-director / scene-style-map-director / project-style-lock.
```

## Scene Style Mapping

When the user provides multi-scene material or asks for different scene/location styles, route through `$scene-style-map-director` before final image/video prompts. A single isolated asset does not require a scene map merely because it has one reference image.

`$scene-style-map-director` decides what changes per scene while protecting the unified project DNA.
