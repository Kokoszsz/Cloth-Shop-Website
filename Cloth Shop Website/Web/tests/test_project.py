from database import update_user, create_user
from models import User


def test_connection(client):
    response = client.get('/')
    assert response.status_code == 200


def test_title_home_page(client):
    response = client.get('/')
    assert b'<title>Kokosz Cloth Shop</title>' in response.data

def test_navigation_bar(client):
    response = client.get('/')
    assert b'<div class="menu">' in response.data

def test_update_user(Session):
    # Create test users
    user1 = User(id=1, name="John", password="password", email="john@example.com")
    user2 = User(id=2, name="Jane", password="password", email="jane@example.com")
    users = [user1, user2]

    # Update user 1
    update_user(Session, 1, "New Name", "newpassword", "newemail@example.com", users)

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
    assert len(users) == 2



def test_create_user(Session):
    user_id = 4
    user_name = "Test User"
    user_password = "password"
    user_email = "testuser@example.com"

    user = create_user(Session, user_id, user_name, user_password, user_email)

    assert user.id == user_id
    assert user.name == user_name
    assert user.password == user_password
    assert user.email == user_email

    session = Session()
    db_user = session.query(User).filter_by(id=user_id).first()
    assert db_user != None
    assert db_user.name == user_name
    assert db_user.password == user_password
    assert db_user.email == user_email
    session.close()








