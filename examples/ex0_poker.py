from cgt_bandits.nodes import ChanceNode, PersonalNode, TerminalNode
from cgt_bandits import export_json

from dataclasses import dataclass, replace, field


# In this game, we do not need to keep track of the actions played.
# We show how to do it only because it might be useful for larger games.


@dataclass
class History:
    """
    Nodes in this game are identified by the initial deal and the
    subsequent actions of both players.
    """
    hand_zero: str
    hand_one: str
    past_zero: list[str] = field(default_factory=list)
    past_one: list[str] = field(default_factory=list)


def knowledge_player_zero(history):
    # The only information player zero knows is the card he is holding.

    return ord(history.hand_zero)


def knowledge_player_one(history):
    # Player one also knows whether the other player bet or folded,
    # but ommiting this information changes nothing in the game.

    return hash((history.hand_one, tuple(history.past_zero)))


def build_endgame(history):
    # We reach this node when a bet is followed by a call.

    cards = history.hand_zero + history.hand_one
    if cards in ["JJ", "QQ"]:
        return TerminalNode("Tie", [0, 0])
    elif cards == "QJ":
        return TerminalNode("P0 wins", [3, -3])
    elif cards == "JQ":
        return TerminalNode("P1 wins", [-3, 3])


def build_fold_one(history):
    return TerminalNode("P1 folded", [1, -1])


def build_fold_zero(history):
    return TerminalNode("P0 folded", [-1, 1])


def build_turn_one(history):
    # Player zero decides if he wants to fold or call

    infoset = knowledge_player_one(history)
    actions = ["fold", "call"]
    children = [
        build_fold_one(replace(history, past_one=[actions[0]])),
        build_endgame(replace(history, past_one=[actions[1]])),
    ]

    return PersonalNode("Turn one", infoset, 1, children, actions)


def build_turn_zero(history):
    # Player zero decides if he wants to fold or bet

    infoset = knowledge_player_zero(history)
    actions = ["fold", "bet"]
    children = [
        build_fold_zero(replace(history, past_zero=[actions[0]])),
        build_turn_one(replace(history, past_zero=[actions[1]])),
    ]

    return PersonalNode("Turn zero", infoset, 0, children, actions)


def build_deal():
    # The root of the game. Each player is dealt either a Queen or a Jack.

    deals = ["JJ", "JQ", "QJ", "QQ"]
    probs = [1 / 6, 1 / 3, 1 / 3, 1 / 6]
    children = [build_turn_zero(History(d[0], d[1])) for d in deals]

    return ChanceNode("Deal", children, deals, probs)


if __name__ == "__main__":
    game = build_deal()
    print(export_json.nodes_to_json(game))
