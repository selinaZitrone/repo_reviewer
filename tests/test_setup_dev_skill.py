import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import setup_dev_skill


class SetupDevSkillTests(unittest.TestCase):
    def test_shared_agent_skills_location_for_codex_and_copilot(self):
        home = Path("home")
        expected = home / ".agents" / "skills" / "repo-reviewer"

        self.assertEqual(setup_dev_skill.destination_for("codex", home), expected)
        self.assertEqual(setup_dev_skill.destination_for("copilot", home), expected)

    def test_claude_uses_its_personal_skill_location(self):
        home = Path("home")
        self.assertEqual(
            setup_dev_skill.destination_for("claude", home),
            home / ".claude" / "skills" / "repo-reviewer",
        )


if __name__ == "__main__":
    unittest.main()
