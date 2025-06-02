
import aiohttp
import fastapi
from loguru import logger

from sqlalchemy import update, select

from app.enum import ResponseStatus
from app.model import Member

from app.schema.request import CreateMemberRequest, UpdateMemberRequest
from app.schema.response import CreateMemberResponse, UpdateMemberResponse, GetMemberResponse, GetManyMemberResponse, GetMemberData
from app.schema.response import CreateMemberData

from app.database import get_async_session

from config import get_settings


member_router = fastapi.APIRouter(prefix="/member", tags=["member"])


@member_router.post(
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


async def gen_users_dict(user_ids, cookies: dict) -> GetMemberData:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"{get_settings().services.user}/users/many",
            params={"ids": user_ids},
            cookies=cookies,
        ) as response:

            data = await response.json()

    return {
        row["id"]: row
        for row in data
    }


@member_router.get(
    path="/",
    response_model=GetMemberResponse,
    description="Get member",
)
async def create_member(
    id: int,
    request: fastapi.Request
) -> GetMemberResponse:

    try:
        async with get_async_session() as session:
            member = (await session.execute(
                select(Member)
                .where(
                    Member.event_id == id
                )
            )).scalars().first()

        users_dict = await gen_users_dict(user_ids=[member.user_id], cookies=request.cookies)
        user = users_dict[member.user_id]

    except Exception as err:
        logger.exception(err)
        return GetMemberResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetMemberResponse(
        data=GetMemberData(
            **{
                **member.__dict__,
                "first_name": user["firstName"],
                "last_name": user["lastName"],
                "avatar": user["avatar"]
            }
        )
    )


@member_router.get(
    path="/many",
    response_model=GetManyMemberResponse,
    description="Get many members",
)
async def create_many_member(
    event_id: int,
    request: fastapi.Request
) -> GetManyMemberResponse:

    try:
        async with get_async_session() as session:
            members = (await session.execute(
                select(Member)
                .where(Member.event_id == event_id)
            )).scalars().all()

            users_dict = await gen_users_dict(
                user_ids=list(map(lambda x: x.user_id, members)),
                cookies=request.cookies
            )

    except Exception as err:
        logger.exception(err)
        return GetManyMemberResponse(
            status=ResponseStatus.unexpected_error,
            description=str(err)
        )

    return GetManyMemberResponse(
        data=[
            GetMemberData(
                **{
                    **member.__dict__,
                    "first_name": users_dict[member.user_id]["firstName"],
                    "last_name": users_dict[member.user_id]["lastName"],
                    "avatar": users_dict[member.user_id]["avatar"]
                }
            )
            for member in members
        ]
    )
