
import fastapi
from uuid import uuid4
from loguru import logger

from sqlalchemy import select, and_

from app.model import EventAlbum
from app.enum import ResponseStatus

from app.schema.request import AddAlbumRequest
from app.schema.response import AddAlbumResponse, AddAlbumData

from app.database import get_async_session


album_router = fastapi.APIRouter(prefix="/album")


@album_router.post(
    path="/add",
    response_model=AddAlbumResponse,
    description="Create new event",
)
async def create_event(
    data: AddAlbumRequest
) -> AddAlbumResponse:

    try:
        async with get_async_session() as session:
            album = (await session.execute(
                select(EventAlbum)
                .where(
                    and_(
                        EventAlbum.event_id == data.event_id,
                    )
                )
            )).scalars().one_or_none()

            if album:
                await session.delete(album)

            album = EventAlbum(
                event_id=data.event_id,
                img=uuid4().hex
            )

            with open(f"resources/images/{album.img}", "wb") as f:
                f.write(data.file)

            session.add(album)

            await session.commit()

    except Exception as err:
        logger.exception(err)
        return AddAlbumResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return AddAlbumResponse(
        data=AddAlbumData(
            url=f"https://bots.innova.ua/image/{album.img}"
        )
    )
