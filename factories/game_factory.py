from utils.utils import get_uuid
from game import Game
from models.game_model import GameConfig
from factories.player_factory import create_player
from tasks.player_task import PlayerTask
from tasks.enemy_task import EnemyTask
from tasks.player_exp_task import PlayerExpTask


def create_game(config: GameConfig):
    game_id = get_uuid()
    seed = config.seed or get_uuid()
    game = Game(game_id, seed)

    for player_config in config.players:
        player = create_player(game, player_config)
        game.objects.add(player)
        game.tasks += [
            PlayerTask(game, player),
            PlayerExpTask(game, player),
        ]

    game.tasks += [
        EnemyTask(game)
    ]

    return game
