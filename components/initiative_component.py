import random

from components.component import Component
from objects.game_object import GameObject


class InitiativeComponent(Component):
    def __init__(self, game_object: GameObject, initiative: float = 1) -> None:
        super().__init__('initiative_component', game_object)
        self._initiative: float = min(initiative, 1)

    @property
    def initiative(self) -> float:
        return self._initiative

    @initiative.setter
    def initiative(self, value: float) -> None:
        self._initiative = value

    def can_do(self) -> bool:
        return random.random() <= self._initiative
