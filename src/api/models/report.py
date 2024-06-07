from pydantic import BaseModel


class ReportRequest(BaseModel):
    data: dict
    screenshot: str