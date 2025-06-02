
import fastapi
from loguru import logger

from sqlalchemy import select, update

from app.enum import ResponseStatus
from app.model import EventTicket

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
    path="/create",
    response_model=CreateTicketResponse,
    description="Create new event ticket",
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
        data=GetTicketData(**ticket.__dict__)
    )


@ticket_router.put(
    path="/update",
    response_model=UpdateTicketResponse,
    description="Update ticket",
)
async def create_event(
    data: UpdateTicketRequest,
    response: fastapi.Response,
) -> UpdateTicketResponse:

    try:
        async with get_async_session() as session:
            data_dict = data.model_dump()

            await session.execute(
                update(EventTicket)
                .where(EventTicket.id == data.id)
                .values(**{
                    key: data_dict[key]
                    for key in data_dict if key not in ["id"] and data_dict.get(key)
                })
                .execution_options(synchronize_session="fetch")
            )

            await session.commit()

    except Exception as err:
        logger.exception(err)
        return UpdateTicketResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return UpdateTicketResponse(
        data=UpdateTicketData(
            id=data.id
        )
    )


@ticket_router.get(
    path="/many",
    response_model=GetManyTicketResponse,
    description="Get many event tickets",
)
async def create_event(
    event_id: int
) -> GetManyTicketResponse:

    try:
        async with get_async_session() as session:
            tickets = (await session.execute(
                select(EventTicket)
                .where(EventTicket.event_id == event_id)
            )).scalars().all()

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
