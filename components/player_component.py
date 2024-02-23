from components.component import Component
from components.melee_component import MeleeComponent
from components.move_component import MoveComponent
from components.position_component import PositionComponent
from components.vitality_component import VitalityComponent
from models.input_model import Direction
from objects.game_object import GameObject
from utils.game import Point
from objects.consumable.health_consumable import HealthConsumable


class PlayerComponent(Component):
    def __init__(self, game_object: GameObject) -> None:
        super().__init__('player_component', game_object)
        self._direction: Direction | None = None

    @property
    def direction(self) -> Direction | None:
        return self._direction

    @direction.setter
    def direction(self, value: Direction | None) -> None:
        self._direction = value

    async def update(self) -> None:
        if not self._direction:
            return

        position_component = self._game_object.require_component(
            PositionComponent)
        move_component = self._game_object.require_component(MoveComponent)
        melee_component = self._game_object.require_component(MeleeComponent)
        vitality_component = self._game_object.require_component(
            VitalityComponent)

        target_point = None

        if self._direction == Direction.LEFT:
            target_point = Point(x=position_component.x -
                                 1, y=position_component.y)
        elif self._direction == Direction.RIGHT:
            target_point = Point(x=position_component.x +
                                 1, y=position_component.y)
        elif self._direction == Direction.UP:
            target_point = Point(x=position_component.x,
                                 y=position_component.y - 1)
        elif self._direction == Direction.DOWN:
            target_point = Point(x=position_component.x,
                                 y=position_component.y + 1)

        if target_point:
            objects = []

            for obj in self._game_object.game.objects:
                obj_position_component = obj.find_component(PositionComponent)
                if obj_position_component and obj_position_component.position.x == target_point.x and obj_position_component.position.y == target_point.y:
                    objects.append(obj)

            for obj in objects:
                if obj.has_tags('enemy'):
                    obj_vitality_component = obj.find_component(
                        VitalityComponent)

                    if not obj_vitality_component:
                        continue

                    if obj_vitality_component.health <= 0:
                        continue

                    melee_component.attack(obj)
                    target_point = None

                if isinstance(obj, HealthConsumable):
                    vitality_component.heal(obj.value)
                    obj.consumed = True

        if target_point:
            move_component.move_to_point(target_point)

        self._direction = None
