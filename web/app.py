from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb  import MySQL
from flask import jsonify



app = Flask(__name__, static_url_path='/static')
app.secret_key = 'm23T#mr4weio4t4gsd$%@'

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rzkyn203h534i90$@#!%#$",
  database = "cloth_shop"
)

mycursor = mydb.cursor()
mycursor.execute('''SELECT * FROM cloths''')
cloth_data = mycursor.fetchall()
mycursor.close()


products = []
for cloth in cloth_data:
    cloth_dict = {
        'name': cloth[1],
        'cost_to_show': cloth[2],
        'cost': float(cloth[2]),
        'cloth_cathegory': cloth[3],
        'gender' : cloth[4],
        'image': cloth[5]
    }
    products.append(cloth_dict)


def filter_products(products, min_value, max_value, genders, kinds):
    filtered_products = []
    for product in products:
        if product['cost'] > min_value and product['cost'] < max_value or max_value == 0 and min_value == 0:
            if product['cloth_cathegory'] in kinds or kinds == []:
                if product['gender'] in genders or genders == []:
                    filtered_products.append(product)
    return filtered_products

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


@app.route('/account')
def some_link():
    

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('account.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
        #if check_login(username, password):
        session['user'] = username

        return render_template('account.html')


    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        return redirect(url_for('home'))
    else:
        pass

## if you are logged in and you try to go back to login page you will get redirected to home page
@app.before_request
def check_login():
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
