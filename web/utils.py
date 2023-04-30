def filter_products(products, min_value, max_value, genders, kinds):
    filtered_products = []
    for product in products:
        if product['cost'] > min_value and product['cost'] < max_value or max_value == 0 and min_value == 0:
            if product['cloth_cathegory'] in kinds or kinds == []:
                if product['gender'] in genders or genders == []:
                    filtered_products.append(product)
    return filtered_products

def check_login(username, password, users):
    for user in users:
        if user['name'] == username:  
            if user['password'] == password: 
                return 'good', user
            else:
                return 'Wrong Password', None
    else:
        return 'Wrong Username', None