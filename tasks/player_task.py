from __future__ import annotations

from typing import TYPE_CHECKING

from components.player_component import PlayerComponent
from models.game_model import GameModel, InputType, WaitForModel
from models.input_model import InputModel
from objects.player import Player
from tasks.input_task import InputTask

if TYPE_CHECKING:
    from game import Game


class PlayerTask(InputTask):
    def __init__(self, game: Game, player: Player) -> None:
        super().__init__('player_task', game, player)

    def _input_listener(self, input_state: InputModel):
        if input_state.player_name != self._player.name:
            return
        self._player.require_component(
            PlayerComponent).direction = input_state.direction
        self.stop_waiting()

    async def update(self):
        self.game.send_to_output(
            GameModel(wait_for=WaitForModel(type=InputType.ACTION, player=self._player.name)))
        await self.wait()
        await self._player.update()
        return self._game.get_state()
