from __future__ import annotations

import asyncio
import random
import uuid
from enum import Enum
from typing import Callable, Type

from game_object_manager import GameObjectManager
from models.game_model import GameModel
from models.input_model import InputModel
from objects.game_object import GameObject
from tasks import GameTask
from game_manager import GameManager


class GameStatus(Enum):
    INIT = 'init',
    RUNNING = 'running',
    STOPPED = 'stopped'


class Game:
    def __init__(self, id: str, seed: str = str(uuid.uuid4())) -> None:
        random.seed(seed)
        self._id: str = id
        self._session: str = seed
        self._status: GameStatus = GameStatus.INIT
        self._tasks: list[GameTask] = list()
        self._current_task: GameTask | None = None
        self._objects: GameObjectManager = GameObjectManager()
        self._input_listeners: list[Callable] = list()
        self._output_listeners: list[Callable] = list()
        self._logs: list[str] = list()

        GameManager.register_game(id, self)

    @property
    def id(self) -> str:
        return self._id

    @property
    def status(self) -> GameStatus:
        return self._status

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
    def objects(self) -> GameObjectManager:
        return self._objects

    # LOG

    @property
    def logs(self) -> list[str]:
        return self._logs

    def log(self, message: str) -> None:
        print(message)  # TODO remove
        self._logs.append(message)

    # END LOG

    # STATE

    def get_state(self) -> GameModel:
        players = [p.get_state() for p in self.objects.find_by_tag('player')]
        enemies = [e.get_state() for e in self.objects.find_by_tag('enemy')]
        consumables = [c.get_state()
                       for c in self.objects.find_by_tag('consumable')]
        return GameModel(players=players, enemies=enemies, consumables=consumables)

    # END STATE

    # LISTENERS

    def add_input_listener(self, listener: Callable[[InputModel], None]):
        if listener not in self._input_listeners:
            self._input_listeners.append(listener)

    def remove_input_listener(self, listener: Callable[[GameModel], None]):
        if listener in self._input_listeners:
            self._input_listeners.remove(listener)

    def send_to_input(self, state: InputModel) -> None:
        for listener in self._input_listeners:
            listener(state)

    def add_output_listener(self, listener: Callable[[GameModel], None]):
        if listener not in self._output_listeners:
            self._output_listeners.append(listener)

    def remove_output_listener(self, listener: Callable[[GameModel], None]):
        if listener in self._output_listeners:
            self._output_listeners.remove(listener)

    def send_to_output(self, state: GameModel) -> None:
        for listener in self._output_listeners:
            listener(state)

    # END LISTENERS

    def instantiate(self, cls: Type[GameObject], *args, **kwargs) -> GameObject:
        game_object = cls(*args, **kwargs)
        self._objects.add(game_object)
        return game_object

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
