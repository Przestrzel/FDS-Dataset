import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, constr

region_regex = r'[0-9]{2}-[0-9]{3}'


class Bid(BaseModel):
    name: str
    city: str
    region: constr(regex=region_regex)


class Tender(BaseModel):
    title: str
    open_date: datetime
    close_date: Optional[datetime] = None
    max_value: Decimal
    end_value: Optional[Decimal]
    description_length: int
    ddl_time: Optional[datetime]
    criterion: Optional[str] = None
    state: Optional[str] = 'ended'
    lots: Optional[List[Bid]] = None
    CPV: Optional[str] = None
    is_euFund: bool = False
    procedure_type: Optional[str] = None


class PublicInstitution(BaseModel):
    name: str
    type: str
    activity: Optional[str] = None
    address_city: str


