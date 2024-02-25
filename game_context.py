from __future__ import annotations

from contextvars import ContextVar

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


game_context = ContextVar('game')


def get_game() -> Game:
    return game_context.get()
