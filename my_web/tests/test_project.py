from database import get_users, get_products, mydb

def test_connection(client):
    response = client.get('/')
    assert response.status_code == 200


def test_title_home_page(client):
    response = client.get('/')
    assert b'<title>Kokosz Cloth Shop</title>' in response.data


def test_get_users():
    users = get_users()

    assert isinstance(users, list)

    assert len(users) > 0

    for user in users:
        assert isinstance(user, dict)

    expected_keys = ['id', 'name', 'password', 'email']
    for user in users:
        assert all(key in user for key in expected_keys)

def test_get_products():
    products = get_products()

    assert isinstance(products, list)

    assert len(products) > 0

    for user in products:
        assert isinstance(user, dict)

    expected_keys = ['id', 'name', 'cost_to_show', 'cost', 'cloth_cathegory', 'gender', 'image']
    for user in products:
        assert all(key in user for key in expected_keys)

def test_login(client):
    valid_username = 'test'
    valid_password = '123'
    user_info = {'name': valid_username, 'email': 'test123@gmail.com', 'id': 1, 'password': valid_password}

    response = client.post('/login', data={'login': valid_username, 'password': valid_password, 'action': 'None'})

    assert response.status_code == 302

    assert response.location == 'http://localhost/account'

    with client.session_transaction() as session:
        assert session['user'] == user_info


def test_logout(client):
    with client.session_transaction() as session:
        session['user'] = {'name': 'test', 'email': 'test123@gmail.com', 'id': 1, 'password': 123}

    response = client.get('/logout')

    assert response.status_code == 302
    assert response.location == 'http://localhost/'

    with client.session_transaction() as session:
        assert 'user' not in session

def test_create_account(client):
    valid_username = 'test123'
    valid_password = 'test123'
    user_info = {'username': valid_username, 'email': 'test123@tets123.com', 'password': valid_password}

    response = client.post('/create_account', data={'username': valid_username, 'email': 'test123@tets123.com', 'password': valid_password})

    assert response.status_code == 302

    assert response.location == 'http://localhost/account'

    with client.session_transaction() as session:
        assert user_info['username'] == session['user']['username']
        assert user_info['email'] == session['user']['email']
        assert user_info['password'] == session['user']['password']

def test_delete_user(client):
    pass
