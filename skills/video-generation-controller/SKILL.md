---
name: video-generation-controller
description: Coordinate Seedance/Ark video generation for film AI workflows. Use when the user explicitly asks to generate video, test first-frame motion, batch Seedance shots, or turn selected keyframes into saved video files while keeping outputs connected to project state.
---

# Video Generation Controller

## Core role

This is the lightweight execution controller for AI video generation. It does not replace `$ai-video-prompt-director` or `$seedance-2-video`; it connects them into a repeatable production step.

Use it when the user says:

- `出视频`
- `用 Seedance 出`
- `即梦/Seedance 生视频`
- `让这张图动起来`
- `测试 5 秒视频`
- `把 S03 做成视频`

## Default policy

- Default provider: Seedance/Ark through `$seedance-2-video`.
- Default input image mode: public URL with `--image-url`.
- Do not use local `--image-file` unless the user explicitly asks for local relay or URL Relay is already configured for this project.
- Do not guess old images. Resolve the first frame from the current project asset index or ask for a public URL.
- Always write `run_manifest.json`.
- If `projectRoot` is provided, ingest the video run into `$project-state-manager`.

## Fast execution mode

When the user says `出视频`, `测试一下`, `继续出`, or `直接跑`, keep the response short:

1. Confirm shot/prompt/image URL in one short line.
2. Run doctor or dry-run only if the input is new or risky.
3. Submit Seedance.
4. Return video preview, local path, and one sentence of QC.

## Token/cost saving

- Prefer one video per run during testing.
- Use 5 seconds for motion tests unless the user specifies another duration.
- Use the frame's natural ratio; do not force 16:9 when the source is vertical.
- Use public image URLs to avoid unnecessary relay calls.
- Keep prompts focused on one main action and one main camera movement.

## Script usage

```powershell
node H:\yingshi\skills\video-generation-controller\scripts\run-video-generation.mjs --provider seedance --prompt-file H:\yingshi\prompt.txt --image-url https://example.com/frame.png --duration 5 --ratio 3:4 --output-dir H:\yingshi\outputs\seedance-test
```

Project-managed run:

```powershell
node H:\yingshi\skills\video-generation-controller\scripts\run-video-generation.mjs --provider seedance --project-root H:\yingshi\projects\project --shot S03 --prompt-file H:\yingshi\projects\project\prompts\S03_video.txt --image-url https://example.com/frame.png --duration 5 --ratio 16:9
```

## Output

The controller prints JSON:

```json
{
  "provider": "seedance",
  "outputDir": "H:\\...",
  "video": "H:\\...\\final.mp4",
  "runManifest": "H:\\...\\run_manifest.json",
  "projectState": {}
}
```

## Guardrails

- Never print or store API keys.
- Stop before generation if `ARK_API_KEY` is missing.
- Prefer `--image-url`; only use local relay on explicit request.
- Do not create a large video studio framework. This is a thin controller around Seedance.
