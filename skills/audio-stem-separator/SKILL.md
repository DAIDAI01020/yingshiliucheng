---
name: audio-stem-separator
description: Separate an existing film/video/audio mix into synchronized speech, music and sound-effects stems for editing. Use for 人声音乐音效三轨分离, 去配乐, 提取对白 or remix preparation. Cutting an audio file into time segments, generating music and video prompting are different tasks.
---

# 影视音频分轨

Own separation of an existing mix into **speech / music / sfx**. Enter directly from `$zongkong` as a postproduction utility; preserve the current project and source timeline. No concept/style/image-generation gates are needed.

## Meaning Of The Three Tracks

- 人声: spoken dialogue, narration and audible speech. Singing/overlapping music vocals may be assigned differently by the selected cinematic model; inspect and report that case rather than promising a clean vocal stem.
- 音乐: score/background music and musical content.
- 音效: physical effects, ambience and other non-speech/non-music content.

These are model estimates, not recovered original recording tracks. A vocals/instrumental or vocals/drums/bass/other model is not a cinematic three-stem model. Do not rename accompaniment/residual/other to clean music or effects. Prefer original production stems when available.

## Execution

1. Inspect input audio streams and timeline. Select the intended mix; do not silently combine languages/commentary tracks. Audio-only and video input are supported.
2. Check actual engine/config/checkpoint availability. Use a verified cinematic model with speech, music and sfx outputs; the bundled adapter targets the upstream MSST BandIt/BandIt v2 route. Read [backend and QC](references/backend-and-qc.md) before setup or execution.
3. Reuse an authorized local backend or set up a dedicated environment when needed. Keep dependencies/model weights outside skills/Git. Missing weights mean not ready, not successful separation. Do not substitute a two-stem model.
4. Preserve duration, channel layout and relative timing. The bundled adapter prepares stereo working audio at the model's declared sample rate and delivers 48 kHz stereo stems; mono is explicitly duplicated and multichannel input needs a downmix decision or another backend. Do not remove silence, stretch time or normalize each stem independently.
5. Produce `speech.wav`, `music.wav`, `sfx.wav` plus a manifest of source hash, selected stream, timeline offset, model/config hashes and technical evidence. For final float-WAV stems preserve headroom; convert format only when required by the editor.
6. Listen to representative dialogue/music/effect overlaps, beginnings/endings and joins. Report leakage, lost consonants/transients or phase artifacts. Technical validation is not listening approval.

Use `scripts/separate_audio.py doctor` for readiness. `separate` runs the installed upstream backend; `verify` checks three externally produced stems without claiming this skill generated them. Commands and installation prerequisites are in the reference.

## Handoffs And Completion

If subtitles are also requested, pass the time-aligned speech track and original-video offset to `$video-srt-director`; verify uncertain words against the original mix. Clear speech may be transcribed directly without compulsory separation.

Use `$asset-librarian` / `$project-state-manager` for requested managed records. Do not disguise WAVs as video or images to fit an incompatible ingest command.

Return links to actual stems, the timeline alignment note and any audible limitation. File existence/duration cannot prove clean separation. Preserve the source and prior versions; a new run uses a new directory. A status request must not trigger new separation, software installation or upload.
