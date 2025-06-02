
import base64
import os
import fastapi
from fastapi.responses import FileResponse

from uuid import uuid4
from loguru import logger

from sqlalchemy import select, and_

from app.model import EventAlbum
from app.enum import ResponseStatus

from app.schema.request import AddAlbumRequest
from app.schema.response import AddAlbumResponse, AddAlbumData

from app.database import get_async_session


album_router = fastapi.APIRouter(prefix="/album")


@album_router.get(
    path="/{album_id}",
    response_class=FileResponse,
    description="Get image"
)
async def get_album(
    album_id: str,
):

    file_path = f"./resources/images/{album_id}"
    if not os.path.isdir(file_path):
        file_path = f"./resources/images/404.jpg"

    return FileResponse(path=file_path, media_type="image/jpeg", filename=f"image.jpg")


@album_router.post(
    path="/",
    response_model=AddAlbumResponse,
    description="Add/Replace album image",
)
async def add_album(
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

            with open(f"./resources/images/{album.img}", "wb") as f:
                f.write(base64.b64decode(data.file))

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
            url=f"https://bots.innova.ua/api/event/album/{album.img}"
        )
    )
