from contextlib import contextmanager
from typing import Any, Iterator
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker
from datetime import datetime
from models import User, Product, Rating, Review ,Base
from exceptions import DuplicateReview, DuplicateUser, ProductNotFound, UserNotFound

SessionFactory = sessionmaker[Session]
ProductDict = dict[str, Any]


UNIQUE_INDEXES = (
    'CREATE UNIQUE INDEX IF NOT EXISTS uq_accounts_name ON accounts (name)',
    'CREATE UNIQUE INDEX IF NOT EXISTS uq_accounts_email ON accounts (email)',
    'CREATE UNIQUE INDEX IF NOT EXISTS uq_ratings_product_user ON ratings (product_id, user_id)',
    'CREATE UNIQUE INDEX IF NOT EXISTS uq_reviews_product_user ON reviews (product_id, user_id)',
)


def create_database_Session(url: str, echo: bool = False) -> SessionFactory:
    engine = create_engine(url, echo=echo)
    Base.metadata.create_all(bind=engine)
    with engine.begin() as connection:
        for statement in UNIQUE_INDEXES:
            connection.execute(text(statement))
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    return Session


@contextmanager
def session_scope(Session: SessionFactory) -> Iterator[Session]:
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_user(Session: SessionFactory, name: str, password: str, email: str) -> User:
    with session_scope(Session) as session:
        user = User(name=name, password=password, email=email)
        session.add(user)
        try:
            session.flush()
        except IntegrityError as exc:
            session.rollback()
            raise DuplicateUser(name, email) from exc
    return user

def update_user(
    Session: SessionFactory,
    id: int,
    name: str,
    password: str,
    email: str,
    users: list[User],
    surname: str = "",
    phone_number: str = "",
    country: str = "",
    city: str = "",
) -> User:
    user = next((user for user in users if user.id == id), None)
    if user is None:
        raise UserNotFound(id)

    user.name = name
    user.set_password(password)
    user.email = email
    user.surname = surname
    user.phone = phone_number
    user.country = country
    user.city = city
    with session_scope(Session) as session:
        session.merge(user)
    return user


def get_users(Session: SessionFactory) -> list[User]:
    with session_scope(Session) as session:
        return session.query(User).all()


def get_user(Session: SessionFactory, user_id: int) -> User | None:
    with session_scope(Session) as session:
        return session.query(User).filter(User.id == user_id).first()
    


def get_products_to_dict(Session: SessionFactory) -> list[ProductDict]:
    with session_scope(Session) as session:
        results = session.query(Product).all()
        return [{'id': r.id, 'name': r.name, 'cost': r.cost, 'cloth_cathegory': r.cloth_cathegory,
                 'gender': r.gender, 'image': r.image, 'url': r.to_url()} for r in results]

def get_product(Session: SessionFactory, product_id: int) -> Product | None:
    with session_scope(Session) as session:
        return session.query(Product).filter(Product.id == product_id).first()


def modify_rating(session: Session, rating_obj: Rating, rating_points: float) -> Rating:
    rating_obj.rating_points = rating_points
    session.merge(rating_obj)
    session.commit()
    return rating_obj


def create_rating(
    Session: SessionFactory,
    product_id: int,
    user_id: int,
    new_rating_points: float,
) -> Rating:
    with session_scope(Session) as session:
        if not session.get(User, user_id):
            raise UserNotFound(user_id)
        if not session.get(Product, product_id):
            raise ProductNotFound(product_id)

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


def get_ratings(Session: SessionFactory) -> list[Rating]:
    with session_scope(Session) as session:
        return session.query(Rating).all()

def get_certain_rating(Session: SessionFactory, product_id: int, user_id: int) -> Rating | None:
    with session_scope(Session) as session:
        return session.query(Rating).filter_by(product_id=product_id, user_id=user_id).first()

def get_all_ratings_of_a_product(Session: SessionFactory, product_id: int) -> tuple[list[Rating], int]:
    with session_scope(Session) as session:
        ratings = session.query(Rating).filter_by(product_id=product_id).all()
        return ratings, len(ratings)

def remove_rating(Session: SessionFactory, product_id: int, user_id: int) -> bool:
    with session_scope(Session) as session:
        rating = session.query(Rating).filter_by(product_id=product_id, user_id=user_id).first()
        if rating is None:
            return False

        session.delete(rating)
        return True
    
    

def create_review(
    Session: SessionFactory,
    product_id: int,
    user_id: int,
    review_content: str,
) -> Review:
    with session_scope(Session) as session:
        if not session.get(User, user_id):
            raise UserNotFound(user_id)
        if not session.get(Product, product_id):
            raise ProductNotFound(product_id)

        review_object = Review(product_id=product_id, user_id=user_id, content=review_content)
        session.add(review_object)
        try:
            session.flush()
        except IntegrityError as exc:
            session.rollback()
            raise DuplicateReview(product_id, user_id) from exc
        return review_object
    
def format_review_dates(reviews: list[Review]) -> list[Review]:
    
    for review in reviews:
        date_object = datetime.strptime(str(review.date), '%Y-%m-%d %H:%M:%S.%f')
        formatted_date = date_object.strftime('%Y-%m-%d %H:%M')
        
        review.date = formatted_date
    
    return reviews
    
def get_reviews_of_a_product(Session: SessionFactory, product_id: int) -> list[Review]:
    with session_scope(Session) as session:
        reviews = session.query(Review).filter_by(product_id=product_id).all()
    return format_review_dates(reviews)

def get_all_reviews(Session: SessionFactory) -> list[Review]:
    with session_scope(Session) as session:
        return session.query(Review).all()



def remove_review(Session: SessionFactory, review_id: int, user_id: int) -> bool:
    with session_scope(Session) as session:
        review = session.query(Review).filter_by(id=review_id, user_id=user_id).first()
        if review is None:
            return False

        session.delete(review)
        return True

    





    

