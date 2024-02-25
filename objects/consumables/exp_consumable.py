from game import Game
from objects.consumables.consumable import Consumable


class ExpConsumable(Consumable):
    def __init__(self, name: str, value: float = 1) -> None:
        super().__init__(name, tags=set(
            ['consumable', 'exp']), value=value)
