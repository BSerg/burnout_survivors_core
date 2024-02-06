from __future__ import annotations

from typing import TYPE_CHECKING

from mixins.named import NameMixin

if TYPE_CHECKING:
    from objects.game_object import GameObject


class Component(NameMixin):
    _game_object: GameObject

    def __init__(self, name: str, game_object: GameObject) -> None:
        super().__init__(name)
        self._game_object = game_object

    @property
    def game_object(self) -> GameObject:
        return self._game_object

    async def update(self) -> None:
        return None
