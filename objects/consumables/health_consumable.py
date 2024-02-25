from game import Game
from objects.consumables.consumable import Consumable


class HealthConsumable(Consumable):
    def __init__(self, name: str, value: float = 1) -> None:
        super().__init__(name, tags=set(
            ['consumable', 'health']), value=value)
