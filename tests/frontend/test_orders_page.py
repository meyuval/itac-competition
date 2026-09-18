import pytest
from pytest_check import check

from business.web.arena_webapp import ArenaWebApp as WebApp
from business.web.clients.orders import PAID_ORDER

pytestmark = [pytest.mark.fe, pytest.mark.orders]


@pytest.mark.sanity
def test_my_orders_lists_paid_order(app: WebApp, login: WebApp) -> None:
    expected = PAID_ORDER

    app.orders.goto()
    app.orders.expect_loaded()
    with check:
        assert app.orders.order_visible(expected.event)
    with check:
        assert app.orders.row_shows(expected.event, expected.event_date)
    with check:
        assert app.orders.row_shows(expected.event, expected.seats)
    with check:
        assert app.orders.row_shows(expected.event, expected.total)
    with check:
        assert app.orders.has_status(expected.event, expected.status)
