from pydantic import BaseModel, Field
from typing import Literal

class FilterParams(BaseModel):
    finished: bool | None = None
    limit: int = Field(ge=1, default=10, le=100)
    offset: int = Field(ge=0, default=0)
    sort_by: Literal["id", "finished", "task_name"] = "id"
    order: Literal["asc", "desc"] = "asc"