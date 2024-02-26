from components.component import Component
from objects.game_object import GameObject
from objects.weapons.weapon import Weapon
from components.status_component import Status, StatusComponent
from game_context import get_current_game


class MeleeComponent(Component):
    def __init__(self, game_object: GameObject, weapon: Weapon | None = None) -> None:
        super().__init__('attack_component', game_object)
        self._weapon: Weapon | None = weapon
        if self._weapon:
            self._weapon.owner = self._game_object

    @property
    def weapon(self) -> GameObject | None:
        return self._weapon

    @weapon.setter
    def weapon(self, value: Weapon) -> None:
        self._weapon = value
        self._weapon.owner = self._game_object

    def can_attack(self, target: GameObject) -> bool:
        if not self._weapon:
            return False
        return self._weapon.can_attack(target)

    def attack(self, target: GameObject) -> None:
        if self._weapon:
            self._weapon.attack(target)

            status_component = self._game_object.find_component(
                StatusComponent)
            if status_component:
                status_component.status = Status.ATTACKING.value

            get_current_game().log(
                f'{self.game_object.name} attacks {target.name} with {self._weapon.name}')

    async def update(self) -> None:
        if self._weapon:
            await self._weapon.update()
