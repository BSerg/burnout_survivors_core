from components.component import Component
from components.position_component import PositionComponent
from game_context import get_current_game
from objects.game_object import GameObject
from utils.game import get_points_in_radius


class VisionComponent(Component):
    def __init__(self, game_object: GameObject, radius: float = 1) -> None:
        super().__init__('vision_component', game_object)
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    def find_visible_objects(self) -> set[GameObject]:
        position_component = self._game_object.require_component(
            PositionComponent)

        visible_objects = None

        for offset in get_points_in_radius(self._radius):
            x, y = position_component.x + offset.x, position_component.y + offset.y

            if x == position_component.x and y == position_component.y:
                continue

            objs = set(get_current_game().objects.find_by_position(x, y))

            if not visible_objects:
                visible_objects = objs
            else:
                objs &= visible_objects

        return visible_objects or set()
