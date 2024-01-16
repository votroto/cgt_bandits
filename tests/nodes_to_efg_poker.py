from cgt_bandits.nodes import ChanceNode, PersonalNode, TerminalNode
from cgt_bandits import export_efg


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
    efg = export_efg.nodes_to_efg(build_deal(), ("0", "1"))
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
