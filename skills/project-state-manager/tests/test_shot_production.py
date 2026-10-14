"""State-contract fixtures, not visual-QC or model-generation tests."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "manage-shot-production.py"


class ShotProductionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("project-intake.json", {"project_intake_packet": {
            "format_spec": {"master_ratio": "16:9", "delivery_ratios": ["9:16", "4:3"]}}})

    def write(self, name, value):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value), encoding="utf-8")
        return target

    def command(self, *args, fails=False):
        result = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), *args, "--project-root", str(self.root)],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode != 0, fails, result.stdout + result.stderr)
        return json.loads(result.stderr if fails else result.stdout)

    def upsert(self, packets, fails=False):
        return self.command("upsert", "--input", str(self.write("input.json", packets)), fails=fails)

    def shots(self):
        return {shot["shot_id"]: shot for shot in json.loads(
            (self.root / "production/shot-production-registry.json").read_text(encoding="utf-8"))["shots"]}

    def frame(self):
        # Only test path persistence/nonempty-file validation, never claim decoded-image QC.
        (self.root / "frame.png").write_bytes(b"state-contract-fixture")
        return "frame.png"

    def test_landscape_portrait_custom_and_partial_update(self):
        self.upsert([{"shot_id": "L", "status": "prompt_ready", "camera_id": "master"},
                     {"shot_id": "P", "ratio": "9:16"}, {"shot_id": "C", "ratio": "4:3"}])
        self.assertEqual([self.shots()[s]["ratio"] for s in ["L", "P", "C"]], ["16:9", "9:16", "4:3"])
        self.upsert({"shot_id": "L", "risk_level": "high"})
        self.assertEqual(self.shots()["L"]["status"], "prompt_ready")
        self.assertEqual(self.shots()["L"]["camera_id"], "master")

    def test_unresolved_ratio_never_defaults_portrait(self):
        self.write("project-intake.json", {"project_intake_packet": {"format_spec": {"master_ratio": ""}}})
        self.assertIn("missing_ratio", self.upsert({"shot_id": "A"}, fails=True)["error"])
        self.assertFalse((self.root / "production/shot-production-registry.json").exists())

    def test_wrong_ratio_is_atomic_rejection(self):
        self.upsert({"shot_id": "A"})
        before = self.shots()
        for value in ["0:9", "16/9", "1:1"]:
            self.upsert({"shot_id": "A", "ratio": value}, fails=True)
            self.assertEqual(self.shots(), before)

    def test_changed_project_format_stops_old_ratio_batch(self):
        self.upsert({"shot_id": "A", "status": "prompt_ready"})
        self.write("project-intake.json", {"project_intake_packet": {"format_spec": {"master_ratio": "9:16"}}})
        result = self.command("next-batch")
        self.assertFalse(result["valid"])
        self.assertEqual(result["count"], 0)

    def test_camera_reference_waits_for_frame_not_finished_clip(self):
        self.upsert([{"shot_id": "A", "status": "image_generated"},
                     {"shot_id": "B", "status": "prompt_ready", "camera_reference_shot_id": "A"},
                     {"shot_id": "C", "status": "prompt_ready", "dependencies": ["A"]}])
        self.assertEqual(self.command("next-batch")["count"], 0)
        self.command("transition", "--shot-id", "A", "--status", "image_approved",
                     "--artifact", "approved_first_frame=" + self.frame())
        self.assertEqual([s["shot_id"] for s in self.command("next-batch")["shots"]], ["B"])

    def test_edit_order_is_not_generation_dependency(self):
        self.upsert([{"shot_id": "A", "status": "blocked"},
                     {"shot_id": "B", "status": "prompt_ready", "previous_shot_id": "A"}])
        self.assertEqual([s["shot_id"] for s in self.command("next-batch")["shots"]], ["B"])

    def test_text_continuity_allows_prompt_work_without_generated_frames(self):
        self.upsert([{"shot_id": "A", "status": "continuity_locked"},
                     {"shot_id": "B", "status": "continuity_locked", "continuity_in": {"inherits_from": "A"}}])
        self.assertEqual(self.command("next-batch", "--from-status", "continuity_locked")["count"], 2)

    def test_unknown_and_combined_reference_cycles(self):
        self.upsert({"shot_id": "A", "camera_reference_shot_id": "absent"}, fails=True)
        self.upsert([{"shot_id": "A", "camera_reference_shot_id": "B"},
                     {"shot_id": "B", "continuity_in": {"inherits_from": "A"}}], fails=True)
        self.upsert({"shot_id": "A", "camera_reference_shot_id": "A"}, fails=True)

    def test_invalidation_transitive_preserves_siblings_and_artifacts(self):
        self.upsert([{"shot_id": "A", "status": "accepted", "camera_id": "v1"},
                     {"shot_id": "B", "status": "accepted", "camera_reference_shot_id": "A"},
                     {"shot_id": "C", "status": "accepted", "dependencies": ["B"],
                      "artifacts": {"video": "old.mp4"}},
                     {"shot_id": "D", "status": "accepted"}])
        result = self.upsert({"shot_id": "A", "camera_id": "v2"})
        self.assertEqual(result["invalidated"], ["A", "B", "C"])
        self.assertEqual(self.shots()["C"]["artifacts"]["video"], "old.mp4")
        self.assertEqual(self.shots()["D"]["status"], "accepted")
        self.command("transition", "--shot-id", "A", "--status", "accepted", "--resume", fails=True)
        self.upsert({"shot_id": "A", "status": "accepted"}, fails=True)
        self.command("transition", "--shot-id", "A", "--status", "prompt_ready", "--resume")

    def test_explicit_in_place_revision_invalidates_references(self):
        self.upsert([{"shot_id": "A"}, {"shot_id": "B", "camera_reference_shot_id": "A"}])
        self.assertEqual(self.command("invalidate", "--shot-id", "A", "--reason", "prompt text revised")["invalidated"], ["A", "B"])

    def test_replacing_approved_frame_marks_existing_children_stale(self):
        self.upsert([{"shot_id": "A", "status": "image_approved", "artifacts": {"approved_first_frame": "old.png"}},
                     {"shot_id": "B", "status": "accepted", "camera_reference_shot_id": "A"}])
        self.command("transition", "--shot-id", "A", "--status", "image_approved", "--artifact", "approved_first_frame=" + self.frame())
        self.assertEqual(self.shots()["A"]["status"], "image_approved")
        self.assertEqual(self.shots()["B"]["status"], "stale")

    def test_dashboard_reports_dependencies_and_is_read_only(self):
        self.upsert([{"shot_id": "A", "status": "image_generated", "camera_id": "master"},
                     {"shot_id": "B", "ratio": "9:16", "status": "prompt_ready", "camera_reference_shot_id": "A"}])
        registry_path = self.root / "production/shot-production-registry.json"
        before = registry_path.read_bytes()
        dashboard = SCRIPT.parents[2] / "production-manager/scripts/build_project_dashboard.py"
        result = subprocess.run([sys.executable, "-X", "utf8", str(dashboard), "--project-root", str(self.root), "--check-only"],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["shots"]["next_image_batch"], [])
        self.assertEqual(report["shots"]["items"][1]["ratio"], "9:16")
        self.assertEqual(registry_path.read_bytes(), before)

    def test_candidate_rejection_selection_and_stale_review(self):
        selection = {"context_revision": "v1 16:9", "candidates": [
            {"candidate_id": "A", "path": self.frame(), "qc_decision": "rejected", "evidence": "wrong prop"}],
            "selected_candidate_id": "A", "reason": "best", "stale": False}
        self.upsert({"shot_id": "A", "status": "image_generated", "frame_selection": selection}, fails=True)
        selection["candidates"][0]["qc_decision"] = "passed"
        self.upsert({"shot_id": "A", "status": "image_generated", "frame_selection": selection})
        self.command("transition", "--shot-id", "A", "--status", "image_approved", fails=True)
        self.command("transition", "--shot-id", "A", "--status", "image_approved", "--artifact", "approved_first_frame=frame.png")
        self.command("invalidate", "--shot-id", "A", "--reason", "reference revised")
        self.assertTrue(self.shots()["A"]["frame_selection"]["stale"])
        self.command("transition", "--shot-id", "A", "--status", "prompt_ready", "--resume")
        self.command("transition", "--shot-id", "A", "--status", "image_generated")
        self.command("transition", "--shot-id", "A", "--status", "image_approved", fails=True)

    def test_candidate_path_escape_and_missing_file(self):
        self.upsert({"shot_id": "A", "frame_selection": {"candidates": [
            {"candidate_id": "A", "path": "../outside.png"}]}}, fails=True)
        self.upsert({"shot_id": "A", "status": "image_approved", "artifacts": {"approved_first_frame": "missing.png"},
                     "frame_selection": {"candidates": [{"candidate_id": "A", "path": "missing.png",
                       "qc_decision": "passed", "evidence": "observed"}], "selected_candidate_id": "A", "reason": "matches"}}, fails=True)

    def test_legacy_registry_is_not_migrated(self):
        (self.root / "project-intake.json").unlink()
        self.upsert({"shot_id": "legacy", "status": "accepted"})
        result = self.command("audit")
        self.assertTrue(result["valid"])
        self.assertIn("legacy:legacy_ratio_unset", result["warnings"])


if __name__ == "__main__":
    unittest.main()
