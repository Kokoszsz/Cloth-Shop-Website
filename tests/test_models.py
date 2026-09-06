from Web.models import User, Product
import pytest



class TestUser:

    def setup_method(self, method):
        print(f"Setting up for {method}")
        self.user = User(1, "John", "password123", "john@example.com")

    def teardown_method(self, method):
        print(f"Tearing down for {method}")
        self.user = None

    def test_one(self):
        assert self.user.id == 1
        assert self.user.name == "John"





@pytest.fixture
def product() -> Product:
    return Product(1, "Laptop", 999.99, "A high-end laptop", "Unisex", "laptop.jpg")

def test_product_initialization(product: Product):
    assert product.id == 1
    assert product.name == "Laptop"
    assert product.cost == 999.99
    assert product.cloth_cathegory == "A high-end laptop"

def test_product_url_generation(product: Product):
    expected_url = "Laptop"
    assert product.url == expected_url




