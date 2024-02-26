from components.component import Component
from components.vitality_component import VitalityComponent
from game import Game
from objects.player import Player
from objects.upgrades.upgrade import Upgrade


class HealthUpgrade(Upgrade):
    def __init__(self, name: str, player: Player, parent: Upgrade | None, value: float = 0) -> None:
        super().__init__(name, player, parent)
        self._value: float = value

    def can_be_applied(self) -> bool:
        return super().can_be_applied() and self._player.has_component(VitalityComponent)

    def apply(self) -> None:
        super().apply()
        vitality_component = self._player.require_component(VitalityComponent)
        vitality_component.max_health += self._value
        vitality_component.health += self._value


class HealRateUpgrade(Upgrade):
    def __init__(self, name: str, player: Player, parent: Upgrade | None, value: float = 1) -> None:
        super().__init__(name, player, parent)
        self._value = value

    def can_be_applied(self) -> bool:
        return super().can_be_applied() and self._player.has_component(VitalityComponent)

    def apply(self) -> None:
        super().apply()
        vitality_component = self._player.require_component(VitalityComponent)
        vitality_component.heal_rate += self._value
