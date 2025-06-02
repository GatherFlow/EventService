
import fastapi
from loguru import logger

from sqlalchemy import select, update

from app.enum import ResponseStatus
from app.model import Ticket

from app.schema.request import CreateTicketRequest
from app.schema.response import (
    CreateTicketResponse, DeleteTicketResponse,
    GetTicketResponse, GetManyTicketResponse,
)
from app.schema.response import (
    CreateTicketData, GetTicketData
)

from app.database import get_async_session


ticket_router = fastapi.APIRouter(prefix="/ticket", tags=["ticket"])


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
            ticket = Ticket(
                event_ticket_id=data.event_ticket_id,
                user_id=data.user_id
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


@ticket_router.delete(
    path="/delete",
    response_model=GetTicketResponse,
    description="Delete ticket",
)
async def delete_ticket(
    id: int,
) -> GetTicketResponse:

    try:
        async with get_async_session() as session:
            ticket = await session.get(Ticket, id)
            await session.delete(ticket)
            await session.commit()

    except Exception as err:
        logger.exception(err)
        return DeleteTicketResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return DeleteTicketResponse()


@ticket_router.get(
    path="/",
    response_model=GetTicketResponse,
    description="Get ticket",
)
async def get_ticket(
    id: int,
) -> GetTicketResponse:

    try:
        async with get_async_session() as session:
            ticket = await session.get(Ticket, id)

    except Exception as err:
        logger.exception(err)
        return GetTicketResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetTicketResponse(
        data=GetTicketData(**ticket.__dict__)
    )


@ticket_router.get(
    path="/many",
    response_model=GetTicketResponse,
    description="Get many tickets",
)
async def get_ticket(
    event_ticket_id: int
) -> GetTicketResponse:

    try:
        async with get_async_session() as session:
            tickets = await session.execute([
                select(Ticket)
                .where(Ticket.event_ticket_id == event_ticket_id)
            ])

    except Exception as err:
        logger.exception(err)
        return GetManyTicketResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetManyTicketResponse(
        data=[
            GetTicketData(**ticket.__dict__)
            for ticket in tickets
        ]
    )
