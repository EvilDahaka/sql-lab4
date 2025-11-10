from datetime import datetime
from pydantic import BaseModel, Field


class CreatedAtMixin(BaseModel):
    create_at: datetime


class Pagination(BaseModel):
    offset: int = Field(gte=0)
    limit: int = Field(ge=0, le=200)
