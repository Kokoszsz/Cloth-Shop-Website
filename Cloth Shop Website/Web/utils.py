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
    
def check_if_error(users, id, username, email, password):
    if ' ' in username:
        return 'Username can not have spaces'
    if ' ' in password:
        return 'Password can not have spaces'
    if username != '':
        if email != '':
            if all(user.name != username or user.id == id for user in users):
                if all(user.email != email or user.id == id for user in users):
                    if len(password) < 8:
                        return 'Password must consist of at lest 8 characters'
                    else:
                        return None
                else:
                    return 'Already such an E-mail'
            else:
                return 'Already such an User'
        else:
            return 'No E-mail provided'
    else:
        return 'No Username provided'
    
def get_product_by_url(products, product_url):
    for product in products:
        if product['url'] == product_url:
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



def get_username_by_id_filter(users, user_id):
    for user in users:
        if user.id == user_id:
            return user.name
    return 'Unknown' 

    