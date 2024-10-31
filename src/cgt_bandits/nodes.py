from dataclasses import dataclass, asdict
from typing import List
import json


@dataclass
class EFGNode:
    name: str

    def __repr__(self):
        json.dumps(asdict(self))


@dataclass
class ChanceNode(EFGNode):
    children: List[EFGNode]
    action_names: List[str]
    action_probs: List[float]


@dataclass
class PersonalNode(EFGNode):
    infoset: int
    player: int
    children: List[EFGNode]
    action_names: List[str]


@dataclass
class TerminalNode(EFGNode):
    payoffs: List[float]
