import unittest
import pygambit as pg
from cgt_bandits import import_efg


expected_poker = """EFG 2 R "" { "0" "1" }
""

c "Deal" 1 "" { "jj" 1/6 "jq" 1/3 "qj" 1/3 "qq" 1/6 } 0
p "" 1 1 "0-106" { "fold1" "bet" } 0
t "p1 folded" 1 "" { -1, 1 }
p "" 2 1 "1-106" { "fold2" "call" } 0
t "p2 folded" 2 "" { 1, -1 }
t "tie" 3 "" { 0, 0 }
p "" 1 1 "0-106" { "fold1" "bet" } 0
t "p1 folded" 4 "" { -1, 1 }
p "" 2 2 "1-113" { "fold2" "call" } 0
t "p2 folded" 5 "" { 1, -1 }
t "p2 wins" 6 "" { -3, 3 }
p "" 1 2 "0-113" { "fold1" "bet" } 0
t "p1 folded" 7 "" { -1, 1 }
p "" 2 1 "1-106" { "fold2" "call" } 0
t "p2 folded" 8 "" { 1, -1 }
t "p1 wins" 9 "" { 3.3, -3.3 }
p "" 1 2 "0-113" { "fold1" "bet" } 0
t "p1 folded" 10 "" { -1, 1 }
p "" 2 2 "1-113" { "fold2" "call" } 0
t "p2 folded" 11 "" { 1, -1 }
t "tie" 12 "" { 0, 0 }"""


class TestNodesToEfg(unittest.TestCase):
    def test_poker(self):
        graph = pg.Game.parse_game(expected_poker)
        root = import_efg.efg_to_nodes(graph)

        expected_names = ["jj", "jq", "qj", "qq"]
        expected_probs = [1 / 6, 1 / 3, 1 / 3, 1 / 6]

        self.assertEqual(root.action_names, expected_names)
        for i in range(len(root.action_probs)):
            self.assertAlmostEqual(root.action_probs[i], expected_probs[i])


if __name__ == "__main__":
    unittest.main()
