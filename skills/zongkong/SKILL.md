---
name: zongkong
description: Top-level orchestrator for AI film and visual-production work. Use when starting or continuing a film, commercial, short-drama, storyboard, KV, poster, image, video, review, archive, or project-management task that needs project setup, speed-mode classification, cross-skill routing, platform selection, formal production gates, QC, or next-action decisions. Also use when the creative request is ambiguous and the correct downstream skill is unclear. Do not trigger merely because a conversation is new or for unrelated coding and general tasks.
---

# Zongkong

## Role

Act as the decision layer above film, short-drama, image, video, and asset skills.

Decide only what the orchestration layer owns:

- whether this request belongs to the AI film/visual workflow;
- whether to create or reuse a project folder;
- `speed_mode`, `project_tier`, `workflow_mode`, and `main_line`;
- the next owning skill and platform target;
- which formal gates apply to this deliverable;
- whether generation, QC, review, state writeback, or archiving is needed.

Do not replace specialist direction, prompt writing, platform audit, generation, or QC. Keep quick work light and formal work traceable.

## Read References on Demand

Load only the reference needed for the current decision:

- Main creative line, workflow mode, specialist director, or storyboard variant: read [references/line-routes-and-workflow-modes.md](references/line-routes-and-workflow-modes.md).
- Tool route, direct generation, image/video platform selection, or external handoff: read [references/tool-routing-and-platforms.md](references/tool-routing-and-platforms.md).
- Formal packets, applicable gates, owners, `missing_fields`, or `route_back_to`: read [references/packets-and-gate-ownership.md](references/packets-and-gate-ownership.md).
- Deliverable-specific prompt fields, response visibility, QC mode, or quality-profile selection: read [references/deliverable-profiles-and-response-modes.md](references/deliverable-profiles-and-response-modes.md).
- Formal project/scene references, mother-library logic, or style inheritance: read [references/reference-library-rules.md](references/reference-library-rules.md).
- After editing this skill or changing a route boundary: read and run [references/regression-checklist.md](references/regression-checklist.md).

Do not copy detailed reference tables back into this file. Each rule must have one source of truth.

## Decision Order

Use this order. Earlier decisions take precedence over later generic triggers.

1. **Scope**: confirm the request belongs to the AI film/visual workflow. If not, do not force `$zongkong` routing.
2. **Explicit platform**: an explicitly named platform outranks generic words such as “出图” or “出视频” and overrides an inherited platform only when the user clearly requests the change. Never silently fall back to another platform.
3. **Continuation state**: if the user says continue, regenerate, revise, or references an existing managed project and does not name a new platform, preserve its current platform, route, approved proposal, references, and style lock.
4. **Execution intent**: distinguish direct generation, prompt-only delivery, planning/direction, review, revision, and archive.
5. **Speed mode**: classify `prompt_only`, `quick_test`, or `formal_managed`.
6. **Deliverable profile**: choose the smallest profile that describes what must be accurate in the result.
7. **Response and QC modes**: decide how much workflow detail the user should see and whether QC is absent, deferred/light, or formal.
8. **Workflow mode and main line**: choose the specialist route.
9. **Applicable gates**: require only the gates relevant to the deliverable profile.
10. **Next action**: name one next owning skill or execute the in-scope next step.

When a conflict remains, use this precedence:

```text
explicit platform
> continue existing managed state
> direct generation request
> prompt-only request
> formal batch/delivery request
> generic image/video wording
```

## Speed Modes

```text
prompt_only
User wants one copyable image/video prompt, a quick rewrite, or platform wording only.
Route directly to the prompt owner. Do not create project state, manifest, formal audit, QC, or asset records unless requested.

quick_test
User wants one image/video/shot/board, or a small set of closely related variants, model tests, or previews.
Protect the supplied references and subject structure. Use only the lightweight checks needed to prevent an obvious failure.

formal_managed
User asks for batch work, delivery, client assets, project-state ingest, style-lock inheritance, manifest, formal QC, or continuation of a managed production.
Create/check project intake and require only the applicable formal gates before execution.
```

When unclear, choose the lighter mode. `project_tier: formal` alone does not activate every production gate; `speed_mode: formal_managed` plus the deliverable type determines them.

Two to four conversational preview images that share one source/reference and differ only by camera, crop, pose, or another controlled variable remain one `quick_test`. Multiple ephemeral chat outputs alone do not create a managed batch, project folder, manifest, or formal gate requirement.

### Quality Floor by Task

```text
image prompt -> subject, scene function, composition/camera, light/material, aspect ratio, forbidden drift
video prompt -> subject action, camera movement, environment/light change, ending frame, duration/ratio, audio mode, default music policy, forbidden items
reference-driven work -> explicit reference roles and do_not_inherit boundaries
product work -> locked product structure, proportions, material, logo/text policy
quick test -> preserve any existing style lock and reference roles without backfilling formal ceremony
formal managed -> pass the applicable gates listed in packets-and-gate-ownership.md
```

Do not apply video-only fields such as action, ending frame, or audio policy to still-image, typography, archive, or review tasks.

For every copyable video prompt, default `music_policy` to `no_music_allow_sfx`: the negative prompt must reject background music, scoring, songs, and sung vocals while explicitly allowing synchronized natural ambience and physical sound effects. Override this only when the user explicitly requests music or complete silence. This is a video-prompt baseline, not a formal gate and not an image-prompt rule.

## Deliverable, Response, And QC Modes

Choose one primary `deliverable_profile`:

```text
live_action_people / product_structure / commercial_kv / graphic_abstract /
typography_asset / led_stage / local_edit / storyboard_frame /
video_i2v / video_multi_shot / archive_review
```

The profile determines which style, camera, realism, typography, motion, audio, and QC fields apply. Do not use photographic camera or anti-AI realism fields as universal requirements. Read [references/deliverable-profiles-and-response-modes.md](references/deliverable-profiles-and-response-modes.md) when selecting or validating a profile.

Choose user visibility separately:

```text
response_mode: direct / compact / diagnostic
qc_mode: none / light_deferred / formal
```

Default direct generation and prompt-only work to `response_mode: direct`. Keep internal packets hidden. Use `diagnostic` only when the user asks to inspect routes, packets, missing gates, or workflow state.

## Project Tier and Folder

```text
formal: client/managed work, named production, batch continuity, or delivery
quick: small but coherent task that benefits from a lightweight project location
misc: isolated tests and disposable experiments
undecided: tier is not yet relevant or cannot be inferred safely
```

Before creating a new managed project, continuing a managed project, reorganizing scattered files, or generating multiple managed on-disk deliverables, route through `$project-folder-director` for `project_folder_contract` and `output_path_rule`. Do not invoke the folder workflow merely because a `quick_test` asks for several images returned in the conversation.

Do not hard-code a drive or project root here. `$project-folder-director` owns `projects_root`, portability, folder naming, and the visible move plan. Route inventory/state work to `$asset-librarian` or `$project-state-manager` only after the folder contract is known.

Ask about project tier or storage only when it materially blocks execution. Do not ask merely to complete a packet.

## Route Packet

Create or preserve this compact internal packet before handing off to another skill:

```text
zongkong_route_packet
speed_mode: prompt_only / quick_test / formal_managed
project_tier: formal / quick / misc / undecided
workflow_mode: proposal / short_drama / storyboard / image_storyboard / commercial_kv / poster_key_art / typography_png_asset / image / video / product_ai_video / review / archive
main_line: commercial_promo / short_drama_story / other
deliverable_profile: live_action_people / product_structure / commercial_kv / graphic_abstract / typography_asset / led_stage / local_edit / storyboard_frame / video_i2v / video_multi_shot / archive_review
platform_target: built_in_image / banana / banana_pro / jimeng / kling / kling_o1 / kling_video_3_omni / seedance_ark / midjourney / layout / none
response_mode: direct / compact / diagnostic
qc_mode: none / light_deferred / formal
next_skill:
missing_fields:
route_reason:
```

Preserve the packet internally or in project state. By default, show the user only a concise routing conclusion and the immediate next action. Show the full packet when the user asks for workflow diagnostics, formal state, or routing details.

Normalize legacy labels such as `Banana Pro`, `Kling O1`, `Ark`, or `Kling VIDEO 3.0 Omni` to the packet enums above while retaining the human-facing product name in prose.

## Formal Gate Applicability

Use this matrix before requiring a gate:

| Gate | Applies when |
| --- | --- |
| project intake/folder | managed work that writes state or multiple deliverables |
| reference/mother-library decision | formal visual work requiring an aesthetic system |
| style lock | approved visual direction must remain stable across a batch |
| hook audit | formal short drama/episodic story with an opening audience-retention requirement |
| character continuity | recurring characters must remain stable across scenes/shots |
| scene map | multi-scene work or scenes requiring distinct visual treatment |
| scene continuity lock | multiple shots share a location, axis, blocking, props, or background |
| shot-language audit | dramatic or multi-shot work where edit motivation and continuity matter |
| prompt-platform audit | formal prompt execution or external platform handoff |
| generation-ready packet | managed image/video execution |
| QC/state writeback | generated managed deliverables |

Do not require short-drama gates for commercial KV, typography, archive, or unrelated formal work. Do not require photorealism constraints for stylized, graphic, abstract, typography, or stage-visual deliverables.

For packet schemas and exact owners, read [references/packets-and-gate-ownership.md](references/packets-and-gate-ownership.md).

## Core Route Boundaries

- `$zongkong` owns classification and routing, not the specialist result.
- Specialist directors own concept, narrative, composition, scene, character, or shot decisions in their domain.
- Prompt directors translate approved upstream decisions; they do not invent missing reference, style, scene, shot, character, or platform decisions for formal work.
- `$prompt-platform-auditor` audits platform execution; it does not replace creative direction.
- Generation tools execute approved prompts; they do not discover or decide the formal project style.
- QC skills diagnose results and route targeted revisions; they do not rewrite the entire project style for an isolated generation failure.

If a formal upstream decision is missing, return `missing_fields` and the owning `route_back_to`. Do not send the gap downstream.

## Prompt and Generation Rules

For `prompt_only`, route directly to the correct prompt owner and return copyable wording.

When a named platform or external handoff needs platform-specific wording, the prompt owner creates the semantic source prompt and `$prompt-platform-auditor` performs only the lightweight platform compilation. This does not activate formal packets, project state, or QC.

For `quick_test`, permit one-pass generation with only necessary reference, structure, platform-risk, and output-path checks. Mark the result as a test; do not promote it into a formal batch lock without completing the applicable gates.

For a small direct-generation variant set, make the route decision once, create one shared invariant lock plus one delta per requested output, and hand the whole set to the generation owner in one execution turn. Do not repeat routing commentary between variants or claim that separate output images require separate workflow decisions. The generation owner may use multiple internal tool calls, but retries must remain bounded and successful variants must not be discarded when another variant fails.

For `formal_managed` generation:

1. Check project intake and applicable upstream packets.
2. Route missing decisions to their owners.
3. Require the current style lock only when batch visual continuity applies.
4. Require shot audit only when dramatic/multi-shot logic applies.
5. Audit the completed prompt for the target platform.
6. Execute only from `generation_ready_packet` or an equivalent managed job.
7. Run the applicable QC and state writeback.

Use deliverable-specific quality gates:

```text
photoreal live action -> photographic realism and anti-AI artifact controls
stylized/graphic/abstract -> style fidelity, shape language, palette, and forbidden drift
product/KV -> structure, proportions, material, brand-safe composition, text/logo-safe areas
typography -> glyph accuracy, legibility, transparency, edge quality, and post-layout suitability
LED/stage -> screen ratio, center safe area, performer/presenter safety, extension, and distance readability
```

Platform-specific motion rules belong to the prompt/platform skills and [references/tool-routing-and-platforms.md](references/tool-routing-and-platforms.md), not to the global gate.

## Continuation, Revision, and Regeneration

When the user says “继续出图”, “重出”, “继续做”, or gives revision feedback:

- preserve the existing project route, platform, approved proposal, reference roles, and style lock;
- classify the failure or requested change before routing;
- make a targeted correction for composition, character, hands, text, light, motion, structure, platform flavor, or style drift;
- return upstream only when QC identifies an upstream director, reference, scene, shot, or style-lock decision as wrong.

Do not restart full development merely because one output failed.

## Post-Generation

```text
formal_managed -> review/QC -> asset index or state writeback
quick_test + qc_mode:none -> preview/path -> stop
quick_test + qc_mode:light_deferred -> preview/path -> separate short QC when requested or scheduled by the workflow
misc isolated test -> preview/path -> one-line judgment
```

For successful built-in imagegen, end the generation response with the generated image result. Run short QC only in a later turn or separate review workflow; do not append status narration after the image.

Use standard QC decisions:

```text
可用 / 可小修 / 定向重出 / 提示词需重写 / 前置导演判断错误
```

## Guardrails

- Never print API keys or tokens.
- Never silently switch between built-in imagegen, Banana, Midjourney, Jimeng, Kling, or Seedance/Ark.
- Do not commit, push, sync, move, or delete project/workflow files unless the user authorizes that action.
- Before changing global workflow contracts, state gates, templates, or scripts, explain the scope, affected files, formal-vs-quick impact, complexity risk, and rollback path unless the user explicitly requested that implementation in the current turn.
- Preserve the boundary between quick tests and formal managed production.
- Prefer execution when the user asks for action; ask only when a missing decision materially changes the result or external state.
