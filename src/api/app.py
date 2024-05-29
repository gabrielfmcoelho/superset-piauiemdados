from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connector import Connector
from docs import FASTAPI_CONFIG, CORS_CONFIG


try:
    db_connector = Connector.get_instance()
except Exception as e:
    print(e)

app = FastAPI(**FASTAPI_CONFIG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_CONFIG["allow_origins"],
    allow_credentials=CORS_CONFIG["allow_credentials"],
    allow_methods=CORS_CONFIG["allow_methods"],
    allow_headers=CORS_CONFIG["allow_headers"],
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
