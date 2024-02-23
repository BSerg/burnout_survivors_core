from game import Game
from objects.consumable.consumable import Consumable


class HealthConsumable(Consumable):
    def __init__(self, name: str, game: Game, value: float = 1) -> None:
        super().__init__(name, game, tags=set(
            ['consumable', 'health']), value=value)
