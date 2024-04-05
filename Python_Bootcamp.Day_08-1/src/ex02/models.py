from pydantic import BaseModel
from pydantic.types import UUID4
from typing import Optional


class Task(BaseModel):
    id: UUID4
    status: str
    results: Optional[list[int]] = None
