from functools import singledispatch
from cgt_bandits.nodes import ChanceNode, PersonalNode, TerminalNode
import json


@singledispatch
def vars_with_type(obj):
    return vars(obj)


@vars_with_type.register(ChanceNode)
def _(node):
    v = vars(node)
    v['TYPE'] = "cgt_bandits.ChanceNode"
    return v


@vars_with_type.register(PersonalNode)
def _(node):
    v = vars(node)
    v['TYPE'] = "cgt_bandits.PersonalNode"
    return v


@vars_with_type.register(TerminalNode)
def _(node):
    v = vars(node)
    v['TYPE'] = "cgt_bandits.TerminalNode"
    return v


def nodes_to_json(root):
    return json.dumps(root, default=vars_with_type)
