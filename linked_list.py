from typing import Any
from typing_extensions import Self
from dataclasses import dataclass

@dataclass
class Node:
    data: Any
    next: Self

n0 = Node(0, None)
n1 = Node(1, n0)
n2 = Node(2, n1)
n3 = Node(3, n2)