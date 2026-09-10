import pytest
from models import Product, User


@pytest.fixture
def product():
    return Product(4, "Red T-shirt Extra", 69.99, "t-shirt", "male", "red_t_shirt.png")


def test_user_leaves_the_id_for_the_database_to_assign():
    user = User("John", "password123", "john@example.com")

    assert user.id is None
    assert user.name == "John"
    assert user.email == "john@example.com"


def test_product_initialization(product):
    assert product.id == 4
    assert product.name == "Red T-shirt Extra"
    assert product.cost == 69.99
    assert product.cloth_cathegory == "t-shirt"
    assert product.gender == "male"
    assert product.image == "red_t_shirt.png"


def test_product_url_generation(product):
    assert product.url == "Red-T-shirt-Extra"
