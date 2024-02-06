from objects.weapons.melee_weapon import MeleeWeapon


class Sword(MeleeWeapon):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._tags = set(['weapon', 'sword'])
