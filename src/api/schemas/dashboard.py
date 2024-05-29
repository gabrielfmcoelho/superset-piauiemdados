from pydantic import BaseModel
from typing import Set, List

class Filter(BaseModel):
    values: Set[str] | None

class DashboardFilters(BaseModel):
    year: Filter | None
    city: Filter | None
    nature_type_descr: Filter | None

class Indicator(BaseModel):
    value: str

class Chart(BaseModel):
