import unittest
import pygambit as pg
from nodes_to_efg_poker import expected_poker
from cgt_bandits import import_efg


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
