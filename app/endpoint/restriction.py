
import fastapi

from app.enum import ResponseStatus
from app.model import Event

from app.schema.request import CreateEventRequest
from app.schema.response import CreateEventResponse

from app.database import get_async_session


restrictions_router = fastapi.APIRouter(prefix="restricitons")


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
async def create_event(
    data: CreateEventRequest
) -> CreateEventResponse:

    pass


