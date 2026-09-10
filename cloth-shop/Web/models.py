import datetime
from typing import Any

from sqlalchemy import Column, DateTime, Float, Index, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = "accounts"
    __table_args__ = (
        Index('uq_accounts_name', 'name', unique=True),
        Index('uq_accounts_email', 'email', unique=True),
    )

    id = Column('id', Integer, primary_key = True)
    name = Column('name', String)
    password_hash = Column('password', String(256))
    email = Column('email', String)
    surname = Column('surname', String)
    phone = Column('phone', String)
    country = Column('country', String)
    city = Column('city', String)

    def __init__(
        self,
        name: str,
        password: str,
        email: str,
        surname: str = "",
        phone: str = "",
        country: str = "",
        city: str = "",
        id: int | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.set_password(password)
        self.email = email
        self.surname = surname
        self.phone = phone
        self.country = country
        self.city = city

    def set_password(self, password: str) -> None:
        """Hash and store the given plaintext password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Return True if the given plaintext password matches the stored hash."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'surname': self.surname,
            'phone': self.phone,
            'country': self.country,
            'city': self.city
        }

    def __repr__(self) -> str:
        return f"({self.id}), ({self.name}), ({self.email}), ({self.surname})"


class Product(Base):
    __tablename__ = "products"

    id = Column('id', Integer, primary_key = True)
    name = Column('name', String)
    cost = Column('cost', Float)
    cloth_cathegory = Column('cloth_cathegory', String)
    gender = Column('gender', String)
    image = Column('image', String)

    def __init__(
        self,
        id: int,
        name: str,
        cost: float,
        cloth_cathegory: str,
        gender: str,
        image: str,
    ) -> None:
        self.id = id
        self.name= name
        self.cost = cost
        self.cloth_cathegory = cloth_cathegory
        self.gender = gender
        self.image = image
        self.url = self.to_url()

    def to_url(self) -> str:
        return self.name.replace(' ', '-')

    def __repr__(self) -> str:
        return f"({self.id})"


class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (
        Index('uq_ratings_product_user', 'product_id', 'user_id', unique=True),
    )

    id = Column('id', Integer, primary_key=True)
    product_id = Column('product_id', Integer)
    user_id = Column('user_id', Integer)
    rating_points = Column('rating_points', Float)

    def __init__(
        self,
        product_id: int,
        user_id: int,
        rating_points: float,
        id: int | None = None,
    ) -> None:
        self.id = id
        self.product_id = product_id
        self.user_id = user_id
        self.rating_points = rating_points

    @validates('rating_points')
    def validate_rating(self, key: str, value: float) -> float:
        if not 1 <= value <= 5:
            raise ValueError("Rating must be between 1 and 5 (inclusive)")
        return value


    def __repr__(self) -> str:
        return (
            f"id ({self.id}), product id({self.product_id}), "
            f"user id({self.user_id}), rating points ({self.rating_points})"
        )


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        Index('uq_reviews_product_user', 'product_id', 'user_id', unique=True),
    )

    id = Column('id', Integer, primary_key=True)
    product_id = Column('product_id', Integer)
    user_id = Column('user_id', Integer)
    content = Column('content', String)
    date = Column('date', DateTime, default=datetime.datetime.utcnow)

    def __init__(
        self,
        product_id: int,
        user_id: int,
        content: str,
        id: int | None = None,
    ) -> None:
        self.id = id
        self.product_id = product_id
        self.user_id = user_id
        self.content = content

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'content': self.content,
            'date': self.date
        }


    def __repr__(self) -> str:
        return (
            f"id ({self.id}), product id({self.product_id}), user id({self.user_id}), "
            f"review content ({self.content}), review date ({self.date})"
        )
