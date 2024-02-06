from game import Game
from utils.decorators import singleton


@singleton
class GameManager:
    def __init__(self) -> None:
        self._games: dict[str, Game] = dict()

    def find_game(self, id: str) -> Game | None:
        return self._games.get(id)

    def add_game(self, game: Game) -> None:
        if game.id in self._games:
            raise Exception('This ID exists')
        self._games[game.id] = game
