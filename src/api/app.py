from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connector import Connector
from app_config import AppConfig


try:
    db_connector = Connector.get_instance()
except Exception as e:
    print(e)

app = FastAPI(**AppConfig.DOCS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=AppConfig.CorsConfig.ALLOW_ORIGINS.value,
    allow_credentials=AppConfig.CorsConfig.ALLOW_CREDENTIALS.value,
    allow_methods=AppConfig.CorsConfig.ALLOW_METHODS.value,
    allow_headers=AppConfig.CorsConfig.ALLOW_HEADERS.value,
    )


from routes.populatedb import router as populatedb_router
from routes.report import router as report_router
from routes.dashboard import router as dashboard_router


try:
    db_connector.create_all()
except Exception as e:
    print(e)


@app.get("/")
async def root():
    return {"message": "Bem-vindo a API de gerenciamento de dados do Piauí em Dados"}

@app.post("/api/ping")
async def root_post():
    return {"data":"pong"}


app.include_router(populatedb_router)
app.include_router(report_router)
app.include_router(dashboard_router)
