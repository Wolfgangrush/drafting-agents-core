"""Smoke test for Direct Access Detector agent."""

import unittest


class TestDirectAccessDetector(unittest.TestCase):
    def test_no_jurisdiction_leak(self):
        with open("agents/direct_access_detector/SKILL.md") as f:
            body = f.read()
        self.assertNotIn("BSB", body)
        self.assertNotIn("rC123", body)


if __name__ == "__main__":
    unittest.main()
