import argparse
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "blender_task.py"
spec = importlib.util.spec_from_file_location("blender_task", SCRIPT)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="blender-runner-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.scene = self.root / "input.blend"
        self.scene.write_bytes(b"test scene")
        self.texture = self.root / "texture.png"
        self.texture.write_bytes(b"texture fixture")
        self.args = runner.parser().parse_args(["render", "--project-root", str(self.root), "--blend", str(self.scene),
            "--frames", "1:3", "--output-dir", str(self.root / "renders")])
        self.environment = {"available": True, "executable": "fixture", "version": "Blender fixture"}
        self.rendered = []

    def fake_invoke(self, executable, payload, *args, **kwargs):
        if payload["action"] == "inspect":
            return {"ok": True, "missing_dependencies": [], "file_output_nodes": [],
                    "unresolved_dependencies": [], "dependencies": [str(self.texture)]}
        self.rendered.append(payload["frame"])
        target = Path(payload["output"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"fixture media")
        return {"ok": True, "decoded": True, "size": [32, 32]}

    def test_frames(self):
        self.assertEqual(runner.frames("1:3,2,8"), [1, 2, 3, 8])
        for value in ("3:1", "-1", "1:20000", "x"):
            with self.assertRaises(ValueError):
                runner.frames(value)

    def test_output_containment(self):
        with self.assertRaises(ValueError):
            runner.contained(self.root, self.root / ".." / "escape")
        with self.assertRaises(ValueError):
            runner.contained(self.root, self.root)

    def test_missing_executable_is_not_ready(self):
        with patch.object(runner, "discover", return_value=None):
            self.assertFalse(runner.doctor()["available"])

    def test_refuse_source_overwrite_before_execution(self):
        args = argparse.Namespace(project_root=str(self.root), output=str(self.scene), script="not-called")
        with patch.object(runner, "invoke") as execute:
            with self.assertRaises(ValueError):
                runner.build(args, self.environment)
            execute.assert_not_called()
        self.assertEqual(self.scene.read_bytes(), b"test scene")

    def test_resume_reuses_only_verified_frames(self):
        with patch.object(runner, "invoke", side_effect=self.fake_invoke):
            self.assertEqual(runner.render(self.args, self.environment)["status"], "rendered")
            self.args.resume = True
            runner.render(self.args, self.environment)
            self.assertEqual(self.rendered, [1, 2, 3])
            manifest = runner.read_json(Path(self.args.output_dir) / "render-manifest.json")
            Path(manifest["outputs"]["2"]["file"]).write_bytes(b"corrupt")
            self.assertEqual(runner.status(self.args.output_dir)["missing_or_invalid_frames"], [2])
            runner.render(self.args, self.environment)
            self.assertEqual(self.rendered, [1, 2, 3, 2])

    def test_changed_texture_requires_new_run(self):
        with patch.object(runner, "invoke", side_effect=self.fake_invoke):
            runner.render(self.args, self.environment)
            self.texture.write_bytes(b"changed texture")
            self.args.resume = True
            with self.assertRaisesRegex(ValueError, "changed"):
                runner.render(self.args, self.environment)

    def test_interruption_preserves_completed_frames(self):
        def fail_second(executable, payload, *args, **kwargs):
            if payload.get("frame") == 2:
                raise RuntimeError("render interrupted")
            return self.fake_invoke(executable, payload, *args, **kwargs)
        with patch.object(runner, "invoke", side_effect=fail_second):
            with self.assertRaises(RuntimeError):
                runner.render(self.args, self.environment)
        self.assertEqual(runner.status(self.args.output_dir)["verified_frames"], [1])
        log = runner.read_json(Path(self.args.output_dir) / "generation-log.json")
        self.assertEqual(log["status"], "incomplete")
        self.assertEqual(log["shots"], [])
        self.args.resume = True
        with patch.object(runner, "invoke", side_effect=self.fake_invoke):
            runner.render(self.args, self.environment)
        self.assertEqual(self.rendered, [1, 2, 3])

    def test_missing_file_cannot_be_complete(self):
        with patch.object(runner, "invoke", side_effect=self.fake_invoke):
            runner.render(self.args, self.environment)
        manifest = runner.read_json(Path(self.args.output_dir) / "render-manifest.json")
        Path(manifest["outputs"]["1"]["file"]).unlink()
        self.assertEqual(runner.status(self.args.output_dir)["status"], "incomplete")

    def test_lock_refuses_concurrent_writer(self):
        with runner.run_lock(self.root):
            with self.assertRaisesRegex(ValueError, "lock"):
                with runner.run_lock(self.root):
                    self.fail("must not acquire twice")

    def test_dependency_directory_content_changes_identity(self):
        cache = self.root / "cache"
        cache.mkdir()
        (cache / "001.bin").write_bytes(b"cache1")
        before = runner.fingerprint(self.scene, [cache], {}, "fixture")
        (cache / "002.bin").write_bytes(b"cache2")
        self.assertNotEqual(before, runner.fingerprint(self.scene, [cache], {}, "fixture"))

    def test_changes_during_render_invalidate_entire_run(self):
        def changing_input(executable, payload, *args, **kwargs):
            if payload.get("frame") == 2:
                self.texture.write_bytes(b"edited during render")
            return self.fake_invoke(executable, payload, *args, **kwargs)
        with patch.object(runner, "invoke", side_effect=changing_input):
            with self.assertRaisesRegex(RuntimeError, "Inputs changed"):
                runner.render(self.args, self.environment)
        self.texture.write_bytes(b"texture fixture")
        self.args.resume = True
        with patch.object(runner, "invoke", side_effect=self.fake_invoke):
            with self.assertRaisesRegex(ValueError, "changed"):
                runner.render(self.args, self.environment)

    def test_render_without_media_is_never_success(self):
        def missing_output(executable, payload, *args, **kwargs):
            if payload["action"] == "inspect":
                return self.fake_invoke(executable, payload, *args, **kwargs)
            return {"ok": True, "decoded": True}
        with patch.object(runner, "invoke", side_effect=missing_output):
            with self.assertRaisesRegex(RuntimeError, "Missing"):
                runner.render(self.args, self.environment)
        self.assertEqual(runner.status(self.args.output_dir)["verified_frames"], [])

    def test_external_output_nodes_block_before_run_creation(self):
        def unsafe_compositor(executable, payload, *args, **kwargs):
            report = self.fake_invoke(executable, payload, *args, **kwargs)
            report["file_output_nodes"] = ["External output"]
            return report
        with patch.object(runner, "invoke", side_effect=unsafe_compositor):
            with self.assertRaisesRegex(ValueError, "Output nodes"):
                runner.render(self.args, self.environment)
        self.assertFalse(Path(self.args.output_dir).exists())


if __name__ == "__main__":
    unittest.main()
