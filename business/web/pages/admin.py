from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from business.web.clients.events import CreateEventRequest, UpdateEventRequest, create_event
from business.web.pages.base_page import BasePage
from core.utils.playwright.playwright_client import PlaywrightClient


class AdminEventsPage(BasePage):
    def __init__(self, page: Page, pw_client: PlaywrightClient):
        super().__init__(page, pw_client)

    @property
    def heading(self) -> Locator:
        return self.pw_client.get_by_role("heading", name="Manage events")

    @property
    def new_event(self) -> Locator:
        return self.pw_client.get_by_role("link", name="New event")

    def promo_link(self) -> Locator:
        return self.pw_client.get_by_role("link", name="Promo codes")

    def goto(self) -> None:
        super().goto("/admin/events")

    def expect_loaded(self) -> None:
        expect(self.heading).to_be_visible()

    def row(self, name: str) -> Locator:
        return self.page.get_by_role("row").filter(
            has=self.page.get_by_role("cell", name=name, exact=True)
        ).first

    def has_event(self, name: str) -> bool:
        return self.row(name).count() > 0

    def event_visible(self, name: str) -> bool:
        expect(self.row(name)).to_be_visible()
        return True

    def has_status(self, name: str, status: str) -> bool:
        return status in (self.row(name).inner_text() or "")

    def row_shows(self, name: str, text: str) -> bool:
        return text in (self.row(name).inner_text() or "")

    def publish_button(self, name: str) -> Locator:
        return self.row(name).get_by_role("button", name="Publish", exact=True)

    def can_publish(self, name: str) -> bool:
        return self.publish_button(name).count() > 0

    def has_edit(self, name: str) -> bool:
        return self.row(name).get_by_role("link", name="Edit").count() > 0

    def has_delete(self, name: str) -> bool:
        row = self.row(name)
        return (
            row.get_by_role("button", name="Delete").count() > 0
            or row.get_by_role("link", name="Delete").count() > 0
        )

    def publish(self, name: str) -> None:
        self.publish_button(name).click()
        expect(self.row(name).get_by_text("Published", exact=True)).to_be_visible()
        expect(self.publish_button(name)).to_have_count(0)

    def open_edit(self, name: str) -> None:
        self.row(name).get_by_role("link", name="Edit").click()

    def delete(self, name: str) -> None:
        row = self.row(name)
        delete_button = row.get_by_role("button", name="Delete")
        delete_link = row.get_by_role("link", name="Delete")
        if delete_button.count():
            delete_button.click()
        else:
            delete_link.click()
        confirm = self.pw_client.get_by_role("button", name="Confirm")
        if confirm.count():
            confirm.click()


class AdminEventFormPage(BasePage):
    def __init__(self, page: Page, pw_client: PlaywrightClient):
        super().__init__(page, pw_client)

    def goto(self) -> None:
        super().goto("/admin/events/new")

    def expect_loaded(self, heading: str = "New event") -> None:
        expect(self.pw_client.get_by_role("heading", name=heading)).to_be_visible()

    def name_value(self) -> str:
        return self.pw_client.locator("#event-name").input_value()

    def fill(
        self,
        request: UpdateEventRequest | CreateEventRequest | None = None,
        **fields: str | None,
    ) -> None:
        data: dict[str, str | None] = {}
        if request is not None:
            data.update(
                {key: value for key, value in request.model_dump().items() if value is not None}
            )
        data.update({key: value for key, value in fields.items() if value is not None})

        if name := data.get("name"):
            self.pw_client.locator("#event-name").fill(name)
        if lineup := data.get("lineup"):
            self.pw_client.locator("#event-lineup").fill(lineup)
        if category := data.get("category"):
            self.pw_client.locator("#event-category").select_option(label=category.capitalize())
        if venue := data.get("venue"):
            select = self.pw_client.locator("#event-venue")
            self.page.wait_for_function(
                "() => document.querySelectorAll('#event-venue option').length > 1"
            )
            match = next(
                (
                    text.strip()
                    for text in select.locator("option").all_inner_texts()
                    if venue in text
                ),
                None,
            )
            if match is None:
                raise AssertionError(
                    f"No venue option containing {venue!r}: {select.locator('option').all_inner_texts()}"
                )
            select.select_option(label=match)
        if start := data.get("start"):
            self.pw_client.locator("#event-starts").fill(start)
        if "description" in data and data["description"] is not None:
            self.pw_client.locator("#event-description").fill(data["description"])

    def add_tier(self, name: str, rows: str, price: str, index: int = 0) -> None:
        row_from, row_to = _split_rows(rows)
        if index > 0:
            self.pw_client.get_by_role("button", name="Add tier").click()
        self.pw_client.locator(f"#tier-name-{index}").fill(name)
        self.pw_client.locator(f"#tier-price-{index}").fill(price)
        self.pw_client.locator(f"#tier-from-{index}").fill(row_from)
        self.pw_client.locator(f"#tier-to-{index}").fill(row_to)

    def save(self) -> None:
        create = self.pw_client.get_by_role("button", name="Create event")
        if create.is_visible():
            create.click()
        else:
            self.pw_client.get_by_role("button", name="Save changes").click()
        expect(self.pw_client.get_by_role("heading", name="Manage events")).to_be_visible()

    def submit(self, request: CreateEventRequest) -> None:
        create_event(request)
        AdminEventsPage(self.page, self.pw_client).goto()
        AdminEventsPage(self.page, self.pw_client).expect_loaded()


def _split_rows(rows: str) -> tuple[str, str]:
    for separator in ("–", "—", "-"):
        if separator in rows:
            start, _, end = rows.partition(separator)
            return start.strip(), end.strip()
    return rows, rows
