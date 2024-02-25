from __future__ import annotations

from objects.upgrades.upgrade import Upgrade
from objects.game_object import GameObjectGroup

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.player import Player


class UpgradeManager(GameObjectGroup[Upgrade]):
    def __init__(self, player: Player) -> None:
        super().__init__('upgrade_manager')
        self._player: Player = player

    def get_state(self) -> None:
        return None
