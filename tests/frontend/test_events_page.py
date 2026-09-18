import pytest
from pytest_check import check

from business.web.arena_webapp import ArenaWebApp as WebApp
from business.web.clients.events import (
    CreateEventRequest,
    FanEventResponse,
)

pytestmark = [pytest.mark.fe, pytest.mark.events]


@pytest.mark.sanity
def test_created_draft_is_hidden_from_fans_until_published(
    app: WebApp,
    created_draft: FanEventResponse,
    event_create_request: CreateEventRequest,
) -> None:
    card: FanEventResponse = event_create_request.as_fan_card()

    app.events.goto()
    app.events.expect_loaded()
    with check:
        assert not app.events.has_card(card.name)

    app.events.publish(created_draft.event_id)
    app.events.goto()
    app.events.expect_loaded()
    with check:
        assert app.events.card_visible(card.name)
    with check:
        assert app.events.card_shows(card.name, card.lineup)
    with check:
        assert app.events.card_shows(card.name, card.from_price)
