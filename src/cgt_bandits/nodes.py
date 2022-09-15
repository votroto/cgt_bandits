from dataclasses import dataclass


@dataclass
class EFGNode:
    name: str


@dataclass
class ChanceNode(EFGNode):
    children: list[EFGNode]
    action_names: list[str]
    action_probs: list[float]


@dataclass
class PersonalNode(EFGNode):
    infoset: int
    player: int
    children: list[EFGNode]
    action_names: list[str]


@dataclass
class TerminalNode(EFGNode):
    payoffs: list[float]
