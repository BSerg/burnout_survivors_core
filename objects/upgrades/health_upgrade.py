from components.component import Component
from game import Game
from objects.upgrades.upgrade import Upgrade


class HealthUpgrade(Upgrade):
    def __init__(self, game: Game, modificator: float = 1) -> None:
        super().__init__('health_upgrade', game, set(['upgrade', 'health']))
        self._modificator = modificator

    @property
    def modificator(self) -> float:
        return self._modificator

    def modify(self, value: float):
        return self._modificator * value


class HealRateUpgrade(Upgrade):
    def __init__(self, game: Game, modificator: float = 1) -> None:
        super().__init__('heal_rate_upgrade',
                         game, set(['upgrade', 'heal_rate']))
        self._modificator = modificator

    @property
    def modificator(self) -> float:
        return self._modificator

    def modify(self, value: float):
        return self._modificator * value
