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


from router import router as main_router


try:
    db_connector.create_all()
except Exception as e:
    print(e)

app.include_router(main_router)