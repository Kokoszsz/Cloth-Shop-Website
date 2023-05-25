from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Product, Base



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

def update_user(Session, id, name, password, email, users):
    session = Session()
    user = next((user for user in users if user.id == id), None)
    if user != None:
        user.name = name
        user.password = password
        user.email = email
        session.merge(user)
        session.commit()
        session.close()
    return user


def get_users(Session):
    session = Session()
    results = session.query(User.id, User.name, User.password, User.email).all()
    users = [User(*r) for r in results]
    session.close()
    return users

def get_products_to_dict(Session):
    session = Session()
    results = session.query(Product.id, Product.name, Product.cost, Product.cloth_cathegory, Product.gender, Product.image).all()
    products = [Product(*r).to_dict() for r in results]
    session.close()
    return products



    

