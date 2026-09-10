---
name: builtin-imagegen-director
description: Use Codex/ChatGPT built-in imagegen, including the current ChatGPT Images 2.5 route, for fast film visual concepts, storyboard keyframes, reference-led generation, precision edits, and quick drafts without external API keys. Use when the user asks for Image 2.5, built-in imagegen, 内置出图, 直接生成一张图, 快速出图, concept preview, or image generation/editing without Banana, OpenAI API, Midjourney, or project logging.
---

# Built-in Imagegen Director

## Role

Use the built-in `imagegen` capability for fast preview images and edits inside the current conversation.

This skill is not an API wrapper. It does not manage external keys, model selection, generation logs, project folders, or Excel execution records unless another workflow captures the result afterward.

## Route Authority And Independent Tool Boundary

Inherit `speed_mode`, `deliverable_profile`, `platform_target`, `model_target`, `response_mode`, and `qc_mode` from `$zongkong` when a route packet is present.

This skill owns built-in imagegen preflight, prompt shaping, and direct generation. It does not choose project tier, change `speed_mode`, skip formal gates, replace `$frame-vision-director`, replace `$prompt-platform-auditor` for formal work, or replace `$image-qc-director` for managed QC.

Built-in imagegen and Banana are separate tools and separate skills. Never use this skill for Banana, Banana Pro, Nano Banana, or OpenRouter image generation; those requests belong to `$banana-image-generator`. Never silently fall back from built-in imagegen to Banana, and never describe a Banana result as built-in imagegen.

For `formal_managed`, route missing style, scene, shot, prompt-audit, output path, or QC requirements back to the owning skill instead of silently treating the request as a casual image test.

## When to Use

- The user asks for `Image 2.5`, `ChatGPT Images 2.5`, `imagegen`, `内置出图`, `直接生成一张图`, `快速出图`, or `先看个效果`.
- The user wants a quick visual concept, mood frame, style test, poster direction, storyboard keyframe, or image edit.
- The user selects built-in generation, including managed work whose versioned files, prompt logs, and state writeback are handled by downstream project skills.

Do not use this skill when the user explicitly selects Banana, MJ/Midjourney, OpenAI API, Seedance, 可灵, or 即梦 execution. Logging requirements alone do not change the chosen generation platform.

## Workflow

1. Determine whether the request is direct generation or prompt-only output.
2. Run `direct_image_preflight_check` before generation.
3. For `model_target:gpt_image_2_5` or a new built-in request routed to the migrated Images 2.5 default, read [GPT Image 2.5 prompt compilation](../prompt-platform-auditor/references/gpt-image-2-5.md) and apply its lightweight prompt shape without creating a formal audit packet.
4. Preserve the current project's approved style, profile-specific locks, reference roles, and pinned model.
5. For narrative storyboards or multi-shot keyframes, prepare one concise self-contained prompt per shot. Repeat only the compact stable controls needed by that shot; never use `同上`.
6. If the user says `直接出图`, call the built-in image generation tool after preflight without printing the full prompt first.
7. If the user says `给提示词`, output only the prompt and do not generate.
8. For edits, state one requested delta first, repeat the concrete preservation lock, and change only the requested elements. Use the latest accepted result as the next edit input.
9. If generation fails, return `imagegen_execution_result` with the real failure type. Never claim success when no image artifact was returned.
10. If generation succeeds, end with the generated image result and do not append a QC line or other text in the same response. Run QC only in a later user turn or separate review workflow.

## Direct Image Preflight Check

Before calling built-in imagegen, check these fields internally and preserve the important ones in the prompt:

```text
direct_image_preflight_check
execution_mode: direct_generation / prompt_only
requested_image_count:
deliverable_profile:
model_target:
task_mode: generate / edit / combine_references / style_transfer / text_layout / transparent_asset / sketch_to_image
intent_or_shot_function:
style_source_or_lock:
must_preserve:
must_change:
subject_or_product_or_character_constraints:
scene_and_action:
camera_composition_light_color_material:
aspect_ratio_and_usage:
reference_image_roles:
text_logo_watermark_risk:
video_first_frame_potential:
response_mode:
qc_mode:
missing_fields:
```

If `missing_fields` would break the image, ask or route back. If the request is a quick test and the missing field is not blocking, make a clear assumption inside the prompt.

## Images 2.5 Routing

For a new generic built-in image request, preserve `$zongkong`'s migrated `model_target:gpt_image_2_5`. A continuation pinned to GPT Image 2 or an older model keeps that model unless the user explicitly asks to migrate.

The built-in tool may not expose Flare/Sunburst selection or API parameters. Use the selected prompt rules without pretending unsupported API parameters were applied. Keep visual requirements such as aspect ratio, transparent background, and composition in natural-language instructions when no dedicated tool field exists. Do not dump model/quality/output-format API key-value settings into the prompt. If the user explicitly asks for OpenAI API execution, this skill is not the executor.

Distinguish `requested_model` from `observed_model`: a pinned prompt branch is not proof of the serving model. If the tool cannot select or report a model, record the observed model as unknown. If exact model execution is essential, report that limitation before generating; never claim a legacy model was selected merely because its prompt rules were retained.

For precision edits, request one meaningful change per turn, restate identity/product/layout/light locks, and inspect each result before the next edit. Never promise pixel-identical preservation; route truly pixel-locked work to compositing or a deterministic local-edit workflow.

## Quick Multi-Variant Generation

When a `quick_test` requests two to four separate images from the same reference, space, subject, or style, treat them as one direct-generation job rather than several workflow decisions.

Create internally:

```text
shared_invariant_lock:
  reference role, space geometry, architecture/set, subject identity, materials, lighting continuity, palette, aspect ratio, text/logo constraints
variant_deltas:
  variant_id, requested camera/crop/pose/element change, framing, camera height/angle, focal behavior
```

Run `direct_image_preflight_check` once for the whole set. Then execute the requested variants in one orchestration turn, using the minimum number of built-in imagegen calls needed to return separate image artifacts. Sequential internal calls are acceptable when they improve reliability, but do not post new routing commentary, repeat the preflight, or describe each call as a new task.

Each variant prompt must repeat the shared invariant lock and change only its declared delta. Do not merge multiple requested camera views into one composite image unless the user explicitly asks for a comparison board or contact sheet. Do not create project state or a project folder only because `requested_image_count` is greater than one.

For new camera views, apply `$frame-vision-director`'s camera-change rule: lock physical scene geometry and light sources, while allowing projection, occlusion, and framing to change. Remove conflicting perspective/composition locks before execution.

## Live-Action / Story-Frame Prompt Shape

Use this shape only for `live_action_people` or photographic `storyboard_frame` when camera language improves the result. Omit inapplicable fields:

```text
[Actual visible subject, action/state, and spatial relationship at this moment].
Scene: [environment and time].
Camera/composition: [shot size, camera position, spatial layout, and useful focal/depth behavior].
Lighting/color: [lighting plan and palette].
Texture/style: [film look, materials, finish].
Continuity: [character, wardrobe, prop, geography, screen-direction, and scene-state locks that apply to this shot].
Constraints: [no text/logos/watermarks/unwanted artifacts].
Aspect ratio: [16:9 / 9:16 / 1:1 / other].
```

## Fielded Storyboard Execution

For accurate storyboard image generation, prefer a fielded source structure over a long prose prompt. If the source includes `Visual Baseline`, `Continuity Lock`, `Shot Size`, `Camera Lens`, `Content`, `Composition`, or `Image Style Prompt`, convert it into one complete prompt per shot instead of sending the whole file to imagegen.

Use this execution order, selecting fields by `deliverable_profile`:

```text
[visible frame] + [must-preserve lock] + [requested delta] + [composition/layout or useful camera language] + [profile-relevant light/color/material/style] + [reference roles] + [targeted avoid list] + [aspect ratio]
```

The first sentence must describe the actual frame to render, not a generic style label. Every independently executed shot must carry its compact visible locks, but do not require camera, photographic realism, mother-library, or skin/hand controls for product, graphic, typography, LED/stage, or local-edit work unless relevant.

Always remove rationale that does not change the visible result. Keep exact structure, era/material, composition/layout, continuity, ratio, and text/logo controls when the task needs them.

## Generation Failure Handling

When the built-in tool does not return an image, output:

```text
imagegen_execution_result
status: failed
failure_type: tool_unavailable / missing_reference / invalid_reference / policy_restriction / transient_service / empty_result / invalid_request / unknown
attempt_count:
retry_allowed:
next_action:
```

Retry once only for `transient_service` or `empty_result`. For multi-variant generation, retry only the failed variant, preserve every successful image artifact, and stop after that variant's single retry. Do not restart the full set or enter an open-ended retry loop. Do not retry missing/invalid references, policy restrictions, invalid requests, or unavailable tools without first fixing the cause. Keep the request on the built-in image route unless the user explicitly chooses Banana.

## Output Behavior

- For real generation requests, keep chat output short and show the generated image result.
- After a successful built-in image generation call, do not append a QC line, summary, or follow-up question in the same response.
- `qc_mode:none` stops after the generated image. `qc_mode:light_deferred` or `formal` runs only in a separate review turn/workflow.
- For prompt-only requests, provide a clean copyable prompt.
- For workflow comparisons, describe it as `内置 imagegen 快速预览`, not as OpenAI API, Banana, or Midjourney.
- If tracking is required, keep the built-in route and hand actual returned artifacts to the existing asset/state owners. Record a local path only after verifying the file exists. An inline-only result remains pending capture; do not invent a saved path, completed archive, or substitute platform. Managed QC remains a separate review workflow.

## Guardrails

- Do not claim an exact serving submodel unless the environment exposes it. `model_target:gpt_image_2_5` identifies the requested/default prompt branch, not proof that Flare or Sunburst was selected.
- Do not ask for API keys.
- Do not promise deterministic file paths or project logging from the built-in tool.
- Do not silently switch to external tools.
- Do not call Banana or OpenRouter as a fallback.
- Do not print long prompts when the user explicitly wants direct generation.
