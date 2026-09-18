from __future__ import annotations

from pydantic import Field

from business.api.models.common import ArenaBaseModel


class Venue(ArenaBaseModel):
    id: str
    name: str
    city: str
    row_count: int | None = None
    seats_per_row: int | None = None


class ListVenuesResponse(ArenaBaseModel):
    items: list[Venue] = Field(default_factory=list)
