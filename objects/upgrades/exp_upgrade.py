from objects.player import Player
from objects.upgrades.upgrade import Upgrade
from components.experience_component import ExperienceComponent


class ExpConsumeRadiusUpgrade(Upgrade):
    def __init__(self, name: str, player: Player, parent: Upgrade | None, value: float) -> None:
        super().__init__(name, player, parent)
        self._value = value

    def can_be_applied(self) -> bool:
        return super().can_be_applied() and self._player.has_component(ExperienceComponent)

    def apply(self) -> None:
        super().apply()
        self._player.require_component(
            ExperienceComponent).consume_radius += self._value


class ExpConsumeRateUpgrade(Upgrade):
    def __init__(self, name: str, player: Player, parent: Upgrade | None, value: float) -> None:
        super().__init__(name, player, parent)
        self._value = value

    def can_be_applied(self) -> bool:
        return super().can_be_applied() and self._player.has_component(ExperienceComponent)

    def apply(self) -> None:
        super().apply()
        self._player.require_component(
            ExperienceComponent).consume_rate += self._value
