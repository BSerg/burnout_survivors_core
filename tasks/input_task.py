import asyncio
from pydantic import BaseModel
from tasks.game_task import GameTask
from game import Game
from objects.player import Player

from typing import Generic, TypeVar

from abc import abstractmethod

T = TypeVar('T')


class InputTask(Generic[T], GameTask):
    def __init__(self, name: str, game: Game, player: Player) -> None:
        super().__init__(name, game)
        self._player: Player = player
        self._waiting: bool = False

    async def wait(self):
        self._game.add_input_listener(self._input_listener)

        self._waiting = True
        while self._waiting:
            await asyncio.sleep(0.1)

        self._game.remove_input_listener(self._input_listener)

    def stop_waiting(self):
        self._waiting = False

    @abstractmethod
    def _input_listener(self, input_state: BaseModel):
        pass
