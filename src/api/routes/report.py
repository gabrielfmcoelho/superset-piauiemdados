from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from icecream import ic


router = APIRouter(
    prefix="/report",
    tags=["report"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/generate",
)
async def generate_report():
    ic("Generating report")
    mock_pdf = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> /ProcSet 5 0 R >> /MediaBox [0 0 612 792] /Contents 6 0 R >>\nendobj\n4 0 obj\n<< /Type /Font /Subtype /Type1 /Name /F1 /BaseFont /Times-Roman >>\nendobj\n5 0 obj\n[ /PDF /Text ]\nendobj\n6 0 obj\n<< /Length 55 >>\nstream\nBT\n/F1 24 Tf\n100 100 Td\n(Hello, world!) Tj\nET\nendstream\nendobj\nxref\n0 7\n0000000000 65535 f \n0000000009 00000 n \n0000000074 00000 n \n0000000121 00000 n \n0000000173 00000 n \n0000000304 00000 n \n0000000363 00000 n \ntrailer\n<< /Size 7 /Root 1 0 R >>\nstartxref\n460\n%%EOF"
    return StreamingResponse(content=mock_pdf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=report.pdf"})