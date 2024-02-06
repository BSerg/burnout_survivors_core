from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Direction(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'


class InputModel(BaseModel):
    player_name: str
    direction: Optional[Direction]
