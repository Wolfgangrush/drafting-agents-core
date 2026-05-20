"""Smoke test for Matter Manager agent."""

import unittest


class TestMatterManager(unittest.TestCase):
    def test_matter_schema_defined(self):
        """Matter schema is defined in the SKILL.md."""

    def test_no_jurisdiction_leak(self):
        with open("agents/matter_manager/SKILL.md") as f:
            body = f.read()
        self.assertNotIn("OSCOLA", body)
        self.assertNotIn("BSB", body)
        self.assertNotIn("UK Supreme Court", body)


if __name__ == "__main__":
    unittest.main()
