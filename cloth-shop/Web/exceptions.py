class ShopError(Exception):
    """Base class for failures raised by the data layer."""


class ProductNotFound(ShopError):
    def __init__(self, product_id: int) -> None:
        super().__init__(f'No product with id {product_id}')
        self.product_id = product_id


class UserNotFound(ShopError):
    def __init__(self, user_id: int) -> None:
        super().__init__(f'No user with id {user_id}')
        self.user_id = user_id


class DuplicateUser(ShopError):
    def __init__(self, name: str, email: str) -> None:
        super().__init__(f'An account already exists for {name!r} or {email!r}')
        self.name = name
        self.email = email


class DuplicateReview(ShopError):
    def __init__(self, product_id: int, user_id: int) -> None:
        super().__init__(f'User {user_id} has already reviewed product {product_id}')
        self.product_id = product_id
        self.user_id = user_id
