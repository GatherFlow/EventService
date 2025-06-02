
import fastapi

from app.enum import ResponseStatus
from app.model import Event

from app.schema.request import CreateEventRequest
from app.schema.response import CreateEventResponse

from app.database import get_async_session


restrictions_router = fastapi.APIRouter(prefix="/restricitons")


@restrictions_router.post(
    path="/create",
    response_model=CreateEventResponse,
    description="Create new restriction",
)
async def create_restriction(
    data: CreateEventRequest
) -> CreateEventResponse:

    pass


@restrictions_router.put(
    path="/update",
    response_model=CreateEventResponse,
    description="Update restriction",
)
async def update_restriction(
    data: CreateEventRequest
) -> CreateEventResponse:

    pass


@restrictions_router.delete(
    path="/delete",
    response_model=CreateEventResponse,
    description="Delete restriction",
)
async def delete_restriction(
    data: CreateEventRequest
) -> CreateEventResponse:

    pass


@restrictions_router.get(
    path="/",
    response_model=CreateEventResponse,
    description="Get restriction",
)
async def get_restriction(
    id: int
) -> CreateEventResponse:

    pass


@restrictions_router.get(
    path="/many",
    response_model=CreateEventResponse,
    description="Get many restriction",
)
async def get_restriction(
    event_id: int
) -> CreateEventResponse:

    pass

