"""Per-environment application settings, selected with APP_ENV."""
import os
import secrets

SECRET_KEY_VARIABLES = ('SECRET_KEY', 'SECRET_KEY_CLOTH_SHOP')


def secret_key_from_environment() -> str | None:
    for variable in SECRET_KEY_VARIABLES:
        key = os.environ.get(variable)
        if key:
            return key
    return None


class Config:
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = True

    DEBUG = False
    TESTING = False

    DATABASE_URL = 'sqlite:///cloth-shop/Databases/mydb.db'
    SQLALCHEMY_ECHO = False

    HOST = '127.0.0.1'
    PORT = 5000

    def __init__(self) -> None:
        self.SECRET_KEY = secret_key_from_environment() or secrets.token_hex(32)


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False
    DATABASE_URL = 'sqlite://'


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
