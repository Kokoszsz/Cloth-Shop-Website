from collections.abc import Callable
from functools import wraps
from typing import Any

from flask import Blueprint, jsonify, request, session
from flask.typing import ResponseReturnValue

from blueprints import db_Session
from database import (
    create_rating,
    create_review,
    get_product,
    get_products_to_dict,
    remove_rating,
    remove_review,
)
from exceptions import DuplicateReview, ProductNotFound, UserNotFound
from utils import filter_products, get_genders_and_kinds

bp = Blueprint('api', __name__, url_prefix='/api/v1')

View = Callable[..., ResponseReturnValue]


class InvalidInput(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def error(status: int, code: str, message: str) -> ResponseReturnValue:
    return jsonify({'error': {'code': code, 'message': message}}), status


@bp.errorhandler(InvalidInput)
def handle_invalid_input(exc: InvalidInput) -> ResponseReturnValue:
    return error(400, exc.code, exc.message)


@bp.errorhandler(ProductNotFound)
def handle_missing_product(exc: ProductNotFound) -> ResponseReturnValue:
    return error(404, 'product_not_found', str(exc))


@bp.errorhandler(UserNotFound)
def handle_missing_user(exc: UserNotFound) -> ResponseReturnValue:
    return error(404, 'user_not_found', str(exc))


@bp.errorhandler(DuplicateReview)
def handle_duplicate_review(exc: DuplicateReview) -> ResponseReturnValue:
    return error(409, 'review_exists', 'You have already reviewed this product')


def login_required(view: View) -> View:
    @wraps(view)
    def wrapper(*args: Any, **kwargs: Any) -> ResponseReturnValue:
        if 'user' not in session:
            return error(401, 'not_logged_in', 'Log in to do this')
        return view(*args, **kwargs)

    return wrapper


def json_body() -> dict[str, Any]:
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        raise InvalidInput('invalid_body', 'Send a JSON object')
    return body


def is_whole_number(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def price_argument(name: str) -> float:
    try:
        return float(request.args.get(name, '0'))
    except ValueError:
        raise InvalidInput('invalid_price', f'{name} must be a number') from None


def basket_response(status: int) -> ResponseReturnValue:
    products = get_products_to_dict(db_Session())
    items = [product for product in products if product['id'] in session['basket']]
    total_cost = round(sum(item['cost'] for item in items), 2)
    return jsonify({'items': items, 'total_cost': total_cost}), status


@bp.get('/products')
def list_products() -> ResponseReturnValue:
    min_price = price_argument('min_price')
    max_price = price_argument('max_price')
    if min_price >= max_price:
        min_price = 0
        max_price = 0

    genders, _ = get_genders_and_kinds(request.args.getlist('gender'))
    _, categories = get_genders_and_kinds(request.args.getlist('category'))

    products = get_products_to_dict(db_Session())
    matching = filter_products(products, min_price, max_price, genders, categories)
    return jsonify({'products': matching})


@bp.post('/basket/items')
def add_basket_item() -> ResponseReturnValue:
    product_id = json_body().get('product_id')
    if not is_whole_number(product_id):
        raise InvalidInput('invalid_product_id', 'product_id must be a whole number')
    if get_product(db_Session(), product_id) is None:
        raise ProductNotFound(product_id)

    session['basket'].append(product_id)
    session.modified = True
    return basket_response(201)


@bp.delete('/basket/items/<int:product_id>')
def remove_basket_item(product_id: int) -> ResponseReturnValue:
    if product_id not in session['basket']:
        return error(404, 'not_in_basket', 'This product is not in the basket')

    session['basket'].remove(product_id)
    session.modified = True
    return basket_response(200)


@bp.put('/products/<int:product_id>/rating')
@login_required
def set_rating(product_id: int) -> ResponseReturnValue:
    rating = json_body().get('rating')
    if not is_number(rating) or not 1 <= rating <= 5:
        raise InvalidInput('invalid_rating', 'rating must be a number from 1 to 5')

    create_rating(db_Session(), product_id, session['user']['id'], rating)
    return jsonify({'rating': rating})


@bp.delete('/products/<int:product_id>/rating')
@login_required
def delete_rating(product_id: int) -> ResponseReturnValue:
    if not remove_rating(db_Session(), product_id, session['user']['id']):
        return error(404, 'rating_not_found', 'You have not rated this product')
    return '', 204


@bp.post('/products/<int:product_id>/reviews')
@login_required
def add_review(product_id: int) -> ResponseReturnValue:
    content = json_body().get('content')
    if not isinstance(content, str):
        raise InvalidInput('invalid_content', 'content must be text')

    review = create_review(db_Session(), product_id, session['user']['id'], content)
    return jsonify({'id': review.id, 'content': review.content}), 201


@bp.delete('/reviews/<int:review_id>')
@login_required
def delete_review(review_id: int) -> ResponseReturnValue:
    if not remove_review(db_Session(), review_id, session['user']['id']):
        return error(404, 'review_not_found', 'Review not found')
    return '', 204
