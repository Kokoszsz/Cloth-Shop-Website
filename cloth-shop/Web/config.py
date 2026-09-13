"""Per-environment application settings, selected with APP_ENV."""
import os
import secrets
from pathlib import Path

SECRET_KEY_VARIABLES = ('SECRET_KEY', 'SECRET_KEY_CLOTH_SHOP')

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE_PATH = PROJECT_ROOT / 'Databases' / 'mydb.db'
DEFAULT_DATABASE_URL = f'sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}'
IN_MEMORY_DATABASE_URL = 'sqlite://'


def secret_key_from_environment() -> str | None:
    for variable in SECRET_KEY_VARIABLES:
        key = os.environ.get(variable)
        if key:
            return key
    return None


def database_url_from_environment() -> str | None:
    return os.environ.get('DATABASE_URL') or None


class Config:
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = True

    DEBUG = False
    TESTING = False

    SQLALCHEMY_ECHO = False

    HOST = '127.0.0.1'
    PORT = 5000

    API_TITLE = 'Cloth Shop API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.3'
    OPENAPI_URL_PREFIX = '/api'
    OPENAPI_JSON_PATH = 'openapi.json'
    OPENAPI_SWAGGER_UI_PATH = '/docs'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    def __init__(self) -> None:
        self.SECRET_KEY = secret_key_from_environment() or secrets.token_hex(32)
        self.DATABASE_URL = database_url_from_environment() or DEFAULT_DATABASE_URL


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False

    def __init__(self) -> None:
        super().__init__()
        self.DATABASE_URL = IN_MEMORY_DATABASE_URL


class ProductionConfig(Config):
    HOST = '0.0.0.0'

    def __init__(self) -> None:
        key = secret_key_from_environment()
        if not key:
            raise RuntimeError(
                'No secret key configured. Set the SECRET_KEY environment '
                'variable to a long random value, for example the output of '
                '`python -c "import secrets; print(secrets.token_hex(32))"`. '
                'It signs session cookies, so it must be secret and stable '
                'across restarts.'
            )
        super().__init__()
        self.SECRET_KEY = key


CONFIGURATIONS = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

DEFAULT_ENVIRONMENT = 'development'


def get_config(environment: str | None = None) -> Config:
    name = (environment or os.environ.get('APP_ENV') or DEFAULT_ENVIRONMENT).strip().lower()
    try:
        configuration = CONFIGURATIONS[name]
    except KeyError:
        known = ', '.join(sorted(CONFIGURATIONS))
        raise RuntimeError(f'Unknown APP_ENV {name!r}. Expected one of: {known}.') from None
    return configuration()
