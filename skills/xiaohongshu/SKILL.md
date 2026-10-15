---
name: xiaohongshu
description: Produce Xiaohongshu art-image and film-diary posts through visual concepts, image sets, finished copy, reviewed posting packs and authorized upload/publishing assistance. Use for explicit Xiaohongshu production or continuation of an established series. Account strategy, editorial calendars and performance analysis belong to xiaohongshu-operator; generic surreal imagery alone does not select this skill.
---

# Xiaohongshu

## Role And Authority

Own individual-post visual concepts, image-set design, finished copy and publishing handoff. Operate as a production branch under `$zongkong`, in the current chat by default. Account positioning, audience hypotheses, topic priorities, calendars, packaging strategy and data analysis belong to [Xiaohongshu Operator](../xiaohongshu-operator/SKILL.md). Inherit its valid operations_brief rather than repeating strategy; a fixed user brief or existing plan may enter production directly.

For an established planned series, “今天做什么 / 继续出图” first reads the current month/week calendar and the next unfinished post_id. Do not invent a new topic each turn or regenerate a completed item. A new idea goes into the planning backlog unless the user explicitly changes the current slot.

Inherit `execution_intent`, `speed_mode`, `project_tier`, `workflow_mode`, `main_line`, `deliverable_profile`, `platform_target`, `model_target`, `response_mode`, and `qc_mode` from `zongkong_route_packet`. Do not downgrade formal production or change an explicit/inherited platform. A branch is a skill route, not permission to create another chat, agent or scheduler.

Respect the single owners in the [capability registry](../zongkong/references/capability-registry.json) and [stage handoff contract](../zongkong/references/stage-handoff-contract.md):

- `$frame-vision-director` owns image prompt semantics; this skill supplies the concrete visual brief.
- `$xiaohongshu-operator` owns account/series operations and packaging review; this skill realizes its brief in actual images and finished copy. Neither replaces the other's review.
- `$prompt-platform-auditor` owns platform compilation and prompt audit.
- `$builtin-imagegen-director`, `$banana-image-generator`, or `$midjourney` owns execution for the selected platform.
- `$image-qc-director` owns evidence-based image QC; `$revision-director` scopes repairs.
- `$project-folder-director`, `$asset-librarian`, and `$project-state-manager` own paths, asset inventory and persistent state.

These are procedures to actually perform, not names to list as proof of review. Read each applicable skill before using it; preserve its concrete result and evidence. Do not spawn reviewers without authorization.

## Select The Content Branch

Apply the [branch isolation rules](references/surreal-art-workflow.md#branch-isolation) before selecting `surreal_art`. Current explicit deliverable and existing project/column state take precedence over aesthetic keywords. Uploading existing work adds a publishing step; it does not migrate the source project into the art series.

| Branch | When | Reference |
| --- | --- | --- |
| `surreal_art` | 明确的小红书艺术栏目需求，或继续已建立的每日艺术图 / 日常之外栏目；仅“神秘感、超现实”不足以触发 | [Mysterious surreal art production](references/surreal-art-workflow.md) |
| `film_diary` | 明确要求影视场景设计、一日一镜、可拍摄场景、商业练习 | [Film diary playbook](references/film-diary.md) and [post templates](references/post-templates.md) |

The approved creative direction for the current art series is **日常空间里的神秘超现实**. Gentle, dreamlike, lonely, curious and mildly unsettling moods are allowed. The suggested series name **日常之外** is a working label, not an approved account rename.

For every `surreal_art` issue, apply the [long-term art direction standards](references/art-direction-standards.md). The user's requirement for sustained imagination and artistic quality applies to the entire series, not only a rejected first image. Specific proposed palettes, media and compositions remain proposals until selected; no single revision becomes the universal template. These standards do not change `film_diary` or shared production skills.

Do not impose the film diary's Saturday commercial exercise, Sunday teaching format, growth pivot, or content percentages on `surreal_art`. Do not require intentional impossible scenes to be physically filmable.

## Resolve The Requested Action

| Request | Deliver |
| --- | --- |
| 账号方向 / 每天发什么 / 排期 / 数据复盘 | Hand off to xiaohongshu-operator for a concrete strategy, topic plan or evidence-based review; no implied generation/scheduling |
| 已定选题，设计画面 | Realize the current operations/user brief as specific visual concepts; do not reopen account positioning |
| 把流程写进总控 / 增加分支 | Update the workflow; do not treat implementation as a request to generate or upload today's post |
| 只给提示词 | Completed prompts through the applicable prompt owner; no image generation |
| 先试一张 | Actual generated image, normally `quick_test`, preserving applicable approved direction |
| 做今天一套 / 出图并审核 / 完整发布素材 | Actual image set, applicable audits, QC and copy; use `formal_managed` when tracked QC/delivery is requested |
| 审核这组 / 继续审核 | Inspect existing assets and finish outstanding checks; do not regenerate passed assets |
| 上传这套 / 填好小红书 | Upload the identified ready pack and fill the page within authorization; final publication is a separate action unless explicitly included |
| 发布这套 | Identify the exact pack/version and target account, finish readiness checks, then execute within the user's explicit scope |

Daily editorial cadence is not a timed automation. Create recurring work only when requested, using the app's automation tool and an explicit schedule/scope; saving this branch alone creates none.

Keep the compact `xiaohongshu_route_packet` internally:

```text
task_mode: strategy / calendar / image_prompt / image_generation / copywriting / publish_assist / review
content_branch: surreal_art / film_diary
series:
post_id:
post_unit: single_image / three_image_set / five_card_post / collection
source_and_approval_basis:
platform_action: none / prepare / fill_publish_page / publish_authorized
missing_fields:
route_back_to:
```

Missing prerequisites go to their owning skills; continue authorized prerequisite work rather than stopping at the route packet. A plan is not a generated set, and generated media is not an approved upload pack.

## Execution And Review Boundary

Use the selected branch's workflow. For new generic built-in image work, follow `$zongkong`'s platform/model default; never switch to a paid provider because saving, QC or uploading is difficult.

For built-in imagegen, follow its native-result response rule: end the generation response with the generated images. Formal QC, capture and copy continue in a separate review stage/turn; record them as pending until performed. If the environment cannot run that stage automatically, state this boundary before generation and leave a resumable task. Do not claim the whole pack is ready after merely displaying images.

Only record returned media and verified paths. Inline-only results remain pending capture. Inspect actual images before visual QC; use technical measurements as supporting evidence, not an aesthetic verdict. Keep successful files and repair only affected images within the execution owner's retry limits and user scope.

## Upload And Publish Assistance

For service-backed publishing of a ready pack, hand off to [Xiaohongshu Publisher](../xiaohongshu-publisher/SKILL.md), which owns transport, account verification and submission receipts. Keep creative and QC ownership here. The publisher's REST endpoints submit immediately or schedule; draft-only filling stays with the browser path below. Both paths reuse the same post_id and account receipts; never switch transports to retry an uncertain submission. Daily continuation uses [daily execution](../xiaohongshu-operator/references/daily-execution.md).

Prepare the exact ordered files, title, body, tags and applicable AI-content disclosure before browser work. A no-text art cover does not become a poster-design task just because it is the first image.

When upload is requested, read the available in-app browser skill first. Use the computer-use skill only if native desktop/file-picker interaction is needed and supported. Inspect the actual creator page; do not guess UI controls, accepted limits, login state or success.

1. Reuse the identified post pack, verify current file/version/QC evidence and target account.
2. Upload only the selected ready files in the documented order; fill the reviewed text and appropriate visible disclosure controls.
3. Verify thumbnails/order, cover crop and actual form values. Stop for user-operated login, CAPTCHA, SMS or identity verification when necessary.
4. Upload/form-filling authorization alone does not authorize final publication. If the user already explicitly authorized publication of this exact pack to this account, do not ask again. Otherwise present the completed preview and ask for that final action only.
5. Record an observed draft or publication result with a real ID/URL when exposed. If submission is uncertain, inspect existing drafts/posts before retrying; never create a duplicate to test success.

If upload or local capture is unavailable, deliver the verified ordered files and copy, name the exact missing capability, and resume from there when possible. Never label a local pack uploaded or published.

## Output

Use concise tables for concepts and calendars. For generation, show actual images following tool rules. For completed review, show inspected versions, the QC verdict, targeted repairs and remaining blockers. For a posting pack, deliver images/order, title, copy, tags and status without internal routing jargon. For upload, report exactly what is filled or published, based on observed evidence.
