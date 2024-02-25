from __future__ import annotations

from typing import TYPE_CHECKING

from tasks import GameTask
from game_context import get_game

if TYPE_CHECKING:
    from game import Game


class EnemyTask(GameTask):
    def __init__(self) -> None:
        super().__init__('enemy_task')

    def _sort_by_distance_to_player(self):
        pass

    async def update(self):
        enemies = get_game().objects.find_by_tag('enemy')

        for enemy in enemies:
            await enemy.update()

        return get_game().get_state()
