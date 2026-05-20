"""Smoke test for Calendar Sync agent."""

import unittest


class TestCalendarSync(unittest.TestCase):
    def test_no_jurisdiction_leak(self):
        with open("agents/calendar_sync/SKILL.md") as f:
            body = f.read()
        self.assertNotIn("Europe/London", body)
        self.assertNotIn("BST", body)


if __name__ == "__main__":
    unittest.main()
