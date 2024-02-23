from pydantic import BaseModel
from models.shared import PointModel


class ConsumableModel(BaseModel):
    name: str
    tags: set[str]
    position: PointModel
    value: float
    consumed: bool


class ConsumableConfig(BaseModel):
    name: str
    type: str
    position: PointModel
    value: float
