
from pydantic import BaseModel, Field

from app.enum import ResponseStatus, EventFormat, MemberRole


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


class LikeData(BaseModel):
    likes: int


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


class CreateTicketData(BaseModel):
    id: int


class UpdateTicketData(BaseModel):
    id: int


class GetTicketData(BaseModel):
    id: int
    event_id: int
    title: str
    description: str
    price: float
    amount: int
    stock: int


class AddAlbumData(BaseModel):
    url: str


class AnnouncedEventData(BaseModel):
    is_announced: bool


class StopGatheringEventData(BaseModel):
    is_gathering: bool


class GetSettingsData(BaseModel):
    id: int
    event_id: int
    is_gathering: bool
    is_announced: bool
    is_dropped: bool


class CreateMemberData(BaseModel):
    id: int


class UpdateMemberData(BaseModel):
    id: int


class GetMemberData(BaseModel):
    id: int
    event_id: int
    user_id: str
    role: MemberRole


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


class DeleteEventResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None


class GetManyEventsResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: list[GetEventData] = Field(default_factory=list)


class LikeResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: LikeData | None = None


class AddAlbumResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: AddAlbumData | None = None


class AnnouncedEventResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: AnnouncedEventData | None = None


class StopGatheringEventResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: StopGatheringEventData | None = None


class CreateTicketResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: CreateTicketData | None = None


class UpdateTicketResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: UpdateTicketData | None = None


class GetTicketResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: GetTicketData | None = None


class GetManyTicketResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: list[GetTicketData] = Field(default_factory=list)


class GetSettingsResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: GetSettingsData | None = None


class CreateMemberResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: CreateMemberData | None = None


class UpdateMemberResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: UpdateMemberData | None = None


class GetMemberResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: GetMemberData | None = None


class GetManyMemberResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: list[GetMemberData] = Field(default_factory=list)
