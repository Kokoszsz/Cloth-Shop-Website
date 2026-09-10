from flask import Flask, Response, render_template, redirect, url_for, jsonify, request, session
from flask.typing import ResponseReturnValue
from config import get_config
from exceptions import DuplicateReview, DuplicateUser, ProductNotFound, ShopError, UserNotFound
from utils import (
    ValidationError,
    authenticate,
    filter_products,
    get_genders_and_kinds,
    get_product_by_url,
    get_username_by_id_filter,
    validate_account,
)
from database import (
    create_database_Session,
    create_rating,
    create_review,
    create_user,
    get_all_ratings_of_a_product,
    get_certain_rating,
    get_products_to_dict,
    get_reviews_of_a_product,
    get_users,
    remove_rating,
    remove_review,
    update_user,
)


app = Flask(__name__)
app.config.from_object(get_config())
db_Session = create_database_Session(
    'sqlite:///Cloth Shop Website/Databases/mydb.db', echo=app.config['SQLALCHEMY_ECHO']
)

app.jinja_env.filters['get_username_by_id'] = get_username_by_id_filter


def messages_by_field(errors: list[ValidationError]) -> dict[str, str]:
    return {error.field: error.message for error in errors}


@app.errorhandler(DuplicateReview)
def handle_duplicate_review(error: DuplicateReview) -> ResponseReturnValue:
    return jsonify({'message': 'You have already reviewed this product'}), 409


@app.errorhandler(ProductNotFound)
@app.errorhandler(UserNotFound)
def handle_missing_record(error: ShopError) -> ResponseReturnValue:
    return jsonify({'message': str(error)}), 404
    
@app.template_filter('nl2br')
def nl2br_filter(s: str) -> str:
    return s.replace('\n', '<br>')

@app.route('/')
def home() -> ResponseReturnValue:
    return render_template('home.html')

@app.route('/cloth')
def cloth() -> ResponseReturnValue:
    products = get_products_to_dict(db_Session)
    product_data_json = jsonify(products)
    return render_template('cloth.html', products = products, products_json = product_data_json)

@app.route('/filtered-products', methods=['POST'])
def get_filtered_products() -> ResponseReturnValue:
    min_value = float(request.form['minvalue'])
    max_value = float(request.form['maxvalue'])

    if min_value >= max_value:
        min_value = 0
        max_value = 0

    genders, kinds = get_genders_and_kinds(request.form)

    products = get_products_to_dict(db_Session)
    filtered_products = filter_products(products, min_value, max_value, genders, kinds)

    return jsonify({'products': filtered_products})

@app.route("/add-to-basket", methods=["POST"])
def my_route() -> ResponseReturnValue:
    product_ID = int(request.json["product_ID"])

    session['basket'].append(product_ID)
    session.modified = True
    return "Success"

@app.route('/account', methods = ['POST', 'GET'])
def account() -> ResponseReturnValue:
    errors: list[ValidationError] = []

    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':

            id = session['user']['id']
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            surname = request.form['surname']
            phone_number = request.form['phone']
            country = request.form['country']
            city = request.form['city']

            users = get_users(db_Session)

            errors = validate_account(users, id, username, email, password)
            if not errors:
                user = update_user(db_Session, id, username, password, email, users, surname, phone_number, country, city)
                session['user'] = user.to_dict()

        user_info = session['user']
        return render_template('account.html', user_info = user_info, errors = messages_by_field(errors))

@app.route('/login', methods = ['POST', 'GET'])
def login() -> ResponseReturnValue:
    error = None
    if request.method == 'POST':

        if request.form['action'] == "Create account":
            return redirect(url_for('create_account'))
        
        username = request.form['login']
        password = request.form['password']

        users = get_users(db_Session)
        user_info, error = authenticate(username, password, users)

        if user_info is not None:
            session['user'] = user_info.to_dict()
            return redirect(url_for('account'))

    return render_template('login.html', error = error.message if error else None)


@app.route('/create_account', methods = ['POST', 'GET'])
def create_account() -> ResponseReturnValue:

    errors: list[ValidationError] = []

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        users = get_users(db_Session)

        errors = validate_account(users, None, username, email, password)

        if not errors:
            try:
                user = create_user(db_Session, username, password, email)
            except DuplicateUser:
                errors = [ValidationError('username', 'Already such an User')]
            else:
                session['user'] = user.to_dict()
                return redirect(url_for('account'))

    return render_template('create_account.html', errors = messages_by_field(errors))

@app.route('/basket', methods = ['GET'])
def basket() -> ResponseReturnValue:
    products = get_products_to_dict(db_Session)
    filtered_products = [product for product in products if product['id'] in session['basket']]
    total_cost = sum(product['cost'] for product in filtered_products)
    total_cost = round(total_cost, 2)
    return render_template('basket.html', products = filtered_products, total_cost = total_cost)

@app.route('/basket/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int) -> ResponseReturnValue:
    if 'basket' in session:
        basket = session['basket']
        if product_id in basket:
            basket.remove(product_id)
            session.modified = True
            products = get_products_to_dict(db_Session)
            filtered_products = [product for product in products if product['id'] in session['basket']]
            total_cost = sum([product['cost'] for product in filtered_products])
            total_cost = round(total_cost, 2)
            return jsonify({'success': True, 'totalCost': total_cost, 'products': filtered_products})
    return jsonify({'success': False, 'message': 'Product not found in the basket'})

@app.route('/checkout')
def checkout() -> ResponseReturnValue:
    if session['basket']:
        if 'user' in session:
            user_info = session['user']
            return render_template('checkout.html', user_info = user_info)
        return render_template('checkout.html')
    return redirect(url_for('basket'))


@app.route('/cloth/product_detail/<product_url>')
def product_detail(product_url: str) -> ResponseReturnValue:


    products = get_products_to_dict(db_Session)
    product_dict = get_product_by_url(products, product_url)
    initial_rating = None
    initial_reviews = None
    users = get_users(db_Session)
    if product_dict:
        initial_reviews = get_reviews_of_a_product(db_Session, product_dict['id'])
    if 'user' in session:
        user_id = session['user']['id']
        rating_obj = get_certain_rating(db_Session, product_dict['id'], user_id)
        if rating_obj:
            initial_rating = rating_obj.rating_points
    if product_dict is not None:
        all_ratings, num_of_ratings = get_all_ratings_of_a_product(db_Session, product_dict['id'])
        if num_of_ratings:
            rating_average = sum([rating.rating_points for rating in all_ratings])/num_of_ratings
        else:
            rating_average = 0
        return render_template('product_detail.html', product=product_dict, initial_rating=initial_rating, initial_reviews=initial_reviews, users=users, rating=rating_average)
    else:
        # If product is None, return a custom error message or redirect to a different page
        return render_template('product_not_found.html')
    
@app.route('/save_rating', methods=['POST'])
def save_rating() -> ResponseReturnValue:
    data = request.get_json()
    rating_data = float(data['rating'])
    product_id_data = int(data['productId'])
    if not 1 <= rating_data <= 5:
        return jsonify({'message': 'Rating must be between 1 and 5 (inclusive)'}), 400
    user_id = session['user']['id']
    create_rating(db_Session, product_id_data, user_id, rating_data)

    return jsonify({'message': 'Rating saved successfully'})

@app.route('/reset_rating', methods=['POST'])
def reset_rating() -> ResponseReturnValue:
    data = request.get_json()
    product_id_data = int(data['productId'])
    user_id = session['user']['id']

    remove_rating(db_Session, product_id_data, user_id)
    return jsonify({'message': 'Rating reset successfully'})


@app.route('/save_review', methods=['POST'])
def save_review() -> ResponseReturnValue:
    if not 'user' in session:
         return jsonify({'message': 'user not logged in'})
    data = request.get_json()
    review_content = str(data['content'])
    product_id_data = int(data['productId'])
    user_id = session['user']['id']
    review_object = create_review(db_Session, product_id_data, user_id, review_content)
    return jsonify({'message': 'Review saved successfully', 'id': review_object.id})

@app.route('/delete_review', methods=['POST'])
def delete_review() -> ResponseReturnValue:
    if not 'user' in session:
         return jsonify({'message': 'user not logged in'})
    else:
        user_id = session['user']['id']
    data = request.get_json()
    reviewId = int(data['reviewId'])

    success = remove_review(db_Session, reviewId, user_id)
    return jsonify({'success': success})



@app.route('/logout')
def logout() -> ResponseReturnValue | None:
    if 'user' in session:
        session.pop('user', None)
        session['basket'] = []
        return redirect(url_for('home'))
    else:
        pass


@app.before_request
def before_request() -> ResponseReturnValue | None:
    if 'user' in session and request.endpoint in ['login']:
        return redirect(url_for('home'))
    if 'user' in session and request.endpoint in ['create_account']:
        return redirect(url_for('home'))
    ## if you are logged in and you try to go back to login page you will get redirected to home page

    if 'basket' not in session:
        session['basket'] = []
    ## sets empty basket

## User will be unable to go back to a previously visited page and remaining logged in after logging out
@app.after_request
def add_header(response: Response) -> Response:
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    response.cache_control.max_age = 0
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = 0
    return response


if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])

