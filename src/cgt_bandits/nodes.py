from dataclasses import dataclass
from typing import List


@dataclass
class EFGNode:
    name: str


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
