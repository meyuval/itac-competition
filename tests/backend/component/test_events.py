from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from business.api.clients.events import EventsClient
from business.api.models.events import (
    CreateEventRequest,
    CreateEventResponse,
    EventTierInput,
    GetEventByIdRequest,
    ListEventsRequest,
    PublishEventRequest,
    UpdateEventRequest,
)
from business.api.models.venues import Venue
from core.utils.config import settings

pytestmark = [pytest.mark.be, pytest.mark.events, pytest.mark.live_api, pytest.mark.component]

CREATE_TITLE_PREFIX = "API CRUD Draft Show"
RENAMED_TITLE_PREFIX = "API CRUD Draft Encore"


def _title(prefix: str) -> str:
    return f"{prefix} {uuid4().hex[:8]}"


def _starts_at() -> str:
    return (datetime.now(UTC) + timedelta(days=21)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _row_letters(count: int) -> list[str]:
    return [chr(ord("A") + index) for index in range(count)]


def _tiers_for_venue(venue: Venue) -> list[EventTierInput]:
    rows = _row_letters(venue.row_count or 8)
    return [
        EventTierInput(
            name="Standard",
            price_agorot=12000,
            row_from=rows[0],
            row_to=rows[-1],
        )
    ]


def _create_draft(
    events: EventsClient, venue: Venue, title: str
) -> CreateEventResponse:
    response = events.create(
        CreateEventRequest(
            title=title,
            category="concert",
            venue_id=venue.id,
            starts_at=_starts_at(),
            description=title,
            lineup=title,
            tiers=_tiers_for_venue(venue),
        )
    )
    assert response.status_code == 201 or response.is_success, response.raw
    assert response.data is not None, response.raw
    return response.data


def _listed_titles(events: EventsClient, **params: object) -> set[str]:
    response = events.search(ListEventsRequest.model_validate(params))
    assert response.is_success, response.raw
    assert response.data is not None
    return {item.title for item in response.data.items}


@pytest.mark.sanity
def test_organizer_creates_draft_and_reads_it_back(
    organizer_events: EventsClient, venue: Venue
) -> None:
    title = _title(CREATE_TITLE_PREFIX)
    created = _create_draft(organizer_events, venue, title)
    assert "draft" in created.status.lower()

    fetched = organizer_events.get_by_id(GetEventByIdRequest(event_id=created.id))
    assert fetched.status_code == 200 or fetched.is_success, fetched.raw
    assert fetched.data is not None, fetched.raw
    assert fetched.data.id == created.id
    assert fetched.data.title == title


@pytest.mark.sanity
def test_created_draft_hidden_from_fans_until_published(
    organizer_events: EventsClient,
    venue: Venue,
) -> None:
    title = _title(CREATE_TITLE_PREFIX)
    created = _create_draft(organizer_events, venue, title)

    listed = _listed_titles(organizer_events, q=title)
    assert title not in listed

    fan = EventsClient.for_fan() if settings.fan_api_key else None
    try:
        if fan is not None:
            fan_get = fan.get_by_id(GetEventByIdRequest(event_id=created.id))
            assert fan_get.status_code == 404
            assert fan_get.error is not None
            assert fan_get.error.code == "NOT_FOUND"

        published = organizer_events.publish(PublishEventRequest(event_id=created.id))
        assert published.is_success, published.raw
        assert published.data is None or published.data.status == "published"

        listed = _listed_titles(organizer_events, q=title)
        assert title in listed

        if fan is not None:
            fan_get = fan.get_by_id(GetEventByIdRequest(event_id=created.id))
            assert fan_get.is_success, fan_get.raw
            assert fan_get.data is not None
            assert fan_get.data.id == created.id
            assert fan_get.data.title == title
    finally:
        if fan is not None:
            fan.close()


def test_organizer_updates_draft_event(
    organizer_events: EventsClient, venue: Venue
) -> None:
    title = _title(CREATE_TITLE_PREFIX)
    renamed = _title(RENAMED_TITLE_PREFIX)
    created = _create_draft(organizer_events, venue, title)

    response = organizer_events.update(
        UpdateEventRequest(event_id=created.id, title=renamed)
    )
    assert response.is_success, response.raw

    fetched = organizer_events.get_by_id(GetEventByIdRequest(event_id=created.id))
    assert fetched.is_success, fetched.raw
    assert fetched.data is not None
    assert fetched.data.title == renamed
    assert fetched.data.title != title
