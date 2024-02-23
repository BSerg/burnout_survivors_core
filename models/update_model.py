from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class HealthUpdateConfig(BaseModel):
    health_modificator: float


class ExpUpdateConfig(BaseModel):
    consume_radius: Optional[float] = 1
    consume_rate: Optional[float] = 1
