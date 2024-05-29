from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from icecream import ic

from handlers.report_builder import build_report


router = APIRouter(
    prefix="/report",
    tags=["report"],
)


@router.post(
    "/generate",
)
async def generate_report(
):
    ic("Generating report")
    report_data = None
    if not report_data:
        #return {"message": "No data to generate report"}
        report_data = {
            "title": "Relatório de empresas ativas",
            "subtitle": "Relatório de empresas ativas por município",
            "data": [
                {
                    "city": "Teresina",
                    "amount": 1000
                },
                {
                    "city": "Parnaíba",
                    "amount": 500
                }
            ]
        }
    pdf = build_report(report_data)
    return StreamingResponse(pdf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=relatorio.pdf"})
