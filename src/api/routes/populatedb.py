from contextlib import contextmanager
# import integrityerror
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter
from icecream import ic
import os
import pandas as pd

from models.opening_companies import OpeningCompany, OpeningCompanyActivities, OpeningCompanyTimeSeries, Opening
from models.active_companies import ActiveCompany, ActiveCompanyActivities
from database.connector import Connector


db_connector = Connector.get_instance()


router = APIRouter(
    prefix="/populatedb",
    tags=["populatedb"],
)


def read_csv(filename: str):
    ic(f"Reading file {filename}")
    #ic(os.getcwd())
    #ic(os.listdir())
    #ic(os.listdir("datasets/preprocessed"))
    df = pd.read_csv(f'datasets/final/{filename}-final.csv', sep=";", decimal=",", encoding="utf-8")
    ic(df.info())
    return df

@contextmanager
def get_db_session():
    SessionLocal = db_connector.get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/opening_companies",
    response_model=dict,
)
async def populate_opening_companies():
    ic("Populating opening companies")
    df = read_csv("aberturas")
    with get_db_session() as db:
        for index, row in df.iterrows():
            company = OpeningCompany(
                hash_key=row["hash_chave_abertura"],
                year=row["ano"],
                month=row["mês"],
                size=row["porte"],
                nature_type_code=row["cod_natureza"],
                nature_type_descr=row["descr_natureza"],
                city=row["municipio"],
                is_branch=row["filial"],
                amount=row["qtd"]
            )
            try:
                db.add(company)
                db.commit()
                db.refresh(company)
            except IntegrityError as e:
                ic(f"Duplicated hash found, ignoring it: {row}")
                db.rollback()
                continue
    return {"message": "Dados de empresas abertas inseridos com sucesso"}

@router.get(
    "/opening_companies_activities",
    response_model=dict,
)
async def populate_opening_companies_activities():
    ic("Populating opening companies activities")
    df = read_csv("atividades-aberturas")
    with get_db_session() as db:
        for index, row in df.iterrows():
            activity = OpeningCompanyActivities(
                hash_key=row["hash_chave_abertura"],
                cnae=row["cod_atividade"],
                cnae_descr=row["descr_atividade"],
                segment=row["seguimento"],
                amount=row["qtd"]
            )
            try:
                db.add(activity)
                db.commit()
                db.refresh(activity)
            except IntegrityError as e:
                ic(f"Duplicated hash found, ignoring it: {row}")
                db.rollback()
                continue
    return {"message": "Dados de atividades de empresas abertas inseridos com sucesso"}

@router.get(
    "/opening_companies_time_series",
    response_model=dict,
)
async def populate_opening_companies_time_series():
    ic("Populating opening companies time series")
    df = read_csv("tempo-aberturas")
    with get_db_session() as db:
        for index, row in df.iterrows():
            time_series = OpeningCompanyTimeSeries(
                year=row["ano"],
                month=row["mês"],
                serial_identifier=row["serial"],
                nature_type_code=row["cod_natureza"],
                nature_type_descr=row["natureza"],
                city=row["municipio"],
                cp_name=row["cp_nome"],
                cp_address=row["cp_endereco"],
                cp_total=row["cp_total"],
                register=row["registro"],
            )
            try:
                db.add(time_series)
                db.commit()
                db.refresh(time_series)
            except IntegrityError as e:
                ic(f"Duplicated hash found, ignoring it: {row}")
                db.rollback()
                continue
    return {"message": "Dados de séries temporais de empresas abertas inseridos com sucesso"}

@router.get(
    "/active_companies",
    response_model=dict,
)
async def populate_active_companies():
    ic("Populating active companies")
    df = read_csv("empresas-ativas")
    with get_db_session() as db:
        for index, row in df.iterrows():
            company = ActiveCompany(
                hash_key=row["hash_chave"],
                size=row["porte"],
                nature_type_code=row["cod_natureza"],
                nature_type_descr=row["natureza"],
                city=row["municipio"],
                is_branch=row["filial"],
                amount=row["qtd"]
            )
            try:
                db.add(company)
                db.commit()
                db.refresh(company)
            except IntegrityError as e:
                ic(f"Duplicated hash found, ignoring it: {row}")
                db.rollback()
                continue
    return {"message": "Dados de empresas ativas inseridos com sucesso"}

@router.get(
    "/active_companies_activities",
    response_model=dict,
)
async def populate_active_companies_activities():
    ic("Populating active companies activities")
    df = read_csv("empresas-ativas-atividades")
    with get_db_session() as db:
        for index, row in df.iterrows():
            activity = ActiveCompanyActivities(
                hash_key=row["hash_chave"],
                cnae=row["cod_atividade"],
                cnae_descr=row["descr_atividade"],
                is_main_cnae=row["principal"],
                segment=row["seguimento"],
                amount=row["qtd"]
            )
            try:
                db.add(activity)
                db.commit()
                db.refresh(activity)
            except IntegrityError as e:
                ic(f"Duplicated hash found, ignoring it: {row}")
                db.rollback()
                continue
    return {"message": "Dados de atividades de empresas ativas inseridos com sucesso"}

@router.get(
    "/opening",
    response_model=dict,
)
async def populate_opening():
    ic("Populating opening")
    df = read_csv("opening")
    with get_db_session() as db:
        for index, row in df.iterrows():
            opening = Opening(
                hash_key=row["hash_chave_abertura"],
                year=row["ano"],
                month=row["mês"],
                size=row["porte"],
                nature_type_code=row["cod_natureza"],
                nature_type_descr=row["descr_natureza"],
                city=row["municipio"],
                is_branch=row["filial"],
                amount_x=row["qtd_x"],
                cnae=row["cod_atividade"],
                cnae_descr=row["descr_atividade"],
                segment=row["seguimento"],
                amount_y=row["qtd_y"]
            )
            try:
                db.add(opening)
                db.commit()
                db.refresh(opening)
            except IntegrityError as e:
                ic(f"Duplicated hash found, ignoring it: {row}")
                db.rollback()
                continue
    return {"message": "Dados de aberturas inseridos com sucesso"}

@router.get(
    "/all",
    response_model=dict,
)
async def populate_all():
    ic("Populating all")
    #await populate_opening_companies()
    #await populate_opening_companies_activities()
    await populate_opening_companies_time_series()
    await populate_active_companies()
    await populate_active_companies_activities()
    return {"message": "Todos os dados inseridos com sucesso"}