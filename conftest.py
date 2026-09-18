from __future__ import annotations

from uuid import uuid4

import pytest
import urllib3
from playwright.sync_api import Page

from business.web.arena_webapp import ArenaWebApp as WebApp
from business.web.clients.events import CREATE_EVENT, UPDATE_EVENT, CreateEventRequest, UpdateEventRequest
from core.utils.config import settings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
settings.ssl_verify = False


@pytest.fixture
def app(page: Page) -> WebApp:
    return WebApp(page)


@pytest.fixture
def login(app: WebApp) -> WebApp:
    app.login.log_in(settings.fan_email, settings.fan_password)
    return app


@pytest.fixture
def event_create_request() -> CreateEventRequest:
    return CREATE_EVENT.model_copy(update={"name": f"Green Build {uuid4().hex[:8]}"})


@pytest.fixture
def event_update_request() -> UpdateEventRequest:
    return UPDATE_EVENT.model_copy(update={"name": f"Green Encore {uuid4().hex[:8]}"})
