from fastapi import APIRouter
from icecream import ic

from routes.populatedb import router as populatedb_router
from routes.report import router as report_router


router = APIRouter(
    prefix="/api",
    tags=["api"],
)

router.include_router(populatedb_router)
router.include_router(report_router)


@router.get("/")
async def root():
    return {"message": "Bem-vindo a API de gerenciamento de dados do Piauí em Dados"}

@router.post("/api/ping")
async def root_post():
    return {"data":"pong"}