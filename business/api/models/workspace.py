from __future__ import annotations

from business.api.models.common import ArenaBaseModel


class ResetWorkspaceResponse(ArenaBaseModel):
    status: str
    seed_pack: str | None = None
    reset_at: str | None = None
