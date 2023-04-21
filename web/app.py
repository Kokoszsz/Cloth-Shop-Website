from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb  import MySQL


app = Flask(__name__, static_url_path='/static')
app.secret_key = 'm23T#mr4weio4t4gsd$%@'

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rzkyn203h534i90$@#!%#$",
  database = "sql_hr"
)

mycursor = mydb.cursor()
mycursor.execute('''SELECT * FROM offices''')
data = mycursor.fetchall()
mycursor.close()
print(str(data))




@app.route('/')
def home():
    return render_template('home.html')


@app.route('/cloth',  methods=['POST', 'GET'])
def cloth():
    min_value = 0
    max_value = 1000000
    products = [{'name': 'Product 1', 'cost': 10, 'image': 'picture_shop.jpg', 'cloth_cathegory': 'jeans' }, {'name': 'Product 2', 'cost': 20, 'image': 'picture_shop.jpg', 'cloth_cathegory': 't_shirt' }, {'name': 'Product 2', 'cost': 20, 'image': 'picture_shop.jpg', 'cloth_cathegory': 't_shirt' }, {'name': 'Product 2', 'cost': 20, 'image': 'picture_shop.jpg', 'cloth_cathegory': 't_shirt' }, {'name': 'Product 2', 'cost': 20, 'image': 'picture_shop.jpg', 'cloth_cathegory': 't_shirt' }, {'name': 'Product 2', 'cost': 20, 'image': 'picture_shop.jpg', 'cloth_cathegory': 't_shirt' }, {'name': 'Product 2', 'cost': 20, 'image': 'picture_shop.jpg', 'cloth_cathegory': 't_shirt' }, {'name': 'Product 2', 'cost': 20, 'image': 'picture_shop.jpg', 'cloth_cathegory': 't_shirt' }]
    if request.method == 'POST':
        if request.form['filter_button'] == 'Filter':
            min_value = int(request.form['minvalue'])
            max_value = int(request.form['maxvalue'])
            if min_value < max_value:
                return render_template('cloth.html', products = products, min_value = min_value, max_value = max_value)

    return render_template('cloth.html', products = products, min_value = 0, max_value = 1000000)


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

