from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ArenaBaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)
