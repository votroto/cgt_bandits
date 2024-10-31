from dataclasses import dataclass, asdict
from typing import List
import json


@dataclass
class EFGNode:
    name: str

    def __repr__(self):
        return json.dumps(asdict(self))


@dataclass(repr=False)
class ChanceNode(EFGNode):
    children: List[EFGNode]
    action_names: List[str]
    action_probs: List[float]


@dataclass(repr=False)
class PersonalNode(EFGNode):
    infoset: int
    player: int
    children: List[EFGNode]
    action_names: List[str]


@dataclass(repr=False)
class TerminalNode(EFGNode):
    payoffs: List[float]


def json_object_hook(dct):
    if 'payoffs' in dct:
        return TerminalNode(**dct)
    elif 'action_probs' in dct:
        return ChanceNode(**dct)
    elif 'player' in dct:
        return PersonalNode(**dct)
    return dct
