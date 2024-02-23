import asyncio
import uuid


def get_uuid() -> str:
    return str(uuid.uuid4())


async def async_input(prompt):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, prompt)
