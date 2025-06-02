
from app.enum import ResponseStatus, EventFormat, MemberRole, RestrictionAction

from pydantic import BaseModel, Field


class CreateEventData(BaseModel):
    id: int


class UpdateEventData(BaseModel):
    id: int


class GetEventTicketData(BaseModel):
    id: int
    title: str
    description: str
    price: float
    amount: int
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


class CreateEventTicketData(BaseModel):
    id: int


class UpdateEventTicketData(BaseModel):
    id: int


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
    first_name: str
    last_name: str
    avatar: str


class UpdateTagData(BaseModel):
    id: list[int]


class SearchTagData(BaseModel):
    id: int
    name: str


class CreateRestrictionData(BaseModel):
    id: int


class UpdateRestrictionData(BaseModel):
    id: int


class GetRestrictionData(BaseModel):
    id: int
    event_id: int
    action: RestrictionAction
    value: dict


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


class CreateEventTicketResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: CreateEventTicketData | None = None


class UpdateEventTicketResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: UpdateEventTicketData | None = None


class GetEventTicketResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: GetEventTicketData | None = None


class GetManyEventTicketResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: list[GetEventTicketData] = Field(default_factory=list)


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


class UpdateTagResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: list[UpdateTagData] = Field(default_factory=list)


class SearchTagResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: list[SearchTagData] = Field(default_factory=list)


class CreateRestrictionResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: list[CreateRestrictionData] = Field(default_factory=list)


class UpdateRestrictionResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: list[UpdateRestrictionData] = Field(default_factory=list)


class GetRestrictionResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: GetRestrictionData | None = None


class GetManyRestrictionResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: list[GetRestrictionData] = Field(default_factory=list)


class DeleteRestrictionResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None


class DeleteEventTicketResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None


class CreateTicketData(BaseModel):
    id: int


class GetTicketData(BaseModel):
    id: int
    event_ticket_id: int
    user_id: str


class CreateTicketResponse(BaseModel):
    status: ResponseStatus | None = ResponseStatus.ok
    description: str | None = None

    data: CreateTicketData | None = None


class DeleteTicketResponse(BaseModel):
    status: ResponseStatus | None = ResponseStatus.ok
    description: str | None = None


class GetTicketResponse(BaseModel):
    status: ResponseStatus | None = ResponseStatus.ok
    description: str | None = None

    data: GetTicketData | None = None


class GetManyTicketResponse(BaseModel):
    status: ResponseStatus | None = ResponseStatus.ok
    description: str | None = None

    data: list[GetTicketData] = Field(default_factory=list)


class GetMyStatsData(BaseModel):
    total_event: int
    total_attendance: int


class GetMyStatsResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ok
    description: str | None = None

    data: GetMyStatsData | None = None
