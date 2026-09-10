from database import (
    create_rating,
    create_review,
    create_user,
    get_all_reviews,
    get_certain_rating,
    get_products_to_dict,
    get_ratings,
    get_reviews_of_a_product,
    get_users,
    remove_rating,
    remove_review,
    update_user,
)
from models import User, Product, Rating, Review
import pytest
from unittest.mock import patch
from exceptions import DuplicateReview, ProductNotFound, UserNotFound
from utils import (
    ValidationError,
    authenticate,
    filter_products,
    get_genders_and_kinds,
    get_product_by_url,
    validate_account,
)

def test_connection_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_connection_cloth(client):
    response = client.get('/cloth')
    assert response.status_code == 200


def test_connection_basket( client):
    
    response = client.get('/basket')
    assert response.status_code == 200

def test_connection_login(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_connection_create_account(client):
    response = client.get('/create_account')
    assert response.status_code == 200

def test_title_home_page(client):
    response = client.get('/')
    assert b'<title>Kokosz Cloth Shop</title>' in response.data

def test_navigation_bar(client):
    response = client.get('/')
    assert b'<div class="menu">' in response.data


### Test functions from database.py


def test_create_user(Session):

    # Define test data
    user_id = 1
    user_name = "John"
    user_password = "password"
    user_email = "john@example.com"

    # Create user
    user = create_user(Session, user_name, user_password, user_email)

    # Check if user was created correctly
    assert user.id == user_id
    assert user.name == user_name
    assert user.check_password(user_password)
    assert user.password_hash != user_password  # stored value must not be the plaintext
    assert user.email == user_email

    # Check if newly created user is in database
    session = Session()
    db_user = session.query(User).filter_by(id=user_id).first()
    assert db_user != None
    assert db_user.name == user_name
    assert db_user.check_password(user_password)
    assert db_user.password_hash != user_password
    assert db_user.email == user_email
    session.close()

def test_get_users(Session):
    users = get_users(Session)
    # Make sure there is only one user creted in previous test
    assert len(users) == 1

    # Make sure data of this user is correct
    assert users[0].id == 1
    assert users[0].name == "John"
    assert users[0].check_password("password")
    assert users[0].email == "john@example.com"

    

def test_update_user(Session):
    # Create test users
    users = [
        User(id=1, name="John", password="password", email="john@example.com")
    ]

    # Update user 1
    user = update_user(Session, 1, "New Name", "newpassword", "newemail@example.com", users)

    # Check if user was properly updated
    assert user.name == "New Name"
    assert user.check_password("newpassword")
    assert user.email == "newemail@example.com"

    # Retrieve user 1 from database and check attributes
    session = Session()
    db_user1 = session.query(User).filter_by(id=1).first()
    session.close()
    assert db_user1.name == "New Name"
    assert db_user1.check_password("newpassword")
    assert db_user1.email == "newemail@example.com"

    # Update user 3 (doesn't exist)
    with pytest.raises(UserNotFound):
        update_user(Session, 3, "New User", "newpassword", "newemail@example.com", users)

    # Check that user list is still the same
    assert len(users) == 1

def test_get_products_to_dict(Session):
    # Check if there are no products
    product = get_products_to_dict(Session)
    assert product == []

    # Add a product  
    session = Session()
    product = Product(1, 'product test', 20, 'jeans', 'male', 'image')
    session.merge(product)
    session.commit()
    session.close()

    # Make sure there is only one product
    products = get_products_to_dict(Session)
    assert len(products) == 1

    # Make sure data of added product is correct
    assert products[0]['id'] == 1
    assert products[0]['name'] == 'product test'
    assert products[0]['cost'] == 20
    assert products[0]['cloth_cathegory'] == 'jeans'
    assert products[0]['gender'] == 'male'
    assert products[0]['image'] == 'image'
    assert products[0]['url'] == 'product-test'

def test_get_ratings(Session):
    # Check if there are no ratings
    ratings = get_ratings(Session)
    assert ratings == []

    # Add a rating  
    session = Session()
    rating = Rating(3, 4, 2.1, id=1)
    session.merge(rating)
    session.commit()
    session.close()

    # Make sure there is only one product
    ratings = get_ratings(Session)
    assert len(ratings) == 1

    # Make sure data of added product is correct
    assert ratings[0].id == 1
    assert ratings[0].product_id == 3
    assert ratings[0].user_id == 4
    assert ratings[0].rating_points == 2.1

def test_create_rating(Session):
    rating1 = (1, 3, 1, 3.5) 
    with pytest.raises(ProductNotFound):
        create_rating(Session, rating1[1], rating1[2], rating1[3])


    # Add a product  
    session = Session()
    product = Product(1, 'product_test', 20, 'jeans', 'male', 'image')
    session.merge(product)
    session.commit()

    # Add a user
    user = User('test123', '123', 'test@mail', id=1)
    session.merge(user)
    session.commit()
    session.close()

    rating1 = (1, 1, 1, 2.5) 
    rating_result = create_rating(Session, rating1[1], rating1[2], rating1[3])
    obj_rating_correct = Rating(*rating1[1:], id=rating1[0])
    assert rating_result.id is not None
    assert rating_result.product_id == obj_rating_correct.product_id
    assert rating_result.user_id == obj_rating_correct.user_id
    assert rating_result.rating_points == obj_rating_correct.rating_points

def test_get_certain_rating(Session):

    # Add a rating  
    session = Session()
    rating = Rating(2, 1, 2.0, id=1)
    session.merge(rating)
    session.commit()
    session.close()

    rating_obj = get_certain_rating(Session, 2, 1)
    assert rating_obj.id == rating.id
    assert rating_obj.product_id == rating.product_id
    assert rating_obj.user_id == rating.user_id
    assert rating_obj.rating_points == rating.rating_points

def test_remove_rating(Session):
    # Add a product  
    session = Session()
    product = Product(1, 'product_test', 20, 'jeans', 'male', 'image')
    session.merge(product)
    session.commit()

    # Add a user
    user = User('test123', '123', 'test@mail', id=1)
    session.merge(user)
    session.commit()
    session.close()

    # Add a rating  
    create_rating(Session, 1, 1, 3)

    assert remove_rating(Session, 1, 1) is True
    assert get_certain_rating(Session, 1, 1) is None

def test_create_review(Session):


    # Add a product  
    session = Session()
    product = Product(1, 'product_test', 20, 'jeans', 'male', 'image')
    session.merge(product)
    session.commit()

    # Add a user
    user = User('test123', '123', 'test@mail', id=1)
    session.merge(user)
    session.commit()
    session.close()

    review = (1, 1, 1, 'great product') 
    review_object = create_review(Session, review[1], review[2], review[3])


    obj_review_correct = Review(*review[1:], id=review[0])
    assert review_object.id is not None
    assert review_object.product_id == obj_review_correct.product_id
    assert review_object.user_id == obj_review_correct.user_id
    assert review_object.content == obj_review_correct.content

def test_get_reviews_of_a_product(Session):
    # Add a product
    session = Session()
    product = Product(1, 'product_test', 20, 'jeans', 'male', 'image')
    session.merge(product)
    session.commit()
    session.close()

    # Add reviews
    reviews = [
        (1, 1, 1, 'great product'),
        (2, 1, 2, 'nice quality'),
        (3, 1, 3, 'not satisfied')
    ]

    session = Session()
    for review in reviews:
        session.merge(Review(*review[1:], id=review[0]))
    session.commit()

    product_reviews = get_reviews_of_a_product(Session, 1)
    assert len(product_reviews) == len(reviews)
    for x, review in enumerate(product_reviews):
        assert review.id == reviews[x][0]
        assert review.product_id == reviews[x][1]
        assert review.user_id == reviews[x][2]
        assert review.content == reviews[x][3]

    session.close()

def test_get_all_reviews(Session):
    # Add reviews
    reviews = [
        (1, 1, 1, 'great product'),
        (2, 2, 2, 'nice quality'),
        (3, 3, 3, 'not satisfied')
    ]

    session = Session()
    for review in reviews:
        session.merge(Review(*review[1:], id=review[0]))
    session.commit()

    all_reviews = get_all_reviews(Session)
    assert len(all_reviews) == len(reviews)

    session.close()

def test_remove_review(Session):
    # Add a review
    session = Session()
    review = Review(1, 1, 'good review', id=1)
    session.merge(review)
    session.commit()
    session.close()

    # Remove the review
    review_id = 1
    user_id = 1
    result = remove_review(Session, review_id, user_id)
    assert result is True

    # Check if the review is removed
    session = Session()
    removed_review = session.query(Review).filter_by(id=review_id).first()
    session.close()
    assert removed_review is None




### Test functions from utils.py

def test_filter_products():
    # Define test data
    products = [
        {'id': 1, 'name': 'cloth1', 'cost_to_show': '10', 'cost': 10, 'cloth_cathegory': 'Shirt', 'gender': 'Male', 'image': 'test'},
        {'id': 2, 'name': 'cloth2', 'cost_to_show': '20', 'cost': 20, 'cloth_cathegory': 'Pants', 'gender': 'Female', 'image': 'test'},
        {'id': 3, 'name': 'cloth3', 'cost_to_show': '30', 'cost': 30, 'cloth_cathegory': 'Shoes', 'gender': 'Male', 'image': 'test'},
    ]
    min_value = 15
    max_value = 25
    genders = ['Female']
    kinds = ['Pants']

    # Call the function being tested
    filtered_products = filter_products(products, min_value, max_value, genders, kinds)

    # Assert the expected output
    expected_output = [{'id': 2, 'name': 'cloth2', 'cost_to_show': '20', 'cost': 20, 'cloth_cathegory': 'Pants', 'gender': 'Female', 'image': 'test'}]
    assert filtered_products == expected_output

    # Define test data
    genders = ['Male']
    kinds = ['Shoes']
    min_value = 0
    max_value = 11

    # Call the function being tested
    filtered_products = filter_products(products, min_value, max_value, genders, kinds)

    # Assert the expected output
    expected_output = []
    assert filtered_products == expected_output

    # Define test data
    genders = ['Female']
    kinds = ['Pants']
    min_value = 12
    max_value = 5

    # Call the function being tested
    filtered_products = filter_products(products, min_value, max_value, genders, kinds)

    # Assert the expected output
    expected_output = []
    assert filtered_products == expected_output

def test_authenticate():
    # Create test users
    users = [
        User(id=1, name="john", password="test1", email="john@example.com"),
        User(id=2, name="emma", password="test2", email="emma@example.com"),
        User(id=3, name="jacob", password="test3", email="jacob@example.com")
    ]

    # Test case: Correct username and password
    user, error = authenticate('john', 'test1', users)
    assert error is None
    assert user.id == 1
    assert user.name == "john"
    assert user.check_password("test1")
    assert user.email == "john@example.com"

    # Test case: Correct username, wrong password
    user, error = authenticate('emma', 'wrong_password', users)
    assert error == ValidationError('password', 'Wrong Password')
    assert user is None

    # Test case: Wrong username
    user, error = authenticate('unknown_user', 'test3', users)
    assert error == ValidationError('username', 'Wrong Username')
    assert user is None

def test_validate_account():
    # Create test users
    users = [
        User(id=1, name="john", password="password1", email="john@example.com"),
        User(id=2, name="jane", password="password2", email="jane@example.com"),
    ]

    # Test case 1: Valid inputs, no errors expected
    result = validate_account(users, 3, 'Alice', 'alice@example.com', 'password3')
    assert result == []

    # Test case 2: Empty username, expect 'No Username' error
    result = validate_account(users, 3, '', 'alice@example.com', 'password3')
    assert result == [ValidationError('username', 'No Username provided')]

    # Test case 3: Existing username, expect 'Already such a User' error
    result = validate_account(users, 3, 'john', 'alice@example.com', 'password3')
    assert result == [ValidationError('username', 'Already such an User')]

    # Test case 4: Empty email, expect 'No E-mail' error
    result = validate_account(users, 3, 'Alice', '', 'password3')
    assert result == [ValidationError('email', 'No E-mail provided')]

    # Test case 5: Existing email, expect 'Already such an E-mail' error
    result = validate_account(users, 3, 'Alice', 'john@example.com', 'password3')
    assert result == [ValidationError('email', 'Already such an E-mail')]

    # Test case 6: Empty password, expect 'No password' error
    result = validate_account(users, 3, 'Alice', 'alice@example.com', '123')
    assert result == [ValidationError('password', 'Password must consist of at least 8 characters')]

    # Test case 7: Space in username, expect 'Username can not have spaces' error
    result = validate_account(users, 3, 'Ali ce', 'alice@example.com', 'password3')
    assert result == [ValidationError('username', 'Username can not have spaces')]

    # Test case 8: Space in password, expect 'Password can not have spaces' error
    result = validate_account(users, 3, 'Alice', 'alice@example.com', 'pass word3')
    assert result == [ValidationError('password', 'Password can not have spaces')]


def test_get_product_by_url():
    # Define test data
    products = [
        {'id': 1, 'name': 'cloth1', 'cost_to_show': '10', 'cost': 10, 'cloth_cathegory': 'Shirt', 'gender': 'Male', 'image': 'test', 'url': 'cloth1'},
        {'id': 2, 'name': 'cloth2', 'cost_to_show': '20', 'cost': 20, 'cloth_cathegory': 'Pants', 'gender': 'Female', 'image': 'test', 'url': 'cloth2'},
        {'id': 3, 'name': 'cloth3', 'cost_to_show': '30', 'cost': 30, 'cloth_cathegory': 'Shoes', 'gender': 'Male', 'image': 'test', 'url': 'cloth3'},
    ]

    # Test case 1: Valid product ID, expect product to be returned
    result = get_product_by_url(products, 'cloth2')
    assert result == {'id': 2, 'name': 'cloth2', 'cost_to_show': '20', 'cost': 20, 'cloth_cathegory': 'Pants', 'gender': 'Female', 'image': 'test', 'url': 'cloth2'}

    # Test case 2: Invalid product ID, expect None to be returned
    result = get_product_by_url(products, 'cloth4')
    assert result is None

def test_get_genders_and_kinds():
    # Define test data
    request1 = ['male', 't-shirt', 'shirt']
    request2 = ['female', 'jeans']
    request3 = ['male', 'female', 't-shirt', 'jeans', 'shirt']
    request4 = []
    request5 = ['jeans', 'shirt']
    request6 = ['male', 'female']
    
    # Test first request
    genders1, kinds1 = get_genders_and_kinds(request1)
    assert genders1 == ['male']
    assert kinds1 == ['t-shirt', 'shirt']

    # Test second request
    genders2, kinds2 = get_genders_and_kinds(request2)
    assert genders2 == ['female']
    assert kinds2 == ['jeans']

    # Test third request
    genders3, kinds3 = get_genders_and_kinds(request3)
    assert genders3 == ['male', 'female']
    assert kinds3 == ['t-shirt', 'jeans', 'shirt']

    # Test fourth request
    genders4, kinds4 = get_genders_and_kinds(request4)
    assert genders4 == []
    assert kinds4 == []

    # Test fifth request
    genders5, kinds5 = get_genders_and_kinds(request5)
    assert genders5 == []
    assert kinds5 == ['jeans', 'shirt']

    # Test sixth request
    genders6, kinds6 = get_genders_and_kinds(request6)
    assert genders6 == ['male', 'female']
    assert kinds6 == []

# Define users 
@patch('blueprints.auth.create_user')
@patch('blueprints.auth.get_users')
def test_create_account_success(mock_get_users, mock_create_user, client):

    # Keep the real database out of it - the route now writes on success
    mock_get_users.return_value = [
        User(id=1, name="john", password="test1", email="john@example.com"),
    ]
    mock_create_user.return_value = User(
        id=2,
        name='test_create_account',
        password='test_create_account',
        email='test_create_account@example.com',
    )

    # Send data
    response = client.post('/create_account', data={
        'username': 'test_create_account',
        'email': 'test_create_account@example.com',
        'password': 'test_create_account'
    })

    # The account is created straight away and the user is logged in
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/account')
    mock_create_user.assert_called_once()


@patch('blueprints.auth.create_user')
@patch('blueprints.auth.get_users')
def test_create_account_keeps_credentials_out_of_the_session(mock_get_users, mock_create_user, client):

    mock_get_users.return_value = [
        User(id=1, name="john", password="test1", email="john@example.com"),
    ]
    mock_create_user.return_value = User(
        id=2,
        name='cookie_check',
        password='sup3rsecretpassword',
        email='cookie_check@example.com',
    )

    client.post('/create_account', data={
        'username': 'cookie_check',
        'email': 'cookie_check@example.com',
        'password': 'sup3rsecretpassword'
    })

    # The session cookie is signed, not encrypted - nothing secret may go in it
    with client.session_transaction() as flask_session:
        assert 'new_user' not in flask_session
        assert 'sup3rsecretpassword' not in str(dict(flask_session))
        assert 'password' not in flask_session['user']

# Mock the get_users function to return some existing users
@patch('blueprints.auth.get_users')
def test_create_account_errorr(mock_get_users, client):
    # Mock the get_users function to return some existing users
    mock_get_users.return_value = [
        User(id=1, name="john", password="test1", email="john@example.com"),
        User(id=2, name="emma", password="test2", email="emma@example.com"),
    ]

    response = client.post('/create_account', data={
        'username': 'john',  # This username already exists
        'email': 'test_create_account@example.com',
        'password': 'test_create_account'
    })

    assert response.status_code == 200


LOGGED_IN_USER = {
    'id': 1,
    'name': 'john',
    'email': 'john@example.com',
    'surname': '',
    'phone': '',
    'country': '',
    'city': '',
}


@patch('blueprints.reviews.create_review')
def test_save_review_reports_a_duplicate_as_a_conflict(mock_create_review, client):
    mock_create_review.side_effect = DuplicateReview(1, 1)

    with client.session_transaction() as flask_session:
        flask_session['user'] = LOGGED_IN_USER

    response = client.post('/save_review', json={'content': 'again', 'productId': 1})

    assert response.status_code == 409
    assert 'already reviewed' in response.get_json()['message']


@patch('blueprints.reviews.create_rating')
def test_save_rating_reports_a_missing_product_as_not_found(mock_create_rating, client):
    mock_create_rating.side_effect = ProductNotFound(99)

    with client.session_transaction() as flask_session:
        flask_session['user'] = LOGGED_IN_USER

    response = client.post('/save_rating', json={'rating': 4, 'productId': 99})

    assert response.status_code == 404


@patch('blueprints.auth.get_users')
def test_account_page_reports_every_invalid_field_at_once(mock_get_users, client):
    mock_get_users.return_value = []

    with client.session_transaction() as flask_session:
        flask_session['user'] = LOGGED_IN_USER

    response = client.post('/account', data={
        'username': 'a b',
        'email': '',
        'password': '123',
        'surname': '',
        'phone': '',
        'country': '',
        'city': '',
    })
    body = response.get_data(as_text=True)

    assert 'Username can not have spaces' in body
    assert 'No E-mail provided' in body
    assert 'at least 8 characters' in body


@patch('blueprints.auth.get_users')
def test_create_account_shows_the_password_error(mock_get_users, client):
    mock_get_users.return_value = []

    response = client.post('/create_account', data={
        'username': 'alice',
        'email': 'alice@example.com',
        'password': '123',
    })

    assert response.status_code == 200
    assert 'at least 8 characters' in response.get_data(as_text=True)
