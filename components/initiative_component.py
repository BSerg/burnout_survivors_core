from typing import Callable

from components.component import Component
from objects.game_object import GameObject


class InitiativeComponent(Component):
    def __init__(self, game_object: GameObject, initiative: float = 1, initiative_accumulator: float = 0) -> None:
        super().__init__('initiative_component', game_object)
        self._initiative: float = initiative
        self._initiative_accumulator: float = initiative_accumulator

    @property
    def initiative(self) -> float:
        return self._initiative

    @initiative.setter
    def initiative(self, value: float) -> None:
        self._initiative = value

    @property
    def initiative_accumulator(self) -> float:
        return self._initiative_accumulator
    
    @initiative_accumulator.setter
    def initiative_accumulator(self, value: float) -> None:
        self._initiative_accumulator = value

    def can_do(self) -> bool:
        return self._initiative_accumulator >= 1

    def do(self, action: Callable) -> None:
        if self.can_do():
            action()
            self._initiative_accumulator -= 1

    async def update(self) -> None:
        self._initiative_accumulator += self._initiative
