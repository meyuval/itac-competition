from __future__ import annotations

from pydantic import BaseModel


class OrderRow(BaseModel):
    event: str
    event_date: str
    seats: str
    total: str
    status: str


PAID_ORDER = OrderRow(
    event="Kickoff Night",
    event_date="16/09/2026 20:30",
    seats="H10",
    total="₪103.84",
    status="Paid",
)
