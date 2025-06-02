
import fastapi
from datetime import datetime, timezone
from loguru import logger

from sqlalchemy import select, update

from app.enum import ResponseStatus
from app.model import EventSettings, Event

from app.schema.request import AnnounceEventRequest, StopGatheringEventRequest
from app.schema.response import AnnouncedEventResponse, StopGatheringEventResponse, GetSettingsResponse
from app.schema.response import AnnouncedEventData, StopGatheringEventData, GetSettingsData

from app.database import get_async_session


settings_router = fastapi.APIRouter(prefix="/settings", tags=["settings"])


@settings_router.get(
    path="/",
    response_model=GetSettingsResponse,
    description="Get settings",
)
async def get_settings(
    event_id: int
) -> GetSettingsResponse:

    try:
        async with get_async_session() as session:
            settings = (await session.execute(
                select(EventSettings)
                .where(
                    EventSettings.event_id == event_id
                )
            )).scalars().first()

    except Exception as err:
        logger.exception(err)
        return GetSettingsResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetSettingsResponse(
        data=GetSettingsData(**settings.__dict__)
    )


@settings_router.post(
    path="/announce",
    response_model=AnnouncedEventResponse,
    description="Announce event",
)
async def announce_event(
    data: AnnounceEventRequest,
) -> AnnouncedEventResponse:

    try:
        async with get_async_session() as session:
            settings = (await session.execute(
                select(EventSettings)
                .where(
                    EventSettings.event_id == data.event_id
                )
            )).scalars().first()

            if not settings.is_announced:
                settings.is_announced = True

                await session.execute(
                    update(EventSettings)
                    .where(EventSettings.id == settings.id)
                    .values(is_announced=settings.is_announced)
                    .execution_options(synchronize_session="fetch")
                )

                event = await session.get(Event, settings.event_id)
                event.announced_at = datetime.now(timezone.utc)

                await session.execute(
                    update(Event)
                    .where(Event.id == event.id)
                    .values(announced_at=event.announced_at)
                    .execution_options(synchronize_session="fetch")
                )

                await session.commit()

    except Exception as err:
        logger.exception(err)
        return AnnouncedEventResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return AnnouncedEventResponse(
        data=AnnouncedEventData(
            is_announced=settings.is_announced,
            is_gathering=settings.is_gathering
        )
    )


@settings_router.post(
    path="/gather",
    response_model=StopGatheringEventResponse,
    description="Gather/Ungather event",
)
async def gather_event(
    data: StopGatheringEventRequest,
) -> StopGatheringEventResponse:

    try:
        async with get_async_session() as session:
            settings = (await session.execute(
                select(EventSettings)
                .where(
                    EventSettings.event_id == data.event_id
                )
            )).scalars().first()

            settings.is_gathering = not settings.is_gathering

            await session.execute(
                update(EventSettings)
                .where(EventSettings.id == settings.id)
                .values(is_gathering=settings.is_gathering)
                .execution_options(synchronize_session="fetch")
            )
            await session.commit()

    except Exception as err:
        logger.exception(err)
        return AnnouncedEventResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return StopGatheringEventResponse(
        data=StopGatheringEventData(
            is_gathering=settings.is_gathering
        )
    )

