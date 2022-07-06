import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel


class DataModel(BaseModel):
    id: uuid.UUID
    title: str
    open_date: datetime
    close_date: Optional[datetime] = None
    max_value: Decimal
    description_length: int
    ddl_time: float
    requirements_length: int
    criterion: Optional[str] = None
    state: Optional[str] = 'ended'

