from __future__ import annotations

from business.api.models.events import (
    CreateEventRequest,
    CreateEventResponse,
    GetEventByIdRequest,
    GetEventByIdResponse,
    GetEventSalesRequest,
    GetEventSalesResponse,
    GetEventSeatsRequest,
    GetEventSeatsResponse,
    ListEventsRequest,
    ListEventsResponse,
    PublishEventRequest,
    PublishEventResponse,
    UnpublishEventRequest,
    UnpublishEventResponse,
    UpdateEventRequest,
    UpdateEventResponse,
)
from core.api.http_client import HttpClient
from core.api.response import ApiResponse
from core.utils.config import settings


class EventsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    @classmethod
    def for_fan(cls) -> EventsClient:
        return cls(HttpClient(api_key=settings.fan_api_key))

    @classmethod
    def for_organizer(cls) -> EventsClient:
        return cls(HttpClient(api_key=settings.organization_api_key))

    def search(
        self, request: ListEventsRequest | None = None
    ) -> ApiResponse[ListEventsResponse]:
        params = (request or ListEventsRequest()).model_dump(
            exclude_none=True, by_alias=True
        )
        return self._http.get("/events", params=params, response_model=ListEventsResponse)

    def get_by_id(
        self, request: GetEventByIdRequest
    ) -> ApiResponse[GetEventByIdResponse]:
        return self._http.get(
            f"/events/{request.event_id}", response_model=GetEventByIdResponse
        )

    def seats(
        self, request: GetEventSeatsRequest
    ) -> ApiResponse[GetEventSeatsResponse]:
        return self._http.get(
            f"/events/{request.event_id}/seats",
            response_model=GetEventSeatsResponse,
        )

    def create(self, request: CreateEventRequest) -> ApiResponse[CreateEventResponse]:
        return self._http.post(
            "/events",
            json=request.model_dump(exclude_none=True, by_alias=True),
            response_model=CreateEventResponse,
        )

    def update(self, request: UpdateEventRequest) -> ApiResponse[UpdateEventResponse]:
        return self._http.patch(
            f"/events/{request.event_id}",
            json=request.model_dump(exclude={"event_id"}, exclude_none=True, by_alias=True),
            response_model=UpdateEventResponse,
        )

    def publish(
        self, request: PublishEventRequest
    ) -> ApiResponse[PublishEventResponse]:
        return self._http.post(
            f"/events/{request.event_id}/publish",
            response_model=PublishEventResponse,
        )

    def unpublish(
        self, request: UnpublishEventRequest
    ) -> ApiResponse[UnpublishEventResponse]:
        return self._http.post(
            f"/events/{request.event_id}/unpublish",
            response_model=UnpublishEventResponse,
        )

    def sales(
        self, request: GetEventSalesRequest
    ) -> ApiResponse[GetEventSalesResponse]:
        return self._http.get(
            f"/events/{request.event_id}/sales",
            response_model=GetEventSalesResponse,
        )

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> EventsClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
