from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


class GameMixin(ABC):
    def __init__(self, game: Game) -> None:
        self._game = game

    @property
    def game(self) -> Game:
        return self._game
