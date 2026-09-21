import re

from data import DEFAULT_PASSWORD, Customer, unique_email, unique_username
from playwright.sync_api import APIRequestContext, APIResponse

FORM_ERROR = re.compile(r'<p style="color:red">(.*?)</p>')


def form_errors(response: APIResponse) -> list[str]:
    return FORM_ERROR.findall(response.text())


def check(response: APIResponse, action: str) -> None:
    if not response.ok:
        raise AssertionError(f'{action} failed with {response.status}: {response.text()}')


def register(
    request: APIRequestContext,
    username: str | None = None,
    email: str | None = None,
    password: str = DEFAULT_PASSWORD,
) -> Customer:
    customer = Customer(
        username if username is not None else unique_username(),
        email if email is not None else unique_email(),
        password,
    )
    response = request.post('/create_account', form={
        'username': customer.username,
        'email': customer.email,
        'password': customer.password,
    })
    if not response.url.endswith('/account'):
        raise AssertionError(f'Registering {customer.username} failed: {form_errors(response)}')
    return customer


def save_details(
    request: APIRequestContext,
    customer: Customer,
    surname: str,
    phone: str,
    country: str,
    city: str,
) -> None:
    response = request.post('/account', form={
        'username': customer.username,
        'email': customer.email,
        'password': customer.password,
        'surname': surname,
        'phone': phone,
        'country': country,
        'city': city,
    })
    errors = form_errors(response)
    if not response.url.endswith('/account') or errors:
        raise AssertionError(f'Saving details for {customer.username} failed: {errors}')


def add_to_basket(request: APIRequestContext, product_id: int) -> None:
    response = request.post('/api/v1/basket/items', data={'product_id': product_id})
    check(response, f'Adding product {product_id} to the basket')


def rate(request: APIRequestContext, product_id: int, stars: int) -> None:
    response = request.put(f'/api/v1/products/{product_id}/rating', data={'rating': stars})
    check(response, f'Rating product {product_id}')


def review(request: APIRequestContext, product_id: int, text: str) -> None:
    response = request.post(f'/api/v1/products/{product_id}/reviews', data={'content': text})
    check(response, f'Reviewing product {product_id}')
