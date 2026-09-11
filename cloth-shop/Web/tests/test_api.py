import pytest

from database import (
    create_review,
    create_user,
    get_all_ratings_of_a_product,
    get_all_reviews,
    get_certain_rating,
    session_scope,
)
from models import Product


@pytest.fixture
def db(test_app):
    return test_app.extensions['db_Session']


def add_product(db, name, cost=20.0, category='jeans', gender='male'):
    with session_scope(db) as session:
        product = Product(None, name, cost, category, gender, 'image.png')
        session.add(product)
    return product


@pytest.fixture
def product(db):
    return add_product(db, 'Blue Jeans')


@pytest.fixture
def user(db):
    return create_user(db, 'john', 'long-enough-password', 'john@example.com')


@pytest.fixture
def logged_in_client(client, user):
    with client.session_transaction() as flask_session:
        flask_session['user'] = user.to_dict()
    return client


def error_code(response):
    return response.get_json()['error']['code']


def test_products_are_listed_when_no_filter_is_given(client, db):
    add_product(db, 'Blue Jeans')
    add_product(db, 'White Shirt', category='shirt', gender='female')

    response = client.get('/api/v1/products')

    assert response.status_code == 200
    assert [p['name'] for p in response.get_json()['products']] == ['Blue Jeans', 'White Shirt']


def test_products_are_filtered_by_price_gender_and_category(client, db):
    add_product(db, 'Cheap Jeans', cost=10, category='jeans', gender='male')
    add_product(db, 'Dear Jeans', cost=90, category='jeans', gender='male')
    add_product(db, 'Cheap Shirt', cost=10, category='shirt', gender='male')
    add_product(db, 'Womens Jeans', cost=10, category='jeans', gender='female')

    response = client.get('/api/v1/products?min_price=5&max_price=50&gender=male&category=jeans')

    assert response.status_code == 200
    assert [p['name'] for p in response.get_json()['products']] == ['Cheap Jeans']


def test_products_reject_a_price_that_is_not_a_number(client):
    response = client.get('/api/v1/products?min_price=cheap')

    assert response.status_code == 400
    assert error_code(response) == 'invalid_price'


def test_adding_a_product_returns_the_basket(client, product):
    response = client.post('/api/v1/basket/items', json={'product_id': product.id})

    assert response.status_code == 201
    body = response.get_json()
    assert [item['name'] for item in body['items']] == ['Blue Jeans']
    assert body['total_cost'] == 20.0


def test_adding_an_unknown_product_is_not_found(client):
    response = client.post('/api/v1/basket/items', json={'product_id': 999})

    assert response.status_code == 404
    assert error_code(response) == 'product_not_found'


@pytest.mark.parametrize('body', [{}, {'product_id': '3'}, {'product_id': True}])
def test_adding_needs_a_whole_number_product_id(client, body):
    response = client.post('/api/v1/basket/items', json=body)

    assert response.status_code == 400
    assert error_code(response) == 'invalid_product_id'


def test_removing_a_product_returns_the_updated_basket(client, db, product):
    shirt = add_product(db, 'Red Shirt', cost=15.5, category='shirt')
    client.post('/api/v1/basket/items', json={'product_id': product.id})
    client.post('/api/v1/basket/items', json={'product_id': shirt.id})

    response = client.delete(f'/api/v1/basket/items/{product.id}')

    assert response.status_code == 200
    body = response.get_json()
    assert [item['name'] for item in body['items']] == ['Red Shirt']
    assert body['total_cost'] == 15.5


def test_removing_a_product_that_is_not_in_the_basket_is_not_found(client, product):
    response = client.delete(f'/api/v1/basket/items/{product.id}')

    assert response.status_code == 404
    assert error_code(response) == 'not_in_basket'


@pytest.mark.parametrize(('method', 'url', 'body'), [
    ('put', '/api/v1/products/1/rating', {'rating': 4}),
    ('delete', '/api/v1/products/1/rating', None),
    ('post', '/api/v1/products/1/reviews', {'content': 'Great fit'}),
    ('delete', '/api/v1/reviews/1', None),
])
def test_rating_and_reviewing_require_login(client, method, url, body):
    response = getattr(client, method)(url, json=body)

    assert response.status_code == 401
    assert error_code(response) == 'not_logged_in'


def test_setting_a_rating_saves_it(logged_in_client, db, user, product):
    response = logged_in_client.put(f'/api/v1/products/{product.id}/rating', json={'rating': 4})

    assert response.status_code == 200
    assert response.get_json() == {'rating': 4}
    assert get_certain_rating(db, product.id, user.id).rating_points == 4


def test_setting_a_rating_again_replaces_it(logged_in_client, db, user, product):
    url = f'/api/v1/products/{product.id}/rating'
    logged_in_client.put(url, json={'rating': 4})

    response = logged_in_client.put(url, json={'rating': 2})

    assert response.status_code == 200
    ratings, count = get_all_ratings_of_a_product(db, product.id)
    assert count == 1
    assert ratings[0].rating_points == 2


@pytest.mark.parametrize('rating', [0, 6, '4', True, None])
def test_a_rating_must_be_a_number_from_one_to_five(logged_in_client, product, rating):
    url = f'/api/v1/products/{product.id}/rating'

    response = logged_in_client.put(url, json={'rating': rating})

    assert response.status_code == 400
    assert error_code(response) == 'invalid_rating'


def test_rating_a_missing_product_is_not_found(logged_in_client):
    response = logged_in_client.put('/api/v1/products/999/rating', json={'rating': 4})

    assert response.status_code == 404
    assert error_code(response) == 'product_not_found'


def test_removing_a_rating(logged_in_client, db, user, product):
    url = f'/api/v1/products/{product.id}/rating'
    logged_in_client.put(url, json={'rating': 4})

    response = logged_in_client.delete(url)

    assert response.status_code == 204
    assert get_certain_rating(db, product.id, user.id) is None


def test_removing_a_rating_that_does_not_exist_is_not_found(logged_in_client, product):
    response = logged_in_client.delete(f'/api/v1/products/{product.id}/rating')

    assert response.status_code == 404
    assert error_code(response) == 'rating_not_found'


def test_posting_a_review_creates_it(logged_in_client, db, product):
    response = logged_in_client.post(
        f'/api/v1/products/{product.id}/reviews', json={'content': 'Great fit'}
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body['content'] == 'Great fit'
    assert [review.id for review in get_all_reviews(db)] == [body['id']]


def test_a_second_review_of_the_same_product_is_a_conflict(logged_in_client, product):
    url = f'/api/v1/products/{product.id}/reviews'
    logged_in_client.post(url, json={'content': 'Great fit'})

    response = logged_in_client.post(url, json={'content': 'Still great'})

    assert response.status_code == 409
    assert error_code(response) == 'review_exists'


@pytest.mark.parametrize('body', [{}, {'content': 42}])
def test_a_review_needs_text_content(logged_in_client, product, body):
    response = logged_in_client.post(f'/api/v1/products/{product.id}/reviews', json=body)

    assert response.status_code == 400
    assert error_code(response) == 'invalid_content'


def test_reviewing_a_missing_product_is_not_found(logged_in_client):
    response = logged_in_client.post('/api/v1/products/999/reviews', json={'content': 'Great fit'})

    assert response.status_code == 404
    assert error_code(response) == 'product_not_found'


def test_deleting_your_own_review(logged_in_client, db, user, product):
    review = create_review(db, product.id, user.id, 'Great fit')

    response = logged_in_client.delete(f'/api/v1/reviews/{review.id}')

    assert response.status_code == 204
    assert get_all_reviews(db) == []


def test_deleting_someone_elses_review_looks_like_it_does_not_exist(
    logged_in_client, db, product
):
    other = create_user(db, 'emma', 'long-enough-password', 'emma@example.com')
    review = create_review(db, product.id, other.id, 'Mine')

    response = logged_in_client.delete(f'/api/v1/reviews/{review.id}')

    assert response.status_code == 404
    assert error_code(response) == 'review_not_found'
    assert len(get_all_reviews(db)) == 1


def test_a_body_that_is_not_json_is_rejected(logged_in_client, product):
    response = logged_in_client.put(
        f'/api/v1/products/{product.id}/rating',
        data='rating=4',
        content_type='application/x-www-form-urlencoded',
    )

    assert response.status_code == 400
    assert error_code(response) == 'invalid_body'
