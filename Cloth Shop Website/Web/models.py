from typing import Any
from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "accounts"

    id = Column('id', Integer, primary_key = True)
    name = Column('name', String)
    password = Column('password', String)
    email = Column('email', String)

    def __init__(self, id, name, password, email, surname=None, phone=None, country=None, city=None):
        self.id = id
        self.name= name
        self.password = password
        self.email = email
        self.surname = surname
        self.phone = phone
        self.country = country
        self.city = city

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'email': self.email,
            'surname': self.surname,
            'phone': self.phone,
            'country': self.country,
            'city': self.city
        }

    def __repr__(self):
        return f"({self.id}), ({self.name}), ({self.password}), ({self.email})"
        
    
class Product(Base):
    __tablename__ = "products"

    id = Column('id', Integer, primary_key = True)
    name = Column('name', String)
    cost = Column('cost', Float)
    cloth_cathegory = Column('cloth_cathegory', String)
    gender = Column('gender', String)
    image = Column('image', String)

    def __init__(self, id, name, cost, cloth_cathegory, gender, image):
        self.id = id
        self.name= name
        self.cost = cost
        self.cloth_cathegory = cloth_cathegory
        self.gender = gender
        self.image = image
        self.url = self.to_url()

    def to_url(self):
        return self.name.replace(' ', '-')

    def __repr__(self):
        return f"({self.id})"
    

class Rating(Base):
    __tablename__ = "ratings"

    id = Column('id', Integer, primary_key=True)
    product_id = Column('product_id', Integer)
    user_id = Column('user_id', Integer)
    rating_points = Column('rating_points', Float)

    def __init__(self, id, product_id, user_id, rating_points) -> None:
        self.id = id
        self.product_id = product_id
        self.user_id = user_id
        self.rating_points = rating_points

    def __post_init__(self):
        self.validate_rating()

    def validate_rating(self):
        if not 1 <= self.rating_points <= 5:
            raise ValueError("Rating must be between 1 and 5 (inclusive)")
        

    def __repr__(self):
        return f"id ({self.id}), product id({self.product_id}), user id({self.user_id}), rating points ({self.rating_points})"
    

class Review(Base):
    __tablename__ = "reviews"

    id = Column('id', Integer, primary_key=True)
    product_id = Column('product_id', Integer)
    user_id = Column('user_id', Integer)
    content = Column('content', String)
    date = Column('date', DateTime, default=datetime.datetime.utcnow)

    def __init__(self, id, product_id, user_id, content) -> None:
        self.id = id
        self.product_id = product_id
        self.user_id = user_id
        self.content = content
 
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'content': self.content,
            'date': self.date
        }
        

    def __repr__(self):
        return f"id ({self.id}), product id({self.product_id}), user id({self.user_id}), review content ({self.content}), review date ({self.date})"
