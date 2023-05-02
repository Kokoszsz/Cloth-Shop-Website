
import pytest
from main import app



@pytest.fixture
def test_app():
  test_app = app
  yield test_app

@pytest.fixture
def client(test_app):
  return test_app.test_client()
  