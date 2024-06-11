from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from icecream import ic
from datetime import datetime as dt

from handlers.report_builder import ReportBuilder
from models.report import ReportRequest
from mock.report_data import MOCK_REPORT_DATA as mock_data


router = APIRouter(
    prefix="/report",
    tags=["report"],
)


@router.post(
    "/generate",
)
async def generate_report(
    report_data: ReportRequest,
):
    ic("Generating report")
    report_data = report_data.dict() if report_data else mock_data

    report_data["screenshot"] = report_data["screenshot"].replace("data:image/png;base64,", "")
    ic(report_data["screenshot"][:10])

    report_data["metadata"] = {
        "title": "Relatório de Desenvolvimento",
        "subtitle": " | ".join(report_data["data"].keys()),
        "date": dt.now().strftime("%d/%m/%Y"),
    }

    pdf_builder = ReportBuilder(report_data)
    pdf_file = pdf_builder.build_report()

    return StreamingResponse(pdf_file, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=relatorio.pdf"})
