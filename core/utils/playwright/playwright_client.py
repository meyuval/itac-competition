class PlaywrightClient:
    def __init__(self, page) -> None:
        self.page = page

    def goto(self, url: str):
        if self.page is None:
            raise RuntimeError("Playwright is not initialized")
        self.page.goto(url)

    def screenshot(self, path: str):
        return self.page.screenshot(path)

    def locator(self, selector: str):
        return self.page.locator(selector)

    def get_by_test_id(self, test_id: str):
        return self.page.get_by_test_id(test_id)

    def get_by_role(self, role, name: str | None = None, exact: bool = False):
        if name is None:
            return self.page.get_by_role(role)
        return self.page.get_by_role(role, name=name, exact=exact)

    def get_by_label(self, label: str):
        return self.page.get_by_label(label)

    def get_by_placeholder(self, placeholder: str):
        return self.page.get_by_placeholder(placeholder)

    def get_by_text(self, text: str, exact: bool = False):
        return self.page.get_by_text(text, exact=exact)
