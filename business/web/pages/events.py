from playwright.sync_api import Locator, Page, expect

from business.web.clients.events import publish_event
from business.web.pages.base_page import BasePage
from core.utils.playwright.playwright_client import PlaywrightClient


class Events(BasePage):
    def __init__(self, page: Page, pw_client: PlaywrightClient):
        super().__init__(page, pw_client)

    def publish(self, event_id: str) -> None:
        publish_event(event_id)

    def goto(self) -> None:
        super().goto("/events")

    def expect_loaded(self) -> None:
        expect(self.pw_client.get_by_role("heading", name="Events", exact=True)).to_be_visible()

    def _search(self, name: str) -> None:
        box = self.page.get_by_placeholder("Name or lineup")
        box.fill(name)
        box.press("Enter")

    def card(self, name: str) -> Locator:
        return self.page.get_by_role("listitem").filter(
            has=self.pw_client.get_by_role("heading", name=name)
        )

    def has_card(self, name: str) -> bool:
        self._search(name)
        return self.pw_client.get_by_role("heading", name=name).count() > 0

    def card_visible(self, name: str) -> bool:
        self._search(name)
        expect(self.pw_client.get_by_role("heading", name=name)).to_be_visible()
        return True

    def card_shows(self, name: str, text: str) -> bool:
        self._search(name)
        expect(self.card(name)).to_contain_text(text)
        return True
