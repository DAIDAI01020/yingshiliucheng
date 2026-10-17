import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import sys
import unittest
from unittest.mock import patch
import wave

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "separate_audio.py"
spec = importlib.util.spec_from_file_location("separate_audio", SCRIPT)
audio = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audio)


class SeparationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="stem-test-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        environment = {k: v for k, v in os.environ.items() if not k.startswith("MSST_") and k != "AUDIO_STEM_BACKEND_PROFILE"}
        environment["CODEX_HOME"] = str(self.root)
        self.environment = patch.dict(os.environ, environment, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def profile(self):
        backend = self.root / "backend"
        backend.mkdir()
        (backend / "inference.py").write_text("# fixture", encoding="utf-8")
        checkpoint = self.root / "model.ckpt"
        checkpoint.write_bytes(b"local fixture")
        config = self.config(["speech", "music", "sfx"])
        data = {"version": 1, "backend_root": str(backend), "backend_python": sys.executable,
                "config": str(config), "checkpoint": str(checkpoint), "model_type": "bandit",
                "checkpoint_sha256": audio.digest(checkpoint)}
        profile = self.root / "tools/audio-separation/backend.json"
        profile.parent.mkdir(parents=True)
        profile.write_text(json.dumps(data), encoding="utf-8")
        return profile, data

    def test_persistent_profile_is_reused_without_network_or_process(self):
        profile, data = self.profile()
        for _ in range(2):
            args = audio.parser().parse_args(["doctor"])
            with patch.object(audio.subprocess, "run", side_effect=AssertionError("No setup or download allowed")):
                result = audio.doctor(args)
            self.assertEqual(args.checkpoint, data["checkpoint"])
            self.assertEqual(args.model_type, "bandit")
            self.assertEqual(result["backend_profile"], str(profile))
            self.assertFalse(result["downloads_performed"])

    def test_explicit_and_environment_paths_override_profile(self):
        _, data = self.profile()
        os.environ["MSST_CONFIG"] = str(self.config(["speech", "music", "effects"]))
        os.environ["MSST_CHECKPOINT"] = str(self.root / "environment.ckpt")
        explicit = self.root / "explicit.ckpt"
        args = audio.parser().parse_args(["doctor", "--checkpoint", str(explicit), "--model-type", "bandit_v2"])
        audio.resolve_backend(args)
        self.assertEqual(args.checkpoint, str(explicit))
        self.assertEqual(args.config, os.environ["MSST_CONFIG"])
        self.assertEqual(args.backend_root, data["backend_root"])
        self.assertEqual(args.model_type, "bandit_v2")

    def test_corrupt_cached_model_fails_without_repair(self):
        _, data = self.profile()
        checkpoint = Path(data["checkpoint"])
        checkpoint.write_bytes(b"partial or changed")
        with self.assertRaisesRegex(ValueError, "hash differs"):
            audio.doctor(audio.parser().parse_args(["doctor"]))
        self.assertEqual(checkpoint.read_bytes(), b"partial or changed")

    def test_explicit_missing_profile_does_not_fall_back(self):
        self.profile()
        with self.assertRaisesRegex(ValueError, "does not exist"):
            audio.doctor(audio.parser().parse_args(["doctor", "--backend-profile", str(self.root / "wrong.json")]))

    def config(self, labels):
        file = self.root / "model.yaml"
        file.write_text("audio:\n  sample_rate: 48000\ntraining:\n  instruments: " + repr(labels) + "\n", encoding="utf-8")
        return file

    def wav(self, name, frames=4800, channels=2):
        file = self.root / name
        with wave.open(str(file), "wb") as output:
            output.setnchannels(channels)
            output.setsampwidth(2)
            output.setframerate(48000)
            output.writeframes(b"\0\0" * frames * channels)
        return file

    def test_reject_music_instrument_models(self):
        for labels in [["vocals", "instrumental"], ["vocals", "drums", "bass", "other"], ["speech", "music"]]:
            with self.assertRaises(ValueError):
                audio.model_config(self.config(labels))

    def test_cinematic_labels(self):
        self.assertEqual(audio.model_config(self.config(["speech", "music", "sfx"]))[1], 48000)
        self.assertEqual(audio.model_config(self.config(["speech", "music", "effects"]))[0][-1], "effects")

    def test_missing_backend_not_ready(self):
        args = audio.parser().parse_args(["doctor", "--backend-root", str(self.root / "missing")])
        self.assertFalse(audio.doctor(args)["configured"])

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
    def test_real_decode_and_three_track_duration(self):
        source = self.wav("mix.wav")
        stems = {role: self.wav(role + ".wav") for role in ["speech", "music", "sfx"]}
        result = audio.verify(source, stems)
        self.assertEqual(result["technical_status"], "verified")
        self.assertEqual(result["listening_status"], "not_reviewed")
        stems["sfx"] = self.wav("short.wav", frames=2400)
        with self.assertRaisesRegex(ValueError, "duration"):
            audio.verify(source, stems)

    def test_missing_and_reused_stems_rejected(self):
        source = self.wav("mix.wav")
        with self.assertRaises(ValueError):
            audio.verify(source, {"speech": source, "music": source, "sfx": source})
        with self.assertRaises(ValueError):
            audio.verify(source, {"speech": source})

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
    def test_adapter_contract_with_explicit_mock_backend(self):
        # This tests process/file contracts only, never ML separation quality.
        backend = self.root / "mock_backend"
        backend.mkdir()
        (backend / "inference.py").write_text("""import argparse,pathlib,shutil
p=argparse.ArgumentParser()
p.add_argument('--input_folder'); p.add_argument('--store_dir')
a,_=p.parse_known_args()
out=pathlib.Path(a.store_dir); out.mkdir()
for name in ['speech','music','sfx']:
 shutil.copy2(pathlib.Path(a.input_folder)/'mix.wav',out/(name+'.wav'))
""", encoding="utf-8")
        checkpoint = self.root / "mock.checkpoint"
        checkpoint.write_bytes(b"fixture only")
        source = self.wav("source.wav")
        args = audio.parser().parse_args(["separate", "--input", str(source), "--output-dir", str(self.root / "run"),
            "--backend-root", str(backend), "--backend-python", sys.executable, "--config", str(self.config(["speech", "music", "sfx"])),
            "--checkpoint", str(checkpoint)])
        before = source.read_bytes()
        report = audio.separate(args)
        self.assertEqual(report["status"], "separated")
        self.assertEqual(report["listening_status"], "not_reviewed")
        self.assertEqual(source.read_bytes(), before)
        self.assertTrue(all(Path(report["stems"][name]["file"]).is_file() for name in ['speech','music','sfx']))
        with self.assertRaisesRegex(ValueError, "new output directory"):
            audio.separate(args)


if __name__ == "__main__":
    unittest.main()
