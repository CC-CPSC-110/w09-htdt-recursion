import math
from dataclasses import dataclass
from typing_extensions import Self
from stop_parser import Latitude, Longitude

@dataclass
class Shape:
    _id: str
    _lat: float
    _lon: float
    _next: Self | None
    
    def __str__(self, level=1) -> str:
        indent = '\t'
        next_str = self._next.__str__(level + 1) if self._next else "None"
        return (
            f"Shape(\n"
            f"{indent * level}  id: {self._id}\n"
            f"{indent * level} lat: {self._lat}\n"
            f"{indent * level} lon: {self._lon}\n"
            f"{indent * level}next: {next_str}\n"
            f"{indent * (level - 1)})"
        )

    def dist_next(self) -> float:
        if self._next != None:
            dlat = abs(self._lat - self._next._lat)
            dlon = abs(self._lon - self._next._lon)
            dist = math.sqrt(dlat ** 2 + dlon ** 2)
            return dist
        return 0.0
    
    def dist_end(self) -> float:
        if self._next != None:
            return self.dist_next() + self._next.dist_end()
        return 0.0    
shape_0 = Shape("000", 49.0, -123.0, None)
shape_1 = Shape("001", 49.1, -123.1, shape_0)
shape_2 = Shape("002", 49.2, -123.2, shape_1)