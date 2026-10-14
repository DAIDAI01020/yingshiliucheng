# Subtitle Execution And Timing

## Backend

The helper uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper) in transcription mode with word timestamps and VAD. Its [implementation](https://github.com/SYSTRAN/faster-whisper/blob/master/faster_whisper/transcribe.py) supports local-only model loading. Inspect the actual installed version if options change.

`doctor` checks FFmpeg/ffprobe and package presence; it does not claim model weights or GPU inference are ready. Pass a local model directory or cached model name. `--allow-model-download` is only for setup scope that includes the download. Device/compute defaults are CPU/int8 for portability; choose CUDA/float16 explicitly after verifying the runtime.

Select the intended audio stream with `--audio-stream N`. The helper extracts mono 16 kHz speech for ASR and retains its offset relative to the video/container start; internal audio gaps are preserved. A separate aligned speech stem needs `--offset` equal to its original-video placement. Do not apply the same source offset twice.

Use `--offset` additionally for placement under a larger edit sequence. If a source was cut, concatenated or retimed, a constant offset is insufficient: get the edit map or transcribe the final edit.

## Timed JSON Input

```json
{
  "segments": [
    {"start": 0.5, "end": 2.8, "text": "你好，欢迎回来。", "words": [
      {"start": 0.5, "end": 1.0, "word": "你好，"},
      {"start": 1.4, "end": 2.8, "word": "欢迎回来。"}
    ]}
  ]
}
```

Start/end are seconds on the input timeline. Word times allow sensible splitting; without them keep each segment's timing rather than guessing per-character timing. The report flags cues exceeding configured limits.

Defaults: up to 32 visible characters and 6 seconds per cue, a 0.4-second within-cue pause uses three spaces, a 0.9-second gap starts a new cue. These are adjustable helper defaults, not universal creative rules. A single long ASR word/segment remains intact and flagged for review.

`format` accepts existing SRT or timed JSON. It removes commas, full stops, question marks and exclamation marks from bodies, using exactly three ASCII spaces at within-cue phrase breaks, while preserving existing SRT timing and other punctuation. Decimal numbers become spoken Chinese form (`3.5` -> `3点5`); standard grouping commas become ungrouped digits (`1,000` -> `1000`). This protects numeric meaning while respecting the no-period/no-comma display style; review unusual expressions manually.

The output report separates `technical_status` from `editorial_status`. Silent/no-speech input generates no fake cues and reports `no_speech_detected`; check the source before treating an empty subtitle file as finished delivery.

## Example Of File Syntax

```srt
1
00:00:00,500 --> 00:00:02,800
你好   欢迎回来
```

Those are exactly three ASCII spaces in the body. Timestamp punctuation and numeric zero are required and remain unchanged. Read the saved file back to validate; do not use a whole-file comma-removal operation.

## Review

Check names, amounts, dates, units, negation, language switching, overlapping voices and quiet dialogue. ASR confidence is a review signal, not truth. No automatic translation or rewritten dialogue. Review sync at actual speech boundaries, especially after separation, source offset changes or editing.

For import into Premiere, Resolve, AE or another editor, use the actual target app's subtitle workflow when available. A valid SRT file alone does not prove import in every editor. Standard SRT has no reliable styling/positioning; use a different requested format if layout styling is essential.
