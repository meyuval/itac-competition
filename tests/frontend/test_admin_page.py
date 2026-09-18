import pytest
from pytest_check import check

from business.web.arena_webapp import ArenaWebApp as WebApp
from business.web.clients.events import (
    AdminEventResponse,
    CreateEventRequest,
    UpdateEventRequest,
)

pytestmark = [pytest.mark.fe, pytest.mark.admin]


def test_create_event_saves_as_draft(
    app: WebApp, login: WebApp, event_create_request: CreateEventRequest
):
    app.admin_events.goto()
    app.admin_events.expect_loaded()
    with check:
        assert not app.admin_events.has_event(event_create_request.name)

    app.admin_event_form.goto()
    app.admin_event_form.expect_loaded()
    app.admin_event_form.submit(event_create_request)
    app.admin_events.expect_loaded()

    with check:
        assert app.admin_events.event_visible(event_create_request.name)
    with check:
        assert app.admin_events.has_status(event_create_request.name, "Draft")
    with check:
        assert app.admin_events.row_shows(event_create_request.name, event_create_request.venue)
    with check:
        assert app.admin_events.row_shows(
            event_create_request.name, event_create_request.start_display
        )
    with check:
        assert app.admin_events.can_publish(event_create_request.name)
    with check:
        assert app.admin_events.has_edit(event_create_request.name)


def test_publish_marks_draft_as_published(
    app: WebApp, created_draft: AdminEventResponse
) -> None:
    app.admin_events.goto()
    app.admin_events.expect_loaded()
    app.admin_events.publish(created_draft.name)
    with check:
        assert app.admin_events.has_status(created_draft.name, "Published")
    with check:
        assert not app.admin_events.can_publish(created_draft.name)


def test_edit_renames_draft_event(
    app: WebApp,
    created_draft: AdminEventResponse,
    event_update_request: UpdateEventRequest,
) -> None:
    app.admin_events.goto()
    app.admin_events.expect_loaded()
    app.admin_events.open_edit(created_draft.name)
    app.admin_event_form.expect_loaded("Edit event")
    with check:
        assert app.admin_event_form.name_value() == created_draft.name

    app.admin_event_form.fill(name=event_update_request.name)
    app.admin_event_form.save()
    app.admin_events.expect_loaded()
    with check:
        assert app.admin_events.event_visible(event_update_request.name)
    with check:
        assert app.admin_events.has_status(event_update_request.name, "Draft")
    with check:
        assert not app.admin_events.has_event(created_draft.name)


def test_delete_removes_draft_event(
    app: WebApp, created_draft: AdminEventResponse
) -> None:
    app.admin_events.goto()
    app.admin_events.expect_loaded()
    if not app.admin_events.has_delete(created_draft.name):
        pytest.skip("Admin list does not expose a Delete action")
    app.admin_events.delete(created_draft.name)
    app.admin_events.expect_loaded()
    with check:
        assert not app.admin_events.has_event(created_draft.name)
