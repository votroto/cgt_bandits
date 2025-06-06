from cgt_bandits.nodes import ChanceNode, PersonalNode, TerminalNode
import json


def json_object_hook(data):
    match data.pop('TYPE', None):
        case "cgt_bandits.TerminalNode":
            return TerminalNode(**data)
        case "cgt_bandits.ChanceNode":
            return ChanceNode(**data)
        case "cgt_bandits.PersonalNode":
            return PersonalNode(**data)
        case _:
            return data


def json_to_nodes(txt):
    return json.loads(txt, object_hook=json_object_hook)
