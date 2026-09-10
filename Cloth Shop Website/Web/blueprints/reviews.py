from flask import Blueprint, jsonify, request, session
from flask.typing import ResponseReturnValue

from blueprints import db_Session
from database import create_rating, create_review, remove_rating, remove_review

bp = Blueprint('reviews', __name__)


@bp.route('/save_rating', methods=['POST'])
def save_rating() -> ResponseReturnValue:
    data = request.get_json()
    rating_data = float(data['rating'])
    product_id_data = int(data['productId'])
    if not 1 <= rating_data <= 5:
        return jsonify({'message': 'Rating must be between 1 and 5 (inclusive)'}), 400
    user_id = session['user']['id']
    create_rating(db_Session(), product_id_data, user_id, rating_data)

    return jsonify({'message': 'Rating saved successfully'})

@bp.route('/reset_rating', methods=['POST'])
def reset_rating() -> ResponseReturnValue:
    data = request.get_json()
    product_id_data = int(data['productId'])
    user_id = session['user']['id']

    remove_rating(db_Session(), product_id_data, user_id)
    return jsonify({'message': 'Rating reset successfully'})


@bp.route('/save_review', methods=['POST'])
def save_review() -> ResponseReturnValue:
    if not 'user' in session:
         return jsonify({'message': 'user not logged in'})
    data = request.get_json()
    review_content = str(data['content'])
    product_id_data = int(data['productId'])
    user_id = session['user']['id']
    review_object = create_review(db_Session(), product_id_data, user_id, review_content)
    return jsonify({'message': 'Review saved successfully', 'id': review_object.id})

@bp.route('/delete_review', methods=['POST'])
def delete_review() -> ResponseReturnValue:
    if not 'user' in session:
         return jsonify({'message': 'user not logged in'})
    else:
        user_id = session['user']['id']
    data = request.get_json()
    reviewId = int(data['reviewId'])

    success = remove_review(db_Session(), reviewId, user_id)
    return jsonify({'success': success})
