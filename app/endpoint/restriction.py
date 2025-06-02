
import fastapi
from loguru import logger

from sqlalchemy import update, select

from app.enum import ResponseStatus
from app.model import EventRestriction

from app.schema.request import (
    CreateRestrictionRequest, UpdateRestrictionRequest
)
from app.schema.response import (
    CreateRestrictionResponse, UpdateRestrictionResponse,
    DeleteRestrictionResponse,
    GetRestrictionResponse, GetManyRestrictionResponse
)
from app.schema.response import (
    CreateRestrictionData, UpdateRestrictionData,
    GetRestrictionData
)

from app.database import get_async_session


restriction_router = fastapi.APIRouter(prefix="/restriction")


@restriction_router.post(
    path="/create",
    response_model=CreateRestrictionResponse,
    description="Create new restriction",
)
async def create_restriction(
    data: CreateRestrictionRequest
) -> CreateRestrictionResponse:

    try:
        async with get_async_session() as session:
            restriction = EventRestriction(
                event_id=data.event_id,
                action=data.action,
                value=data.value
            )
            session.add(restriction)
            await session.commit()

    except Exception as err:
        logger.exception(err)
        return CreateRestrictionResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return CreateRestrictionResponse(
        data=CreateRestrictionData(
            id=restriction.id
        )
    )


@restriction_router.put(
    path="/update",
    response_model=UpdateRestrictionResponse,
    description="Update restriction",
)
async def update_restriction(
    data: UpdateRestrictionRequest
) -> UpdateRestrictionResponse:

    try:
        async with get_async_session() as session:
            data_dict = data.model_dump()

            await session.execute(
                update(EventRestriction)
                .where(EventRestriction.id == data.id)
                .values(**{
                    key: data_dict[key]
                    for key in data_dict if key not in ["id"] and data_dict.get(key)
                })
                .execution_options(synchronize_session="fetch")
            )

            await session.commit()

    except Exception as err:
        logger.exception(err)
        return UpdateRestrictionResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return UpdateRestrictionResponse(
        data=UpdateRestrictionData(
            id=data.id
        )
    )


@restriction_router.delete(
    path="/delete",
    response_model=DeleteRestrictionResponse,
    description="Delete restriction",
)
async def delete_restriction(
    id: int
) -> DeleteRestrictionResponse:

    try:
        async with get_async_session() as session:
            event = await session.get(EventRestriction, id)
            await session.delete(event)
            await session.commit()

    except Exception as err:
        logger.exception(err)
        return DeleteRestrictionResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return DeleteRestrictionResponse()


@restriction_router.get(
    path="/",
    response_model=GetRestrictionResponse,
    description="Get restriction",
)
async def get_restriction(
    id: int
) -> GetRestrictionResponse:

    try:
        async with get_async_session() as session:
            restriction = await session.get(EventRestriction, id)

    except Exception as err:
        logger.exception(err)
        return GetRestrictionResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetRestrictionResponse(
        data=GetRestrictionData(**restriction.__dict__)
    )


@restriction_router.get(
    path="/many",
    response_model=GetManyRestrictionResponse,
    description="Get many restriction",
)
async def get_restriction(
    event_id: int
) -> GetManyRestrictionResponse:

    try:
        async with get_async_session() as session:
            restrictions = (await session.execute(
                select(EventRestriction)
                .where(EventRestriction.event_id == event_id)
            )).scalars().all()

    except Exception as err:
        logger.exception(err)
        return GetManyRestrictionResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetManyRestrictionResponse(
        data=[
            GetRestrictionData(**restriction.__dict__)
            for restriction in restrictions
        ]
    )
