import json
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import collect_repository_evidence


class CollectRepositoryEvidenceTests(unittest.TestCase):
    def make_repo(self):
        root = Path(__file__).resolve().parent / f"runtime-{uuid4().hex}"
        root.mkdir()
        self.addCleanup(shutil.rmtree, root, True)
        return root

    def test_known_artifacts_pass(self):
        root = self.make_repo()
        (root / "README.md").write_text(
            "# Study\n\nThis explains what the study does and why it exists.",
            encoding="utf-8",
        )
        (root / "LICENSE").write_text("MIT License", encoding="utf-8")
        (root / "requirements.txt").write_text("pandas==2.2.0", encoding="utf-8")

        result = collect_repository_evidence.collect_facts(root)
        states = {item["check_id"]: item["state"] for item in result["facts"]}

        self.assertEqual(states["readme-present"], "pass")
        self.assertEqual(states["license-present"], "pass")
        self.assertEqual(states["env-file-present"], "pass")
        self.assertEqual(states["readme-has-content"], "pass")
        self.assertEqual(states["license-machine-readable"], "pass")
        self.assertEqual(states["no-secrets-present"], "pass")
        self.assertEqual(states["no-junk-files"], "pass")
        self.assertEqual(states["no-absolute-paths"], "pass")
        self.assertEqual(states["no-setwd-or-chdir"], "pass")
        self.assertFalse(result["safety"]["repository_code_executed"])
        self.assertEqual(result["target"], root.name)

    def test_requirements_variants_are_environment_records(self):
        root = self.make_repo()
        (root / "requirements-dev.txt").write_text("PyYAML==6.0.3", encoding="utf-8")

        result = collect_repository_evidence.collect_facts(root)
        environment = next(item for item in result["facts"] if item["check_id"] == "env-file-present")

        self.assertEqual(environment["state"], "pass")
        self.assertEqual(environment["evidence"], [{"path": "requirements-dev.txt"}])

    def test_missing_long_tail_artifacts_escalate_to_ai(self):
        root = self.make_repo()

        result = collect_repository_evidence.collect_facts(root)
        states = {item["check_id"]: item["state"] for item in result["facts"]}

        self.assertEqual(states["readme-present"], "fail")
        self.assertEqual(states["license-present"], "needs-ai")
        self.assertEqual(states["env-file-present"], "needs-ai")

    def test_secret_candidates_are_redacted(self):
        root = self.make_repo()
        secret_value = "super-secret-value-123"
        (root / ".env").write_text(f"API_KEY={secret_value}\n", encoding="utf-8")

        result = collect_repository_evidence.collect_facts(root)
        serialized = json.dumps(result)
        secret_fact = next(item for item in result["facts"] if item["check_id"] == "no-secrets-present")

        self.assertEqual(secret_fact["state"], "candidate-fail")
        self.assertNotIn(secret_value, serialized)
        self.assertIn(".env", serialized)

    def test_portability_candidates_name_locations_without_emitting_path_values(self):
        root = self.make_repo()
        path_value = "/Users/researcher/private-study/data.csv"
        (root / "analysis.py").write_text(
            f'DATA = "{path_value}"\nos.chdir("results")\n', encoding="utf-8"
        )

        result = collect_repository_evidence.collect_facts(root)
        serialized = json.dumps(result)
        states = {item["check_id"]: item["state"] for item in result["facts"]}

        self.assertEqual(states["no-absolute-paths"], "candidate-fail")
        self.assertEqual(states["no-setwd-or-chdir"], "candidate-fail")
        self.assertNotIn(path_value, serialized)

    def test_junk_candidates_are_reported_for_confirmation(self):
        root = self.make_repo()
        cache = root / "__pycache__"
        cache.mkdir()
        (cache / "analysis.pyc").write_bytes(b"not bytecode")

        result = collect_repository_evidence.collect_facts(root)
        junk = next(item for item in result["facts"] if item["check_id"] == "no-junk-files")

        self.assertEqual(junk["state"], "candidate-fail")
        self.assertEqual(junk["evidence"][0]["path"], "__pycache__")

    def test_cli_writes_requested_output(self):
        root = self.make_repo()
        output = root / "facts.json"
        with patch.object(
            sys,
            "argv",
            ["collect_repository_evidence.py", str(root), "--out", str(output)],
        ):
            self.assertEqual(collect_repository_evidence.main(), 0)
        self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["schema_version"], "0.1.0")


if __name__ == "__main__":
    unittest.main()
