from collections.abc import Callable
from functools import wraps
from typing import Any

from flask import jsonify, request, session
from flask.typing import ResponseReturnValue
from flask_smorest import Blueprint
from werkzeug.exceptions import HTTPException

from blueprints import db_Session
from blueprints.schemas import (
    ApiErrorSchema,
    BasketItemSchema,
    BasketSchema,
    ProductListSchema,
    RatingResultSchema,
    RatingSchema,
    ReviewResultSchema,
    ReviewSchema,
)
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


@bp.errorhandler(400)
def handle_failed_validation(exc: HTTPException) -> ResponseReturnValue:
    problems = getattr(exc, 'data', {}).get('messages', {}).get('json', {})
    if not problems or not isinstance(request.get_json(silent=True), dict):
        return error(400, 'invalid_body', 'Send a JSON object')

    field, messages = next(iter(problems.items()))
    return error(400, f'invalid_{field}', messages[0])


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


def price_argument(name: str) -> float:
    try:
        return float(request.args.get(name, '0'))
    except ValueError:
        raise InvalidInput('invalid_price', f'{name} must be a number') from None


def basket_response(status: int) -> ResponseReturnValue:
    products = get_products_to_dict(db_Session())
    items = [product for product in products if product['id'] in session['basket']]
    total_cost = round(sum(item['cost'] for item in items), 2)
    return {'items': items, 'total_cost': total_cost}, status


@bp.get('/products')
@bp.response(200, ProductListSchema)
@bp.alt_response(400, schema=ApiErrorSchema)
def list_products() -> ResponseReturnValue:
    """List products, optionally filtered by price, gender and category."""
    min_price = price_argument('min_price')
    max_price = price_argument('max_price')
    if min_price >= max_price:
        min_price = 0
        max_price = 0

    genders, _ = get_genders_and_kinds(request.args.getlist('gender'))
    _, categories = get_genders_and_kinds(request.args.getlist('category'))

    products = get_products_to_dict(db_Session())
    matching = filter_products(products, min_price, max_price, genders, categories)
    return {'products': matching}


@bp.post('/basket/items')
@bp.arguments(BasketItemSchema, error_status_code=400)
@bp.response(201, BasketSchema)
@bp.alt_response(404, schema=ApiErrorSchema)
def add_basket_item(body: dict[str, Any]) -> ResponseReturnValue:
    """Add a product to the basket and return the whole basket."""
    product_id = body['product_id']
    if get_product(db_Session(), product_id) is None:
        raise ProductNotFound(product_id)

    session['basket'].append(product_id)
    session.modified = True
    return basket_response(201)


@bp.delete('/basket/items/<int:product_id>')
@bp.response(200, BasketSchema)
@bp.alt_response(404, schema=ApiErrorSchema)
def remove_basket_item(product_id: int) -> ResponseReturnValue:
    """Remove a product from the basket and return the whole basket."""
    if product_id not in session['basket']:
        return error(404, 'not_in_basket', 'This product is not in the basket')

    session['basket'].remove(product_id)
    session.modified = True
    return basket_response(200)


@bp.put('/products/<int:product_id>/rating')
@login_required
@bp.arguments(RatingSchema, error_status_code=400)
@bp.response(200, RatingResultSchema)
@bp.alt_response(401, schema=ApiErrorSchema)
@bp.alt_response(404, schema=ApiErrorSchema)
def set_rating(body: dict[str, Any], product_id: int) -> ResponseReturnValue:
    """Set the logged-in user's rating for a product, replacing any earlier one."""
    rating = body['rating']
    create_rating(db_Session(), product_id, session['user']['id'], rating)
    return {'rating': rating}


@bp.delete('/products/<int:product_id>/rating')
@login_required
@bp.response(204)
@bp.alt_response(401, schema=ApiErrorSchema)
@bp.alt_response(404, schema=ApiErrorSchema)
def delete_rating(product_id: int) -> ResponseReturnValue:
    """Remove the logged-in user's rating for a product."""
    if not remove_rating(db_Session(), product_id, session['user']['id']):
        return error(404, 'rating_not_found', 'You have not rated this product')
    return '', 204


@bp.post('/products/<int:product_id>/reviews')
@login_required
@bp.arguments(ReviewSchema, error_status_code=400)
@bp.response(201, ReviewResultSchema)
@bp.alt_response(401, schema=ApiErrorSchema)
@bp.alt_response(404, schema=ApiErrorSchema)
@bp.alt_response(409, schema=ApiErrorSchema)
def add_review(body: dict[str, Any], product_id: int) -> ResponseReturnValue:
    """Post the logged-in user's review of a product."""
    content = body['content']
    review = create_review(db_Session(), product_id, session['user']['id'], content)
    return {'id': review.id, 'content': review.content}


@bp.delete('/reviews/<int:review_id>')
@login_required
@bp.response(204)
@bp.alt_response(401, schema=ApiErrorSchema)
@bp.alt_response(404, schema=ApiErrorSchema)
def delete_review(review_id: int) -> ResponseReturnValue:
    """Delete one of the logged-in user's own reviews."""
    if not remove_review(db_Session(), review_id, session['user']['id']):
        return error(404, 'review_not_found', 'Review not found')
    return '', 204
