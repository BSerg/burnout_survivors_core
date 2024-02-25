from game_context import game_context
from utils.utils import get_uuid
from game import Game
from models.game_model import GameConfig
from factories.player_factory import create_player
from tasks.player_task import PlayerTask
from tasks.enemy_task import EnemyTask
from tasks.player_exp_task import PlayerExpTask

import random
from factories.enemy_factory import create_enemy
from components.ai_component import AiComponent
from models.shared import PointModel


def create_game(config: GameConfig):
    game_id = get_uuid()
    seed = config.seed or get_uuid()
    game = Game(game_id, seed)

    game_context.set(game)

    for player_config in config.players:
        player = create_player(player_config)
        game.objects.add(player)
        game.tasks += [
            PlayerTask(player),
            PlayerExpTask(player),
        ]

    game.tasks += [
        EnemyTask()
    ]

    # TODO delete

    for _ in range(3):
        for enemy_config in config.enemies:
            enemy_config_copy = enemy_config.model_copy()
            enemy_config_copy.position = PointModel(x=random.randint(-5, 5),
                                                    y=random.randint(-5, 5))
            enemy = create_enemy(enemy_config_copy)
            enemy.require_component(AiComponent).target = player
            game.objects.add(enemy)

    return game
