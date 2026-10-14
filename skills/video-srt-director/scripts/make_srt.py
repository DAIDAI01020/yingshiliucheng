"""Speech-to-SRT and body-only subtitle cleanup. Host Python + optional faster-whisper."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys

TIME = r"(\d{2,}):([0-5]\d):([0-5]\d),(\d{3})"
TIMELINE = re.compile(r"^" + TIME + r"\s+-->\s+" + TIME + r"$")


def clean_body(text):
    text = re.sub(r"(?<!\d)\d{1,3}(?:,\d{3})+(?!\d)", lambda m: m[0].replace(",", ""), str(text))
    text = re.sub(r"(?<=\d)\.(?=\d)", "点", text)
    text = re.sub(r"[\r\n\t]+", "   ", text)
    text = re.sub(r"[ \t]*[,，.。．？?！!]+[ \t]*", "   ", text)
    text = re.sub(r" {2,}", "   ", text)
    return text.strip()


def milliseconds(value):
    value = float(value)
    if not math.isfinite(value) or value < 0:
        raise ValueError("Subtitle times must be finite and nonnegative.")
    return int(math.floor(value * 1000 + 0.5))


def stamp(ms):
    h, rest = divmod(ms, 3600000)
    m, rest = divmod(rest, 60000)
    s, fraction = divmod(rest, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{fraction:03d}"


def parse_srt(text):
    rows = []
    for block in re.split(r"\n[ \t]*\n", text.lstrip("\ufeff").replace("\r\n", "\n").strip()):
        if not block.strip():
            continue
        lines = block.splitlines()
        if len(lines) < 3 or not lines[0].isdigit():
            raise ValueError("Malformed SRT cue.")
        match = TIMELINE.fullmatch(lines[1])
        if not match:
            raise ValueError("Malformed SRT timecode; expected HH:MM:SS,mmm.")
        nums = list(map(int, match.groups()))
        def seconds(items):
            return items[0] * 3600 + items[1] * 60 + items[2] + items[3] / 1000
        rows.append({"start": seconds(nums[:4]), "end": seconds(nums[4:]), "text": "\n".join(lines[2:])})
    return rows


def group_segments(segments, max_chars=32, max_seconds=6, phrase_gap=.4, cue_gap=.9):
    result = []
    for segment in segments:
        words = segment.get("words")
        if not words:
            result.append({"start": segment["start"], "end": segment["end"], "text": segment["text"]})
            continue
        buffer = []
        last_end = None
        def cue(items):
            text = ""
            previous = None
            for item in items:
                if previous is not None and float(item["start"]) - float(previous["end"]) >= phrase_gap:
                    text += "   "
                text += item.get("word", item.get("text", ""))
                previous = item
            return {"start": float(items[0]["start"]), "end": float(items[-1]["end"]), "text": text}
        def too_long(items):
            candidate = cue(items)
            return (candidate["end"] - candidate["start"] > max_seconds
                    or len(clean_body(candidate["text"]).replace(" ", "")) > max_chars)
        for word in words:
            start, end = float(word["start"]), float(word["end"])
            if milliseconds(end) <= milliseconds(start):
                raise ValueError("Invalid word timing; review alignment rather than inventing it.")
            if last_end is not None and start < last_end - .001:
                raise ValueError("Overlapping word timing requires alignment review.")
            token = word.get("word", word.get("text", ""))
            if not token.strip():
                last_end = end
                continue
            if buffer and start - float(buffer[-1]["end"]) >= cue_gap:
                result.append(cue(buffer))
                buffer = []
            while buffer and too_long(buffer + [word]):
                # Prefer observed phrase boundaries over cutting a Chinese ASR character token.
                boundaries = [i + 1 for i, item in enumerate(buffer)
                              if re.search(r"[,，。.!！？?;；、]$", item.get("word", item.get("text", "")).strip())]
                split = boundaries[-1] if boundaries else len(buffer)
                result.append(cue(buffer[:split]))
                buffer = buffer[split:]
            buffer.append(word)
            last_end = end
        if buffer:
            result.append(cue(buffer))
    return result


def render_srt(rows, offset=0, max_chars=32, max_seconds=6):
    cues, warnings = [], []
    previous_end = 0
    for row in rows:
        start, end = milliseconds(float(row["start"]) + offset), milliseconds(float(row["end"]) + offset)
        if end <= start or start < previous_end:
            raise ValueError("Subtitle times overlap or have nonpositive duration; review source alignment.")
        previous_end = end
        body = clean_body(row["text"])
        if not body:
            continue
        number = len(cues) + 1
        if len(body.replace(" ", "")) > max_chars or (end - start) / 1000 > max_seconds:
            warnings.append({"cue": number, "reason": "long_cue_needs_editorial_review"})
        cues.append(f"{number}\n{stamp(start)} --> {stamp(end)}\n{body}\n")
    return "\n".join(cues), warnings


def probe(source, stream, ffprobe):
    completed = subprocess.run([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(source)],
                               check=True, capture_output=True, text=True, encoding="utf-8")
    data = json.loads(completed.stdout)
    audio = [s for s in data["streams"] if s["codec_type"] == "audio"]
    if stream < 0 or stream >= len(audio):
        raise ValueError("Selected audio stream does not exist.")
    origin = float(data.get("format", {}).get("start_time", 0))
    selected = audio[stream]
    offset = float(selected.get("start_time", origin)) - origin
    return selected, max(0, offset)


def transcribe(args, directory):
    from faster_whisper import WhisperModel
    selected, offset = probe(args.input, args.audio_stream, args.ffprobe)
    wav = directory / "asr-input.wav"
    subprocess.run([args.ffmpeg, "-v", "error", "-nostdin", "-n", "-i", str(args.input), "-map", f"0:a:{args.audio_stream}",
                    "-vn", "-af", "asetpts=PTS-STARTPTS,aresample=async=1:first_pts=0", "-ac", "1", "-ar", "16000",
                    "-c:a", "pcm_s16le", str(wav)], check=True, capture_output=True)
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type,
                         local_files_only=not args.allow_model_download)
    segments, info = model.transcribe(str(wav), task="transcribe", language=args.language, word_timestamps=True,
                                      vad_filter=True, condition_on_previous_text=False)
    rows = [{"start": s.start, "end": s.end, "text": s.text,
             "avg_logprob": s.avg_logprob, "no_speech_prob": s.no_speech_prob,
             "words": [{"start": w.start, "end": w.end, "word": w.word, "probability": w.probability}
                       for w in (s.words or [])]} for s in segments]
    raw = {"segments": rows, "language": info.language, "source_audio_offset": offset,
           "audio_stream_index": selected["index"], "model": args.model, "review_status": "not_listened"}
    (directory / "transcript.raw.json").write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    return rows, offset


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["doctor", "format", "transcribe"])
    p.add_argument("--input", type=Path)
    p.add_argument("--output-dir", type=Path)
    p.add_argument("--model", default="small")
    p.add_argument("--language", default=None)
    p.add_argument("--device", default="cpu", choices=["cpu", "cuda", "auto"])
    p.add_argument("--compute-type", default="int8")
    p.add_argument("--allow-model-download", action="store_true")
    p.add_argument("--audio-stream", type=int, default=0)
    p.add_argument("--offset", type=float, default=0)
    p.add_argument("--max-chars", type=int, default=32)
    p.add_argument("--max-seconds", type=float, default=6)
    p.add_argument("--phrase-gap", type=float, default=.4)
    p.add_argument("--cue-gap", type=float, default=.9)
    p.add_argument("--ffmpeg", default="ffmpeg")
    p.add_argument("--ffprobe", default="ffprobe")
    return p


def main():
    args = parser().parse_args()
    if args.command == "doctor":
        return {"ffmpeg": shutil.which(args.ffmpeg), "ffprobe": shutil.which(args.ffprobe),
                "faster_whisper_installed": importlib.util.find_spec("faster_whisper") is not None,
                "model_load_verified": False, "formatting_ready": True}
    if not args.input or not args.input.is_file() or not args.output_dir:
        raise ValueError("Existing --input and a new --output-dir are required.")
    if not all(math.isfinite(v) for v in [args.offset, args.max_seconds, args.phrase_gap, args.cue_gap]):
        raise ValueError("Timing options must be finite.")
    if args.max_chars < 1 or args.max_seconds <= 0 or not 0 <= args.phrase_gap < args.cue_gap:
        raise ValueError("Invalid subtitle length/pause settings.")
    directory = args.output_dir.resolve()
    directory.mkdir(parents=True, exist_ok=False)
    offset = args.offset
    if args.command == "transcribe":
        segments, source_offset = transcribe(args, directory)
        offset += source_offset
        rows = group_segments(segments, args.max_chars, args.max_seconds, args.phrase_gap, args.cue_gap)
    else:
        text = args.input.read_text(encoding="utf-8-sig")
        if args.input.suffix.lower() == ".srt":
            rows = parse_srt(text)
        else:
            data = json.loads(text)
            segments = data["segments"] if isinstance(data, dict) else data
            # Raw ASR JSON carries source placement; ordinary timed JSON is already relative to its intended timeline.
            if isinstance(data, dict):
                offset += float(data.get("source_audio_offset", 0))
            rows = group_segments(segments, args.max_chars, args.max_seconds, args.phrase_gap, args.cue_gap)
    output, warnings = render_srt(rows, offset, args.max_chars, args.max_seconds)
    target = directory / "subtitles.srt"
    target.write_text(output, encoding="utf-8", newline="\n")
    saved = parse_srt(target.read_text(encoding="utf-8"))
    if len(saved) != (output.count(" --> ")):
        raise RuntimeError("SRT readback failed.")
    report = {"srt": str(target), "source": str(args.input.resolve()), "cue_count": len(saved),
              "technical_status": "valid" if saved else "no_speech_detected", "editorial_status": "needs_listening_review",
              "offset_seconds": offset, "phrase_spaces": 3, "warnings": warnings,
              "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
    (directory / "subtitle-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    try:
        print(json.dumps(main(), ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, RuntimeError, ImportError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
