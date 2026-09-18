from playwright.sync_api import Locator, Page

from core.utils.playwright.playwright_client import PlaywrightClient


class SideBarPage:
    def __init__(self, page: Page, playwright_client: PlaywrightClient):
        """Main navigation side bar."""
        self.page = page
        self.pw_client = playwright_client

    def _get_page(self, name: str):
        return self.pw_client.get_by_role("link", name=name)

    @property
    def events(self) -> Locator:
        return self._get_page("Events")

    @property
    def orders(self):
        return self._get_page("My Orders")

    @property
    def inbox(self):
        return self._get_page("Inbox")

    @property
    def admin(self):
        return self._get_page("Admin")

    @property
    def workspace(self):
        return self._get_page("Workspace")

    @property
    def api(self):
        return self._get_page("API")

    def open_events(self):
        self.events.click()

    def open_orders(self):
        self.orders.click()

    def open_inbox(self):
        self.inbox.click()

    def open_admin(self):
        self.admin.click()

    def open_workspace(self):
        self.workspace.click()

    def open_api(self):
        self.api.click()
