from functools import singledispatch
from nodes import ChanceNode, PersonalNode, TerminalNode


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
    action_probs = inaction_probs + [float('nan')] * (lc - lp)
    children = list(map(fixup_node, inchildren))

    out_node = ChanceNode(in_node.name, children, action_names, action_probs)
    return out_node


@fixup_node.register(PersonalNode)
def _(in_node):
    inchildren = list(in_node.children)
    inaction_names = list(in_node.action_names)

    lc = len(inchildren)
    ln = len(inaction_names)

    action_names = inaction_names + [""] * (lc - ln)
    children = list(map(fixup_node, inchildren))

    out_node = PersonalNode(in_node.name, in_node.infoset,
                            in_node.player, children, action_names)
    return out_node


@fixup_node.register(TerminalNode)
def _(in_node):
    ps = list(in_node.payoffs)
    lp = len(ps)

    if lp == 2:
        payoffs = ps
    elif lp == 1:
        payoffs = [ps[0], -ps[0]]
    else:
        payoffs = [float('nan'), float('nan')]

    out_node = TerminalNode(in_node.name, payoffs)
    return out_node
