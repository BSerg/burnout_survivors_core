from __future__ import annotations

from abc import ABC
from typing import Generic, Type, TypeVar

from objects.upgrades.upgrade import Upgrade

U = TypeVar('U', bound=Upgrade)


class UpgradableMixin(ABC, Generic[U]):
    def __init__(self) -> None:
        super().__init__()
        self._upgrades: list[Upgrade] = []

    @staticmethod
    def modified_by(upgrade_class: Type[U]):
        def decorator(fn):
            def wrapper(self, *args, **kwargs):
                value = fn(self, *args, **kwargs)
                for u in self._upgrades:
                    if isinstance(u, upgrade_class):
                        value = u.modify(value)
                return value
            return wrapper
        return decorator

    @property
    def upgrades(self) -> list[Upgrade]:
        return self._upgrades

    def add_upgrade(self, upgrade: Upgrade) -> None:
        self.upgrades.append(upgrade)
