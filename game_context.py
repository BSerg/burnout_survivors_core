from __future__ import annotations

from contextvars import ContextVar, Token
from typing import TYPE_CHECKING

from game_manager import GameManager

if TYPE_CHECKING:
    from game import Game


game_id = ContextVar('game_id')


class GameContext:
    def __init__(self, game_id: str) -> None:
        self._game_id = game_id
        self._token: Token

    def __enter__(self):
        self._token = game_id.set(self._game_id)
        return game_id.get()

    def __exit__(self, exc_type, exc_val, exc_tb):
        game_id.reset(self._token)

    @staticmethod
    def get_game_id():
        return game_id.get()


def get_game() -> Game:
    return GameManager.get_game(game_id.get())
