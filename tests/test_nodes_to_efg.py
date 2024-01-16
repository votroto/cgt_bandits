import unittest
from contextlib import redirect_stdout
from io import StringIO
from cgt_bandits.nodes import ChanceNode, PersonalNode, TerminalNode
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


def build_terminal(cards, history=[]):
    if cards in ["jj", "qq"]:
        return TerminalNode("tie", [0, 0])
    elif cards == "qj":
        return TerminalNode("p1 wins", [3.3, -3.3])
    elif cards == "jq":
        return TerminalNode("p2 wins", [-3, 3])


def build_second_player(cards, history=[]):
    infoset = ord(cards[1])
    actions = ["fold2", "call"]
    children = [
        TerminalNode("p2 folded", [1, -1]),
        build_terminal(cards, history + [actions[1]]),
    ]

    return PersonalNode("", infoset, 1, children, actions)


def build_first_player(cards, history=[]):
    infoset = ord(cards[0])
    actions = ["fold1", "bet"]
    children = [
        TerminalNode("p1 folded", [-1, 1]),
        build_second_player(cards, history + [actions[1]]),
    ]

    return PersonalNode("", infoset, 0, children, actions)


def build_deal():
    deals = ["jj", "jq", "qj", "qq"]
    probs = [1 / 6, 1 / 3, 1 / 3, 1 / 6]
    children = map(build_first_player, deals)

    return ChanceNode("Deal", children, deals, probs)


def build_poker():
    efg = nodes_to_efg(build_deal(), ("0", "1"))
    return repr(efg)


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
