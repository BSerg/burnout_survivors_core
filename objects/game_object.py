from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar

from pydantic import BaseModel

from components.component import Component
from mixins.gamed import GameMixin
from mixins.named import UniqueNameMixin
from mixins.serializable import SerializerMixin
from mixins.taged import TagsMixin

if TYPE_CHECKING:
    from game import Game

T = TypeVar('T', bound=BaseModel)
C = TypeVar('C', bound=Component)


class GameObject(UniqueNameMixin, GameMixin, TagsMixin, SerializerMixin[T]):
    def __init__(self, name: str, game: Game, tags: set[str] = set(), components: list[Component] = list()) -> None:
        UniqueNameMixin.__init__(self, name)
        GameMixin.__init__(self, game)
        TagsMixin.__init__(self, tags)
        self._components: list[Component] = components
        self._updated: bool = False

    @property
    def game(self) -> Game:
        return self._game

    @property
    def components(self) -> list[Component]:
        return self._components

    @property
    def updated(self) -> bool:
        return self._updated

    @updated.setter
    def updated(self, value: bool) -> None:
        self._updated = value

    def findComponent(self, cls: Type[C]) -> C | None:
        for component in self._components:
            if isinstance(component, cls):
                return component

    def requireComponent(self, cls: Type[C]) -> C:
        component = self.findComponent(cls)
        if not component:
            raise Exception(f'{cls.__name__} is required')
        return component

    async def update(self) -> None:
        self._updated = False
        for component in self._components:
            await component.update()


class GameObjectGroup(GameObject[T]):
    def __init__(self, name: str, game: Game, objects: list[GameObject] = list(), *args, **kwargs) -> None:
        super().__init__(name, game, *args, **kwargs)
        self._objects_by_name: dict[str, GameObject] = dict()
        self._objects_by_tag: dict[str, set[GameObject]] = dict()
        for obj in objects:
            self.add(obj)

    def add(self, obj: GameObject):
        self._objects_by_name[obj.name] = obj
        for tag in obj.tags:
            if tag not in self._objects_by_tag:
                self._objects_by_tag[tag] = set([obj])
            else:
                self._objects_by_tag[tag].add(obj)

    def remove(self, name: str):
        if name in self._objects_by_name:
            obj = self._objects_by_name[name]
            for tag in obj.tags:
                self._objects_by_tag[tag].remove(obj)
            del obj

    def findByName(self, name: str) -> GameObject | None:
        return self._objects_by_name.get(name)

    def findByTag(self, tag: str) -> set[GameObject]:
        return self._objects_by_tag.get(tag) or set()

    def __iter__(self):
        for obj in self._objects_by_name.values():
            yield obj
