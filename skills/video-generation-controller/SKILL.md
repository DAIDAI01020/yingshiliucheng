---
name: video-generation-controller
description: Coordinate video generation or external video-platform handoff for film AI workflows. Use when the user explicitly asks to generate video, test first-frame motion, batch Seedance shots, prepare Jimeng/Kling manual execution, or turn selected keyframes into saved video files while keeping outputs connected to project state.
---

# Video Generation Controller

## Core role

This is the lightweight execution controller for AI video generation and manual platform handoff. It does not replace `$ai-video-prompt-director` or `$seedance-2-video`; it connects approved prompts, references, run manifests, and project state into a repeatable production step.

Use it when the user says:

- `出视频`
- `用 Seedance 出`
- `即梦/Seedance 生视频`
- `可灵出视频`
- `可灵 O1 / Omni 手动执行`
- `让这张图动起来`
- `测试 5 秒视频`
- `把 S03 做成视频`

## Default policy

- Default API provider: Seedance/Ark through `$seedance-2-video`.
- Jimeng/Kling/Kling O1/Kling VIDEO 3.0 Omni are treated as external/manual platform runs unless a dedicated API runner exists.
- Default Jimeng/Kling audio policy: `不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白。`
- Default input image mode: public URL with `--image-url`.
- Do not use local `--image-file` unless the user explicitly asks for local relay or URL Relay is already configured for this project.
- Do not guess old images. Resolve the first frame from the current project asset index or ask for a public URL.
- Always write `run_manifest.json`.
- If `projectRoot` is provided, ingest the video run into `$project-state-manager`.

## No Lazy Execution Rule

This controller executes video only. It does not write or repair video prompts, choose the first frame, decide style, or fix missing shot logic.

Real Seedance/Ark generation may run only when all execution inputs are present:

```text
ai-video-prompt-director final video prompt exists
prompt-platform-auditor decision is 通过 or 保效精简后通过
first frame / reference image role is clear
public http/https image URL is available, or explicit local relay approval exists
duration and ratio are specified or inherited from the approved prompt
project-style-lock is present for formal project batches
```

For formal or managed work, execution must come from a `generation_ready_packet` or a managed video job containing the same fields:

```text
generation_ready_packet
target_tool: Seedance / Ark / Jimeng / Kling / Kling O1 / Kling VIDEO 3.0 Omni
prompt_direction: first_frame_motion / dialogue_coverage / product_motion / reference_continuity / local_edit / multi_shot_omni / quick_motion_test
project_root:
shot_or_asset_id:
final_prompt:
negative_or_forbidden:
audit_status: 通过 / 保效精简后通过
audited_prompt_packet:
source_lock:
reference_roles:
first_frame_or_image_refs:
duration:
ratio:
audio_policy: default "不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白。"
output_path_rule:
state_writeback:
```

If any item is missing, stop before submission and route back:

```text
missing video prompt -> ai-video-prompt-director
missing platform approval -> prompt-platform-auditor
missing first frame/public URL -> project-state-manager / asset-librarian / url-relay
missing shot logic -> shot-language-auditor
missing generation_ready_packet fields -> project-state-manager / prompt-platform-auditor
missing Kling O1/Omni role map -> project-state-manager / scene-style-map-director / project-style-lock
```

Do not submit Seedance/Ark as a way to test unclear style, unclear action, missing first frame, or unaudited prompts.

## Fast execution mode

When the user says `出视频`, `测试一下`, `继续出`, or `直接跑`, keep the response short:

1. Confirm audited prompt, shot, and image URL in one short line.
2. Run doctor or dry-run only if the input is new or risky.
3. Submit Seedance only if the No Lazy Execution Rule passes, or write a Jimeng/Kling manual handoff manifest when the target platform is external.
4. Return video preview/local path if present, the handoff manifest path, and one sentence of QC or next action.

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

Kling / O1 / Omni manual handoff:

```powershell
node H:\yingshi\skills\video-generation-controller\scripts\run-video-generation.mjs --provider kling-omni --project-root H:\yingshi\projects\project --shot S03 --prompt-file H:\yingshi\projects\project\prompts\S03_kling_omni.txt --image-file H:\yingshi\projects\project\references\S03_first_frame.png --reference-roles H:\yingshi\projects\project\prompts\S03_kling_roles.json --task-type multi_shot_storyboard --duration 10 --ratio 9:16 --audio-policy "不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白。"
```

If the video has already been downloaded from Kling, add:

```powershell
--output-video H:\yingshi\projects\project\video-runs\S03_kling_omni_v01.mp4 --status succeeded
```

## Output

For Seedance, the controller prints JSON:

```json
{
  "provider": "seedance",
  "outputDir": "H:\\...",
  "video": "H:\\...\\final.mp4",
  "runManifest": "H:\\...\\run_manifest.json",
  "projectState": {}
}
```

For Jimeng/Kling manual handoff, the controller writes:

```json
{
  "provider": "kling-omni",
  "outputDir": "H:\\...",
  "runManifest": "H:\\...\\run_manifest.json",
  "promptCopy": "H:\\...\\approved_prompt.txt",
  "video": "",
  "projectState": {}
}
```

## Guardrails

- Never print or store API keys.
- Stop before generation if `ARK_API_KEY` is missing.
- Stop before generation if the prompt has not passed `$prompt-platform-auditor`.
- Stop before generation if no public first-frame URL or explicit local relay approval exists.
- Prefer `--image-url`; only use local relay on explicit request.
- For Jimeng/Kling manual handoff, do not pretend the platform has been executed. Use `task.status: manual_handoff` until a downloaded video path is attached.
- For Jimeng/Kling manual handoff, preserve or default `audio_policy` to `不要音乐，不要配乐；可以保留真实环境音效和动作音效，不要额外旁白。` unless the user explicitly requested music, score, dialogue, voiceover, native audio, or a reference voice.
- For Kling O1 / VIDEO 3.0 Omni, require `reference_roles` / role-map provenance before handoff.
- Do not create a large video studio framework. This is a thin controller around Seedance plus manual platform state logging.
