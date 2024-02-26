from __future__ import annotations


from typing import TYPE_CHECKING

from components.component import Component
from game_context import get_current_game
from utils.game import Point

if TYPE_CHECKING:
    from objects.game_object import GameObject


class PositionComponent(Component):
    def __init__(self, game_object: GameObject, x: int = 0, y: int = 0) -> None:
        super().__init__('position_component', game_object)
        self._position = Point(x=x, y=y)

    # TODO optimize
    def _update_manager_position(self):
        get_current_game().objects.remove(self._game_object.name)
        get_current_game().objects.add(self._game_object)

    @property
    def position(self) -> Point:
        return self._position

    @position.setter
    def position(self, value: Point) -> None:
        self._position = value
        self._update_manager_position()

    @property
    def x(self) -> int:
        return self._position.x

    @x.setter
    def x(self, value: int) -> None:
        self._position.x = value
        self._update_manager_position()

    @property
    def y(self) -> int:
        return self._position.y

    @y.setter
    def y(self, value: int) -> None:
        self.position.y = value
        self._update_manager_position()

    def get_neighbor_points(self) -> list[Point]:
        return [
            Point(x=self.x - 1, y=self.y),
            Point(x=self.x, y=self.y - 1),
            Point(x=self.x + 1, y=self.y),
            Point(x=self.x, y=self.y + 1)
        ]
