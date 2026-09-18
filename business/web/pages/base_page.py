from __future__ import annotations

from urllib.parse import urljoin

from playwright.sync_api import Page

from business.web.pages.side_bar import SideBarPage
from core.utils.playwright.playwright_client import PlaywrightClient

BASE_URL: str = "https://arena.itac.co.il/"


class BasePage:
    def __init__(self, page: Page, pw_client: PlaywrightClient):
        self.page = page
        self.pw_client = pw_client
        self.base_url = BASE_URL.rstrip("/") + "/"
        self.side_bar = SideBarPage(page, pw_client)

    def goto(self, path: str = "") -> None:
        self.pw_client.goto(urljoin(self.base_url, path.lstrip("/")))
