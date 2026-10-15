---
name: xiaohongshu-publisher
description: Execute authorized Xiaohongshu image or video publication and scheduled submissions through a local xiaohongshu-mcp service, with account checks, immutable content fingerprints and duplicate-submit receipts. Use for ready posting packs, publication status or publisher setup; content creation and editorial calendars stay with their existing owners.
---

# Xiaohongshu Publisher

Own transport and observed publication evidence under zongkong. Receive the exact ready pack from [xiaohongshu](../xiaohongshu/SKILL.md); [xiaohongshu-operator](../xiaohongshu-operator/SKILL.md) owns topics, calendars and daily orchestration. Do not recreate images, change copy, crop media, or add engagement automation while publishing.

## Execution

Read [service and packet contract](references/service-and-packets.md) for setup, packet fields and commands. Prefer an already configured compatible MCP connection; the bundled Python client provides a narrow REST adapter to the same upstream server when no connector is installed. Do not run both transports for one post. Installation is not account login or a live publishing test.

1. Identify account by actual user ID, project/series and stable post_id. Reuse the same account receipt directory across projects and transports. Read prior receipts and the ready pack. Inline media without verified local files is not ready.
2. Prepare the packet offline. The helper hashes media bytes, copy, target account, visibility, schedule and review evidence. Show the actual ordered media and final copy when user approval is still needed. A successful dry run proves packet validity only.
3. Reuse explicit publication authorization already present in the conversation, including a bounded recurring authorization. Otherwise finish preparation before asking for publication. Record its source. Setup approval alone authorizes no account action. The helper's execute flag is an operator safeguard, not proof of human approval.
4. Before sending, check service health, actual logged-in user ID, review result and the prepared fingerprint. Scheduled publishing requires an explicit timezone and a supported future time. Do not silently change an expired schedule to immediate publishing.
5. Write a durable `submitting` receipt before sending once. Preserve `submission_unknown` after errors, timeout, crash or ambiguous response and inspect the creator's drafts/scheduled/published list before any retry. Never change post_id, ledger directory or transport to bypass a duplicate block.
6. An upstream success response is `server_accepted` or `schedule_accepted`, not independent confirmation of visibility. Verify the matching entry in the creator UI and record its real ID/URL and observation. An accepted scheduled post is still pending publication. Do not infer published status just because its scheduled time passed.

The receipt is transport evidence linked to the post's existing project state, not another editorial calendar or asset database. The helper deliberately has no automatic retry or delete/reset command. Reconcile ambiguous receipts with evidence; only an observed non-submission and the still-valid user scope permit a controlled retry.

## Limits

The upstream REST publish endpoints submit directly; they do not provide a draft-only preview. For “填好 / 存草稿”, use the existing authorized browser workflow and record actual draft evidence. Read current MCP schemas before using additional options. If a required disclosure/cover control is unsupported, use the creator UI; do not silently omit it or claim an unrelated `is_original` flag is an AI disclosure.

Credentials, browser profiles, binaries, runtime logs and receipts remain outside the workflow repository. Bind the service to loopback and keep its bearer token in a local file/environment. User-operated login/CAPTCHA stays with the user. Do not copy unrelated browser cookies.

For everyday automation read [daily execution](../xiaohongshu-operator/references/daily-execution.md). Installing this skill creates no timer. Report readiness precisely: adapter tested, runtime healthy, account logged in, submission accepted, and post observed are different milestones.
