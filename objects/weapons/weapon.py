from abc import abstractmethod

from objects.game_object import GameObject
from game import Game


class Weapon(GameObject):
    def __init__(self, name: str, owner: GameObject, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self._tags = set(['weapon'])
        self._owner = owner

    @property
    def owner(self) -> GameObject:
        return self._owner

    @owner.setter
    def owner(self, value: GameObject) -> None:
        self._owner = value

    @abstractmethod
    def can_attack(self, target: GameObject) -> bool:
        pass

    @abstractmethod
    def attack(self, target: GameObject) -> None:
        pass
