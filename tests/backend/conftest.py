from __future__ import annotations

import time

import pytest

from business.api.clients.events import EventsClient
from business.api.clients.venues import VenuesClient
from business.api.clients.workspace import WorkspaceClient
from business.api.models.venues import Venue
from core.utils.config import settings


@pytest.fixture(autouse=True)
def reset_workspace() -> None:
    client = WorkspaceClient.for_organizer()
    try:
        response = client.reset()
        if response.status_code == 429:
            time.sleep(6)
            response = client.reset()
        assert response.is_success, response.raw
    finally:
        client.close()


@pytest.fixture
def organizer_events() -> EventsClient:
    client = EventsClient.for_organizer()
    yield client
    client.close()


@pytest.fixture
def fan_events() -> EventsClient:
    if not settings.fan_api_key:
        pytest.skip("FAN_API_KEY is not set")
    client = EventsClient.for_fan()
    yield client
    client.close()


@pytest.fixture
def venue() -> Venue:
    client = VenuesClient.for_organizer()
    try:
        response = client.list()
        assert response.is_success, response.raw
        assert response.data and response.data.items, "no venue to create an event"
        return response.data.items[0]
    finally:
        client.close()
