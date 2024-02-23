import uuid
from abc import ABC


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
