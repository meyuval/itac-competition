from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from business.web.pages.base_page import BasePage
from core.utils.playwright.playwright_client import PlaywrightClient


class LoginPage(BasePage):
    def __init__(self, page: Page, pw_client: PlaywrightClient):
        super().__init__(page, pw_client)

    @property
    def email(self) -> Locator:
        return self.pw_client.get_by_label("Email")

    @property
    def password(self) -> Locator:
        return self.pw_client.get_by_label("Password")

    @property
    def submit(self) -> Locator:
        return self.pw_client.get_by_role("button", name="Log in")

    def goto(self) -> None:
        super().goto("/")

    def log_in(self, email: str, password: str) -> None:
        self.goto()
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()
        expect(self.side_bar.events).to_be_visible()
