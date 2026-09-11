import pytest

from database import session_scope
from models import Product


@pytest.fixture
def app_database(test_app):
    return test_app.extensions['db_Session']


def add_product(Session, name):
    with session_scope(Session) as session:
        product = Product(None, name, 49.99, 'jackets', 'female', 'coat.png')
        session.add(product)
    return product


def test_cloth_page_lists_a_product_added_after_startup(app_database, client):
    add_product(app_database, 'Late Arrival Coat')

    response = client.get('/cloth')

    assert b'Late Arrival Coat' in response.data


def test_basket_shows_a_product_added_after_startup(app_database, client):
    product = add_product(app_database, 'Late Arrival Scarf')
    with client.session_transaction() as flask_session:
        flask_session['basket'] = [product.id]

    response = client.get('/basket')

    assert b'Late Arrival Scarf' in response.data
