from typing import Optional

from pydantic import BaseModel

from models.shared import Point
from models.melee_weapon_model import MeleeWeaponConfig


class EnemyModel(BaseModel):
    name: str
    tags: set[str]
    position: Point
    health: float
    max_health: float
    status: str


class EnemyConfig(BaseModel):
    name: str
    tags: set[str]
    position: Point
    health: float
    weapon: MeleeWeaponConfig
    initiative: float
