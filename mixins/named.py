from abc import ABC
from contextvars import ContextVar
import uuid

unique_name_pool = ContextVar('name_pool', default=set())


class NameMixin(ABC):
    _name: str

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self):
        return self._name

    @staticmethod
    def generate_name():
        return str(uuid.uuid4())


class UniqueNameMixin(NameMixin):
    def __init__(self, name: str) -> None:
        super().__init__(name)

        name_pool = unique_name_pool.get()

        if (name in name_pool):
            raise Exception('Name is not unique')
        
        name_pool.add(name)
