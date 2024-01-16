from functools import singledispatch
from cgt_bandits.utils import fixup_node
from cgt_bandits.nodes import ChanceNode, PersonalNode, TerminalNode
import random
import pydot
import math


def _make_personal_node(id, player, **kwargs):
    col = f"{math.fmod(math.sqrt(2) * player, 1.0)}+0.4+0.95"
    kwargs.setdefault("fillcolor", col)
    kwargs.setdefault("style", "filled")
    kwargs.setdefault("shape", "circle")
    node = pydot.Node(id, **kwargs)
    return node


def _make_chance_node(id, **kwargs):
    kwargs.setdefault("shape", "circle")
    node = pydot.Node(id, **kwargs)
    return node


def _make_terminal_node(id, **kwargs):
    kwargs.setdefault("shape", "none")
    kwargs.setdefault("height", 0)
    kwargs.setdefault("margin", 0)
    kwargs.setdefault("width", 0)
    node = pydot.Node(id, **kwargs)
    return node


def _make_infoset_cluster(id, **kwargs):
    kwargs.setdefault("style", "filled")
    kwargs.setdefault("fillcolor", "0+0+0.9")
    kwargs.setdefault("color", "transparent")
    cluster = pydot.Cluster(id, **kwargs)
    return cluster


def _make_edge(tail, head, **kwargs):
    kwargs.setdefault("color", f"{random.random()}+0.8+0.5")
    edge = pydot.Edge(tail, head, **kwargs)
    return edge


@singledispatch
def _nodes_to_dot(node, out_node, info_dict):
    raise NotImplementedError("Can not export unexpected type.")


@_nodes_to_dot.register(ChanceNode)
def _(in_node, graph, info_dict):
    node = _make_chance_node(id(in_node), label=in_node.name)
    graph.add_node(node)

    lc = len(in_node.children)
    for i in range(lc):
        child = _nodes_to_dot(in_node.children[i], graph, info_dict)
        lab = f"{in_node.action_probs[i]:.3f}\n{in_node.action_names[i]}"
        graph.add_edge(_make_edge(node, child, label=lab))

    return node


@_nodes_to_dot.register(PersonalNode)
def _(in_node, graph, info_dict):
    node = _make_personal_node(id(in_node), in_node.player, label=in_node.name)
    graph.add_node(node)

    infoid = f"{in_node.player}-{in_node.infoset}"
    if infoid not in info_dict:
        cluster = _make_infoset_cluster(infoid)
        info_dict[infoid] = cluster
    info_dict[infoid].add_node(node)

    lc = len(in_node.children)
    for i in range(lc):
        child = _nodes_to_dot(in_node.children[i], graph, info_dict)
        lab = f"{in_node.action_names[i]}"
        graph.add_edge(_make_edge(node, child, label=lab))

    return node


@_nodes_to_dot.register(TerminalNode)
def _(in_node, graph, info_dict):
    payoff_string = ", ".join(map(str, in_node.payoffs))
    lab = f"{in_node.name}\n [{payoff_string}]"
    node = _make_terminal_node(id(in_node), label=lab)
    graph.add_node(node)

    return node


def _add_infosets(graph, infosets):
    for c in infosets.values():
        if len(c.get_nodes()) > 1:
            graph.add_subgraph(c)


def nodes_to_dot(root):
    graph = pydot.Dot(ranksep=2, rankdir="LR")

    isets = dict()
    froot = fixup_node(root)
    _nodes_to_dot(froot, graph, isets)
    _add_infosets(graph, isets)

    return graph
