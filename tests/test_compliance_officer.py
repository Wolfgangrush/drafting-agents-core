"""Smoke test for Compliance Officer agent."""

import unittest


class TestComplianceOfficer(unittest.TestCase):
    def test_no_jurisdiction_leak(self):
        with open("agents/compliance_officer/SKILL.md") as f:
            body = f.read()
        self.assertNotIn("BSB", body)
        self.assertNotIn("SRA", body)
        self.assertNotIn("CCBE", body)
        self.assertNotIn("LSRA", body)


if __name__ == "__main__":
    unittest.main()
