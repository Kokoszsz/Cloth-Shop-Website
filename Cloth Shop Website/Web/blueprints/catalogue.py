from flask import Blueprint, jsonify, render_template, request, session
from flask.typing import ResponseReturnValue

from blueprints import db_Session
from database import (
    get_all_ratings_of_a_product,
    get_certain_rating,
    get_products_to_dict,
    get_reviews_of_a_product,
    get_users,
)
from utils import filter_products, get_genders_and_kinds, get_product_by_url

bp = Blueprint('catalogue', __name__)


@bp.route('/')
def home() -> ResponseReturnValue:
    return render_template('home.html')

@bp.route('/cloth')
def cloth() -> ResponseReturnValue:
    products = get_products_to_dict(db_Session())
    product_data_json = jsonify(products)
    return render_template('cloth.html', products = products, products_json = product_data_json)

@bp.route('/filtered-products', methods=['POST'])
def get_filtered_products() -> ResponseReturnValue:
    min_value = float(request.form['minvalue'])
    max_value = float(request.form['maxvalue'])

    if min_value >= max_value:
        min_value = 0
        max_value = 0

    genders, kinds = get_genders_and_kinds(request.form)

    products = get_products_to_dict(db_Session())
    filtered_products = filter_products(products, min_value, max_value, genders, kinds)

    return jsonify({'products': filtered_products})


@bp.route('/cloth/product_detail/<product_url>')
def product_detail(product_url: str) -> ResponseReturnValue:


    products = get_products_to_dict(db_Session())
    product_dict = get_product_by_url(products, product_url)
    initial_rating = None
    initial_reviews = None
    users = get_users(db_Session())
    if product_dict:
        initial_reviews = get_reviews_of_a_product(db_Session(), product_dict['id'])
    if 'user' in session:
        user_id = session['user']['id']
        rating_obj = get_certain_rating(db_Session(), product_dict['id'], user_id)
        if rating_obj:
            initial_rating = rating_obj.rating_points
    if product_dict is not None:
        all_ratings, num_of_ratings = get_all_ratings_of_a_product(db_Session(), product_dict['id'])
        if num_of_ratings:
            rating_average = sum([rating.rating_points for rating in all_ratings])/num_of_ratings
        else:
            rating_average = 0
        return render_template('product_detail.html', product=product_dict, initial_rating=initial_rating, initial_reviews=initial_reviews, users=users, rating=rating_average)
    else:
        # If product is None, return a custom error message or redirect to a different page
        return render_template('product_not_found.html')
