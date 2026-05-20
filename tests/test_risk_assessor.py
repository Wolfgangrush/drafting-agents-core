"""Smoke test for Risk Assessor agent."""

import unittest


class TestRiskAssessor(unittest.TestCase):
    def test_no_jurisdiction_leak(self):
        with open("agents/risk_assessor/SKILL.md") as f:
            body = f.read()
        self.assertNotIn("BSB", body)
        self.assertNotIn("rC", body)


if __name__ == "__main__":
    unittest.main()
