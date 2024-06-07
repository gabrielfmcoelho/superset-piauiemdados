from enum import Enum


class AppConfig:

    class CorsConfig(Enum):
        ALLOW_ORIGINS = ["*"]
        ALLOW_CREDENTIALS = False
        ALLOW_METHODS = ["*"]
        ALLOW_HEADERS = ["*"]

    DOCS = {
        "title": "Piauí em Dados BD API",
        "description": "API para acesso e gerenciamento de dados da plataforma Piauí em Dados",
        "version": "1.2",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
        "servers": [
            {
                "url": "localhost:8050",
                "description": "Local DEV server"
            },
            {
                "url": "10.0.100.121",
                "description": "VM ETIPI DEV server"
            }
        ],
        "contact": {
            "name": "Investe Piauí | Coordenação de Governança de Dados",
            "url": "https://investepiaui.com",
        },
        "license_info": {
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        }
    }

    