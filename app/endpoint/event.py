from enum import member

import fastapi
from loguru import logger
from sqlalchemy import update, select
from sqlalchemy.orm import Mapped

from app.enum import MemberRole, ResponseStatus
from app.model import Event, Member, EventSettings

from app.schema.request import (
    CreateEventRequest, UpdateEventRequest,
    GetEventRequest, GetMyEventsRequest)
from app.schema.response import (
    CreateEventResponse, UpdateEventResponse,
    GetEventResponse, GetMyEventsResponse
)
from app.schema.response import (
    CreateEventData, UpdateEventData,
    GetEventData
)

from app.database import get_async_session


event_router = fastapi.APIRouter()


@event_router.post(
    path="/create",
    response_model=CreateEventResponse,
    description="Create new event",
)
async def create_event(
    data: CreateEventRequest,
    request: fastapi.Request
) -> CreateEventResponse:

    try:
        async with get_async_session() as session:
            event = Event(
                title=data.title,
                description=data.description,
                duration=data.duration,
                format=data.format,
                meeting_link=data.meeting_link,
                location=data.location,
                announced_at=data.announced_at
            )
            session.add(event)
            await session.flush()

            settings = EventSettings(
                event_id=event.id
            )
            session.add(settings)
            await session.flush()

            member = Member(
                event_id=event.id,
                user_id=request.state.user_id,
                role=MemberRole.owner
            )

            session.add(member)
            await session.commit()

    except Exception as err:
        logger.exception(err)
        return UpdateEventResponse(status=ResponseStatus.unexpected_error)

    return CreateEventResponse(
        data=CreateEventData(
            id=event.id
        )
    )


@event_router.post(
    path="/update",
    response_model=UpdateEventResponse,
    description="Update event",
)
async def update_event(
    data: UpdateEventRequest,
    response: fastapi.Response,
) -> UpdateEventResponse:

    try:
        async with get_async_session() as session:
            data_dict = data.model_dump()

            await session.execute(
                update(Event)
                .where(Event.id == data.id)
                .values(**{
                    key: data_dict[key]
                    for key in data_dict if key not in ["id"] and data_dict.get(key)
                })
                .execution_options(synchronize_session="fetch")
            )

            await session.commit()

    except Exception as err:
        logger.exception(err)
        return UpdateEventResponse(status=ResponseStatus.unexpected_error)

    return UpdateEventResponse(
        data=UpdateEventData(
            id=data.id
        )
    )


@event_router.get(
    path="/",
    response_model=GetEventResponse,
    description="Get event",
)
async def create_event(
    data: GetEventRequest,
) -> CreateEventResponse:

    try:
        async with get_async_session() as session:
            event = await session.get(Event, data.id)

    except Exception as err:
        logger.exception(err)
        return GetEventResponse(status=ResponseStatus.unexpected_error)

    return GetEventResponse(
        data=GetEventData(**event.__dict__)
    )


@event_router.get(
    path="/my",
    response_model=GetMyEventsResponse,
    description="Get my events",
)
async def create_event(
    data: GetMyEventsRequest,
    request: fastapi.Request,
) -> GetMyEventsResponse:

    try:
        async with get_async_session() as session:
            owners = (await session.execute(
                select(Member)
                .where(
                    Member.user_id == request.state.user_id,
                    Member.role == MemberRole.owner
                )
            )).scalars().all()

            events = (await session.execute(
                select(Event)
                .where(Event.id.in_(map(lambda x: x.event_id, owners)))
            )).scalars().all()

    except Exception as err:
        logger.exception(err)
        return GetMyEventsResponse(status=ResponseStatus.unexpected_error)

    return GetMyEventsResponse(
        data=[
            GetEventData(**event.__dict__)
            for event in events
        ]
    )


@event_router.get(
    path="/search",
    response_model=CreateEventResponse,
    description="Create new event",
)
async def create_event(
    data: CreateEventRequest,
    response: fastapi.Response,
) -> CreateEventResponse:

    pass
