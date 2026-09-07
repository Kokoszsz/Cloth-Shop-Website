from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import User, Product, Rating, Review ,Base


UNIQUE_INDEXES = (
    'CREATE UNIQUE INDEX IF NOT EXISTS uq_accounts_name ON accounts (name)',
    'CREATE UNIQUE INDEX IF NOT EXISTS uq_accounts_email ON accounts (email)',
    'CREATE UNIQUE INDEX IF NOT EXISTS uq_ratings_product_user ON ratings (product_id, user_id)',
    'CREATE UNIQUE INDEX IF NOT EXISTS uq_reviews_product_user ON reviews (product_id, user_id)',
)


def create_database_Session(url):
    engine = create_engine(url, echo=True)
    Base.metadata.create_all(bind=engine)
    with engine.begin() as connection:
        for statement in UNIQUE_INDEXES:
            connection.execute(text(statement))
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    return Session


@contextmanager
def session_scope(Session):
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_user(Session, name, password, email):
    with session_scope(Session) as session:
        user = User(name=name, password=password, email=email)
        session.add(user)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            return None
    return user

def update_user(Session, id, name, password, email, users, surname="", phone_number="", country="", city=""):
    session = Session()
    user = next((user for user in users if user.id == id), None)
    if user is not None:
        user.name = name
        user.set_password(password)
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
    users = session.query(User).all()
    session.close()
    return users


def get_user(Session, user_id):
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()
    return user
    


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


def create_rating(Session, product_id, user_id, new_rating_points):
    with session_scope(Session) as session:
        if not session.get(User, user_id) or not session.get(Product, product_id):
            return 'Could not find this product or this user'

        rating_obj = session.query(Rating).filter_by(product_id=product_id, user_id=user_id).first()
        if rating_obj is None:
            rating_obj = Rating(product_id=product_id, user_id=user_id, rating_points=new_rating_points)
            session.add(rating_obj)
            try:
                session.flush()
                return rating_obj
            except IntegrityError:
                session.rollback()
                rating_obj = session.query(Rating).filter_by(product_id=product_id, user_id=user_id).one()

        rating_obj.rating_points = new_rating_points
        session.flush()
        return rating_obj


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
    
    

def create_review(Session, product_id, user_id, review_content):
    with session_scope(Session) as session:
        if not session.get(User, user_id) or not session.get(Product, product_id):
            return None

        review_object = Review(product_id=product_id, user_id=user_id, content=review_content)
        session.add(review_object)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            return False
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



def remove_review(Session, review_id, user_id):
    session = Session()
    review = session.query(Review).filter_by(id=review_id, user_id=user_id).first()

    if review:
        session.delete(review)
        session.commit()
        session.close()
        return True  
    else:
        session.close()
        return False  

    





    

