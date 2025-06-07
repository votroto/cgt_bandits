from cgt_bandits.nodes import PersonalNode, TerminalNode
from cgt_bandits import export_json


def knowledge_player(history):
    # The game of NIM is fully observable.

    return hash(tuple(history))


def payoffs(player):
    return [-1, 1] if player == 0 else [1, -1]


def switch(player):
    return 1 if player == 0 else 0


def build_turn(player, tokens, history, max_grab=2):
    # The last player to take a stone wins.

    if tokens == 0:
        return TerminalNode(f"P{player} lost", payoffs(player))

    options = range(1, min(tokens, max_grab) + 1)
    infoset = knowledge_player(history)
    actions = [f"take {t}" for t in options]
    children = [build_turn(switch(player), tokens - t, history + [t]) for t in options]
    name = f"P{player}'s turn\n({tokens} left)"

    return PersonalNode(name, infoset, player, children, actions)


def build_game():
    """A five-stone game of NIM"""
    return build_turn(0, 5, [])


if __name__ == "__main__":
    game = build_game()
    print(export_json.nodes_to_json(game))
