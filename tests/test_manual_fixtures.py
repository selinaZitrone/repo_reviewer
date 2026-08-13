import json
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import collect_repository_evidence


class ManualFixtureTests(unittest.TestCase):
    def test_fixture_deterministic_states_match_expectations(self):
        manual = Path(__file__).resolve().parent / "manual"
        fixtures = manual / "fixtures"
        expected = json.loads(
            (manual / "expected-deterministic.json").read_text(encoding="utf-8")
        )

        self.assertEqual(
            sorted(path.name for path in fixtures.iterdir() if path.is_dir()),
            sorted(expected),
        )

        for fixture_name, expected_states in expected.items():
            with self.subTest(fixture=fixture_name):
                result = collect_repository_evidence.collect_facts(fixtures / fixture_name)
                actual_states = {
                    item["check_id"]: item["state"] for item in result["facts"]
                }
                self.assertEqual(actual_states, expected_states)
                self.assertFalse(result["safety"]["repository_code_executed"])


if __name__ == "__main__":
    unittest.main()
