from __future__ import annotations

from components.position_component import PositionComponent
from objects.game_object import GameObjectGroup


class GameObjectManager(GameObjectGroup):
    def __init__(self) -> None:
        super().__init__('object_manager')

    def find_by_position(self, x: int, y: int):
        for obj in self:
            if obj.has_component(PositionComponent):
                obj_position = obj.require_component(
                    PositionComponent).position
                if obj_position.x == x and obj_position.y == y:
                    yield obj

    def get_state(self) -> None:
        return None
