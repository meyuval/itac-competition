from __future__ import annotations

from business.api.models.workspace import ResetWorkspaceResponse
from core.api.client import HttpClient
from core.api.response import ApiResponse
from core.utils.config import settings


class WorkspaceClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    @classmethod
    def for_organizer(cls) -> WorkspaceClient:
        return cls(HttpClient(api_key=settings.organization_api_key))

    def reset(self) -> ApiResponse[ResetWorkspaceResponse]:
        return self._http.post("/reset", response_model=ResetWorkspaceResponse)

    def close(self) -> None:
        self._http.close()
