from components.component import Component
from objects.game_object import GameObject


class ExperienceComponent(Component):
    def __init__(self, game_object: GameObject, level_map: list[float] = list()) -> None:
        super().__init__('experience_component', game_object)
        self._exp: float = 0
        self._level: int = 0
        self._level_map: list[float] = level_map

    @property
    def exp(self) -> float:
        return self._exp

    @property
    def level(self) -> int:
        return self._level

    def is_next_level_available(self) -> bool:
        if self._level >= len(self._level_map):
            return False
        next_level_requirement = self._level_map[self._level]
        return self._exp >= next_level_requirement

    def increase_exp(self, value: float) -> None:
        self._exp += value
        if self.is_next_level_available():
            self._exp -= self._level_map[self._level]
            self._level += 1
            self._game_object.updated = True
