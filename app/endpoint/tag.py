
import fastapi

from sqlalchemy import select, delete

from app.enum import ResponseStatus
from app.model import Tag, EventTag

from app.schema.request import UpdateTagRequest
from app.schema.response import UpdateTagResponse, SearchTagResponse

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

    tag_names = list(map(lambda x: f"#{x}" if not x.startswith("#") else x, data.tags))

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
            .where(EventTag.event_id == 1)
        )

        for tag_name in tag_names:
            event_tag = EventTag()
