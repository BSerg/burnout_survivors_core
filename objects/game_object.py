from __future__ import annotations

from typing import Generic, Type, TypeVar

from pydantic import BaseModel

from components.component import Component
from mixins.named import NameMixin
from mixins.serializable import SerializerMixin
from mixins.taged import TagsMixin
from utils.utils import get_uuid

T = TypeVar('T', bound=BaseModel)
C = TypeVar('C', bound=Component)


class GameObject(NameMixin, TagsMixin, SerializerMixin[T]):
    def __init__(self, name: str, tags: set[str] = set(), components: list[Component] = list()) -> None:
        NameMixin.__init__(self, name)
        TagsMixin.__init__(self, tags)
        self._id = get_uuid()
        self._components: list[Component] = components

    @property
    def id(self) -> str:
        return self._id

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


O = TypeVar('O', bound=GameObject)


class GameObjectGroup(GameObject, Generic[O]):
    def __init__(self, name: str, objects: list[O] = list(), *args, **kwargs) -> None:
        super().__init__(name, *args, **kwargs)
        self._objects_by_id: dict[str, O] = dict()
        self._objects_by_name: dict[str, set[O]] = dict()
        self._objects_by_tag: dict[str, set[O]] = dict()
        for obj in objects:
            self.add(obj)

    def add(self, obj: O):
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

    def find_by_id(self, id: str) -> O | None:
        return self._objects_by_id.get(id)

    def find_by_name(self, *names: str) -> set[O]:
        result = None

        for name in names:
            if not result:
                result = self._objects_by_name.get(name, set())
            else:
                result &= self._objects_by_name.get(name, set())

        return result or set()

    def find_by_tag(self, *tags: str) -> set[O]:
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
