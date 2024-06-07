from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter
from icecream import ic
import pandas as pd

from schemas.opening_companies import OpeningCompany, OpeningCompanyActivities, OpeningCompanyTimeSeries, Opening
from handlers.db_file_ingester import DatabaseFileIngester
from database.connector import Connector


db_connector = Connector.get_instance()


router = APIRouter(
    prefix="/populatedb",
    tags=["populatedb"],
)


@contextmanager
def get_db_session():
    SessionLocal = db_connector.get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/file/{filename}",
    response_model=dict,
)
async def populate_from_file(filename: str):
    ic(f"Populating {filename}")
    with get_db_session() as db:
        file_ingester = DatabaseFileIngester(db, filename)
        output = file_ingester.ingest_into_db()
        file_ingester.generate_insertion_report()
        if output["integrity_errors"] < 1:
            return {"message": f"Dados de {filename} inseridos com sucesso"}
        return {"message": f"Dados de {filename} inseridos com sucesso, com erros de integridade", "log": f"Erros: {output['integrity_errors']}, registros com erro: {output['integrity_errors']}"}

@router.get(
    "/",
    response_model=dict,
)
async def populate_all():
    ic("Populating all")
    output_compiled = []

    files = ["empresas-ativas", "empresas-ativas-atividades", "aberturas", "atividades-aberturas", "tempo-aberturas", "opening"]

    for filename in files:
        output = await populate_from_file(filename)
        output_compiled.append(output)

    return {"message": "Processo finalizado", "output": output_compiled}