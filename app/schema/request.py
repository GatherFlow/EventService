
from app.enum import EventFormat, MemberRole, RestrictionAction
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


class CreateEventTicketRequest(BaseModel):
    event_id: int
    title: str
    description: str
    price: float
    amount: int
    stock: int


class UpdateEventTicketRequest(BaseModel):
    id: int
    title: str | None = None
    description: str | None = None
    price: float | None = None
    amount: int | None = None
    stock: int | None = None


class CreateMemberRequest(BaseModel):
    event_id: int
    user_id: str
    role: MemberRole


class UpdateMemberRequest(BaseModel):
    id: int
    role: MemberRole = None


class UpdateTagRequest(BaseModel):
    event_id: int
    tags: list[str]


class CreateRestrictionRequest(BaseModel):
    event_id: int
    action: RestrictionAction
    value: dict


class UpdateRestrictionRequest(BaseModel):
    id: int
    action: RestrictionAction | None = None
    value: dict | None = None


class CreateTicketRequest(BaseModel):
    event_id: int
    user_id: str
