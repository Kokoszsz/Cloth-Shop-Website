
import pytest, os
from main import app
from database import create_database_Session
from tests.test_utils import insert_data


@pytest.fixture(scope='module')
def Session(request):
    Session = create_database_Session('sqlite:///Cloth Shop Website/Databases/test.db')
    insert_data(Session)
    def fin():
        os.remove('Cloth Shop Website/Databases/test.db')

    request.addfinalizer(fin)
    yield Session

@pytest.fixture
def test_app():
  test_app = app
  yield test_app

@pytest.fixture
def client(test_app):
  return test_app.test_client()
  