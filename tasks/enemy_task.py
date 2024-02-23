from __future__ import annotations

from typing import TYPE_CHECKING

from tasks import GameTask

if TYPE_CHECKING:
    from game import Game


class EnemyTask(GameTask):
    def __init__(self, game: Game) -> None:
        super().__init__('enemy_task', game)

    def _sort_by_distance_to_player(self):
        pass

    async def update(self):
        enemies = self.game.objects.find_by_tag('enemy')

        for enemy in enemies:
            await enemy.update()

        return self._game.get_state()
