import pytest

import config


@pytest.fixture
def clean_environment(monkeypatch):
    for variable in ('APP_ENV', 'SECRET_KEY', 'SECRET_KEY_CLOTH_SHOP'):
        monkeypatch.delenv(variable, raising=False)


def test_production_refuses_to_start_without_a_secret_key(clean_environment):
    with pytest.raises(RuntimeError, match='secret key'):
        config.ProductionConfig()


def test_production_uses_the_key_from_the_environment(clean_environment, monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'a-real-secret')
    assert config.ProductionConfig().SECRET_KEY == 'a-real-secret'


def test_production_accepts_the_legacy_variable_name(clean_environment, monkeypatch):
    monkeypatch.setenv('SECRET_KEY_CLOTH_SHOP', 'a-real-secret')
    assert config.ProductionConfig().SECRET_KEY == 'a-real-secret'


def test_development_key_is_random_rather_than_a_shared_constant(clean_environment):
    first, second = config.DevelopmentConfig().SECRET_KEY, config.DevelopmentConfig().SECRET_KEY
    assert first != second
    assert len(first) >= 32


def test_debugger_is_only_available_in_development(clean_environment, monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'a-real-secret')
    assert config.DevelopmentConfig().DEBUG is True
    assert config.TestingConfig().DEBUG is False
    assert config.ProductionConfig().DEBUG is False


def test_production_sets_every_session_cookie_flag(clean_environment, monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'a-real-secret')
    production = config.ProductionConfig()
    assert production.SESSION_COOKIE_HTTPONLY is True
    assert production.SESSION_COOKIE_SECURE is True
    assert production.SESSION_COOKIE_SAMESITE == 'Lax'


def test_cookie_is_not_marked_secure_outside_production(clean_environment):
    assert config.DevelopmentConfig().SESSION_COOKIE_SECURE is False
    assert config.TestingConfig().SESSION_COOKIE_SECURE is False


def test_get_config_selects_the_environment_named_by_app_env(clean_environment, monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'a-real-secret')
    monkeypatch.setenv('APP_ENV', 'production')
    assert isinstance(config.get_config(), config.ProductionConfig)


def test_get_config_defaults_to_development(clean_environment):
    assert isinstance(config.get_config(), config.DevelopmentConfig)


def test_get_config_rejects_an_unknown_environment(clean_environment):
    with pytest.raises(RuntimeError, match='Unknown APP_ENV'):
        config.get_config('staging')


def test_running_app_applies_the_cookie_flags(test_app):
    assert test_app.config['SESSION_COOKIE_HTTPONLY'] is True
    assert test_app.config['SESSION_COOKIE_SAMESITE'] == 'Lax'
    assert test_app.config['DEBUG'] is False
    assert test_app.config['TESTING'] is True


def test_sql_echo_is_off_in_every_environment(clean_environment, monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'a-real-secret')
    assert config.DevelopmentConfig().SQLALCHEMY_ECHO is False
    assert config.TestingConfig().SQLALCHEMY_ECHO is False
    assert config.ProductionConfig().SQLALCHEMY_ECHO is False


def test_running_app_does_not_echo_sql(test_app):
    assert test_app.config['SQLALCHEMY_ECHO'] is False
    assert test_app.extensions['db_Session'].kw['bind'].echo is False


def test_session_cookie_is_sent_with_its_flags(client):
    response = client.get('/')
    cookie = response.headers['Set-Cookie']
    assert 'HttpOnly' in cookie
    assert 'SameSite=Lax' in cookie
    assert 'Secure' not in cookie
