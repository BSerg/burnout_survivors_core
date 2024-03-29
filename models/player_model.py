from pydantic import BaseModel

from models.melee_weapon_model import MeleeWeaponConfig
from models.shared import PointModel
from models.upgrade_model import UpgradeConfig


class PlayerModel(BaseModel):
    name: str
    tags: set[str]
    position: PointModel
    health: float
    max_health: float
    vision_radius: float
    experience: float
    level: int
    status: str


class PlayerConfig(BaseModel):
    name: str
    position: PointModel
    health: float
    exp_level_map: list[float]
    exp_consume_radius: float
    vision_radius: float
    weapon: MeleeWeaponConfig
    upgrades: list[UpgradeConfig]
