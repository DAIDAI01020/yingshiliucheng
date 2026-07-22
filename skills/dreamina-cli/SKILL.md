---
name: dreamina-cli
description: Operate Dreamina（即梦）through the local `dreamina` CLI for login/session checks, credit inspection, explicitly approved image or video submission, async task polling, downloads, recovery, and run-manifest handoff. Use when the user asks Codex to execute 即梦 generation through CLI, says 确认生成 or 直接测试一版, wants task status/history, resumes a known submit_id, or needs downloaded outputs connected to project state. Do not use merely to write a prompt or install/update the CLI without separate authorization.
---

# Dreamina CLI

## Role

Own local Dreamina CLI execution. Connect an approved prompt and references to login, credit checking, task submission, polling, download, run safety, and state handoff.

Inherit route fields from `$zongkong`. Keep `platform_target:jimeng` and identify the runner as `provider:jimeng-cli`. `$ai-video-prompt-director` owns motion semantics, `$prompt-platform-auditor` owns final Dreamina wording, `$video-generation-controller` owns execution readiness/idempotency, and `$project-state-manager` owns persisted run state.

Read [references/cli-command-map.md](references/cli-command-map.md) before installation, login, generation, or task recovery.

## Availability

Check without changing the system:

```powershell
Get-Command dreamina -ErrorAction SilentlyContinue
dreamina -h
dreamina <subcommand> -h
```

Treat current help as the source of truth for subcommands, flags, models, duration, ratio, resolution, references, session, credit, and output behavior. Do not infer current flags from this Skill.

## Installation boundary

The user-provided installer is:

```bash
curl -fsSL https://jimeng.jianying.com/cli | bash
```

Never auto-run it. A separate installation instruction is required because it downloads a binary, writes under the user profile, changes `PATH`, installs a companion Skill, and may modify another tool workspace.

Before authorized installation, download and inspect the script, report target paths/side effects, confirm a compatible Bash surface, then verify `dreamina -h` without submitting a paid task. Never auto-update during generation.

## Confirmation and run safety

Use two stages:

```text
prompt_review_only -> write/audit prompt and stop
execute_after_confirmation -> submit only after 确认生成 or equivalent approval
```

`直接测试一版` approves one bounded task. Preserve:

```text
generation_confirmation: approved / direct_test
cost_scope: one_test / approved_batch
retry_limit: 0 by default
idempotency_key
available_credits when returned by CLI
estimated_cost when the CLI exposes it
```

Before submission, `$video-generation-controller` computes an idempotency key. Check `generation-run-ledger.jsonl`; reuse an existing `submit_id`/result for the same key and never submit a duplicate running/succeeded task. A failed paid run requires explicit resume approval and defaults to at most two confirmed attempts. Never auto-retry paid generation.

## Command selection

Choose the smallest matching command, then inspect help:

```text
text2video -> prompt-only video
image2video -> one main image or first frame
frames2video -> explicit first and last frames
multiframe2video -> several images forming one coherent story
multimodal2video -> supported image/video/audio reference workflow
text2image / image2image / image_upscale -> image tasks
query_result -> recover/query one submit_id and optionally download
list_task -> inspect saved task history
user_credit -> inspect current credit
session -> manage sessions
```

Do not silently change command family or model.

## Preflight

Before paid submission, require:

```text
executable and live subcommand help
valid/reusable login session
user_credit checked when available
available credit >= estimated cost when both are known
explicit generation_confirmation
final approved prompt and negative prompt
existing reference files with explicit roles
supported duration / ratio / resolution
approved output directory
idempotency preflight passed
bounded retry policy
```

Formal work requires `generation_ready_packet`; quick tests require the approved prompt, reference, supported parameters, output path, and explicit confirmation.

## Login

Reuse current login. Run `dreamina login` or `dreamina relogin` only when needed or requested. Surface OAuth/device/QR instructions without exposing secrets. If output contains `[DREAMINA:QR_READY] <absolute-path>`, show that local QR image. Confirm `[DREAMINA:LOGIN_SUCCESS]` or `[DREAMINA:LOGIN_REUSED]` explicitly.

Never print, store, or request raw cookies, tokens, private keys, or account secrets.

## Submit, recover, and download

Treat submission as accepted only when `submit_id` exists and `gen_status` is `querying` or `success`. On `gen_status:fail`, preserve `fail_reason` and stop.

For async work:

1. Save `submit_id`, idempotency key, and non-secret arguments.
2. Query the known task with `query_result`; do not resubmit merely because polling stopped.
3. Poll at a reasonable interval with concise updates.
4. Download to the approved directory.
5. Verify the expected media exists before success.
6. Update `run_manifest.json`, generation ledger, and project state.

If `AigcComplianceConfirmationRequired` appears, ask the user to complete the one-time web confirmation and resume the same task only after confirmation.

## Run packet

```text
dreamina_cli_run_packet
provider: jimeng-cli
platform_target: jimeng
cli_version / subcommand / help_checked
generation_confirmation / cost_scope / retry_count
idempotency_key / credit_checked / available_credits / estimated_cost
session_id / task_type / approved_prompt_source / reference_roles
duration / ratio / resolution / music_policy
submit_id / gen_status / fail_reason
output_paths / run_manifest / project_state
```

Default video `music_policy` to `no_music_allow_sfx`: no background music, score, songs, or sung vocals; synchronized natural ambience and physical sound effects remain allowed unless the user asks for music or full silence.

## User output

```text
prompt_review_only -> final prompt only; no CLI claim
submit accepted -> submit_id, current status, output target
recovered -> existing submit_id/result and no new credit claim
success -> local path, run manifest, concise QC next action
failure -> fail_reason, known credit effect, safest next step
```

## Guardrails

- Never run `curl | bash` without separate installation authorization.
- Never submit a paid task to discover flags.
- Never claim success without `submit_id`, supported status, and verified output when download is expected.
- Never expose credentials.
- Never silently switch platform, model, prompt, or reference role.
- Never open an unbounded polling or retry loop.
- Preserve every successful result when another batch item fails.
