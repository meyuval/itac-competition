from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypeVar

import requests
from pydantic import BaseModel
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from core.api.response import ApiError, ApiResponse
from core.utils.config import settings
from core.utils.logger.logger import get_logger

T = TypeVar("T", bound=BaseModel)
logger = get_logger()

_RETRY_METHODS = frozenset({"GET", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"})
_RETRY_STATUSES = (500, 502, 503, 504)


@dataclass(frozen=True)
class RetryStrategy:
    total: int = 3
    backoff_factor: float = 0.5
    status_forcelist: tuple[int, ...] = _RETRY_STATUSES
    allowed_methods: frozenset[str] = field(default_factory=lambda: _RETRY_METHODS)

    def __post_init__(self) -> None:
        object.__setattr__(self, "allowed_methods", frozenset(self.allowed_methods))

    def to_retry(self) -> Retry:
        return Retry(
            total=self.total,
            connect=self.total,
            read=self.total,
            status=self.total,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
            allowed_methods=self.allowed_methods,
            raise_on_status=False,
        )


class HttpClient:
    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        api_key_header: str | None = None,
        timeout_ms: int | None = None,
        retry: RetryStrategy | None = None,
        verify: bool | None = None,
    ) -> None:
        self.base_url = (base_url or settings.api_base).rstrip("/")
        self.timeout_s = (timeout_ms or settings.default_timeout_ms) / 1000
        self._session = requests.Session()
        self._session.verify = settings.ssl_verify if verify is None else verify
        self._session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        if api_key:
            self._session.headers[api_key_header or settings.api_key_header] = api_key
        adapter = HTTPAdapter(max_retries=(retry or RetryStrategy()).to_retry())
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        response_model: type[T] | None = None,
    ) -> ApiResponse[T]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self._session.request(
            method=method.upper(),
            url=url,
            params=_query_params(params),
            json=json,
            timeout=self.timeout_s,
        )
        logger.info("%s %s -> %s", method.upper(), url, response.status_code)
        return _to_api_response(response, response_model)

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        response_model: type[T] | None = None,
    ) -> ApiResponse[T]:
        return self.request("GET", path, params=params, response_model=response_model)

    def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        response_model: type[T] | None = None,
    ) -> ApiResponse[T]:
        return self.request("POST", path, json=json, response_model=response_model)

    def patch(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        response_model: type[T] | None = None,
    ) -> ApiResponse[T]:
        return self.request("PATCH", path, json=json, response_model=response_model)

    def delete(
        self,
        path: str,
        *,
        response_model: type[T] | None = None,
    ) -> ApiResponse[T]:
        return self.request("DELETE", path, response_model=response_model)

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> HttpClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


def _query_params(params: dict[str, Any] | None) -> dict[str, Any] | None:
    if not params:
        return None
    serialized: dict[str, Any] = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, bool):
            serialized[key] = "true" if value else "false"
        else:
            serialized[key] = value
    return serialized


def _json_body(response: requests.Response) -> Any:
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def _to_api_response(
    response: requests.Response, response_model: type[T] | None
) -> ApiResponse[T]:
    raw = _json_body(response)
    data: T | None = None
    error: ApiError | None = None
    if response.ok:
        if response_model is not None and raw not in (None, ""):
            data = response_model.model_validate(raw)
    elif isinstance(raw, dict) and isinstance(raw.get("error"), dict):
        error = ApiError.model_validate(raw["error"])
    return ApiResponse(
        response.status_code,
        data=data,
        error=error,
        raw=raw,
        is_success=response.ok,
    )
