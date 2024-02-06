from pydantic import BaseModel

from components.component import Component
from models.shared import Point
from objects.game_object import GameObject


class PositionComponent(Component):
    def __init__(self, game_object: GameObject, x: int = 0, y: int = 0) -> None:
        super().__init__('position_component', game_object)
        self._position = Point(x=x, y=y)

    @property
    def position(self) -> Point:
        return self._position

    @position.setter
    def position(self, value: Point) -> None:
        self._position = value

    @property
    def x(self) -> int:
        return self._position.x

    @x.setter
    def x(self, value: int) -> None:
        self._position.x = value

    @property
    def y(self) -> int:
        return self._position.y

    @y.setter
    def y(self, value: int) -> None:
        self.position.y = value

    def get_neighbors(self) -> list[Point]:
        return [
            Point(x=self.x - 1, y=self.y),
            Point(x=self.x, y=self.y - 1),
            Point(x=self.x + 1, y=self.y),
            Point(x=self.x, y=self.y + 1)
        ]
