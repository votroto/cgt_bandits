from functools import singledispatch
from cgt_bandits.utils import fixup_nodes
from cgt_bandits.nodes import ChanceNode, PersonalNode, TerminalNode
import pygambit as pg


def _add_moves(node, player, infoset, action_names):
    game = node.game
    game.append_move(node, player, action_names)

    try:
        game.set_infoset(node, infoset)
    except KeyError:
        node.infoset.label = infoset


@singledispatch
def _nodes_to_efg(node, pg_node, info_dict):
    raise NotImplementedError("Can not export unexpected type.", node)


@_nodes_to_efg.register(ChanceNode)
def _(efg_node, pg_node, game):
    probs = [pg.Rational(p) for p in efg_node.action_probs]

    pg_node.label = efg_node.name
    game.append_move(pg_node, game.players.chance, efg_node.action_names)
    game.set_chance_probs(pg_node.infoset, probs)

    for e_child, p_child in zip(efg_node.children, pg_node.children):
        _nodes_to_efg(e_child, p_child, game)


@_nodes_to_efg.register(PersonalNode)
def _(efg_node, pg_node, game):
    infoid = f"{efg_node.player}-{efg_node.infoset}"

    pg_node.label = efg_node.name
    _add_moves(pg_node, efg_node.player, infoid, efg_node.action_names)

    for e_child, p_child in zip(efg_node.children, pg_node.children):
        _nodes_to_efg(e_child, p_child, game)


@_nodes_to_efg.register(TerminalNode)
def _(efg_node, pg_node, game):
    pg_node.label = efg_node.name
    outcome = game.add_outcome(efg_node.payoffs)
    game.set_outcome(pg_node, outcome)


def nodes_to_efg(root, players, name=""):
    player_names = [str(p) for p in players]
    froot = fixup_nodes(root)

    game = pg.Game.new_tree(title=name, players=player_names)
    _nodes_to_efg(froot, game.root, game)

    return game
