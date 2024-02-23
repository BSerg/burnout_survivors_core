from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar, Iterator, Generator, Any

from pydantic import BaseModel

from components.component import Component
from mixins.gamed import GameMixin
from mixins.named import NameMixin
from mixins.serializable import SerializerMixin
from mixins.taged import TagsMixin
from utils.utils import get_uuid

if TYPE_CHECKING:
    from game import Game

T = TypeVar('T', bound=BaseModel)
C = TypeVar('C', bound=Component)


class GameObject(NameMixin, GameMixin, TagsMixin, SerializerMixin[T]):
    def __init__(self, name: str, game: Game, tags: set[str] = set(), components: list[Component] = list()) -> None:
        NameMixin.__init__(self, name)
        GameMixin.__init__(self, game)
        TagsMixin.__init__(self, tags)
        self._id = get_uuid()
        self._components: list[Component] = components

    @property
    def id(self) -> str:
        return self._id

    @property
    def game(self) -> Game:
        return self._game

    @property
    def components(self) -> list[Component]:
        return self._components

    def has_component(self, cls: Type[C]) -> bool:
        return cls in [type(c) for c in self._components]

    def find_component(self, cls: Type[C]) -> C | None:
        for component in self._components:
            if isinstance(component, cls):
                return component

    def require_component(self, cls: Type[C]) -> C:
        component = self.find_component(cls)
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
        self._objects_by_id: dict[str, GameObject] = dict()
        self._objects_by_name: dict[str, set[GameObject]] = dict()
        self._objects_by_tag: dict[str, set[GameObject]] = dict()
        for obj in objects:
            self.add(obj)

    def add(self, obj: GameObject):
        self._objects_by_id[obj.id] = obj

        if obj.name not in self._objects_by_name:
            self._objects_by_name[obj.name] = set([obj])
        else:
            self._objects_by_name[obj.name].add(obj)

        for tag in obj.tags:
            if tag not in self._objects_by_tag:
                self._objects_by_tag[tag] = set([obj])
            else:
                self._objects_by_tag[tag].add(obj)

    def remove(self, id: str):
        if id in self._objects_by_id:
            obj = self._objects_by_id[id]
            self._objects_by_name[obj.name].remove(obj)
            for tag in obj.tags:
                self._objects_by_tag[tag].remove(obj)
            del obj

    def find_by_id(self, id: str) -> GameObject | None:
        return self._objects_by_id.get(id)

    def find_by_name(self, *names: str) -> set[GameObject]:
        result = None

        for name in names:
            if not result:
                result = self._objects_by_name.get(name, set())
            else:
                result &= self._objects_by_name.get(name, set())

        return result or set()

    def find_by_tag(self, *tags: str) -> set[GameObject]:
        result = None

        for tag in tags:
            if not result:
                result = self._objects_by_tag.get(tag, set())
            else:
                result &= self._objects_by_tag.get(tag, set())

        return result or set()

    def __iter__(self):
        for obj in self._objects_by_id.values():
            yield obj
