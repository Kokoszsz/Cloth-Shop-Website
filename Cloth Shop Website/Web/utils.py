from dataclasses import dataclass
from typing import Any, Iterable

from models import User

ProductDict = dict[str, Any]

MINIMUM_PASSWORD_LENGTH = 8


@dataclass(frozen=True)
class ValidationError:
    field: str
    message: str


def filter_products(
    products: list[ProductDict],
    min_value: float,
    max_value: float,
    genders: list[str],
    kinds: list[str],
) -> list[ProductDict]:
    filtered_products = []
    for product in products:
        if product['cost'] > min_value and product['cost'] < max_value or max_value == 0:
            if product['cloth_cathegory'] in kinds or kinds == []:
                if product['gender'] in genders or genders == []:
                    filtered_products.append(product)
    return filtered_products

def authenticate(
    username: str,
    password: str,
    users: list[User],
) -> tuple[User | None, ValidationError | None]:
    for user in users:
        if user.name == username:
            if user.check_password(password):
                return user, None
            return None, ValidationError('password', 'Wrong Password')
    return None, ValidationError('username', 'Wrong Username')
    
def validate_account(
    users: list[User],
    id: int | None,
    username: str,
    email: str,
    password: str,
) -> list[ValidationError]:
    errors = []

    if username == '':
        errors.append(ValidationError('username', 'No Username provided'))
    elif ' ' in username:
        errors.append(ValidationError('username', 'Username can not have spaces'))
    elif any(user.name == username and user.id != id for user in users):
        errors.append(ValidationError('username', 'Already such an User'))

    if email == '':
        errors.append(ValidationError('email', 'No E-mail provided'))
    elif any(user.email == email and user.id != id for user in users):
        errors.append(ValidationError('email', 'Already such an E-mail'))

    if ' ' in password:
        errors.append(ValidationError('password', 'Password can not have spaces'))
    elif len(password) < MINIMUM_PASSWORD_LENGTH:
        errors.append(
            ValidationError(
                'password',
                f'Password must consist of at least {MINIMUM_PASSWORD_LENGTH} characters',
            )
        )

    return errors


def get_product_by_url(products: list[ProductDict], product_url: str) -> ProductDict | None:
    for product in products:
        if product['url'] == product_url:
            return product
    return None

def get_genders_and_kinds(request: Iterable[str]) -> tuple[list[str], list[str]]:
    genders = []
    kinds = []
    if 'male' in request:
        genders.append('male')
    if 'female' in request:
        genders.append('female')    
    if 't-shirt' in request:
        kinds.append('t-shirt')
    if 'jeans' in request:
        kinds.append('jeans')
    if 'shirt' in request:
        kinds.append('shirt')

    return genders, kinds



def get_username_by_id_filter(users: list[User], user_id: int) -> str:
    for user in users:
        if user.id == user_id:
            return user.name
    return 'Unknown' 

    