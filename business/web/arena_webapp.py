from playwright.sync_api import Page

from business.web.pages.admin import AdminEventFormPage, AdminEventsPage
from business.web.pages.events import Events
from business.web.pages.login import LoginPage
from business.web.pages.orders import OrdersPage
from business.web.pages.side_bar import SideBarPage
from core.utils.playwright.playwright_client import PlaywrightClient


class ArenaWebApp:
    def __init__(self, page: Page):
        self.page = page
        self.pw_client = PlaywrightClient(self.page)

        self.side_bar = SideBarPage(self.page, self.pw_client)
        self.login = LoginPage(self.page, self.pw_client)
        self.admin_events = AdminEventsPage(self.page, self.pw_client)
        self.admin_event_form = AdminEventFormPage(self.page, self.pw_client)
        self.admin = self.admin_events
        self.events = Events(self.page, self.pw_client)
        self.orders = OrdersPage(self.page, self.pw_client)
