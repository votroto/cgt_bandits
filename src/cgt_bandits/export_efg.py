from functools import singledispatch
from cgt_bandits.utils import fixup_node
from cgt_bandits.nodes import ChanceNode, PersonalNode, TerminalNode
import pygambit as pg


@singledispatch
def _nodes_to_efg(node, out_node, info_dict):
    raise NotImplementedError("Can not export unexpected type.")


@_nodes_to_efg.register(ChanceNode)
def _(in_node, out_node, info_dict):
    lc = len(list(in_node.children))
    out_node.label = in_node.name
    info = out_node.append_move(out_node.game.players.chance, lc)
    for i in range(lc):
        info.actions[i].prob = in_node.action_probs[i]
        info.actions[i].label = in_node.action_names[i]
        _nodes_to_efg(in_node.children[i], out_node.children[i], info_dict)


@_nodes_to_efg.register(PersonalNode)
def _(in_node, out_node, info_dict):
    lc = len(list(in_node.children))
    out_node.label = in_node.name

    if in_node.infoset in info_dict:
        info = out_node.append_move(info_dict[in_node.infoset])
    else:
        player = in_node.player % 2
        info = out_node.append_move(out_node.game.players[player], lc)
        info_dict[in_node.infoset] = info
        for i in range(lc):
            info.actions[i].label = in_node.action_names[i]

    for i in range(lc):
        _nodes_to_efg(in_node.children[i], out_node.children[i], info_dict)


@_nodes_to_efg.register(TerminalNode)
def _(in_node, out_node, info_dict):
    out_node.label = in_node.name
    out_node.outcome = out_node.game.outcomes.add()

    for (i, p) in enumerate(in_node.payoffs):
        out_node.outcome[i] = p


def nodes_to_efg(root):
    g = pg.Game.new_tree()
    g.players.add("p1")
    g.players.add("p2")

    froot = fixup_node(root)
    _nodes_to_efg(froot, g.root, dict())

    return g
