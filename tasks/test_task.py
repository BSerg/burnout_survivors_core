from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from components.initiative_component import InitiativeComponent
from components.player_input_component import PlayerInputComponent
from models.game_model import GameModel, WaitForModel
from models.input_model import InputModel
from objects.player import Player
from tasks import GameTask

if TYPE_CHECKING:
    from game import Game


class TestEnemyTask(GameTask):
    def __init__(self, game: Game) -> None:
        super().__init__('test_enemy_task', game)

    async def update(self):
        enemies = self.game.objects.find_by_tag('enemy')
        for enemy in enemies:
            await enemy.update()
        return self._game.get_state()


class TestPlayerInputTask(GameTask):
    def __init__(self, game: Game, player: Player) -> None:
        super().__init__('test_player_input_task', game)
        self._player: Player = player
        self._wait_for_input: bool = False
        self._game.on_input(self._input_listener)

    def _input_listener(self, input_state: InputModel):
        if input_state.player_name != self._player.name:
            return

        self._player.require_component(
            PlayerInputComponent).direction = input_state.direction

        self._wait_for_input = False

    async def wait_for_input(self):
        self._wait_for_input = True
        while True:
            await asyncio.sleep(0.1)
            if not self._wait_for_input:
                break

    async def update(self):
        initiative_cmp = self._player.require_component(InitiativeComponent)

        while initiative_cmp.can_do():
            self.game.send_to_output(
                GameModel(wait_for=WaitForModel(player=self._player.name)))

            await self.wait_for_input()

            def act():
                self.game.send_to_output(self._game.get_state())

            initiative_cmp.do(act)

        await self._player.update()
