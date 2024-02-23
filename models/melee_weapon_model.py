from pydantic import BaseModel


class MeleeWeaponModel(BaseModel):
    name: str
    tags: set[str]
    damage: float


class MeleeWeaponConfig(BaseModel):
    type: str
    damage: float
