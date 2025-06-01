
from app.enum import EventFormat
from pydantic import BaseModel


class CreateEventRequest(BaseModel):
    title: str
    description: str
    duration: int
    format: EventFormat
    meeting_link: str | None = None
    location: str | None = None
    starting_time: int | None = None


class UpdateEventRequest(BaseModel):
    id: int
    title: str | None = None
    description: str | None = None
    duration: int | None = None
    format: EventFormat | None = None
    meeting_link: str | None = None
    location: str | None = None
    starting_time: int | None = None


class GetEventRequest(BaseModel):
    id: int


class GetMyEventsRequest(BaseModel):
    pass


class SearchEventRequest(BaseModel):
    query: str


class LikeRequest(BaseModel):
    event_id: int
