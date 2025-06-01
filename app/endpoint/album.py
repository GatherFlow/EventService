
from typing import Any

import fastapi
from datetime import datetime, timedelta

from aiomonobnk.types import InvoiceCreated

from app.enum import CreateEventStatus
from app.model import Event

from app.schema.request import CreateEventRequest
from app.schema.response import CreateEventResponse

from app.database import get_async_session
from app.mono import mono_client

from config import get_settings


member_router = fastapi.APIRouter(prefix="/album")


@member_router.post(
    path="/add",
    response_model=CreateEventResponse,
    description="Create new event",
)
async def create_event(
    data: CreateEventRequest,
    response: fastapi.Response,
) -> CreateEventResponse:

    pass


@member_router.post(
    path="/remove",
    response_model=CreateEventResponse,
    description="Create new event",
)
async def create_event(
    data: CreateEventRequest,
    response: fastapi.Response,
) -> CreateEventResponse:

    pass
