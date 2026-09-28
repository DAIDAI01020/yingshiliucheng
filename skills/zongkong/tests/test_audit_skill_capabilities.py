import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_skill_capabilities.py"
SPEC = importlib.util.spec_from_file_location("capability_audit", SCRIPT)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class SkillTreeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skill-tree-audit-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "skills"
        self.root.mkdir()

    def skill(self, name="example", body="", declared=None):
        path = self.root / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\nname: {declared or name}\ndescription: A scoped skill.\n---\n{body}", encoding="utf-8")
        return path

    def result(self):
        return AUDIT.audit_skill_tree(self.root)

    def test_all_entrypoints_and_shared_resources_are_checked(self):
        self.skill("one", "[Shared](../two/reference%20notes.md#rules)")
        self.skill("two")
        (self.root / "two" / "reference notes.md").write_text("# Rules", encoding="utf-8")
        result = self.result()
        self.assertEqual(result["skill_count"], 2)
        self.assertEqual(result["resource_links_checked"], 1)
        self.assertEqual(result["failures"], [])

    def test_missing_resource_is_reported(self):
        self.skill(body="[Required](references/missing.md)")
        self.assertIn("missing linked resource", self.result()["failures"][0])

    def test_directory_identity_mismatch_is_reported(self):
        self.skill(declared="another-skill")
        self.assertIn("does not match directory", self.result()["failures"][0])

    def test_flat_metadata_is_rejected_and_mapping_is_accepted(self):
        self.skill()
        metadata = self.root / "example" / "agents" / "openai.yaml"
        metadata.parent.mkdir()
        metadata.write_text('display_name: "Example"\n', encoding="utf-8")
        self.assertTrue(self.result()["failures"])
        metadata.write_text('interface:\n  display_name: "Example"\n  short_description: "Scoped helper"\n  default_prompt: "Use $example."\npolicy:\n  allow_implicit_invocation: false\n', encoding="utf-8")
        self.assertEqual(self.result()["failures"], [])

    def test_documented_examples_and_external_links_are_not_local_dependencies(self):
        self.skill(body='```markdown\n[Example](fictional/file.md)\n```\n[Web](https://example.com)\n[Section](#intro)\n[Absolute](/absolute/example.png)')
        self.assertEqual(self.result()["resource_links_checked"], 0)
        self.assertEqual(self.result()["failures"], [])

    def test_optional_ui_fields_are_not_required(self):
        self.skill()
        metadata = self.root / "example" / "agents" / "openai.yaml"
        metadata.parent.mkdir()
        metadata.write_text('interface:\n  display_name: "Example"\n', encoding="utf-8")
        self.assertEqual(self.result()["failures"], [])

    def test_cross_root_dependency_is_reported_even_if_file_exists(self):
        (self.root.parent / "outside.md").write_text("outside", encoding="utf-8")
        self.skill(body="[Unsafe dependency](../../outside.md)")
        self.assertIn("escapes skills root", self.result()["failures"][0])

    def test_empty_tree_is_not_a_successful_audit(self):
        self.assertTrue(self.result()["failures"])


if __name__ == "__main__":
    unittest.main()
