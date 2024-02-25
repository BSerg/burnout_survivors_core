from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class UpgradeConfig(BaseModel):
    name: str
    tags: set[str]
    next_upgrades: list[UpgradeConfig]


class HealthUpgradeConfig(UpgradeConfig):
    value: float


class HealRateUpgradeConfig(UpgradeConfig):
    value: float


class ExpConsumeRadiusUpgradeConfig(UpgradeConfig):
    value: float


class ExpConsumeRateUpgradeConfig(UpgradeConfig):
    value: float
