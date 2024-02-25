from __future__ import annotations

from abc import abstractmethod

from mixins.named import NameMixin
from models.game_model import GameModel


class GameTask(NameMixin):
    def __init__(self, name: str) -> None:
        NameMixin.__init__(self, name)

    @abstractmethod
    async def update(self) -> GameModel | None:
        pass
