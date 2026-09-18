from __future__ import annotations

from datetime import datetime
from typing import cast
from zoneinfo import ZoneInfo

from pydantic import BaseModel

from business.api.clients.events import EventsClient
from business.api.clients.venues import VenuesClient
from business.api.models.events import (
    CreateEventRequest as ApiCreateEventRequest,
)
from business.api.models.events import EventCategory, EventTierInput, PublishEventRequest
from business.api.models.venues import Venue

_JERUSALEM = ZoneInfo("Asia/Jerusalem")


class EventTierRequest(BaseModel):
    name: str
    rows: str
    price: str

    @property
    def display_price(self) -> str:
        if self.price.startswith("₪"):
            return self.price
        return f"₪{float(self.price):,.2f}"

    @property
    def price_agorot(self) -> int:
        return int(round(float(self.price) * 100))

    def row_range(self) -> tuple[str, str]:
        for separator in ("–", "—", "-"):
            if separator in self.rows:
                start, _, end = self.rows.partition(separator)
                return start.strip(), end.strip()
        return self.rows, self.rows


class FanEventResponse(BaseModel):
    name: str
    lineup: str = ""
    from_price: str = ""
    event_id: str = ""


class AdminEventResponse(BaseModel):
    name: str
    status: str
    venue_line: str = ""
    start_display: str = ""
    can_publish: bool = False
    can_edit: bool = False
    can_delete: bool = False
    event_id: str = ""


class UpdateEventRequest(BaseModel):
    name: str | None = None
    venue: str | None = None
    lineup: str | None = None
    category: str | None = None
    description: str | None = None
    start: str | None = None


class CreateEventRequest(BaseModel):
    name: str
    venue: str
    city: str
    lineup: str
    category: str = "concert"
    description: str = ""
    start: str
    tier: EventTierRequest
    event_id: str | None = None

    @property
    def start_display(self) -> str:
        stamp = self.start.replace("T", " ")
        date, _, time = stamp.partition(" ")
        year, month, day = date.split("-")
        return f"{day}/{month}/{year} {time[:5]}"

    @property
    def venue_line(self) -> str:
        return f"{self.venue} · {self.city}"

    @property
    def from_price(self) -> str:
        return self.tier.display_price

    def as_admin_row(self, status: str = "Draft") -> AdminEventResponse:
        return AdminEventResponse(
            name=self.name,
            status=status,
            venue_line=self.venue,
            start_display=self.start_display,
            can_publish=status == "Draft",
            can_edit=True,
            can_delete=False,
            event_id=self.event_id or "",
        )

    def as_fan_card(self) -> FanEventResponse:
        return FanEventResponse(
            name=self.name,
            lineup=self.lineup,
            from_price=self.tier.display_price,
            event_id=self.event_id or "",
        )

    def api_starts_at(self) -> str:
        start = self.start
        if start.endswith("Z") or (len(start) > 10 and ("+" in start[10:] or start.count("-") > 2)):
            return start
        local = datetime.fromisoformat(start)
        if local.tzinfo is None:
            local = local.replace(tzinfo=_JERUSALEM)
        return local.isoformat()


CREATE_EVENT = CreateEventRequest(
    name="Green Build Live",
    venue="BDO Arena",
    city="Tel Aviv",
    lineup="Green Build Live",
    category="concert",
    description="",
    start="2026-10-05T21:00",
    tier=EventTierRequest(name="Standard", rows="A–H", price="90.00"),
)

UPDATE_EVENT = UpdateEventRequest(name="Green Build Encore")


def _venue_for(request: CreateEventRequest) -> Venue:
    client = VenuesClient.for_organizer()
    try:
        response = client.list()
        assert response.is_success, response.raw
        assert response.data and response.data.items, "no venue to create an event"
        return next(
            (
                venue
                for venue in response.data.items
                if request.venue in venue.name or venue.name in request.venue
            ),
            response.data.items[0],
        )
    finally:
        client.close()


def _tiers_for(request: CreateEventRequest, venue: Venue) -> list[EventTierInput]:
    row_from, row_to = request.tier.row_range()
    if venue.row_count:
        last = chr(ord("A") + venue.row_count - 1)
        row_from, row_to = "A", last
    return [
        EventTierInput(
            name=request.tier.name,
            price_agorot=request.tier.price_agorot,
            row_from=row_from,
            row_to=row_to,
        )
    ]


def create_event(request: CreateEventRequest) -> CreateEventRequest:
    venue = _venue_for(request)
    client = EventsClient.for_organizer()
    try:
        response = client.create(
            ApiCreateEventRequest(
                title=request.name,
                category=cast(EventCategory, request.category),
                venue_id=venue.id,
                starts_at=request.api_starts_at(),
                description=request.description or request.name,
                lineup=request.lineup,
                tiers=_tiers_for(request, venue),
            )
        )
        assert response.status_code == 201 or response.is_success, response.raw
        assert response.data is not None, response.raw
        request.event_id = response.data.id
        return request
    finally:
        client.close()


def publish_event(event_id: str) -> None:
    client = EventsClient.for_organizer()
    try:
        response = client.publish(PublishEventRequest(event_id=event_id))
        assert response.is_success, response.raw
    finally:
        client.close()
