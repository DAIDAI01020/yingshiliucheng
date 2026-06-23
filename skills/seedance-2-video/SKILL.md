---
name: seedance-2-video
description: "Call Seedance 2.0 directly through Volcano Ark to generate videos from Chinese prompts and public image URLs or local image files relayed through SW URL Relay. Use when Codex needs only the Seedance 2.0 video generation capability, outside the full IP Video Factory planning flow: submit Ark video tasks, poll slow queues, download final.mp4, and write run_manifest.json without using Luna."
---

# Seedance 2.0 Video

## Operating Principle

Use this skill when the user already has a Seedance-ready prompt and one or more public image URLs, or local image files that must be converted into public URLs, and wants to generate a video through Ark/Seedance directly.

This skill is a narrow generation module, not a story planner. It does not create IP profiles, titles, story candidates, covers, subtitles, or publish packs. For full IP planning, use `$ip-video-factory`; for direct Seedance generation, use this skill.

## Security Rule

Never write a real API key into this skill, generated files, prompts, manifests, logs, or examples. Read the key from `ARK_API_KEY` first, then from the local private key file created by `setup-key`.

Never write the SW media uploader token into this skill, generated files, prompts, manifests, logs, or examples. URL Relay reads uploader settings from the private local file `~/.config/sw-media-uploader/config.json` or local environment variables. `run_manifest.json` may record source file paths, relay URLs, relay type, and expiry hints, but must not record upload tokens.

If the user asks to package a key inside the shareable skill, explain that the shareable skill can contain the key-reading wrapper and setup instructions, but not the real key. Each user can either set an environment variable:

```bash
export ARK_API_KEY="your_ark_api_key"
```

Or run a one-time local setup command:

```bash
python3 scripts/seedance_task.py setup-key
```

`setup-key` saves the key to `~/.config/codex-seedance-2-video/secrets.json` with private file permissions. This file is outside the shareable skill folder.

For employee distribution, prefer the wrapper:

```bash
scripts/install_employee_key.sh
```

It hides key input, writes the same local private file, and runs `doctor` after installation.

Optional:

```bash
export ARK_BASE_URL="https://ark.cn-beijing.volces.com"
```

On this Windows workflow, prefer the Node runner. Direct `--image-url` runs entirely in Node; `--image-file` calls the local URL Relay helper and therefore needs a Python 3 executable available through `PYTHON`, `PYTHON_EXE`, or a known local install:

```powershell
& 'C:\Program Files\Adobe\Adobe Creative Cloud Experience\libs\node.exe' scripts\seedance_task.mjs doctor
```

## Default Contract

- Provider: Volcano Ark direct API.
- Model: `doubao-seedance-2-0-260128`.
- Submit endpoint: `POST /api/v3/contents/generations/tasks`.
- Poll endpoint: `GET /api/v3/contents/generations/tasks/{task_id}`.
- Auth: `Authorization: Bearer <local key>`, loaded from `ARK_API_KEY` or the private `setup-key` file.
- Input images: 1-9 inputs total, either public `http`/`https` URLs via `--image-url` or local files via `--image-file`. Local files are uploaded through the SW URL Relay before Ark submission.
- Default video settings: `ratio=9:16`, `duration=15`, `resolution=720p`, `watermark=false`, `seed=-1`.
- Output: `final.mp4` and `run_manifest.json` in the selected output directory.

## URL Relay For Local Files

Use `--image-url` when the image is already a public URL. Use `--image-file` when the user gives a local file path. The runner uploads the local file through `url-relay/scripts/url_relay.py`, receives a public URL, and then builds the normal Ark payload.

One-time private relay setup:

```powershell
python C:\Users\admin\.codex\skills\seedance-2-video\url-relay\scripts\url_relay.py setup --upload-url http://123.56.255.86/upload --public-base http://123.56.255.86/u --temporary-relay-fallback auto --litterbox-time 24h
```

Optional token can be stored in the private config by adding `--token <token>` to setup, or supplied locally through `SW_MEDIA_UPLOADER_TOKEN`. Do not put the token in this skill folder.

Relay checks:

```powershell
python C:\Users\admin\.codex\skills\seedance-2-video\url-relay\scripts\url_relay.py doctor

node C:\Users\admin\.codex\skills\seedance-2-video\scripts\seedance_task.mjs doctor --image-file H:\yingshi\reference.png
```

Relay behavior:

- Existing public URL: submit directly.
- Local file: upload through SW media uploader.
- SW uploader timeout/network/5xx failure with `temporary_fallback=auto`: fallback to Litterbox 24h and print `SW media uploader unavailable; temporary relay fallback used: litterbox.`
- Missing token, missing upload URL, bad config, missing local file, or local permission error: fail without fallback and do not submit Ark.

## Workflow

1. Read `references/ark-seedance-api.md` when you need exact payload shape, status parsing, or troubleshooting details.
2. For first-time setup on a new machine, save the key locally:

   ```bash
   scripts/install_employee_key.sh
   ```

3. Run a dry payload check before spending credits when prompt or image URLs are new:

   ```bash
   node scripts/seedance_task.mjs dry-run \
     --prompt-file video_prompt.txt \
     --image-url https://example.com/source.png
   ```

   For a local image file, dry-run still performs the relay upload so the sanitized payload contains the real public URL:

   ```powershell
   node C:\Users\admin\.codex\skills\seedance-2-video\scripts\seedance_task.mjs dry-run --prompt-file H:\yingshi\video_prompt.txt --image-file H:\yingshi\reference.png
   ```

4. Check environment and optional image URLs:

   ```bash
   node scripts/seedance_task.mjs doctor \
     --image-url https://example.com/source.png
   ```

5. Submit, poll, download, and write the manifest:

   ```bash
   node scripts/seedance_task.mjs run \
     --prompt-file video_prompt.txt \
     --image-url https://example.com/source.png \
     --output-dir outputs/seedance-demo
   ```

   Local-file version:

   ```powershell
   node C:\Users\admin\.codex\skills\seedance-2-video\scripts\seedance_task.mjs run --prompt-file H:\yingshi\video_prompt.txt --image-file H:\yingshi\reference.png --output-dir H:\yingshi\outputs\seedance-test
   ```

6. If the task is queued for a long time or a session is interrupted, continue with:

   ```bash
   node scripts/seedance_task.mjs poll \
     --output-dir outputs/seedance-demo
   ```

The original Python runner is kept as a fallback for machines with Python installed.

## IP Video Factory Compatibility

When called from an `$ip-video-factory` story directory, prefer:

```bash
python3 scripts/seedance_task.py run --run-dir <story-dir>
```

The script reads `<story-dir>/video_prompt.txt` and the prepared `luna_public_url` from `<story-dir>/run_manifest.json` or the parent `batch_manifest.json`. It still calls Ark directly; the Luna URL is only used as the already-public image URL.

## Slow Queue Behavior

Seedance video generation can queue for hours. The script uses slow adaptive polling:

- 0-2 minutes: every 15 seconds.
- 2-15 minutes: every 45 seconds.
- After 15 minutes: every 120 seconds.
- If the provider returns queue or estimated wait fields, record them in `run_manifest.json`; do not fail when those fields are absent.

## Resource Guide

- `scripts/seedance_task.mjs --help`: Node runner for Windows/Codex workflows.
- `scripts/seedance_task.py --help`: Python fallback, including `setup-key`.
- `url-relay/scripts/url_relay.py --help`: minimal SW URL Relay helper for local image files.
- `scripts/install_employee_key.sh --help`: one-command employee key setup wrapper.
- `references/ark-seedance-api.md`: Ark endpoint, payload, response parsing, and image URL rules.
