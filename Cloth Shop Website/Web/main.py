from flask import Flask, render_template, redirect, url_for, jsonify, request, session
import os
from utils import *
from database import *
from send_email import send_email


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY_CLOTH_SHOP', 'DefaultSecretKeyTesting123456789')
db_Session = create_database_Session('sqlite:///Cloth Shop Website/Databases/mydb.db')


test_users = get_users(db_Session)
print(test_users)
products = get_products_to_dict(db_Session)
print(products)
test_ratings = get_ratings(db_Session)
print(test_ratings)
print(get_all_reviews(db_Session))

app.jinja_env.filters['get_username_by_id'] = get_username_by_id_filter
    
@app.template_filter('nl2br')
def nl2br_filter(s):
    return s.replace('\n', '<br>')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cloth')
def cloth():
    product_data_json = jsonify(products)
    return render_template('cloth.html', products = products, products_json = product_data_json)

@app.route('/filtered-products', methods=['POST'])
def get_filtered_products():
    min_value = float(request.form['minvalue'])
    max_value = float(request.form['maxvalue'])

    if min_value >= max_value:
        min_value = 0
        max_value = 0

    genders, kinds = get_genders_and_kinds(request.form)

    filtered_products = filter_products(products, min_value, max_value, genders, kinds)

    return jsonify({'products': filtered_products})

@app.route("/add-to-basket", methods=["POST"])
def my_route():
    product_ID = int(request.json["product_ID"])

    session['basket'].append(product_ID)
    session.modified = True
    return "Success"

@app.route('/account', methods = ['POST', 'GET'])
def account():
    error = None

    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':

            id = session['user']['id']
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            users = get_users(db_Session)

            error = check_if_error(users, id, username, email, password)
            if error is None:

                user = update_user(db_Session, id, username, password, email, users)
                
                if user is not None:
                    session['user'] = user.to_dict()

        user_info = session['user']
        return render_template('account.html', user_info = user_info, error = error)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    potential_error = None
    if request.method == 'POST':

        if request.form['action'] == "Create account":
            return redirect(url_for('create_account'))
        
        username = request.form['login']
        password = request.form['password']

        users = get_users(db_Session)
        potential_error, user_info = check_login(username, password, users)


        if potential_error == 'good':
            session['user'] = user_info.to_dict()
            return redirect(url_for('account'))

    return render_template('login.html', error = potential_error)


@app.route('/create_account', methods = ['POST', 'GET'])
def create_account():

    error = None

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        users = get_users(db_Session)
        ids = [user.id for user in users ]
        id = max(ids)+1 ## this should be changed

        error = check_if_error(users, id, username, email, password)

        if error is None:

            verification_code = send_email('account registration verification', email)
            
            session['new_user'] = {'id': id, 'username': username, 'password': password, 'email': email, 'verification code': verification_code}

            # this will be changed to appear after user provided valid code
            return redirect(url_for('create_account_verification'))
        
        else:
            return render_template('create_account.html', error = error)

    return render_template('create_account.html', error = error)

@app.route('/create_account_verification', methods = ['POST', 'GET'])
def create_account_verification():


    if request.method == 'POST':
        if 'confirm' in request.form and request.form['confirm'] == "Confirm":
            if session['new_user'] is not None:
                id = session['new_user']['id']
                username = session['new_user']['username']
                password = session['new_user']['password']
                email = session['new_user']['email']
                verification_code = session['new_user']['verification code']

                if verification_code == request.form['verification-code']:
                
                    session.pop('new_user', None)
                    user = create_user(db_Session, id, username, password, email)
                    session['user'] = user.to_dict()

                else:
                    ## wrong code
                    return render_template('create_account_verification.html')


            ## Check if code provided by user is valid
            return redirect(url_for('account'))
        
        elif 'resend' in request.form and request.form['resend'] == "Send again":
            email = session['new_user']['email']
            verification_code = send_email('account registration verification', email)
            session['new_user']['verification code'] = verification_code

    # Check if the request is redirected from the create_account route
    referrer = request.referrer
    if referrer is None or '/create_account' not in referrer:
        # If the referrer is not from the create_account route, redirect to a different page
        return redirect(url_for('home'))

    # Rest of the code...

    # Render the verification template
    return render_template('create_account_verification.html')

@app.route('/basket', methods = ['GET'])
def basket():
    filtered_products = [product for product in products if product['id'] in session['basket']]
    total_cost = sum(product['cost'] for product in filtered_products)
    total_cost = round(total_cost, 2)
    return render_template('basket.html', products = filtered_products, total_cost = total_cost)

@app.route('/basket/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if 'basket' in session:
        basket = session['basket']
        if product_id in basket:
            basket.remove(product_id)
            session.modified = True
            filtered_products = [product for product in products if product['id'] in session['basket']]
            total_cost = sum([product['cost'] for product in filtered_products])
            total_cost = round(total_cost, 2)
            return jsonify({'success': True, 'totalCost': total_cost, 'products': filtered_products})
    return jsonify({'success': False, 'message': 'Product not found in the basket'})

@app.route('/checkout')
def checkout():
    if session['basket']:
        if 'user' in session:
            user_info = session['user']
            return render_template('checkout.html', user_info = user_info)
        return render_template('checkout.html')
    return redirect(url_for('basket'))


@app.route('/cloth/product_detail/<product_url>')
def product_detail(product_url):


    product_dict = get_product_by_url(products, product_url)
    product_name = product_dict['name']
    initial_rating = None
    initial_reviews = None
    users = get_users(db_Session)
    if product_dict:
        initial_reviews = get_reviews_of_a_product(db_Session, product_dict['id'])
    if 'user' in session:
        user_id = session['user']['id']
        rating_obj = get_certain_rating(db_Session, product_name, user_id)
        if rating_obj:
            initial_rating = rating_obj.rating_points
    if product_dict is not None:
        return render_template('product_detail.html', product=product_dict, initial_rating=initial_rating, initial_reviews=initial_reviews, users=users)
    else:
        # If product is None, return a custom error message or redirect to a different page
        return render_template('product_not_found.html')
    
@app.route('/save_rating', methods=['POST'])
def save_rating():
    data = request.get_json()
    rating_data = float(data['rating'])
    product_id_data = int(data['productId'])
    user_id = session['user']['id']
    ratings = get_ratings(db_Session)
    id = ratings[-1].id + 1 
    ids = [rating.id for rating in ratings]
    try:
        id = max(ids) + 1
    except:
        id = 1
    create_rating(db_Session, id, product_id_data, user_id, rating_data)

    return jsonify({'message': 'Rating saved successfully'})

@app.route('/reset_rating', methods=['POST'])
def reset_rating():
    data = request.get_json()
    product_id_data = int(data['productId'])
    user_id = session['user']['id']

    remove_rating(db_Session, product_id_data, user_id)
    return jsonify({'message': 'Rating reset successfully'})


@app.route('/save_review', methods=['POST'])
def save_review():
    if not 'user' in session:
         return jsonify({'message': 'user not logged in'})
    data = request.get_json()
    review_content = str(data['content'])
    product_id_data = int(data['productId'])
    user_id = session['user']['id']
    reviews = get_all_reviews(db_Session)
    ids = [review.id for review in reviews]
    try:
        id = max(ids) + 1
    except:
        id = 1
    review_object = create_review(db_Session, id, product_id_data, user_id, review_content)
    if review_object:
        object_id = review_object.id
        return jsonify({'message': 'Review saved successfully', 'id': object_id})
    else:
        return jsonify({'message': 'error'})

@app.route('/delete_review', methods=['POST'])
def delete_review():
    data = request.get_json()
    print(data)
    reviewId = int(data['reviewId'])

    success = remove_review(db_Session, reviewId)
    return jsonify({'success': success})



@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        session['basket'] = []
        return redirect(url_for('home'))
    else:
        pass


@app.before_request
def before_request():
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
def add_header(response):
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    response.cache_control.max_age = 0
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = 0
    return response


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)

