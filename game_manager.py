from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

class GameManager:
    instances: dict[str, Game] = {}

    @classmethod
    def register_game(cls, id: str, game: Game) -> None:
        cls.instances[id] = game
        

    @classmethod
    def get_game(cls, id) -> Game:
        return cls.instances[id]
