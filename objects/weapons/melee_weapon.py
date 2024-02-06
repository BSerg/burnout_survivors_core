from components.position_component import PositionComponent
from components.status_component import Status, StatusComponent
from components.vitality_component import VitalityComponent
from game import Game
from models.melee_weapon_model import MeleeWeaponModel
from objects.game_object import GameObject
from objects.weapons.weapon import Weapon
from utils.game import get_distance_between


class MeleeWeapon(Weapon):
    def __init__(self, name: str, game: Game, owner: GameObject, damage: float = 1, **kwargs) -> None:
        super().__init__(name, game, owner, **kwargs)
        self._damage = damage

    @property
    def damage(self) -> float:
        return self._damage

    def can_attack(self, target: GameObject) -> bool:
        target_status = target.requireComponent(StatusComponent).status

        if target_status == Status.DEAD:
            return False

        target_position = target.requireComponent(PositionComponent).position
        position = self.owner.requireComponent(PositionComponent).position

        return get_distance_between(position, target_position) <= 1

    def attack(self, target: GameObject) -> None:
        if not self.can_attack(target):
            return

        target_vitality_component = target.requireComponent(VitalityComponent)
        target_vitality_component.damage(self._damage)

    def get_state(self) -> MeleeWeaponModel:
        return MeleeWeaponModel(name=self.name, tags=self.tags, damage=self._damage)

    async def update(self) -> None:
        return None
