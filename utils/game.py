from __future__ import annotations

import math
from functools import lru_cache

from models.shared import PointModel


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, __value: 'Point') -> bool:
        return self.x == __value.x and self.y == __value.y

    def __hash__(self) -> int:
        return hash(hash(self.x) + hash(self.y))

    def get_state(self) -> PointModel:
        return PointModel(x=self.x, y=self.y)


def get_distance_between(a: Point, b: Point) -> float:
    return math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))


@lru_cache
def get_points_in_radius(radius: float) -> set[Point]:
    points = set()
    zero_point = Point(x=0, y=0)
    for x in range(-int(radius), int(radius) + 1):
        for y in range(-int(radius), int(radius) + 1):
            point = Point(x=x, y=y)
            if get_distance_between(zero_point, point) <= radius:
                points.add(point)
    return points
