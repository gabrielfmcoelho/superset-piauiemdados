from pydantic import BaseModel
from typing import Set, List

class Filter(BaseModel):
    values: Set[str] | None

class DashboardFilters(BaseModel):
    year: Filter
    city: Filter
    nature_type_descr: Filter

class Chart(BaseModel):
    
