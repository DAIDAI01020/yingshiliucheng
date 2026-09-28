---
name: kling-api
description: Configure and validate the official Kling AI API Key for this Windows film workflow without storing it in skills or Git. Use when the user asks to configure, replace, inspect, or test a 可灵/Kling API key or API connection.
---

# Kling API Credential

## Role

Manage the official Kling AI API credential and verify API connectivity. This skill does not write video prompts, submit paid generation, or replace `$video-generation-controller`.

## Security contract

Never place a real key in `SKILL.md`, source code, prompts, manifests, logs, command examples, or the workflow repository. Load credentials in this order:

1. Process environment variable `KLING_API_KEY`.
2. Private local file `~/.config/codex-kling-api/secrets.json` created by `setup-key`.

The default China-region API base is `https://api-beijing.klingai.com`. `KLING_API_BASE_URL` or `--base-url` may override it. Permit plain HTTP only for loopback test servers.

Do not print the key or provider responses containing private account details. Report only source, redacted length, endpoint, authentication state, API code, and whether data was returned.

## Commands

Run from this skill directory:

```powershell
node scripts/kling_api.mjs setup-key --key-stdin
node scripts/kling_api.mjs doctor
node scripts/kling_api.mjs doctor --live
```

`setup-key --key-stdin` reads the key from standard input and writes the private file with restricted permissions. `doctor` is local-only. `doctor --live` calls the official free `/account/costs` endpoint once to verify Bearer authentication; it does not generate content or consume video credits.

## Boundaries

- A configured key is not approval for paid generation.
- Never infer API readiness from a key prefix alone; use `doctor --live` when the user asks to verify it.
- A failed live check may mean invalid credentials, wrong region, network failure, or provider outage. Preserve the key and report only the failure class/status.
- Paid Kling execution remains under `$video-generation-controller` until a reviewed dedicated generation runner is present.

## Source authority

Authentication and regional endpoint details follow the current official [KlingAI Open Platform authentication page](https://kling.ai/document-api/api/get-started/authentication). Recheck the official documentation before changing endpoint paths or authentication semantics.
