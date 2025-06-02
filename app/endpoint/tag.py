
import fastapi
import re

from loguru import logger

from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.enum import ResponseStatus
from app.model import Tag, EventTag

from app.schema.request import UpdateTagRequest
from app.schema.response import UpdateTagResponse, SearchTagResponse
from app.schema.response import UpdateTagData, SearchTagData

from app.database import get_async_session


tag_router = fastapi.APIRouter(prefix="/tag", tags=["tag"])


async def update_tags(tags: list[str], event_id: int, session: AsyncSession) -> list[EventTag]:
    if not len(tags):
        return []

    tag_names = [
        f"#{tag.lower()}" if not tag.startswith("#") else tag.lower()
        for tag in tags
    ]

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
        .where(EventTag.event_id == event_id)
    )

    event_tags = []

    for tag_name in tag_names:
        event_tag = EventTag(
            tag_id=tags_dict[tag_name].id,
            event_id=event_id
        )
        event_tags.append(event_tag)

        session.add(event_tag)
        await session.flush()

    return event_tags


@tag_router.put(
    path="/update",
    response_model=UpdateTagResponse,
    description="Update tags",
)
async def create_event(
    data: UpdateTagRequest
) -> UpdateTagResponse:

    try:

        async with get_async_session() as session:
            event_tags = await update_tags(
                tags=data.tags,
                event_id=data.event_id,
                session=session
            )
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
    response_model=SearchTagResponse,
    description="Search tags",
)
async def search_tags(
    query: str
) -> SearchTagResponse:

    response_data = []

    query_tags = re.findall(r'#\S+', query)
    if not len(query_tags):
        return SearchTagResponse(
            data=response_data
        )

    last_query_tag = query_tags[-1][1:]

    try:
        async with get_async_session() as session:
            tags = (await session.execute(
                select(Tag)
                .where(Tag.name.op('%')(last_query_tag))
            )).scalars().unique().all()

            for tag in tags:
                response_data.append(SearchTagData(**tag.__dict__))

    except Exception as err:
        logger.exception(err)
        return SearchTagResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return SearchTagResponse(
        data=response_data
    )

