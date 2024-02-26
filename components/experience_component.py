from components.component import Component
from components.position_component import PositionComponent
from game_context import get_current_game
from objects.consumables.exp_consumable import ExpConsumable
from objects.game_object import GameObject
from utils.game import get_points_in_radius, Point


class ExperienceComponent(Component):
    def __init__(self, game_object: GameObject, level_map: list[float] = list(), consume_radius: float = 1, consume_rate: float = 1) -> None:
        super().__init__('experience_component', game_object)
        self._exp: float = 0
        self._level: int = 0
        self._level_map: list[float] = level_map
        self._consume_radius: float = consume_radius
        self._consume_rate: float = consume_rate

    @property
    def exp(self) -> float:
        return self._exp

    @property
    def level(self) -> int:
        return self._level
    
    @property
    def level_map(self) -> list[float]:
        return self._level_map
    
    @level_map.setter
    def level_map(self, value: list[float]) -> None:
        self._level_map = value

    @property
    def consume_radius(self) -> float:
        return self._consume_radius

    @consume_radius.setter
    def consume_radius(self, value: float) -> None:
        self._consume_radius = value

    @property
    def consume_rate(self) -> float:
        return self._consume_rate

    @consume_rate.setter
    def consume_rate(self, value: float) -> None:
        self._consume_rate = value

    def is_next_level_available(self) -> bool:
        if self._level >= len(self._level_map):
            return False

        next_level_exp_amount = self._level_map[self._level]

        return self._exp >= next_level_exp_amount

    def increase_exp(self, value: float) -> None:
        _value = self._consume_rate * value
        self._exp += _value
        get_current_game().log(f'{self._game_object.name} got {_value}XP')

        while self.is_next_level_available():
            self._exp -= self._level_map[self._level]
            self._level += 1
            get_current_game().log(
                f'{self._game_object.name} got level {self._level}')

    def consume_exp_in_radius(self):
        position_component = self._game_object.require_component(
            PositionComponent)

        for offset in get_points_in_radius(self._consume_radius):
            point = Point(position_component.x + offset.x,
                          position_component.y + offset.y)

            for obj in get_current_game().objects.find_by_position(point.x, point.y):
                if isinstance(obj, ExpConsumable) and not obj.consumed:
                    self.increase_exp(obj.value)
                    obj.consumed = True
                    get_current_game().log(
                        f'{obj.name} has been consumed by {self._game_object.name}')
