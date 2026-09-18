from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from business.web.pages.base_page import BasePage
from core.utils.playwright.playwright_client import PlaywrightClient


class OrdersPage(BasePage):
    def __init__(self, page: Page, pw_client: PlaywrightClient):
        super().__init__(page, pw_client)

    @property
    def heading(self) -> Locator:
        return self.pw_client.get_by_role("heading", name="My orders")

    def goto(self) -> None:
        super().goto("/orders")

    def expect_loaded(self) -> None:
        expect(self.heading).to_be_visible()

    def row(self, event: str) -> Locator:
        return self.page.get_by_role("row").filter(
            has=self.page.get_by_role("cell", name=event, exact=True)
        ).first

    def order_visible(self, event: str) -> bool:
        expect(self.row(event)).to_be_visible()
        return True

    def has_status(self, event: str, status: str) -> bool:
        return status in (self.row(event).inner_text() or "")

    def row_shows(self, event: str, text: str) -> bool:
        return text in (self.row(event).inner_text() or "")
