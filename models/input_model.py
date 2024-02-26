from enum import Enum
from typing import Optional, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')

class Direction(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'


class InputModel(BaseModel, Generic[T]):
    player_name: str
    input: Optional[T]

class InputActionModel(InputModel[Direction]):
    player_name: str


class InputSelectModel(InputModel[str]):
    player_name: str
