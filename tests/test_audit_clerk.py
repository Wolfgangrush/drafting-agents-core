"""Smoke test for Audit Clerk agent."""

import unittest


class TestAuditClerk(unittest.TestCase):
    def test_no_jurisdiction_leak(self):
        with open("agents/audit_clerk/SKILL.md") as f:
            body = f.read()
        self.assertNotIn("UK", body)
        self.assertNotIn("EU", body)


if __name__ == "__main__":
    unittest.main()
