from pydantic import BaseModel

from models.shared import Point
from models.melee_weapon_model import MeleeWeaponConfig


class PlayerModel(BaseModel):
    name: str
    tags: set[str]
    position: Point
    health: float
    max_health: float
    experience: float
    level: int
    status: str


class PlayerConfig(BaseModel):
    name: str
    position: Point
    health: float
    initiative: float
    weapon: MeleeWeaponConfig
