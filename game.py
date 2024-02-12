import asyncio
import random
import uuid
from enum import Enum
from typing import Any, Callable

from pydantic import BaseModel

from components.position_component import PositionComponent
from models.game_model import GameModel
from models.input_model import InputModel
from models.shared import Point
from objects.game_object import GameObjectGroup
from tasks import GameTask


class GameStatus(Enum):
    INIT = 'init',
    RUNNING = 'running',
    STOPPED = 'stopped'


class GameObjects(GameObjectGroup):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('object_pool', *args, **kwargs)

    def findObjectsByPosition(self, position: Point):
        for object in self.game.objects:
            position_component = object.find_component(PositionComponent)
            if position_component and position_component.position == position:
                yield object

    def get_state(self) -> Any:
        # TODO return state
        return None


class Game:
    def __init__(self, id: str, seed: str = str(uuid.uuid4())) -> None:
        random.seed(seed)
        self._id: str = id
        self._session: str = seed
        self._status: GameStatus = GameStatus.INIT
        self._tasks: list[GameTask] = list()
        self._current_task: GameTask | None = None
        self._objects: GameObjects = GameObjects(self)
        self._input_listeners: list[Callable] = list()
        self._output_listeners: list[Callable] = list()
        self._logs: list[str] = list()

    @property
    def id(self) -> str:
        return self._id

    @property
    def status(self) -> GameStatus:
        return self._status

    @property
    def objects(self) -> GameObjects:
        return self._objects

    @property
    def tasks(self):
        return self._tasks

    @tasks.setter
    def tasks(self, value: list[GameTask]):
        self._tasks = value

    @property
    def current_task(self):
        return self._current_task

    @property
    def logs(self) -> list[str]:
        return self._logs

    def log(self, message: str) -> None:
        self._logs.append(message)

    def get_state(self, updated_only: bool = True) -> GameModel:
        if updated_only:
            players = [p.get_state()
                       for p in self.objects.find_by_tag('player') if p.updated]
            enemies = [e.get_state()
                       for e in self.objects.find_by_tag('enemy') if e.updated]
            return GameModel(players=players, enemies=enemies)

        players = [p.get_state() for p in self.objects.find_by_tag('player')]
        enemies = [e.get_state() for e in self.objects.find_by_tag('enemy')]
        return GameModel(players=players, enemies=enemies)

    def on_input(self, listener: Callable[[InputModel], None]):
        if listener not in self._input_listeners:
            self._input_listeners.append(listener)

    def on_output(self, listener: Callable[[GameModel], None]):
        if listener not in self._output_listeners:
            self._output_listeners.append(listener)

    def send_to_input(self, state: InputModel) -> None:
        for listener in self._input_listeners:
            listener(state)

    def send_to_output(self, state: GameModel) -> None:
        for listener in self._output_listeners:
            listener(state)

    async def _run(self):
        if not len(self._tasks):
            raise Exception('Game does not have any tasks')

        index = 0
        while True:
            index %= len(self._tasks)
            self._current_task = self._tasks[index]
            state = await self._current_task.update()
            if state:
                self.send_to_output(state)
            index += 1

    async def run(self):
        self._run_coroutine = asyncio.create_task(self._run())
        try:
            self._status = GameStatus.RUNNING
            await self._run_coroutine
            print(f"Game {self._session} has been started")
        except asyncio.CancelledError:
            self._status = GameStatus.STOPPED
            print(f"Game {self._session} has been stopped")

    async def stop(self):
        if self._run_coroutine:
            self._run_coroutine.cancel()
