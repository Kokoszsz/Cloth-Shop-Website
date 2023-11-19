from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import User, Product, Rating, Review ,Base


def create_database_Session(url):
    engine = create_engine(url, echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session


def create_user(Session, id, name, password, email):
    session = Session()
    user = User(id, name, password, email)
    session.merge(user)
    session.commit()
    session.close()
    return user

def update_user(Session, id, name, password, email, users, surname="", phone_number="", country="", city=""):
    session = Session()
    user = next((user for user in users if user.id == id), None)
    if user is not None:
        user.name = name
        user.password = password
        user.email = email
        user.surname = surname
        user.phone = phone_number
        user.country = country
        user.city = city
        session.merge(user)
        session.commit()
        session.close()
    return user


def get_users(Session):
    session = Session()
    results = session.query(User.id, User.name, User.password, User.email, User.surname, User.phone, User.country, User.city).all()
    users = [User(*r) for r in results]
    session.close()
    return users


def get_user(Session, user_id):
    session = Session()
    result = session.query(User.id, User.name, User.password, User.email, User.surname, User.phone, User.country, User.city).filter(User.id == user_id).first()
    session.close()

    if result:
        user = User(*result)
        return user
    else:
        return None
    


def get_products_to_dict(Session):
    session = Session()
    results = session.query(Product).all()
    products = [{'id': r.id, 'name': r.name, 'cost': r.cost, 'cloth_cathegory': r.cloth_cathegory,
                 'gender': r.gender, 'image': r.image, 'url': r.to_url()} for r in results]
    session.close()
    return products

def get_product(Session, product_id):
    session = Session()
    result = session.query(Product).filter(Product.id == product_id).first()
    session.close()

    if result:
        return result
    else:
        return None


def modify_rating(session, rating_obj, rating_points):
    rating_obj.rating_points = rating_points
    session.merge(rating_obj)
    session.commit()
    session.close()
    return rating_obj


def create_rating(Session, id, product_id, user_id, new_rating_points):
    session = Session()

    if get_user(Session, user_id) and get_product(Session, product_id):
        rating_objects = session.query(Rating).all()
        for rating_obj in rating_objects:
            if rating_obj.product_id == product_id and rating_obj.user_id == user_id:
                return modify_rating(session, rating_obj, new_rating_points)

        rating_obj = Rating(id, product_id, user_id, new_rating_points)
        session.merge(rating_obj)
        session.commit()
        session.close()
        return rating_obj
        

    return 'Could not find this product or this user'


def get_ratings(Session):
    session = Session()
    results = session.query(Rating).all()
    session.close()
    return results

def get_certain_rating(Session, product_id, user_id):
    session = Session()
    rating = session.query(Rating).filter_by(product_id=product_id, user_id=user_id).first()
    session.close()
    return rating

def get_all_ratings_of_a_product(Session, product_id):
    session = Session()
    ratings = session.query(Rating).filter_by(product_id=product_id).all()
    session.close()
    return ratings, len(ratings)

def remove_rating(Session, product_id, user_id):
    session = Session()
    rating = session.query(Rating).filter_by(product_id=product_id, user_id=user_id).first()

    if rating:
        session.delete(rating)
        session.commit()
        session.close()
        return True  
    else:
        session.close()
        return False  
    
    

def create_review(Session, id, product_id, user_id, review_content):
    session = Session()
    if get_user(Session, user_id) and get_product(Session, product_id):
        review_objects = session.query(Review).all()
        for review_object in review_objects:
            if review_object.product_id == product_id and review_object.user_id == user_id:
                print("User already created review for this product")
                return False
            

        review_object = Review(id, product_id, user_id, review_content)
        session.merge(review_object)
        session.commit()
        session.close()
        return review_object
    
def format_review_dates(reviews):
    
    for review in reviews:
        date_object = datetime.strptime(str(review.date), '%Y-%m-%d %H:%M:%S.%f')
        formatted_date = date_object.strftime('%Y-%m-%d %H:%M')
        
        review.date = formatted_date
    
    return reviews
    
def get_reviews_of_a_product(Session, product_id):
    session = Session()
    reviews = session.query(Review).filter_by(product_id=product_id).all()
    session.close()
    reviews = format_review_dates(reviews)
    return reviews

def get_all_reviews(Session):
    session = Session()
    reviews = session.query(Review).all()
    session.close()
    return reviews



def remove_review(Session, review_id):
    session = Session()
    review = session.query(Review).filter_by(id=review_id).first()

    if review:
        session.delete(review)
        session.commit()
        session.close()
        return True  
    else:
        session.close()
        return False  

    





    

