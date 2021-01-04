from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Graph:
    min_x: float
    min_y: float
    max_x: float
    max_y: float
    coords: List[Tuple[float, float]]
