import asyncio
from models.game_model import GameModel
from tasks.game_task import GameTask
from game import Game
from objects.player import Player
from tasks.input_task import InputTask
from models.input_model import InputModel
from components.experience_component import ExperienceComponent


class PlayerExpTask(InputTask):
    def __init__(self, game: Game, player: Player) -> None:
        super().__init__('player_exp_task', game, player)

    def _input_listener(self, input_state: InputModel):
        if input_state.player_name != self._player.name:
            return

        # TODO select powerup

        self._game.send_to_output(self._game.get_state())

        self.stop_waiting()

    async def update(self) -> GameModel | None:
        exp_component = self._player.require_component(ExperienceComponent)

        level = exp_component.level
        exp_component.consume_exp_in_radius()

        for level in range(exp_component.level - level):
            await self.wait()

        await self._player.update()
        return self._game.get_state()
