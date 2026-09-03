import shutil
import unittest
from pathlib import Path
from uuid import uuid4

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import compile_skill
import collect_repository_evidence


class CompileSkillTests(unittest.TestCase):
    def test_every_deterministic_check_has_a_collector_fact(self):
        root = Path(__file__).resolve().parents[1]
        criteria = compile_skill.load_criteria(root / "criteria")
        expected = {
            (criterion["id"], check["id"])
            for criterion in criteria
            for check in criterion["checks"]
            if check["mode"] == "deterministic"
        }
        actual = {
            (fact["criterion_id"], fact["check_id"])
            for fact in collect_repository_evidence.collect_facts(root)["facts"]
        }

        self.assertEqual(expected, actual)

    def test_current_groups_render_in_canonical_order_with_titles(self):
        root = Path(__file__).resolve().parents[1]
        rendered = compile_skill.render_criteria(compile_skill.load_criteria(root / "criteria"))

        structure = rendered.index("### Structure & orientation")
        licensing = rendered.index("### Licensing & citation")
        environment = rendered.index("### Environment & dependencies")
        hygiene = rendered.index("### Repository hygiene")

        self.assertLess(structure, licensing)
        self.assertLess(licensing, environment)
        self.assertLess(environment, hygiene)
        self.assertNotIn("### structure", rendered)

    def test_compiled_distribution_includes_evidence_collector(self):
        root = Path(__file__).resolve().parents[1]
        temporary = Path(__file__).resolve().parent / f"runtime-{uuid4().hex}"
        temporary.mkdir()
        try:
            out = temporary / "repo-reviewer" / "SKILL.md"
            old_argv = sys.argv
            try:
                sys.argv = ["compile_skill.py", "--out", str(out), "--version", "test"]
                self.assertEqual(compile_skill.main(), 0)
            finally:
                sys.argv = old_argv

            self.assertTrue(out.is_file())
            self.assertTrue(
                (out.parent / "scripts" / "collect_repository_evidence.py").is_file()
            )
            self.assertTrue((out.parent / "README.md").is_file())
            self.assertIn("### Structure & orientation", out.read_text(encoding="utf-8"))
            distribution_readme = (out.parent / "README.md").read_text(encoding="utf-8")
            self.assertIn("criteria and", distribution_readme)
            self.assertNotIn("{{CRITERIA_COUNT}}", distribution_readme)
        finally:
            shutil.rmtree(temporary, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
