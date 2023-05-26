def filter_products(products, min_value, max_value, genders, kinds):
    filtered_products = []
    for product in products:
        if product['cost'] > min_value and product['cost'] < max_value or max_value == 0:
            if product['cloth_cathegory'] in kinds or kinds == []:
                if product['gender'] in genders or genders == []:
                    filtered_products.append(product)
    return filtered_products

def check_login(username, password, users):
    for user in users:
        if user.name == username:  
            if user.password == password: 
                return 'good', user
            else:
                return 'Wrong Password', None
    else:
        return 'Wrong Username', None
    
def check_if_error(users, username, email, password):
    if username != '':
        if email != '':
            if all(user.name != username for user in users):
                if all(user.email != email for user in users):
                    if password != '':
                        return ''
                    else:
                        return 'No password'
                else:
                    return 'Already such an E-mail'
            else:
                return 'Already such a User'
        else:
            return 'No E-mail'
    else:
        return 'No Username'
    
def get_product_by_id(products, product_id):
    for product in products:
        if product['id'] == product_id:
            return product
    return None

def get_genders_and_kinds(request):
    genders = []
    kinds = []
    if 'male' in request:
        genders.append('male')
    if 'female' in request:
        genders.append('female')    
    if 't-shirt' in request:
        kinds.append('t-shirt')
    if 'jeans' in request:
        kinds.append('jeans')
    if 'shirt' in request:
        kinds.append('shirt')

    return genders, kinds
    