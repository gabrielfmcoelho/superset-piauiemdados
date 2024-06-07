from fastapi import Query
from pydantic import BaseModel, Field
from typing import Set, List, Optional

class Filter(BaseModel):
    values: Set[str] | None = Field(None)

class DashboardFilters(BaseModel):
    year: Optional[Filter] = Field(Query(None))
    city: Optional[Filter] = Field(Query(None))
    nature_type_descr: Optional[Filter] = Field(Query(None))

class Indicator(BaseModel):
    value: str