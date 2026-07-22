---
name: video-generation-controller
description: Coordinate approved AI video generation and external-platform handoff with project traceability. Use when the user explicitly asks to generate video, confirms a Jimeng prompt, tests first-frame motion, batches Seedance shots, prepares Kling manual execution, resumes a failed run, or attaches a downloaded video while requiring idempotency, credit preflight, run manifests, partial recovery, and state writeback.
---

# Video Generation Controller

## Core role

Execute or hand off an approved video job. Do not write prompts, choose visual style, invent first frames, approve audits, or change `$zongkong` route decisions.

Execution ownership:

```text
semantic prompt -> ai-video-prompt-director
platform audit -> prompt-platform-auditor
Jimeng live CLI -> dreamina-cli
Seedance/Ark live API -> seedance-2-video through this controller
Kling/O1/Omni -> manual handoff unless a dedicated runner exists
state, idempotency and observations -> project-state-manager
```

For formal work, execute only from `generation_ready_packet` or an equivalent managed job. Quick tests may stay light but still require a final prompt, explicit reference role, platform target, ratio/duration, and paid-run confirmation.

## Required execution packet

```text
generation_ready_packet
target_tool: Jimeng / Seedance / Ark / Kling / Kling O1 / Kling VIDEO 3.0 Omni
project_root:
shot_or_asset_id:
final_prompt:
negative_or_forbidden:
audit_status: 通过 / 保效精简后通过
audited_prompt_packet:
source_lock:
reference_roles:
first_frame_or_image_refs:
task_type:
complexity_mode:
duration:
ratio:
ending_behavior:
audio_policy:
music_policy: no_music_allow_sfx / music_requested / full_silence
generation_confirmation: approved / direct_test
output_path_rule:
state_writeback:
```

Default `music_policy` to `no_music_allow_sfx`: reject background music, score, songs, and sung vocals while allowing synchronized natural ambience and physical sound effects. Explicit music or full silence overrides this default.

Route missing inputs back to their owners. Never use paid generation to discover a missing style, action, first frame, or shot plan.

## Run safety and recovery

For every managed API/CLI run:

1. Compute one idempotency key from provider/model, prompt, reference roles, first-frame source, task type, duration, ratio, resolution, and audio policy.
2. Require `generation_confirmation` before paid submission.
3. Compare `available_credits` and `estimated_cost` when both are available; stop when insufficient and never guess a balance.
4. Write `revision-logs/generation-run-ledger.jsonl` through `$project-state-manager`.
5. Reuse or block an existing succeeded/submitted/running task with the same key.
6. After a failure, require explicit `--resume`; default to at most two confirmed attempts.
7. Use `--force-new-run` only after an explicit request for a genuinely new paid attempt.
8. Preserve successful outputs and task IDs. Never auto-retry a paid video submission.

The ledger is recovery state, not creative state. It stores no keys, tokens, private upload credentials, or payment data.

## Provider rules

### Seedance / Ark

- Require `ARK_API_KEY`, an audited prompt, and a public image URL unless the user explicitly approves local relay.
- Prefer `--image-url`; accept `--image-file` only with `--allow-image-file`.
- Submit through `$seedance-2-video`, preserve its task ID/run manifest, ingest state, and record ledger completion/failure.
- If an identical task is already submitted/running, return the existing task instead of resubmitting.

### Jimeng / Dreamina CLI

- Check command availability and current subcommand help through `$dreamina-cli`.
- Discover whether `text2video`, `image2video`, `frames2video`, `multiframe2video`, or `multimodal2video` fits the approved reference plan.
- Check credit when the CLI exposes it, submit only after confirmation, capture `submit_id`, query/download, write `run_manifest.json`, and ingest state.
- Never install/update the CLI implicitly and never execute `curl | bash` from this controller.
- If CLI availability/help fails, preserve a Jimeng manual handoff; do not pretend execution succeeded.

### Kling / O1 / Omni

- Keep manual unless a dedicated runner exists.
- Require `reference_roles`; O1/Omni also require role-map provenance.
- Write the approved prompt copy and `run_manifest.json` with status `manual_handoff`.
- When the user provides a downloaded video, attach the path, mark `succeeded`, and ingest it without creating another handoff.

## Fast mode

When the user says `出视频`, `测试一下`, `继续出`, or `直接跑`:

1. Confirm shot, audited prompt, reference source, and paid confirmation in one short line.
2. Run only the necessary availability/credit/idempotency checks.
3. Execute or create the manual handoff.
4. Return the video/path, run manifest, reused/resumed state, and one next action.

Prefer one five-second video per motion test unless the user specifies otherwise. Preserve the source ratio.

## Script usage

Seedance managed run:

```powershell
node H:\yingshi\skills\video-generation-controller\scripts\run-video-generation.mjs --provider seedance --project-root H:\project --shot S03 --prompt-file H:\project\prompts\S03.txt --image-url https://example.com/frame.png --duration 5 --ratio 16:9 --generation-confirmation approved
```

Resume a failed Seedance run:

```powershell
node H:\yingshi\skills\video-generation-controller\scripts\run-video-generation.mjs --provider seedance --project-root H:\project --shot S03 --prompt-file H:\project\prompts\S03.txt --image-url https://example.com/frame.png --duration 5 --ratio 16:9 --generation-confirmation approved --resume
```

Kling/O1/Omni handoff:

```powershell
node H:\yingshi\skills\video-generation-controller\scripts\run-video-generation.mjs --provider kling-omni --project-root H:\project --shot S03 --prompt-file H:\project\prompts\S03.txt --image-file H:\project\references\S03.png --reference-roles H:\project\prompts\S03_roles.json --task-type multi_shot_storyboard --duration 10 --ratio 9:16 --audio-policy "不要背景音乐；允许同步环境声和物理音效"
```

Attach an externally downloaded result with `--output-video ... --status succeeded`.

## Output contract

Return:

```text
provider / shot / output_dir / video / run_manifest / project_state
idempotency_key / reused / resumed / ledger_event
task_id or submit_id when available
```

Every run manifest preserves `music_policy`, reference provenance, task status, idempotency key, elapsed time, and credit/cost metrics when available.

## Guardrails

- Never print or store API keys or tokens.
- Never submit without prompt audit and paid-generation confirmation.
- Never silently switch platform or reference source.
- Never auto-retry a paid task.
- Never discard a successful artifact because another batch item failed.
- Never claim manual handoff or an existing task was newly executed.
- Keep this controller thin; provider-specific request compilation remains with the provider skill.
