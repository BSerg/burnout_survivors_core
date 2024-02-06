from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class SerializerMixin(Generic[T], ABC):
    @abstractmethod
    def get_state(self) -> T:
        pass
