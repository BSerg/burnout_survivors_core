from __future__ import annotations

from typing import TYPE_CHECKING

from objects.game_object import GameObject, GameObjectGroup


if TYPE_CHECKING:
    from objects.player import Player


class Upgrade(GameObjectGroup['Upgrade']):
    def __init__(self, name: str, player: Player, parent: Upgrade | None) -> None:
        super().__init__(name, tags=set(['upgrade']))
        self._player: Player = player
        self._parent: Upgrade | None = parent
        self._applied: bool = False

    @property
    def applied(self) -> bool:
        return self._applied

    def find_by_id(self, id: str) -> Upgrade | None:
        upgrade = super().find_by_id(id)

        if upgrade:
            return upgrade

        for next_upgrade in self:
            upgrade = next_upgrade.find_by_id(id)
            if upgrade:
                return upgrade

    def can_be_applied(self) -> bool:
        if self._parent and not self._parent.applied:
            return False
        return not self._applied

    def apply(self) -> None:
        if not self.can_be_applied():
            return
        self._applied = True

    def get_state(self) -> None:
        return None
