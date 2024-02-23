from __future__ import annotations

from components.component import Component
from components.status_component import Status, StatusComponent
from mixins.upgradable import UpgradableMixin
from objects.game_object import GameObject
from objects.upgrades.health_upgrade import HealRateUpgrade, HealthUpgrade


class VitalityComponent(Component, UpgradableMixin):
    def __init__(self, game_object: GameObject, health: float = 1, heal_rate: float = 1) -> None:
        super().__init__('vitality_component', game_object)
        UpgradableMixin.__init__(self)
        self._max_health = health
        self._health = self.max_health
        self._heal_rate: float = heal_rate

    @property
    def health(self) -> float:
        return self._health

    @health.setter
    def health(self, value: float) -> None:
        self._health = value

    @property
    @UpgradableMixin.modified_by(HealthUpgrade)
    def max_health(self) -> float:
        return self._max_health

    @max_health.setter
    def max_health(self, value: float) -> None:
        self._max_health = value

    @property
    @UpgradableMixin.modified_by(HealRateUpgrade)
    def heal_rate(self) -> float:
        return self._heal_rate

    @property
    def is_dead(self) -> bool:
        return self.health <= 0

    def heal(self, value: float) -> None:
        self._health = min(self.health + self.heal_rate *
                           value, self.max_health)

    def damage(self, value: float) -> None:
        self.health = max(self.health - value, 0)

        status_component = self._game_object.find_component(StatusComponent)
        if status_component:
            status_component.status = Status.DAMAGED.value

        if self._health > 0:
            self._game_object.game.log(
                f'{self._game_object.name} got damage {value}HP')
        else:
            self._game_object.game.log(f'{self._game_object.name} is dead')

    def increase_max_health(self, value: float) -> None:
        self._max_health += value
