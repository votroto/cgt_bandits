from functools import singledispatch
from collections import defaultdict
from fractions import Fraction
from cgt_bandits.nodes import ChanceNode, PersonalNode, TerminalNode


def fixup_nodes(root):
    infos = dict()
    return fixup_node(root, infos)


@singledispatch
def fixup_node(node, infos):
    raise NotImplementedError("Can not fix unexpected type.", node)


@fixup_node.register(ChanceNode)
def _(in_node, infos):
    inchildren = list(in_node.children)
    inaction_names = list(in_node.action_names)
    inaction_probs = list(in_node.action_probs)

    lc = len(inchildren)
    ln = len(inaction_names)
    lp = len(inaction_probs)

    action_names = inaction_names + [""] * (lc - ln)
    action_probs = inaction_probs + [0.0] * (lc - lp)
    children = list(map(lambda c: fixup_node(c, infos), inchildren))

    probs = [Fraction(p).limit_denominator() for p in action_probs]
    probs_sum = sum(probs)
    probs = [p / probs_sum for p in probs]

    out_node = ChanceNode(in_node.name, children, action_names, probs)
    return out_node


@fixup_node.register(PersonalNode)
def _(in_node, infos):
    inchildren = list(in_node.children)
    inaction_names = list(in_node.action_names)

    lc = len(inchildren)
    ln = len(inaction_names)

    action_names = inaction_names + [""] * (lc - ln)
    children = list(map(lambda c: fixup_node(c, infos), inchildren))
    player_name = str(in_node.player)

    if in_node.infoset in infos and infos[in_node.infoset] != lc:
        raise RuntimeError(
            f"Infoset {in_node.infoset} identifies nodes with "
            f"different numbers of children. Last node: "
            f"{in_node.name} with actions {inaction_names}."
        )
    else:
        infos[in_node.infoset] = lc

    out_node = PersonalNode(
        in_node.name, in_node.infoset, player_name, children, action_names
    )

    return out_node


@fixup_node.register(TerminalNode)
def _(in_node, infos):
    payoffs = list(in_node.payoffs)

    out_node = TerminalNode(in_node.name, payoffs)
    return out_node


def has_perfect_recall(root):
    def relevant_actions(player, history):
        return tuple(filter(lambda x: x[0] == player, history))

    def traverse(node, history):
        if isinstance(node, PersonalNode):
            hist = relevant_actions(node.player, history)
            if hists[node.player].get(node.infoset, hist) != hist:
                return False
            hists[node.player][node.infoset] = hist

            for i, child in enumerate(node.children):
                new_history = history + [(node.player, node.infoset, i)]
                if not traverse(child, new_history):
                    return False

        if isinstance(node, ChanceNode):
            for i, child in enumerate(node.children):
                new_history = history + [(None, None, i)]
                if not traverse(child, new_history):
                    return False

        return True

    hists = defaultdict(dict)
    return traverse(root, [])
