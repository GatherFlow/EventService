
import asyncio
from loguru import logger

from sqlalchemy import select, func, update
from app.model import EventTicket, Ticket, Event

from app.database import get_async_session

from config import get_settings


class Updater:
    def __init__(self):
        self.log = logger.bind(classname=self.__class__.__name__)

        self.tasks = [self.calc_stock]
        self.__tasks = []

        self.delay = get_settings().updater.task_delay_seconds

    async def calc_stock(self):
        async with get_async_session() as session:
            event_tickets = (await session.execute(
                select(EventTicket)
            )).scalars().all()

            for event_ticket in event_tickets:
                bought = (await session.execute(
                    select(func.count()).select_from(Ticket).where(Ticket.event_ticket_id == event_ticket.id)
                )).scalar()

                event_ticket.stock = event_ticket.amount - bought
                session.execute(
                    update(EventTicket)
                    .where(EventTicket.id == event_ticket.id)
                )

            await session.commit()

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
