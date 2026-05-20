"""Smoke test for Citation Clerk agent."""

import unittest


class TestCitationClerk(unittest.TestCase):
    def test_no_jurisdiction_leak(self):
        with open("agents/citation_clerk/SKILL.md") as f:
            body = f.read()
        self.assertNotIn("OSCOLA", body)
        self.assertNotIn("EWHC", body)
        self.assertNotIn("UKSC", body)


if __name__ == "__main__":
    unittest.main()
