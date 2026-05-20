"""Smoke test for Transparency Gate agent."""

import unittest


class TestTransparencyGate(unittest.TestCase):
    def test_no_jurisdiction_leak(self):
        with open("agents/transparency_gate/SKILL.md") as f:
            body = f.read()
        self.assertNotIn("rC19", body)
        self.assertNotIn("BSB", body)


if __name__ == "__main__":
    unittest.main()
