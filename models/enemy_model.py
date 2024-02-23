from typing import Optional

from pydantic import BaseModel

from models.shared import PointModel
from models.melee_weapon_model import MeleeWeaponConfig
from models.consumable_model import ConsumableConfig


class EnemyModel(BaseModel):
    name: str
    tags: set[str]
    position: PointModel
    health: float
    max_health: float
    status: str


class EnemyConfig(BaseModel):
    name: str
    tags: set[str]
    position: PointModel
    health: float
    weapon: MeleeWeaponConfig
    initiative: float
    drop_object: Optional[ConsumableConfig]
