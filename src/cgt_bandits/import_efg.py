import pygambit as pg
from cgt_bandits.nodes import ChanceNode, PersonalNode, TerminalNode


def _efg_to_nodes(n):
    if n.is_terminal:
        return TerminalNode(n.label, list(n.outcome))
    elif n.player.is_chance:
        acts = n.infoset.actions
        labels = [a.label for a in acts]
        probs = [a.prob for a in acts]
        children = [_efg_to_nodes(n) for n in n.children]
        return ChanceNode(n.label, children, labels, probs)
    else:
        info = list(n.game.infosets).index(n.infoset)
        player = n.player.number
        labels = [a.label for a in n.infoset.actions]
        children = [_efg_to_nodes(n) for n in n.children]
        return PersonalNode(n.label, info, player, children, labels)


def efg_to_nodes(game):
    return _efg_to_nodes(game.root)

