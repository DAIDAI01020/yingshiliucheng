from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "manage_thread_registry.py"
SPEC = importlib.util.spec_from_file_location("manage_thread_registry", SCRIPT_PATH)
assert SPEC and SPEC.loader
registry_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(registry_module)


class ThreadRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.manifest_path = self.root / "project-manifest.json"
        self.asset_path = self.root / "asset-index.json"
        self.original_manifest = {
            "project": "测试总项目",
            "project_slug": "test_project",
            "folder_contract": ["01_brief", "11_delivery"],
            "custom_legacy_field": {"keep": True},
        }
        self.manifest_path.write_text(json.dumps(self.original_manifest, ensure_ascii=False), encoding="utf-8")
        self.asset_path.write_text('{"sentinel":"unchanged"}\n', encoding="utf-8")
        self.asset_before = self.asset_path.read_bytes()
        registry_module.init_registry(str(self.root), str(self.root), str(self.root), "测试总项目")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def make_plan(self, count: int = 12, dependency: bool = False) -> Path:
        tasks = []
        for index in range(1, count + 1):
            task_id = f"P{index:02d}"
            tasks.append(
                {
                    "task_id": task_id,
                    "title": f"部分{index}",
                    "goal": f"完成部分{index}",
                    "scope_boundary": "只处理本部分",
                    "source_files": [],
                    "inherited_locks": ["style_lock"],
                    "must_not_change": ["global_context"],
                    "dependencies": ["P01"] if dependency and index == 2 else [],
                    "owning_skill": "script-writer",
                    "deliverables": [f"部分{index}稿件"],
                    "output_path_rule": "accepted outputs are promoted by the hub",
                    "status": "queued",
                }
            )
        plan = {
            "schema_version": 1,
            "project_id": str(self.root),
            "project_path": str(self.root),
            "project_root": str(self.root),
            "container_mode": "shared_project_shared_root",
            "split_reason": "独立修改",
            "global_prerequisites": [],
            "parallel_limit": 4,
            "confirmed": True,
            "tasks": tasks,
        }
        path = self.root / "confirmed-plan.json"
        path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def load_registry(self) -> dict:
        return json.loads((self.root / "00_project_control" / "thread-registry.json").read_text(encoding="utf-8"))

    def test_init_is_non_destructive_and_adds_pointer(self) -> None:
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        for key, value in self.original_manifest.items():
            self.assertEqual(manifest[key], value)
        self.assertEqual(manifest["current"]["thread_registry"], "00_project_control/thread-registry.json")
        self.assertEqual(self.asset_path.read_bytes(), self.asset_before)
        self.assertTrue((self.root / "00_project_control" / "project-context.md").is_file())
        again = registry_module.init_registry(str(self.root), str(self.root), str(self.root), "测试总项目")
        self.assertEqual(again["action"], "already_initialized")

    def test_twelve_tasks_select_only_four_and_do_not_create_threads(self) -> None:
        result = registry_module.register_plan(str(self.root), str(self.make_plan()))
        self.assertEqual(len(result["created"]), 12)
        batch = registry_module.next_batch(str(self.root))
        self.assertEqual([item["task_id"] for item in batch["selected"]], ["P01", "P02", "P03", "P04"])
        self.assertTrue(all(task["thread_id"] is None for task in self.load_registry()["tasks"]))
        for index in range(1, 13):
            self.assertTrue((self.root / "00_project_control" / "thread-tasks" / f"P{index:02d}" / "working").is_dir())

    def test_active_limit_and_duplicate_thread_guard(self) -> None:
        registry_module.register_plan(str(self.root), str(self.make_plan(5)))
        for index in range(1, 5):
            registry_module.bind_thread(str(self.root), f"P{index:02d}", f"thread-{index}")
        self.assertEqual(registry_module.next_batch(str(self.root))["selected"], [])
        with self.assertRaises(registry_module.RegistryError):
            registry_module.bind_thread(str(self.root), "P05", "thread-5")
        with self.assertRaises(registry_module.RegistryError):
            registry_module.bind_thread(str(self.root), "P05", "thread-1")

    def test_hub_binding_is_unique_and_persisted(self) -> None:
        registry_module.register_plan(str(self.root), str(self.make_plan(1)))
        result = registry_module.bind_hub(str(self.root), "hub-thread", "[测试总项目][总控]", pinned=True)
        self.assertEqual(result["hub"]["status"], "active")
        self.assertTrue(result["hub"]["pinned"])
        self.assertEqual(registry_module.summary(str(self.root))["hub"]["thread_id"], "hub-thread")
        again = registry_module.bind_hub(str(self.root), "hub-thread", pinned=True)
        self.assertEqual(again["action"], "hub_already_bound")
        registry_module.bind_thread(str(self.root), "P01", "child-thread")
        with self.assertRaises(registry_module.RegistryError):
            registry_module.bind_hub(str(self.root), "child-thread", pinned=True)

    def test_dependencies_wait_until_acceptance(self) -> None:
        registry_module.register_plan(str(self.root), str(self.make_plan(2, dependency=True)))
        self.assertEqual([item["task_id"] for item in registry_module.next_batch(str(self.root))["selected"]], ["P01"])
        registry_module.bind_thread(str(self.root), "P01", "thread-1")
        registry_module.update_status(str(self.root), "P01", "ready_for_review")
        registry_module.update_status(str(self.root), "P01", "accepted")
        self.assertEqual([item["task_id"] for item in registry_module.next_batch(str(self.root))["selected"]], ["P02"])

    def test_register_is_idempotent_but_rejects_changed_task(self) -> None:
        plan_path = self.make_plan(2)
        registry_module.register_plan(str(self.root), str(plan_path))
        again = registry_module.register_plan(str(self.root), str(plan_path))
        self.assertEqual(again["unchanged"], ["P01", "P02"])
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        plan["tasks"][0]["goal"] = "不同目标"
        plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(registry_module.RegistryError):
            registry_module.register_plan(str(self.root), str(plan_path))

    def test_project_and_source_path_mismatch_are_rejected(self) -> None:
        with self.assertRaises(registry_module.RegistryError):
            registry_module.init_registry(str(self.root), "H:\\another", str(self.root), "bad")
        plan_path = self.make_plan(1)
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        plan["tasks"][0]["source_files"] = [str(self.root.parent / "outside.txt")]
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        with self.assertRaises(registry_module.RegistryError):
            registry_module.register_plan(str(self.root), str(plan_path))

    def test_handoff_validation_and_sync(self) -> None:
        registry_module.register_plan(str(self.root), str(self.make_plan(1)))
        registry_module.bind_thread(str(self.root), "P01", "thread-1")
        with self.assertRaises(registry_module.RegistryError):
            registry_module.sync_handoff(str(self.root), "P01")
        handoff_path = self.root / "00_project_control" / "thread-tasks" / "P01" / "handoff.json"
        handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
        handoff.update(
            {
                "thread_id": "thread-1",
                "status": "ready_for_review",
                "summary": "已完成",
                "deliverables": ["00_project_control/thread-tasks/P01/working/result.md"],
            }
        )
        handoff_path.write_text(json.dumps(handoff, ensure_ascii=False), encoding="utf-8")
        result = registry_module.sync_handoff(str(self.root), "P01")
        self.assertEqual(result["task"]["status"], "ready_for_review")
        handoff["deliverables"] = [str(self.root.parent / "outside.md")]
        handoff_path.write_text(json.dumps(handoff), encoding="utf-8")
        with self.assertRaises(registry_module.RegistryError):
            registry_module.sync_handoff(str(self.root), "P01")

    def test_context_change_marks_only_created_threads_stale(self) -> None:
        registry_module.register_plan(str(self.root), str(self.make_plan(2)))
        registry_module.bind_thread(str(self.root), "P01", "thread-1")
        result = registry_module.mark_stale(str(self.root), ["P01", "P02"], 2, "style_lock changed")
        self.assertEqual(result["stale"], ["P01"])
        self.assertEqual(result["queued_refreshed"], ["P02"])
        tasks = {task["task_id"]: task for task in self.load_registry()["tasks"]}
        self.assertEqual(tasks["P01"]["status"], "stale")
        self.assertEqual(tasks["P02"]["status"], "queued")
        packet = json.loads((self.root / tasks["P02"]["task_packet_path"]).read_text(encoding="utf-8"))
        self.assertEqual(packet["global_context_version"], 2)

    def test_validate_complete_registry(self) -> None:
        registry_module.register_plan(str(self.root), str(self.make_plan(2)))
        result = registry_module.validate_registry(str(self.root))
        self.assertTrue(result["valid"])
        self.assertEqual(result["task_count"], 2)


if __name__ == "__main__":
    unittest.main()
