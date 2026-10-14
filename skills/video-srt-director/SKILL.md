---
name: video-srt-director
description: Transcribe speech from existing video/audio into an editable SRT subtitle file, or clean supplied timed transcripts/SRT for editing. Apply the user's confirmed style of no commas/full stops/question marks/exclamation marks in subtitle body and exactly three ASCII spaces for within-cue phrase breaks. Do not generate video or burn in captions unless requested.
---

# 视频字幕 SRT

Own speech transcription, timing, subtitle segmentation and editing-ready SRT delivery under `$zongkong`. This is a postproduction branch, separate from script writing and video-generation prompts. Reuse source/project context and act directly on existing media.

## Confirmed Text Style

The user confirmed: **字幕正文去掉逗号、句号、问号和感叹号，同一条字幕中断句用三个半角空格**.

- Apply to subtitle body only: remove `， , 。 . ． ？ ? ！ !` as punctuation and use exactly three U+0020 spaces at the phrase break. Do not use tabs, full-width spaces or a line break instead.
- Preserve ordinary single spaces between English words. Preserve other punctuation unless the user requests broader removal.
- Keep numeric zero and all other digits. SRT sequence numbers, `-->`, colons and timestamp commas remain valid standard syntax.
- Do not join different cues with spaces; longer pauses or speaker/shot changes may require separate timed cues. Three-space breaks are inside a cue.
- Protect numerical meaning. Decimal points are spoken as `点` in this Chinese style; standard thousands grouping commas can be removed without changing value. Review names, abbreviations, URLs and unusual numeric expressions against audio before final delivery. Keep raw transcription for corrections.

## Workflow

1. Inspect the source audio stream/language and timeline origin. Existing timed transcripts/SRT can enter at cleanup; do not transcribe again unnecessarily.
2. Use a verified local ASR backend. The helper supports installed `faster-whisper` and cached/local models, defaulting to no automatic model download. Read [execution and timing](references/execution-and-timing.md).
3. Transcribe the original language, with word timing when available. Do not translate, polish away spoken content or invent words in silence/music. Inspect uncertain names/numbers and mixed/overlapping speech.
4. Group by audible phrasing, word timestamps and readable cue length. Keep a short within-cue pause as three spaces; split long pauses into new cues. No uniform character-based interpolation to manufacture timestamps.
5. Clean body text and validate numbering, millisecond timestamps, ordering, nonnegative duration and required spaces. Retain raw ASR JSON, final SRT and a report of unreviewed/overlong/uncertain parts.
6. Spot-check sync and words against video at beginning/middle/end; full editorial approval requires actual listening/playback. Report machine-generated draft status until reviewed.

For noisy material use `$audio-stem-separator` only when it helps; do not require three-track separation for every subtitle job. Keep the speech stem's source offset and do not trim its silences before ASR.

## Tools

From this skill directory:

```powershell
python scripts/make_srt.py doctor
python scripts/make_srt.py transcribe --input "PATH/video.mp4" --output-dir "PATH/project/subtitles/v001" --model small --language zh
python scripts/make_srt.py format --input "PATH/existing.srt" --output-dir "PATH/project/subtitles/v002"
python scripts/make_srt.py format --input "PATH/transcript.json" --output-dir "PATH/project/subtitles/v003"
```

Deliver an actual UTF-8 `.srt`, not only displayed transcript text. Preserve source files and prior subtitle versions. Subtitles, burned-in video, project timelines and automatic editing decisions are distinct outputs; produce extras only when requested.

For managed delivery pass actual file/source/timing/QC metadata to `$asset-librarian` and `$project-state-manager`. Do not mark the audio transcript as visually or editorially checked based only on syntax validation.
