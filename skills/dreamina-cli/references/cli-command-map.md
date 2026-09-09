# Dreamina CLI Command Map

Use live `dreamina -h` and `dreamina <subcommand> -h` as authority. This reference records only workflow boundaries.

## Installer

```text
https://jimeng.jianying.com/cli
```

The observed installer is a Bash script that downloads `dreamina`/`dreamina.exe`, writes CLI state under the user profile, changes `PATH`, installs a companion Skill, and may modify an OpenClaw workspace. Inspect it before every authorized installation; never pipe it directly to a shell as an implicit generation step.

## Discovery and account

```text
dreamina -h
dreamina <subcommand> -h
login / relogin / logout
login --headless
login checklogin --device_code=<device_code>
user_credit
session
list_task
```

Reuse login state. Never store authentication payloads in project files.

## Generation families

```text
text2image
image2image
image_upscale
text2video
image2video
frames2video
multiframe2video
multimodal2video
query_result
```

Confirm possible aliases from current help.

## Dynamic fields

Read help for model/version, prompt input, negative prompt, local/remote references, role/count behavior, session, duration, ratio, resolution, seed, download directory, credit/cost, and machine-readable output.

For `model_target:seedance_2_5`, treat prompt task modes and platform command families as separate decisions. Preserve the audited reference map, stages, unique edit master, extension boundary, and locked parameters; map them only to flags/subcommands shown by live help. Video edit inherits source ratio and approximate duration, first/end-frame work inherits the first-frame ratio, and extension inherits the source-video ratio. Do not force a conflicting override merely because a generic runner accepts `--ratio` or `--duration`.

## Result and recovery semantics

Accept submission only when `submit_id` exists and `gen_status` is `querying` or `success`. Preserve `fail_reason`, downloaded paths, and credit information when returned.

Use `query_result` for one known task and `list_task` for history. Prefer recovery by `submit_id` and idempotency key over resubmission.

## Workflow mapping

```text
先写提示词 -> ai-video-prompt-director -> prompt-platform-auditor -> stop
确认生成 -> video-generation-controller safety preflight -> dreamina-cli -> submit/query/download
直接测试一版 -> one bounded task, no automatic paid retry
恢复任务 -> reuse submit_id -> query_result -> download/state writeback
正式批量 -> generation_ready_packet -> sequential/small batch -> partial success preserved -> state writeback
```
