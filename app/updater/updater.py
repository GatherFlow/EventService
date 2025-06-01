
import asyncio
from loguru import logger

from config import get_settings


class Updater:
    def __init__(self):
        self.log = logger.bind(classname=self.__class__.__name__)

        self.tasks = []
        self.__tasks = []

        self.delay = get_settings().updater.task_delay_seconds

    async def task_wrapper(self, func):
        while True:
            try:
                await func()

            except Exception as err:
                self.log.error(f"Occurred error with {func.__name__} -> {err}")
                self.log.exception(err)

            await asyncio.sleep(self.delay)

    async def start(self):
        self.log.info(f"Starting updater tasks")

        for task in self.tasks:
            self.tasks.append(asyncio.create_task(self.task_wrapper(task)))
            self.log.info(f"Started task -> {task.__name__}")
