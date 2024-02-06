from utils.utils import get_uuid
from game import Game
from tasks.test_task import TestPlayerInputTask, TestEnemyTask
from models.game_model import GameConfig, GameModel
from factories.player_factory import create_player


def create_game(config: GameConfig):
    game_id = get_uuid()
    seed = config.seed or get_uuid()
    game = Game(game_id, seed)

    for player_config in config.players:
        player = create_player(game, player_config)
        game.objects.add(player)
        game.tasks.append(TestPlayerInputTask(game, player))

    game.tasks += [
        TestEnemyTask(game)
    ]

    return game
