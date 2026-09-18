from __future__ import annotations

from business.api.models.venues import ListVenuesResponse
from core.api.client import HttpClient
from core.api.response import ApiResponse
from core.utils.config import settings


class VenuesClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    @classmethod
    def for_organizer(cls) -> VenuesClient:
        return cls(HttpClient(api_key=settings.organization_api_key))

    def list(self) -> ApiResponse[ListVenuesResponse]:
        return self._http.get("/venues", response_model=ListVenuesResponse)

    def close(self) -> None:
        self._http.close()
