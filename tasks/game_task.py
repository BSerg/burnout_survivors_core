from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from mixins.gamed import GameMixin
from mixins.named import NameMixin
from models.game_model import GameModel

if TYPE_CHECKING:
    from game import Game


class GameTask(NameMixin, GameMixin):
    def __init__(self, name: str, game: Game) -> None:
        NameMixin.__init__(self, name)
        GameMixin.__init__(self, game)

    @abstractmethod
    async def update(self) -> GameModel | None:
        pass
