from enum import Enum

from components.component import Component
from objects.game_object import GameObject


class Status(Enum):
    IDLE = 'idle'
    MOVING = 'moving'
    ATTACKING = 'attacking'
    DAMAGED = 'damaged'
    DEAD = 'dead'


class StatusComponent(Component):
    def __init__(self, game_object: GameObject) -> None:
        super().__init__('status_component', game_object)
        self._status: str = Status.IDLE.value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = value

    async def update(self) -> None:
        self._status = Status.IDLE.value