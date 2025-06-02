
import fastapi
from datetime import datetime, timezone

from app.enum import ResponseStatus
from app.model import Event

from app.schema.request import CreateTicketRequest, UpdateTicketRequest
from app.schema.response import (
    CreateTicketResponse, UpdateTicketResponse,
    CreateTicketData, UpdateTicketData,
    GetTicketResponse, GetManyTicketResponse,
    GetTicketData
)

from app.database import get_async_session


ticket_router = fastapi.APIRouter(prefix="ticket")


@ticket_router.post(
    path="/",
    response_model=CreateTicketResponse,
    description="Create new ticket",
)
async def create_event(
    data: CreateTicketRequest,
    response: fastapi.Response,
) -> CreateTicketResponse:

    pass


@ticket_router.get(
    path="/",
    response_model=GetTicketResponse,
    description="Create new event",
)
async def create_event(
    id: int,
    response: fastapi.Response,
) -> GetTicketResponse:

    pass


@ticket_router.get(
    path="/",
    response_model=GetTicketResponse,
    description="Create new event",
)
async def create_event(
    id: int,
    response: fastapi.Response,
) -> GetTicketResponse:

    pass


@ticket_router.put(
    path="/update",
    response_model=UpdateTicketResponse,
    description="Update ticket",
)
async def create_event(
    data: UpdateTicketRequest,
    response: fastapi.Response,
) -> UpdateTicketResponse:

    pass
