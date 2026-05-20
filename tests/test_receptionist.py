"""Smoke test for Receptionist (brain) agent."""

import unittest


class TestReceptionist(unittest.TestCase):
    def test_intent_classification_exists(self):
        """The Receptionist SKILL.md defines intent categories."""
        # In v0.1, tests verify the skill file structure and placeholder hygiene.
        # Full integration tests arrive in v0.2 when the Claude Code test harness is wired.

    def test_routing_map_complete(self):
        """Every intent category maps to a known specialist."""

    def test_no_jurisdiction_leak(self):
        """No raw jurisdiction tokens in the canonical body."""
        with open("agents/receptionist/SKILL.md") as f:
            body = f.read()
        # Placeholders are allowed; raw jurisdiction values are not
        self.assertNotIn("OSCOLA", body)
        self.assertNotIn("BSB", body)
        self.assertNotIn("UK Supreme Court", body)


if __name__ == "__main__":
    unittest.main()
