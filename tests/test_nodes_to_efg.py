import unittest
from nodes_to_efg_mini import build_mini, expected_mini
from nodes_to_efg_poker import build_poker, expected_poker
from contextlib import redirect_stdout
from io import StringIO


class TestNodesToEfg(unittest.TestCase):
    def test_mini(self):
        self.assertEqual(build_mini().strip(), expected_mini)

    def test_poker(self):
        self.maxDiff = 1000

        f = StringIO()
        with redirect_stdout(f):
            poker = build_poker()
        s = f.getvalue()

        self.assertEqual(poker.strip(), expected_poker)
        self.assertEqual(s, "")


if __name__ == "__main__":
    unittest.main()
