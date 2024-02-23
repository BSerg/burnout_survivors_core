from pydantic import BaseModel


class PointModel(BaseModel):
    x: int
    y: int
