import asyncio
from models.game_model import GameModel, InputType, WaitForModel
from tasks.game_task import GameTask
from game import Game
from objects.player import Player
from tasks.input_task import InputTask
from models.input_model import InputSelectModel
from components.experience_component import ExperienceComponent
from game_context import get_current_game


class PlayerExpTask(InputTask):
    def __init__(self, player: Player) -> None:
        super().__init__('player_exp_task', player)

    def _input_listener(self, input_state: InputSelectModel):
        if input_state.player_name != self._player.name:
            return

        print(input_state.input)
        if input_state.input:
            upgrade = self._player.upgrades.find_by_id(input_state.input)
            print(upgrade)
            if upgrade:
                upgrade.apply()
            
        get_current_game().send_to_output(get_current_game().get_state())

        self.stop_waiting()

    async def update(self) -> GameModel | None:
        exp_component = self._player.require_component(ExperienceComponent)

        level = exp_component.level
        exp_component.consume_exp_in_radius()

        for level in range(exp_component.level - level):
            get_current_game().send_to_output(
                GameModel(wait_for=WaitForModel(type=InputType.POWER_UP, player=self._player.name)))
            await self.wait()

        await self._player.update()
        return get_current_game().get_state()
