"""Smoke test for Drafting Assistant agent."""

import unittest


class TestDraftingAssistant(unittest.TestCase):
    def test_no_jurisdiction_leak(self):
        with open("agents/drafting_assistant/SKILL.md") as f:
            body = f.read()
        self.assertNotIn("OSCOLA", body)
        self.assertNotIn("Bombay HC", body)
        self.assertNotIn("UK", body)


if __name__ == "__main__":
    unittest.main()
