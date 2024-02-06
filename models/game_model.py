from pydantic import BaseModel

from models.enemy_model import EnemyModel
from models.player_model import PlayerConfig, PlayerModel
from typing import Optional

class WaitForModel(BaseModel):
    player: str
    timeout: Optional[int] = None

class GameModel(BaseModel):
    turn: Optional[int] = None
    wait_for: Optional[WaitForModel] = None
    players: Optional[list[PlayerModel]] = None
    enemies: Optional[list[EnemyModel]] = None


class GameConfig(BaseModel):
    seed: Optional[str]
    players: list[PlayerConfig]
