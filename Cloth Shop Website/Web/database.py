import mysql.connector

mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="rzkyn203h534i90$@#!%#$",
      database = "cloth_shop"
    )

def get_users():

    mycursor = mydb.cursor()
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
        }
        users.append(user_dict)

    return users

def get_products():

    mycursor = mydb.cursor()
    mycursor.execute('''SELECT * FROM products''')
    product_data = mycursor.fetchall()
    mycursor.close()

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

    return products
