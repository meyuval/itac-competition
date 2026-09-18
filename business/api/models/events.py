from __future__ import annotations

from typing import Literal

from pydantic import AliasChoices, Field

from business.api.models.common import ArenaBaseModel

EventCategory = Literal["concert", "theater", "sports", "conference", "family"]
EventSort = Literal["starts_at", "title", "min_price"]
SortOrder = Literal["asc", "desc"]


class EventTierInput(ArenaBaseModel):
    name: str
    price_agorot: int
    row_from: str
    row_to: str


class EventTier(EventTierInput):
    id: str | None = None


class EventVenue(ArenaBaseModel):
    id: str | None = None
    name: str
    city: str


class EventListItem(ArenaBaseModel):
    id: str
    title: str = Field(validation_alias=AliasChoices("title", "name"))
    category: str
    status: str
    starts_at: str
    venue: EventVenue
    description: str | None = None
    lineup: str | None = None
    min_price_agorot: int | None = None
    seats_available: int | None = None
    seats_total: int | None = None
    tiers: list[EventTier] = Field(default_factory=list)


class EventSeat(ArenaBaseModel):
    seat_id: str
    label: str
    row: str
    number: int
    tier: str
    price_agorot: int
    status: str
    held_by_me: bool = False


class EventSalesEvent(ArenaBaseModel):
    id: str
    title: str = Field(validation_alias=AliasChoices("title", "name"))
    starts_at: str


class EventSalesOrder(ArenaBaseModel):
    id: str
    order_number: str
    email: str
    seats: list[str]
    total_agorot: int
    status: str


class ListEventsRequest(ArenaBaseModel):
    q: str | None = None
    category: EventCategory | None = None
    city: str | None = None
    from_: str | None = Field(default=None, alias="from")
    to: str | None = None
    sort: EventSort | None = None
    order: SortOrder | None = None
    page: int | None = None
    page_size: int | None = None
    include_drafts: bool | None = None


class ListEventsResponse(ArenaBaseModel):
    items: list[EventListItem] = Field(default_factory=list)
    page: int | None = None
    page_size: int | None = None
    total: int | None = None


class GetEventByIdRequest(ArenaBaseModel):
    event_id: str


class GetEventByIdResponse(ArenaBaseModel):
    id: str
    title: str = Field(validation_alias=AliasChoices("title", "name"))
    category: str
    status: str
    description: str | None = None
    lineup: str | None = None
    starts_at: str
    venue: EventVenue
    tiers: list[EventTier] = Field(default_factory=list)
    min_price_agorot: int | None = None
    seats_available: int | None = None
    seats_total: int | None = None


class GetEventSeatsRequest(ArenaBaseModel):
    event_id: str


class GetEventSeatsResponse(ArenaBaseModel):
    seats: list[EventSeat] = Field(default_factory=list)


class CreateEventRequest(ArenaBaseModel):
    title: str = Field(validation_alias=AliasChoices("title", "name"), serialization_alias="name")
    category: EventCategory
    venue_id: str
    starts_at: str
    description: str | None = None
    lineup: str | None = None
    tiers: list[EventTierInput]


class CreateEventResponse(ArenaBaseModel):
    id: str
    title: str = Field(validation_alias=AliasChoices("title", "name"))
    status: str
    tiers: list[EventTier] = Field(default_factory=list)


class UpdateEventRequest(ArenaBaseModel):
    event_id: str
    title: str | None = Field(
        default=None,
        validation_alias=AliasChoices("title", "name"),
        serialization_alias="name",
    )
    category: EventCategory | None = None
    venue_id: str | None = None
    starts_at: str | None = None
    description: str | None = None
    lineup: str | None = None
    tiers: list[EventTierInput] | None = None


class UpdateEventResponse(ArenaBaseModel):
    id: str | None = None
    title: str | None = Field(default=None, validation_alias=AliasChoices("title", "name"))
    category: str | None = None
    status: str | None = None
    description: str | None = None
    starts_at: str | None = None
    venue: EventVenue | None = None
    tiers: list[EventTier] = Field(default_factory=list)
    min_price_agorot: int | None = None
    seats_available: int | None = None


class PublishEventRequest(ArenaBaseModel):
    event_id: str


class PublishEventResponse(ArenaBaseModel):
    id: str
    status: str


class UnpublishEventRequest(ArenaBaseModel):
    event_id: str


class UnpublishEventResponse(ArenaBaseModel):
    id: str
    status: str


class GetEventSalesRequest(ArenaBaseModel):
    event_id: str


class GetEventSalesResponse(ArenaBaseModel):
    event: EventSalesEvent
    tickets_sold: int
    tickets_refunded: int
    gross_agorot: int
    refunded_agorot: int
    net_agorot: int
    orders: list[EventSalesOrder] = Field(default_factory=list)
