FASTAPI_CONFIG = {
    "title": "Piauí em Dados BD API",
    "description": "API para acesso e gerenciamento de dados do Piauí em Dados",
    "version": "1.0",
    "docs_url": "/docs",
    "openapi_url": "/openapi.json",
    "servers": [
        {
            "url": "localhost:8000",
            "description": "Local DEV server"
        },
    ],
    "contact": {
        "name": "ETIPI",
    },
    "license_info": {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
}

CORS_CONFIG = {
    "allow_origins": ["*"],
    "allow_credentials": False,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}