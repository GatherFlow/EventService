
import fastapi

from app.schema.request import CreateEventRequest
from app.schema.response import CreateEventResponse

from app.database import get_async_session


member_router = fastapi.APIRouter(prefix="/member")


@member_router.update(
    path="/announce",
    response_model=CreateEventResponse,
    description="Create new event",
)
async def create_event(
    data: CreateEventRequest,
    response: fastapi.Response,
) -> CreateEventResponse:

    pass
