import math

from models.shared import Point


def get_distance_between(a: Point, b: Point) -> float:
    return math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
