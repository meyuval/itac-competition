from __future__ import annotations

from uuid import uuid4

import pytest
from playwright.sync_api import Page, expect

from business.web.arena_webapp import ArenaWebApp as WebApp
from business.web.clients.events import (
    CREATE_EVENT,
    CreateEventRequest,
    FanEventResponse,
    UPDATE_EVENT,
    UpdateEventRequest,
    create_event,
)
from core.utils.config import settings


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "timezone_id": "Asia/Jerusalem",
        "locale": "en-IL",
    }


@pytest.fixture(scope="session", autouse=True)
def configure_playwright_expect() -> None:
    expect.set_options(timeout=settings.default_timeout_ms)


@pytest.fixture(autouse=True)
def configure_page(page: Page) -> None:
    timeout_ms = settings.default_timeout_ms
    page.set_default_timeout(timeout_ms)
    page.set_default_navigation_timeout(timeout_ms)
    page.context.set_default_timeout(timeout_ms)
    page.context.set_default_navigation_timeout(timeout_ms)


@pytest.fixture
def event_create_request() -> CreateEventRequest:
    return CREATE_EVENT.model_copy(update={"name": f"{CREATE_EVENT.name} {uuid4().hex[:8]}"})


@pytest.fixture
def event_update_request() -> UpdateEventRequest:
    return UPDATE_EVENT.model_copy(update={"name": f"{UPDATE_EVENT.name} {uuid4().hex[:8]}"})


@pytest.fixture
def created_draft(
    app: WebApp,
    login: WebApp,
    event_create_request: CreateEventRequest,
) -> FanEventResponse:
    create_event(event_create_request)
    return event_create_request.as_fan_card()


@pytest.fixture
def created_published(app: WebApp, created_draft: FanEventResponse) -> FanEventResponse:
    app.events.publish(created_draft.event_id)
    return created_draft
