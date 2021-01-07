from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Graph:
    """Class for converting (x,y) coordinates to Chart.js datasets"""
    label: str
    coords: List[Tuple[float, float]]

    def chart_js_dataset(self):
        data = [{'x': p[0], 'y': p[1]} for p in self.coords]
        return {
            'label': self.label,
            'data': data,
            'showLine': True,
        }
