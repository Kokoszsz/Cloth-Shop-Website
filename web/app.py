from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from flask_mysqldb  import MySQL
import mysql.connector



app = Flask(__name__, static_url_path='/static')
app.secret_key = 'm23T#mr4weio4t4gsd$%@'


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rzkyn203h534i90$@#!%#$",
  database = "cloth_shop"
)

mycursor = mydb.cursor()
mycursor.execute('''SELECT * FROM products''')
product_data = mycursor.fetchall()
mycursor.execute('''SELECT * FROM users''')
users_data = mycursor.fetchall()
mycursor.close()

users = []
for user in users_data:
    user_dict = {
        'id': user[0],
        'name': user[1],
        'password': user[2],
        'email': user[3],
        'basket': []
    }
    users.append(user_dict)


products = []
for product in product_data:
    product_dict = {
        'id': product[0],
        'name': product[1],
        'cost_to_show': product[2],
        'cost': float(product[2]),
        'cloth_cathegory': product[3],
        'gender' : product[4],
        'image': product[5]
    }
    products.append(product_dict)

basket_for_not_logged_in = []


def filter_products(products, min_value, max_value, genders, kinds):
    filtered_products = []
    for product in products:
        if product['cost'] > min_value and product['cost'] < max_value or max_value == 0 and min_value == 0:
            if product['cloth_cathegory'] in kinds or kinds == []:
                if product['gender'] in genders or genders == []:
                    filtered_products.append(product)
    return filtered_products

def check_login(username, password):
    for user in users:
        if user['name'] == username:  
            if user['password'] == password: 
                return 'good', user
            else:
                return 'Wrong Password', None
    else:
        return 'Wrong Username', None

@app.route('/')
def home():
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

    if 'user' not in session:
        basket_for_not_logged_in.append(product_ID)
        #print(basket_for_not_logged_in)
    else:
        session['user']['basket'].append(product_ID)
        session.modified = True
        #print(session['user']['basket'])
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
            basket = session['user']['basket']




            if all(user['name'] != username or user['id'] == id for user in users):
                if all(user['email'] != email or user['id'] == id for user in users):
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
                        'basket': basket
                    }
                else:
                    error = 'Already sucha an e-mail'
            else:
                error = 'Already such a user'


        user_info = session['user']
        return render_template('account.html', user_info = user_info, error = error)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    potential_error = ''
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
    
        potential_error, user_info = check_login(username, password)

        user_info['basket'] = basket_for_not_logged_in

        if potential_error == 'good':
            session['user'] = user_info
            return redirect(url_for('account'))


    return render_template('login.html', error = potential_error)




@app.route('/basket')
def basket():

    if 'user' in session:
        filtered_products = [product for product in products if product['id'] in session['user']['basket']]
        #print(filtered_products)
        return render_template('basket.html', products = filtered_products)
    else:
        filtered_products = [product for product in products if product['id'] in basket_for_not_logged_in]
        #print(filtered_products)
        return render_template('basket.html', products = filtered_products)



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
    #db.create_all()
    app.run(host = '0.0.0.0', debug=True)

