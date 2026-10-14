import importlib.util
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "make_srt.py"
spec = importlib.util.spec_from_file_location("make_srt", SCRIPT)
srt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(srt)


class SubtitleTests(unittest.TestCase):
    def test_confirmed_style(self):
        self.assertEqual(srt.clean_body("你好，欢迎回来。"), "你好   欢迎回来")
        self.assertEqual(srt.clean_body("你好, 欢迎回来."), "你好   欢迎回来")

    def test_three_ascii_spaces(self):
        body = srt.clean_body("第一段，   第二段\n第三段。")
        self.assertEqual(body, "第一段   第二段   第三段")
        self.assertNotIn("\t", body)

    def test_digits_and_other_punctuation(self):
        self.assertEqual(srt.clean_body("0个人，10元。你确定？太好了！"), "0个人   10元   你确定   太好了")

    def test_numeric_meaning(self):
        self.assertEqual(srt.clean_body("共1,000元，重3.5千克。"), "共1000元   重3点5千克")

    def test_english_word_spaces(self):
        self.assertEqual(srt.clean_body("Hello world?! welcome back!"), "Hello world   welcome back")

    def test_srt_syntax_and_readback(self):
        value, _ = srt.render_srt([{"start": .5, "end": 2.8, "text": "你好？！欢迎回来!?"}])
        self.assertEqual(value, "1\n00:00:00,500 --> 00:00:02,800\n你好   欢迎回来\n")
        self.assertEqual(srt.parse_srt(value)[0]["start"], .5)

    def test_no_fabricated_empty_cue(self):
        value, _ = srt.render_srt([{"start": 0, "end": 1, "text": "，。？！?!"}])
        self.assertEqual(value, "")

    def test_reject_invalid_timings(self):
        for start, end in [(-1, 1), (2, 1), (1, 1), (float("nan"), 2), (0, float("inf"))]:
            with self.assertRaises(ValueError):
                srt.render_srt([{"start": start, "end": end, "text": "测试"}])
        with self.assertRaises(ValueError):
            srt.render_srt([{"start": 0, "end": 2, "text": "甲"}, {"start": 1, "end": 3, "text": "乙"}])

    def test_phrases_vs_cue_breaks(self):
        rows = srt.group_segments([{"words": [{"word": "今天", "start": 0, "end": .4},
            {"word": "很好", "start": .85, "end": 1.2}, {"word": "再见", "start": 2.5, "end": 3}]}])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["text"], "今天   很好")

    def test_no_word_timing_no_invented_splits(self):
        rows = srt.group_segments([{"start": 0, "end": 10, "text": "很长的句子"}], max_chars=2)
        _, warnings = srt.render_srt(rows, max_chars=2)
        self.assertEqual(len(rows), 1)
        self.assertTrue(warnings)

    def test_limit_prefers_existing_phrase_boundary(self):
        rows = srt.group_segments([{"words": [{"word": "人声、", "start": 0, "end": 1},
            {"word": "音", "start": 1, "end": 2}, {"word": "效", "start": 2, "end": 3}]}], max_seconds=2.5)
        self.assertEqual([r["text"] for r in rows], ["人声、", "音效"])
        self.assertEqual(rows[1]["start"], 1)

    def test_cli_preserves_input_and_uses_source_offset(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "raw.json"
            source.write_text(json.dumps({"source_audio_offset": .5, "segments": [{"start": 0, "end": 1, "text": "欢迎？回来！"}]}), encoding="utf-8")
            before = source.read_bytes()
            result = subprocess.run([sys.executable, str(SCRIPT), "format", "--input", str(source), "--output-dir", str(root / "out")], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(source.read_bytes(), before)
            result = srt.parse_srt((root / "out/subtitles.srt").read_text(encoding="utf-8"))
            self.assertEqual(result[0]["start"], .5)
            self.assertEqual(result[0]["text"], "欢迎   回来")


if __name__ == "__main__":
    unittest.main()
