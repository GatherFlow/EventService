
from app.enum import EventFormat, MemberRole
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


class AddAlbumRequest(BaseModel):
    event_id: int
    file: str


class AnnounceEventRequest(BaseModel):
    event_id: int


class StopGatheringEventRequest(BaseModel):
    event_id: int


class CreateTicketRequest(BaseModel):
    event_id: int
    title: str
    description: str
    price: float
    amount: int
    stock: int


class UpdateTicketRequest(BaseModel):
    id: int
    title: str = None
    description: str = None
    price: float = None
    amount: int = None
    stock: int = None


class CreateMemberRequest(BaseModel):
    event_id: int
    user_id: str
    role: MemberRole


class UpdateMemberRequest(BaseModel):
    id: int
    role: MemberRole = None
