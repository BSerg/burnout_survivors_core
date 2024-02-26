from __future__ import annotations

from objects.upgrades.upgrade import Upgrade
from objects.game_object import GameObjectGroup

from typing import TYPE_CHECKING, Generator, Any

if TYPE_CHECKING:
    from objects.player import Player


class UpgradeManager(GameObjectGroup[Upgrade]):
    def __init__(self, player: Player) -> None:
        super().__init__('upgrade_manager')
        self._player: Player = player

    def _get_next_upgrades(self, upgrade: Upgrade) -> Generator[Upgrade, Any, None]:
        if upgrade.can_be_applied():
            yield upgrade
        for next_upgrade in upgrade:
            for u in self._get_next_upgrades(next_upgrade):
                yield u

    def get_next_upgrades(self) -> Generator[Upgrade, Any, None]:
        for next_upgrade in self:
            for u in self._get_next_upgrades(next_upgrade):
                yield u

    def get_state(self) -> None:
        return None
