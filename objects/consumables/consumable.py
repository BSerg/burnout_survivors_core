from components.position_component import PositionComponent
from game import Game
from models.consumable_model import ConsumableModel
from objects.game_object import GameObject


class Consumable(GameObject[ConsumableModel]):
    def __init__(self, name: str, tags: set[str] = set(['consumable']), value: float = 1) -> None:
        super().__init__(name, tags, components=[
            PositionComponent(self),
        ])
        self._value: float = value
        self._consumed: bool = False

    @property
    def value(self) -> float:
        return self._value

    @property
    def consumed(self) -> bool:
        return self._consumed

    @consumed.setter
    def consumed(self, value: bool) -> None:
        self._consumed = value

    def get_state(self) -> ConsumableModel:
        return ConsumableModel(
            name=self.name,
            tags=self.tags,
            position=self.require_component(
                PositionComponent).position.get_state(),
            value=self.value,
            consumed=self._consumed
        )
