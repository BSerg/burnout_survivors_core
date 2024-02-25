import math

from components.component import Component
from components.drop_component import DropComponent
from components.initiative_component import InitiativeComponent
from components.melee_component import MeleeComponent
from components.move_component import MoveComponent
from components.position_component import PositionComponent
from components.vitality_component import VitalityComponent
from game_context import get_game
from objects.game_object import GameObject
from utils.game import get_distance_between


class AiComponent(Component):
    _target: GameObject | None = None

    def __init__(self, game_object: GameObject) -> None:
        super().__init__('ai_component', game_object)

    @property
    def target(self) -> GameObject | None:
        return self._target

    @target.setter
    def target(self, value: GameObject) -> None:
        self._target = value

    def _attack(self) -> None:
        if self._target:
            self._game_object.require_component(
                MeleeComponent).attack(self._target)

    def _move(self) -> None:
        if not self._target:
            return

        if self.game_object.require_component(
                InitiativeComponent).can_do():
            return

        game = get_game()
        target_position_cmp = self._target.require_component(PositionComponent)
        position_cmp = self.game_object.require_component(PositionComponent)

        min_distance = math.inf
        move_point = None

        for point in position_cmp.get_neighbor_points():
            for obj in game.objects:
                obj_position_component = obj.find_component(PositionComponent)

                if not obj_position_component:
                    continue

                if obj_position_component.position != point:
                    continue

                if obj == self._target:
                    self._attack()
                    move_point = None
                    return

                if obj.has_tags('enemy') and not obj.require_component(VitalityComponent).is_dead:
                    break

            else:
                distance = get_distance_between(
                    point, target_position_cmp.position)

                if distance < min_distance:
                    min_distance = distance
                    move_point = point

        if move_point:
            move_cmp = self.game_object.require_component(
                MoveComponent)
            move_cmp.move_to(move_point.x, move_point.y)

    async def update(self) -> None:
        if self._game_object.require_component(VitalityComponent).is_dead:
            self._game_object.require_component(DropComponent).drop()
        else:
            self._move()
