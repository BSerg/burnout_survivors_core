from components.component import Component
from components.initiative_component import InitiativeComponent
from components.position_component import PositionComponent
from models.shared import Point
from objects.game_object import GameObject
from components.status_component import Status, StatusComponent


class MoveComponent(Component):
    def __init__(self, game_object: GameObject) -> None:
        super().__init__('move_component', game_object)
        self._path: list[Point] = list()

    @property
    def path(self) -> list[Point]:
        return self._path

    def can_move(self) -> bool:
        initiative_cmp = self.game_object.findComponent(InitiativeComponent)
        if not initiative_cmp:
            return True
        return initiative_cmp.can_do()

    def move_to_point(self, point: Point) -> None:
        self._game_object.requireComponent(PositionComponent).position = point
        self._path.append(point)
        
        self._game_object.updated = True
        
        status_component = self._game_object.findComponent(StatusComponent)
        if status_component:
            status_component.status = Status.MOVING.value
        
        self._game_object.game.log(f'{self._game_object.name} moved to [{point.x},{point.y}]')

    def move_to(self, x: int, y: int) -> None:
        self.move_to_point(Point(x=x, y=y))
