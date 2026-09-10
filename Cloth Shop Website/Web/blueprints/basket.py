from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from flask.typing import ResponseReturnValue

from blueprints import db_Session
from database import get_products_to_dict

bp = Blueprint('basket', __name__)


@bp.route("/add-to-basket", methods=["POST"])
def my_route() -> ResponseReturnValue:
    product_ID = int(request.json["product_ID"])

    session['basket'].append(product_ID)
    session.modified = True
    return "Success"

@bp.route('/basket', methods = ['GET'])
def basket() -> ResponseReturnValue:
    products = get_products_to_dict(db_Session())
    filtered_products = [product for product in products if product['id'] in session['basket']]
    total_cost = sum(product['cost'] for product in filtered_products)
    total_cost = round(total_cost, 2)
    return render_template('basket.html', products = filtered_products, total_cost = total_cost)

@bp.route('/basket/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int) -> ResponseReturnValue:
    if 'basket' in session:
        basket = session['basket']
        if product_id in basket:
            basket.remove(product_id)
            session.modified = True
            products = get_products_to_dict(db_Session())
            filtered_products = [product for product in products if product['id'] in session['basket']]
            total_cost = sum([product['cost'] for product in filtered_products])
            total_cost = round(total_cost, 2)
            return jsonify({'success': True, 'totalCost': total_cost, 'products': filtered_products})
    return jsonify({'success': False, 'message': 'Product not found in the basket'})

@bp.route('/checkout')
def checkout() -> ResponseReturnValue:
    if session['basket']:
        if 'user' in session:
            user_info = session['user']
            return render_template('checkout.html', user_info = user_info)
        return render_template('checkout.html')
    return redirect(url_for('basket.basket'))
