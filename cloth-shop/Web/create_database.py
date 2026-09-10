import json
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLSession
from sqlalchemy.orm import sessionmaker

from models import Base, Product, Rating, User

engine = create_engine("sqlite:///cloth-shop/Databases/mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)


# Function to load data from a JSON file
def load_data_from_json(filename: str) -> dict[str, Any] | None:
    try:
        with open(filename) as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return None


def insert_data_to_database(Session: sessionmaker[SQLSession]) -> None:
    session = Session()


    loaded_data = load_data_from_json('cloth-shop/Databases/json/data.json')
    if loaded_data:
        users_data = loaded_data.get("users", [])
        products_data = loaded_data.get("products", [])
        rating_data = loaded_data.get("ratings", [])


    for user in users_data:
        user_obj = User(*user[1:], id=user[0])
        session.add(user_obj)

    for product in products_data:
        product_obj = Product(*product)
        session.add(product_obj)

    for rating in rating_data:
        product_obj = Rating(*rating[1:], id=rating[0])
        session.add(product_obj)


    session.commit()
    session.close()

insert_data_to_database(Session)
