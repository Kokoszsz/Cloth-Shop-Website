from database import update_user, create_user, get_users, get_products_to_dict
from models import User, Product
from unittest.mock import patch
from utils import filter_products, check_login, check_if_error, get_product_by_id

def test_connection_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_connection_cloth(client):
    response = client.get('/cloth')
    assert response.status_code == 200

@patch('main.products')
def test_connection_basket(mock_products, client):
    products = [
        {'id': 1, 'name': 'Product 1', 'cost_to_show': 24.99, 'cost': '24.99', 'cloth_cathegory': 'jeans', 'gender': 'man', 'image': ''},
        {'id': 2, 'name': 'Product 2', 'cost_to_show': 25.99, 'cost': '25.99', 'cloth_cathegory': 'jeans', 'gender': 'woman', 'image': ''},
        {'id': 3, 'name': 'Product 3', 'cost_to_show': 26.99, 'cost': '26.99', 'cloth_cathegory': 'jeans', 'gender': 'woman', 'image': ''},
        {'id': 4, 'name': 'Product 4', 'cost_to_show': 27.99, 'cost': '27.99', 'cloth_cathegory': 'jeans', 'gender': 'man', 'image': ''}
    ]

    mock_products.return_value = products
    
    with client.session_transaction() as session:
        session['basket'] = [1, 2, 3]  

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
    user = create_user(Session, user_id, user_name, user_password, user_email)

    # Check if user was created correctly
    assert user.id == user_id
    assert user.name == user_name
    assert user.password == user_password
    assert user.email == user_email

    # Check if newly created user is in database
    session = Session()
    db_user = session.query(User).filter_by(id=user_id).first()
    assert db_user != None
    assert db_user.name == user_name
    assert db_user.password == user_password
    assert db_user.email == user_email
    session.close()

def test_get_users(Session):
    users = get_users(Session)
    # Make sure there is only one user creted in previous test
    assert len(users) == 1

    # Make sure data of this user is correct
    assert users[0].id == 1
    assert users[0].name == "John"
    assert users[0].password == "password"
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
    assert user.password == "newpassword"
    assert user.email == "newemail@example.com"

    # Retrieve user 1 from database and check attributes
    session = Session()
    db_user1 = session.query(User).filter_by(id=1).first()
    session.close()
    assert db_user1.name == "New Name"
    assert db_user1.password == "newpassword"
    assert db_user1.email == "newemail@example.com"

    # Update user 3 (doesn't exist)
    update_user(Session, 3, "New User", "newpassword", "newemail@example.com", users)

    # Check that user list is still the same
    assert len(users) == 1

def test_get_products_to_dict(Session):
    # Check if there are no products
    product = get_products_to_dict(Session)
    assert product == []

    # Add a product  
    session = Session()
    product = Product(1, 'product_test', 20, 'jeans', 'male', 'image')
    session.merge(product)
    session.commit()
    session.close()

    # Make sure there is only one product
    products = get_products_to_dict(Session)
    assert len(products) == 1

    # Make sure data of added product is correct
    assert products[0]['id'] == 1
    assert products[0]['name'] == 'product_test'
    assert products[0]['cost'] == 20
    assert products[0]['cloth_cathegory'] == 'jeans'
    assert products[0]['gender'] == 'male'
    assert products[0]['image'] == 'image'


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

def test_check_login():
    # Create test users
    users = [
        User(id=1, name="john", password="test1", email="john@example.com"),
        User(id=2, name="emma", password="test2", email="emma@example.com"),
        User(id=3, name="jacob", password="test3", email="jacob@example.com")
    ]

    # Test case: Correct username and password
    result, user = check_login('john', 'test1', users)
    assert result == 'good'
    assert user.id == 1
    assert user.name == "john"
    assert user.password == "test1"
    assert user.email == "john@example.com"

    # Test case: Correct username, wrong password
    result, user = check_login('emma', 'wrong_password', users)
    assert result == 'Wrong Password'
    assert user is None

    # Test case: Wrong username
    result, user = check_login('unknown_user', 'test3', users)
    assert result == 'Wrong Username'
    assert user is None

def test_check_if_error():
    # Create test users
    users = [
        User(id=1, name="john", password="password1", email="john@example.com"),
        User(id=2, name="jane", password="password2", email="jane@example.com"),
    ]

    # Test case 1: Valid inputs, no errors expected
    result = check_if_error(users, 'Alice', 'alice@example.com', 'password3')
    assert result == ''

    # Test case 2: Empty username, expect 'No Username' error
    result = check_if_error(users, '', 'alice@example.com', 'password3')
    assert result == 'No Username'

    # Test case 3: Existing username, expect 'Already such a User' error
    result = check_if_error(users, 'john', 'alice@example.com', 'password3')
    assert result == 'Already such a User'

    # Test case 4: Empty email, expect 'No E-mail' error
    result = check_if_error(users, 'Alice', '', 'password3')
    assert result == 'No E-mail'

    # Test case 5: Existing email, expect 'Already such an E-mail' error
    result = check_if_error(users, 'Alice', 'john@example.com', 'password3')
    assert result == 'Already such an E-mail'

    # Test case 6: Empty password, expect 'No password' error
    result = check_if_error(users, 'Alice', 'alice@example.com', '')
    assert result == 'No password'


def test_get_product_by_id():
    # Define test data
    products = [
        {'id': 1, 'name': 'cloth1', 'cost_to_show': '10', 'cost': 10, 'cloth_cathegory': 'Shirt', 'gender': 'Male', 'image': 'test'},
        {'id': 2, 'name': 'cloth2', 'cost_to_show': '20', 'cost': 20, 'cloth_cathegory': 'Pants', 'gender': 'Female', 'image': 'test'},
        {'id': 3, 'name': 'cloth3', 'cost_to_show': '30', 'cost': 30, 'cloth_cathegory': 'Shoes', 'gender': 'Male', 'image': 'test'},
    ]

    # Test case 1: Valid product ID, expect product to be returned
    result = get_product_by_id(products, 2)
    assert result == {'id': 2, 'name': 'cloth2', 'cost_to_show': '20', 'cost': 20, 'cloth_cathegory': 'Pants', 'gender': 'Female', 'image': 'test'}

    # Test case 2: Invalid product ID, expect None to be returned
    result = get_product_by_id(products, 4)
    assert result is None















