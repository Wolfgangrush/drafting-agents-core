"""Smoke test for Court Registrar agent."""

import unittest


class TestCourtRegistrar(unittest.TestCase):
    def test_no_jurisdiction_leak(self):
        with open("agents/court_registrar/SKILL.md") as f:
            body = f.read()
        self.assertNotIn("UK Supreme Court", body)
        self.assertNotIn("CJEU", body)
        self.assertNotIn("Court of Appeal", body)


if __name__ == "__main__":
    unittest.main()
