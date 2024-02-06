import math

from components.component import Component
from components.initiative_component import InitiativeComponent
from components.melee_component import MeleeComponent
from components.move_component import MoveComponent
from components.position_component import PositionComponent
from components.vitality_component import VitalityComponent
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
            self._game_object.requireComponent(
                MeleeComponent).attack(self._target)

    def _move(self) -> None:
        if not self._target:
            return

        game = self.game_object.game
        target_position_cmp = self._target.requireComponent(PositionComponent)
        position_cmp = self.game_object.requireComponent(PositionComponent)
        initiative_cmp = self.game_object.requireComponent(InitiativeComponent)

        while initiative_cmp.can_do():

            def _do():
                min_distance = math.inf
                move_point = None

                for point in position_cmp.get_neighbors():
                    for obj in game.objects.findObjectsByPosition(point):
                        if obj == self._target:
                            self._attack()
                            move_point = None
                            return

                        if obj.hasTag('enemy') and not obj.requireComponent(VitalityComponent).is_dead:
                            break

                    else:
                        distance = get_distance_between(
                            point, target_position_cmp.position)

                        if distance < min_distance:
                            min_distance = distance
                            move_point = point

                if move_point:
                    move_cmp = self.game_object.requireComponent(MoveComponent)
                    move_cmp.move_to(move_point.x, move_point.y)

            initiative_cmp.do(_do)

    async def update(self) -> None:
        if self._game_object.requireComponent(VitalityComponent).is_dead:
            return
        self._move()
