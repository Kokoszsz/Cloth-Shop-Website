
import pytest

from main import create_app
from database import create_database_Session


@pytest.fixture(scope='module')
def Session():
    Session = create_database_Session('sqlite://')


    yield Session

@pytest.fixture
def test_app():
  test_app = create_app('testing')
  yield test_app

@pytest.fixture
def client(test_app):
  return test_app.test_client()

