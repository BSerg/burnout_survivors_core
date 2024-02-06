import asyncio
import math
import uuid

from components.component import Component
from models.shared import Point
from objects.game_object import GameObject


def get_uuid() -> str:
    return str(uuid.uuid4())


async def async_input(prompt):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, prompt)
