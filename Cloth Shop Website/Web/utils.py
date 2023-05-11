def filter_products(products, min_value, max_value, genders, kinds):
    filtered_products = []
    for product in products:
        if product.cost > min_value and product.cost < max_value or max_value == 0 and min_value == 0:
            if product.cloth_cathegory in kinds or kinds == []:
                if product.cloth_cathegory in genders or genders == []:
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
    
def check_if_error(users, id, username, password, email):
    if username != '':
        if email != '':
            if all(user.name != username or user.id == id for user in users):
                if all(user.email != email or user.id == id for user in users):
                    if password != '':
                        return ''
                    else:
                        return 'No password'
                else:
                    return 'Already sucha an E-mail'
            else:
                return 'Already such a User'
        else:
            return 'No E-mail'
    else:
        return 'No Username'