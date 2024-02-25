from objects.weapons.weapon import Weapon
from models.melee_weapon_model import MeleeWeaponConfig
from objects.weapons.melee_weapon import MeleeWeapon
from objects.weapons.sword import Sword
from objects.game_object import GameObject
from objects.weapons.teeth import Teeth


def create_weapon(owner: GameObject, config: MeleeWeaponConfig) -> Weapon:
    if config.type == 'sword':
        return Sword(name=f'sword_of_{owner.name}', owner=owner,  damage=config.damage)

    if config.type == 'teeth':
        return Teeth(name=f'teeth_of_{owner.name}', owner=owner,  damage=config.damage)

    raise Exception('Unknown weapon type')
