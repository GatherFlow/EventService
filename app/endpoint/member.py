
import fastapi
from loguru import logger

from sqlalchemy import update, select

from app.enum import ResponseStatus
from app.model import Member

from app.schema.request import CreateMemberRequest, UpdateMemberRequest
from app.schema.response import CreateMemberResponse, UpdateMemberResponse, GetMemberResponse, GetManyMemberResponse, GetMemberData
from app.schema.response import CreateMemberData

from app.database import get_async_session


member_router = fastapi.APIRouter(prefix="/member")


@member_router.put(
    path="/create",
    response_model=CreateMemberResponse,
    description="Create new member",
)
async def create_member(
    data: CreateMemberRequest
) -> CreateMemberResponse:

    try:
        async with get_async_session() as session:
            member = Member(
                event_id=data.event_id,
                user_id=data.user_id,
                role=data.role,
            )
            session.add(member)
            await session.commit()

    except Exception as err:
        logger.exception(err)
        return CreateMemberResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return CreateMemberResponse(
        data=CreateMemberData(
            id=member.id
        )
    )


@member_router.put(
    path="/update",
    response_model=UpdateMemberResponse,
    description="Update member",
)
async def update_member(
    data: UpdateMemberRequest,
) -> UpdateMemberResponse:

    try:
        async with get_async_session() as session:
            data_dict = data.model_dump()

            await session.execute(
                update(Member)
                .where(Member.id == data.id)
                .values(**{
                    key: data_dict[key]
                    for key in data_dict if key not in ["id"] and data_dict.get(key)
                })
                .execution_options(synchronize_session="fetch")
            )

            await session.commit()

    except Exception as err:
        logger.exception(err)
        return UpdateMemberResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return UpdateMemberResponse(
        data=UpdateMemberResponse(
            id=data.id
        )
    )


@member_router.get(
    path="/",
    response_model=GetMemberResponse,
    description="Get member",
)
async def create_event(
    id: int
) -> GetMemberResponse:

    try:
        async with get_async_session() as session:
            member = (await session.execute(
                select(Member)
                .where(
                    Member.event_id == id
                )
            )).scalars().first()

    except Exception as err:
        logger.exception(err)
        return GetMemberResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetMemberResponse(
        data=GetMemberData(**member.__dict__)
    )


@member_router.get(
    path="/many",
    response_model=GetManyMemberResponse,
    description="Get many members",
)
async def create_event(
    event_id: int
) -> GetManyMemberResponse:

    try:
        async with get_async_session() as session:
            members = (await session.execute(
                select(Member)
                .where(Member.event_id == event_id)
            )).scalars().all()

    except Exception as err:
        logger.exception(err)
        return GetManyMemberResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetManyMemberResponse(
        data=[
            GetMemberData(**member.__dict__)
            for member in members
        ]
    )
