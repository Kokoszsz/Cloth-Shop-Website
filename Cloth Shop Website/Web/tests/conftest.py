import pytest
from main import app
from database import create_database_Session


@pytest.fixture(scope='module')
def Session():
    Session = create_database_Session('sqlite://')


    yield Session

@pytest.fixture
def test_app():
  test_app = app
  yield test_app

@pytest.fixture
def client(test_app):
  return test_app.test_client()
  