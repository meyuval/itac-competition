from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ApiError(BaseModel):
    model_config = ConfigDict(extra="ignore")

    code: str
    message: str = ""
    details: dict[str, Any] | None = None


class ApiResponse(Generic[T]):
    def __init__(
        self,
        status_code: int,
        *,
        data: T | None = None,
        error: ApiError | None = None,
        raw: Any = None,
        is_success: bool = False,
    ) -> None:
        self.status_code = status_code
        self.data = data
        self.error = error
        self.raw = raw
        self.is_success = is_success
