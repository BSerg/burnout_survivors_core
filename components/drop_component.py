from components.component import Component
from objects.game_object import GameObject
from components.position_component import PositionComponent
import random
from game_context import get_current_game


class DropComponent(Component):
    def __init__(self, game_object: GameObject, drop_object: GameObject | None = None, chance: float = 1) -> None:
        super().__init__('drop_component', game_object)
        self._drop_object: GameObject | None = drop_object
        self._chance: float = chance

    @property
    def drop_object(self) -> GameObject | None:
        return self._drop_object

    @drop_object.setter
    def drop_object(self, value: GameObject | None) -> None:
        self._drop_object = value

    @property
    def chance(self) -> float:
        return self._chance

    def drop(self) -> None:
        if not self._drop_object:
            return

        if random.random() > self._chance:
            return

        drop_object = self._drop_object
        drop_object.require_component(
            PositionComponent).position = self._game_object.require_component(PositionComponent).position
        get_current_game().objects.add(drop_object)
        self._drop_object = None
