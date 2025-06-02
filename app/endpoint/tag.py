
import fastapi
from loguru import logger

from sqlalchemy import select, delete

from app.enum import ResponseStatus
from app.model import Tag, EventTag

from app.schema.request import UpdateTagRequest
from app.schema.response import UpdateTagResponse, SearchTagResponse, UpdateTagData, GetTicketResponse

from app.database import get_async_session


tag_router = fastapi.APIRouter(prefix="/tag")


@tag_router.post(
    path="/update",
    response_model=UpdateTagResponse,
    description="Update tags",
)
async def create_event(
    data: UpdateTagRequest
) -> UpdateTagResponse:

    try:

        tag_names = [
            f"#{tag.lower()}" if not tag.startswith("#") else tag.lower()
            for tag in data.tags
        ]

        async with get_async_session() as session:
            tags = (await session.execute(
                select(Tag)
                .where(Tag.name.in_(tag_names))
            )).scalars().all()

            tags_dict = {
                tag.name: tag
                for tag in tags
            }

            for tag_name in tag_names:
                if tag_name in tags_dict:
                    continue

                tag = Tag(name=tag_name)
                tags_dict.update({tag_name: tag})

                session.add(tag)
                await session.flush()

            await session.execute(
                delete(EventTag)
                .where(EventTag.event_id == data.event_id)
            )

            event_tags = []

            for tag_name in tag_names:
                event_tag = EventTag(
                    tag_id=tags_dict[tag_name],
                    event_id=data.event_id
                )
                event_tags.append(event_tag)

                session.add(event_tag)
                await session.flush()

            await session.commit()

    except Exception as err:
        logger.exception(err)
        return UpdateTagResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return UpdateTagResponse(
        data=[
            UpdateTagData(id=tag.id)
            for tag in event_tags
        ]
    )


@tag_router.get(
    path="/search",
    response_model=GetTicketResponse,
    description="Search events",
)
async def search_events(
    query: str
) -> GetTicketResponse:

    parts = query.split("# ")

    """
    qwe #qwe #q
    """

    response_data = []

    try:
        async with get_async_session() as session:
            tags = (await session.execute(
                select(Tag)
                .where(
                    func.lower(Event.title).op('%')(query)
                )
            )).scalars().unique().all()

            for event in events:
                response_data.append(tag)

    except Exception as err:
        logger.exception(err)
        return GetTicketResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetTicketResponse(
        data=response_data
    )

