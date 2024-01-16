from functools import singledispatch
from cgt_bandits.nodes import ChanceNode, PersonalNode, TerminalNode
from fractions import Fraction


@singledispatch
def fixup_node(node):
    raise NotImplementedError("Can not fix unexpected type.", node)


@fixup_node.register(ChanceNode)
def _(in_node):
    inchildren = list(in_node.children)
    inaction_names = list(in_node.action_names)
    inaction_probs = list(in_node.action_probs)

    lc = len(inchildren)
    ln = len(inaction_names)
    lp = len(inaction_probs)

    action_names = inaction_names + [""] * (lc - ln)
    action_probs = inaction_probs + [0.0] * (lc - lp)
    children = list(map(fixup_node, inchildren))

    probs = [Fraction(p).limit_denominator() for p in action_probs]
    probs_sum = sum(probs)
    probs = [p / probs_sum for p in probs]

    out_node = ChanceNode(in_node.name, children, action_names, probs)
    return out_node


@fixup_node.register(PersonalNode)
def _(in_node):
    inchildren = list(in_node.children)
    inaction_names = list(in_node.action_names)

    lc = len(inchildren)
    ln = len(inaction_names)

    action_names = inaction_names + [""] * (lc - ln)
    children = list(map(fixup_node, inchildren))
    player_name = str(in_node.player)

    out_node = PersonalNode(
        in_node.name, in_node.infoset, player_name, children, action_names
    )
    return out_node


@fixup_node.register(TerminalNode)
def _(in_node):
    payoffs = list(in_node.payoffs)

    out_node = TerminalNode(in_node.name, payoffs)
    return out_node
