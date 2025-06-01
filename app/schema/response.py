
from pydantic import BaseModel, Field

from app.enum import ResponseStatus, EventFormat


class CreateEventData(BaseModel):
    id: int


class UpdateEventData(BaseModel):
    id: int


class GetEventTicketData(BaseModel):
    id: int
    title: str
    description: str
    price: float
    stock: int


class GetEventData(BaseModel):
    id: int
    title: str
    description: str
    duration: int
    format: EventFormat
    meeting_link: str | None = None
    location: str | None = None
    starting_time: int | None = None
    announced_at: int | None = None

    likes: int | None = None
    bought: int | None = None

    tags: list[str] = []
    album: list[str] = []
    tickets: list[GetEventTicketData] = []


class CreateEventResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: CreateEventData | None = None


class UpdateEventResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: UpdateEventData | None = None


class GetEventResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: GetEventData | None = None


class GetManyEventsResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: list[GetEventData] = Field(default_factory=list)


class LikeResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None
