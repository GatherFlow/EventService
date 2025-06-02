
import fastapi
from loguru import logger

from sqlalchemy import select, update

from app.enum import ResponseStatus
from app.model import EventTicket

from app.schema.request import CreateTicketRequest
from app.schema.response import (
    CreateTicketResponse, DeleteTicketResponse,
    GetTicketResponse, GetManyTicketResponse,
    GetEventTicketData
)

from app.database import get_async_session


ticket_router = fastapi.APIRouter()


@ticket_router.post(
    path="/create",
    response_model=CreateTicketResponse,
    description="Create new ticket",
)
async def create_ticket(
    data: CreateTicketRequest,
) -> CreateTicketResponse:

    try:
        async with get_async_session() as session:
            ticket = EventTicket(
                event_id=data.event_id,
                title=data.title,
                description=data.description,
                price=data.price,
                amount=data.amount,
                stock=data.stock
            )
            session.add(ticket)
            await session.commit()

    except Exception as err:
        logger.exception(err)
        return CreateTicketResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return CreateTicketResponse(
        data=CreateTicketData(
            id=ticket.id
        )
    )


@ticket_router.get(
    path="/",
    response_model=GetTicketResponse,
    description="Get event ticket",
)
async def get_ticket(
    id: int,
) -> GetTicketResponse:

    try:
        async with get_async_session() as session:
            ticket = await session.get(EventTicket, id)

    except Exception as err:
        logger.exception(err)
        return GetTicketResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetTicketResponse(
        data=GetEventTicketData(**ticket.__dict__)
    )


@ticket_router.get(
    path="/",
    response_model=GetTicketResponse,
    description="Get many tickets",
)
async def get_ticket(
    id: int,
) -> GetTicketResponse:

    try:
        async with get_async_session() as session:
            ticket = await session.get(EventTicket, id)

    except Exception as err:
        logger.exception(err)
        return GetTicketResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetTicketResponse(
        data=GetEventTicketData(**ticket.__dict__)
    )
