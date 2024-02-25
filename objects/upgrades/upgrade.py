from __future__ import annotations

from typing import TYPE_CHECKING

from objects.game_object import GameObject


if TYPE_CHECKING:
    from objects.player import Player


class Upgrade(GameObject):
    def __init__(self, name: str, player: Player, tags: set[str]) -> None:
        super().__init__(name, tags=tags)
        self._player: Player = player
        self._applied: bool = False
        self._next_upgrades: list[Upgrade] = list()

    @property
    def next_upgrades(self) -> list[Upgrade]:
        return self._next_upgrades

    @next_upgrades.setter
    def next_upgrades(self, value: list[Upgrade]) -> None:
        self._next_upgrades = value

    def can_be_applied(self) -> bool:
        return not self._applied

    def apply(self) -> None:
        if not self.can_be_applied():
            return
        self._applied = True

    def get_state(self) -> None:
        return None
