from components.component import Component
from components.initiative_component import InitiativeComponent
from components.position_component import PositionComponent
from game_context import get_game
from objects.game_object import GameObject
from components.status_component import Status, StatusComponent
from utils.game import Point


class MoveComponent(Component):
    def __init__(self, game_object: GameObject) -> None:
        super().__init__('move_component', game_object)
        self._path: list[Point] = list()

    @property
    def path(self) -> list[Point]:
        return self._path

    def move_to_point(self, point: Point) -> None:
        self._game_object.require_component(PositionComponent).position = point
        self._path.append(point)

        status_component = self._game_object.find_component(StatusComponent)
        if status_component:
            status_component.status = Status.MOVING.value

        get_game().log(
            f'{self._game_object.name} moved to [{point.x},{point.y}]')

    def move_to(self, x: int, y: int) -> None:
        self.move_to_point(Point(x=x, y=y))
