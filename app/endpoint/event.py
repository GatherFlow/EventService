
import fastapi
from loguru import logger
from sqlalchemy import update, select, or_, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.enum import MemberRole, ResponseStatus
from app.model import Event, Member, EventSettings, Tag, EventTag, Like, EventTicket, EventAlbum

from app.schema.request import (
    CreateEventRequest, UpdateEventRequest,
    GetEventRequest
)
from app.schema.response import (
    CreateEventResponse, UpdateEventResponse,
    GetEventResponse, GetManyEventsResponse
)
from app.schema.response import (
    CreateEventData, UpdateEventData,
    GetEventData, GetEventTicketData
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
                location=data.location
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
        return UpdateEventResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return CreateEventResponse(
        data=CreateEventData(
            id=event.id
        )
    )


@event_router.put(
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
        return UpdateEventResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return UpdateEventResponse(
        data=UpdateEventData(
            id=data.id
        )
    )


async def gen_response_event(event: Event, session: AsyncSession):
    async with get_async_session() as session:
        event_tickets = (await session.execute(
            select(EventTicket)
            .where(
                EventTicket.event_id == event.id
            )
        )).scalars().all()
        album = (await session.execute(
            select(EventAlbum)
            .where(
                EventAlbum.event_id == event.id
            )
        )).scalars().all()
        event_tags = (await session.execute(
            select(EventTag)
            .where(
                EventTag.event_id == event.id
            )
        )).scalars().all()
        tags = (await session.execute(
            select(Tag)
            .where(
                Tag.id.in_(map(lambda x: x.tag_id, event_tags))
            )
        )).scalars().all()
        likes = (await session.execute(
            select(func.count()).select_from(Like).where(event.id == event.id)
        )).scalar()

    return GetEventData(
        **event.__dict__,
        likes=likes,
        bought=0,
        tags=list(map(lambda x: x.name, tags)),
        album=list(map(lambda x: f"https://bots.innova.ua/api/event/album/{x.img}", album)),
        event_tickets=[
            GetEventTicketData(
                id=event_ticket.id,
                title=event_ticket.title,
                description=event_ticket.description,
                price=event_ticket.price,
                stock=event_ticket.stock
            )
            for event_ticket in event_tickets
        ]
    )


@event_router.get(
    path="/",
    response_model=GetEventRequest,
    description="Get event",
)
async def create_event(
    id: int
) -> GetEventResponse:

    try:
        async with get_async_session() as session:
            event = await session.get(Event, id)
            response_data = await gen_response_event(event, session)

    except Exception as err:
        logger.exception(err)
        return GetEventResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetEventResponse(
        data=response_data
    )


@event_router.get(
    path="/mine",
    description="Get my events",
)
async def create_event(
    request: fastapi.Request,
) -> GetManyEventsResponse:

    response_data = []

    try:
        async with get_async_session() as session:
            owners = (await session.execute(
                select(Member)
                .where(
                    and_(
                        Member.user_id == request.state.user_id,
                        Member.role == MemberRole.owner
                    )
                )
            )).scalars().all()
            event_ids = map(lambda x: x.event_id, owners)

            events = (await session.execute(
                select(Event)
                .where(
                    Event.id.in_(event_ids)
                )
            )).scalars().all()

            for event in events:
                response_data.append(await gen_response_event(event, session))

    except Exception as err:
        logger.exception(err)
        return GetManyEventsResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetManyEventsResponse(
        data=response_data
    )


@event_router.get(
    path="/search",
    description="Search events",
)
async def create_event(
    query: str
) -> GetManyEventsResponse:

    response_data = []

    try:
        async with get_async_session() as session:
            events = (await session.execute(
                select(Event)
                .outerjoin(EventTag, Event.id == EventTag.event_id)
                .outerjoin(Tag, Tag.id == EventTag.tag_id)
                .where(
                    or_(
                        func.lower(Event.title).op('%')(query),
                        func.lower(Event.description).op('%')(query),
                    )
                )
            )).scalars().unique().all()

            for event in events:
                response_data.append(await gen_response_event(event, session))

    except Exception as err:
        logger.exception(err)
        return GetManyEventsResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetManyEventsResponse(
        data=response_data
    )
