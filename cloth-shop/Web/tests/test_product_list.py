import pytest

from database import create_rating, create_user, session_scope
from models import Product


@pytest.fixture
def app_database(test_app):
    return test_app.extensions['db_Session']


def add_product(Session, name):
    with session_scope(Session) as session:
        product = Product(None, name, 49.99, 'jackets', 'female', 'coat.png')
        session.add(product)
    return product


def test_product_page_shows_the_average_of_every_rating(app_database, client):
    product = add_product(app_database, 'Late Arrival Hat')
    john = create_user(app_database, 'john', 'long-enough-password', 'john@example.com')
    mary = create_user(app_database, 'mary', 'long-enough-password', 'mary@example.com')
    create_rating(app_database, product.id, john.id, 5)
    create_rating(app_database, product.id, mary.id, 4)

    response = client.get(f'/cloth/product_detail/{product.url}')

    assert b'Total Rating 4.5</div>' in response.data


def test_product_page_shows_zero_when_nobody_has_rated(app_database, client):
    product = add_product(app_database, 'Late Arrival Belt')

    response = client.get(f'/cloth/product_detail/{product.url}')

    assert b'Total Rating 0</div>' in response.data


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
