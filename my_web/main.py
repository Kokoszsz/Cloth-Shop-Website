from flask import render_template, redirect, url_for, jsonify, request, session, Flask
from database import get_users, get_products, mydb
from utils import filter_products, check_login, check_if_error



app = Flask(__name__)
app.secret_key = 'm23T#mr4weio4t4gsd$%@'
users = get_users()
products = get_products()



@app.route('/')
def home():
    session['basket'] = []
    return render_template('home.html')


@app.route('/cloth')
def cloth():
    return render_template('cloth.html', products = products)

@app.route('/filtered-products', methods=['POST'])
def get_filtered_products():
    min_value = int(request.form['minvalue'])
    max_value = int(request.form['maxvalue'])

    if min_value >= max_value:
        min_value = 0
        max_value = 0

    genders = []
    kinds = []

    if 'male' in request.form:
        genders.append('male')
    if 'female' in request.form:
        genders.append('female')    
    if 't_shirt' in request.form:
        kinds.append('t_shirt')
    if 'jeans' in request.form:
        kinds.append('jeans')
    if 'shirt' in request.form:
        kinds.append('shirt')

    filtered_products = filter_products(products, min_value, max_value, genders, kinds)

    return jsonify({'products': filtered_products})

@app.route("/my-route", methods=["POST"])
def my_route():

    product_ID = int(request.json["product_ID"])

    session['basket'].append(product_ID)
    session.modified = True
    return "Success"

@app.route('/account', methods = ['POST', 'GET'])
def account():
    error = ''

    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':

            id = session['user']['id']
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']



            error = check_if_error(users, username, id, email, password)

            if error == '':
                cursor = mydb.cursor()

                sql = "UPDATE users SET Name = %s, Password = %s, `e-mail` = %s WHERE idUsers = %s"

                val = (username, password, email, id)
                cursor.execute(sql, val)

                mydb.commit()

                cursor.close()
                session['user'] = {
                    'email': email, 
                    'id': id, 
                    'name': username, 
                    'password': password,
                }

        user_info = session['user']
        return render_template('account.html', user_info = user_info, error = error)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    potential_error = ''
    if request.method == 'POST':

        if request.form["action"] == "Create account":
            return redirect(url_for('create_account'))
        
        username = request.form['login']
        password = request.form['password']

        potential_error, user_info = check_login(username, password, users)


        if potential_error == 'good':
            session['user'] = user_info
            return redirect(url_for('account'))


    return render_template('login.html', error = potential_error)


@app.route('/create_account', methods = ['POST', 'GET'])
def create_account():

    error = ''

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        id = users[-1]['id'] + 1 ## this should be changed
        error = check_if_error(users, username, id, email, password)

        print(error)

        if error == '':
            cursor = mydb.cursor()

            sql = "INSERT INTO users (idUsers, Name, Password, `e-mail`) VALUES (%s, %s, %s, %s)"

            val = (id, username, password, email)
            cursor.execute(sql, val)
            mydb.commit()
            cursor.close()

            this_user = {
                'email': email, 
                'id': id, 
                'name': username, 
                'password': password,
            }

            users.append(this_user)

            session['user'] = this_user

            return redirect(url_for('account'))
        
        else:
            return render_template('create_account.html', error = error)

    return render_template('create_account.html', error = error)




@app.route('/basket')
def basket():

    filtered_products = [product for product in products if product['id'] in session['basket']]
    total_cost = sum(product['cost'] for product in filtered_products)
    #print(filtered_products)
    return render_template('basket.html', products = filtered_products, total_cost = total_cost)

@app.route('/basket/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if 'basket' in session:
        basket = session['basket']
        print(basket)
        if product_id in basket:
            basket.remove(product_id)
            session.modified = True
            filtered_products = [product for product in products if product['id'] in session['basket']]
            total_cost = sum([product['cost'] for product in filtered_products])
            return jsonify({'success': True, 'totalCost': total_cost, 'products': filtered_products})
    return jsonify({'success': False, 'message': 'Product not found in the basket'})



@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        return redirect(url_for('home'))
    else:
        pass


## if you are logged in and you try to go back to login page you will get redirected to home page
@app.before_request
def check_if_logged():
    if 'user' in session and request.endpoint in ['login']:
        return redirect(url_for('home'))
    if 'user' in session and request.endpoint in ['create_account']:
        return redirect(url_for('home'))

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

