
import fastapi
from loguru import logger

from sqlalchemy import select, and_, func

from app.enum import ResponseStatus
from app.model import Like, Event

from app.schema.request import LikeRequest
from app.schema.response import LikeResponse, LikeData

from app.database import get_async_session


like_router = fastapi.APIRouter(prefix="/like")


@like_router.post(
    path="/",
    response_model=LikeResponse,
    description="Like/unlike event"
)
async def create_event(
    data: LikeRequest,
    request: fastapi.Request
) -> LikeResponse:

    try:
        async with get_async_session() as session:
            like = (await session.execute(
                select(Like)
                .where(
                    and_(
                        Like.event_id == data.event_id,
                        Like.user_id == request.state.user_id,
                    )
                )
            )).scalars().one_or_none()

            if like:
                await session.delete(like)

            else:
                like = Like(
                    event_id=data.event_id,
                    user_id=request.state.user_id,
                )

                session.add(like)

            likes = (await session.execute(
                select(func.count()).select_from(Like).where(Event.id == data.event_id)
            )).scalar()

            await session.commit()

    except Exception as err:
        logger.exception(err)

        return LikeResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return LikeResponse(
        data=LikeData(
            likes=likes
        )
    )
