from objects.weapons.melee_weapon import MeleeWeapon


class Teeth(MeleeWeapon):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._tags = set(['weapon', 'teeth'])
