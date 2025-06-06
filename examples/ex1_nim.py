from cgt_bandits.nodes import PersonalNode, TerminalNode, ChanceNode
from cgt_bandits import export_json
from cgt_bandits import import_json


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


def dict_to_nodes(d):
    if "payoffs" in d.keys():
        return TerminalNode(d["name"], d["payoffs"])
    elif "action_probs" in d.keys():
        name = d["name"]
        actions = d["action_names"]
        probs = d["action_probs"]
        children = [dict_to_nodes(c) for c in d["children"]]
        return ChanceNode(name, children, actions, probs)
    else:
        name = d["name"]
        player = d["player"]
        actions = d["action_names"]
        infoset = d["infoset"]
        children = [dict_to_nodes(c) for c in d["children"]]
        return PersonalNode(name, infoset, player, children, actions)


if __name__ == "__main__":
    game = build_game()
    print(export_json.nodes_to_json(game))
