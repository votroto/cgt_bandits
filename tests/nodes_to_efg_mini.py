from cgt_bandits.nodes import ChanceNode, TerminalNode
from cgt_bandits.export_efg import nodes_to_efg


def build_mini():
    probs = [0.5, 0.5, 0.0]
    names = ["1", "2", "3"]
    terms = [
        TerminalNode("t1", [0, 1]),
        TerminalNode("t2", [0, 2]),
        TerminalNode("t3", [12.34, -56.7891011]),
    ]
    root = ChanceNode("c", terms, names, probs)

    game_name = "EFGTEST"
    players = ("player0", "player1")
    efg = nodes_to_efg(root, name=game_name, players=players)

    return repr(efg)


expected_mini = """EFG 2 R "EFGTEST" { "player0" "player1" }
""

c "c" 1 "" { "1" 1/2 "2" 1/2 "3" 0 } 0
t "t1" 1 "" { 0, 1 }
t "t2" 2 "" { 0, 2 }
t "t3" 3 "" { 12.34, -56.7891011 }"""
