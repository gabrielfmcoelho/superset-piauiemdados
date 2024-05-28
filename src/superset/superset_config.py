WTF_CSRF_ENABLED = False

APP_NAME = "SUPERSET Piauí em Dados"

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
    "EMBEDDED_SUPERSET": True,
    "EMBEDDED_CHART": True
}

ENABLE_CORS = True
TALISMAN_ENABLED = False
CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "expose_headers": ["*"],
    "resources": ["*"],
    "origins": ["*", "http://localhost:3000", "http://10.0.100.121:3000", "http://10.0.80.7:3000", "http://169.254.2.1:3000", "https://dados.pi.gov.br/", "https://dados.pi.gov.br"],
}

GUEST_ROLE_NAME = "Gamma"
GUEST_TOKEN_JWT_SECRET = "test-guest-secret-change-me"
GUEST_TOKEN_JWT_ALGO = "HS256"
GUEST_TOKEN_HEADER_NAME = "X-GuestToken"
GUEST_TOKEN_JWT_EXP_SECONDS = 600

#ENABLE_PROXY_FIX = True
SECRET_KEY = "ULTRA_SECRET_KEY"