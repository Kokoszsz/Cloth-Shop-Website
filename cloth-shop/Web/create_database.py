import json
import os
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLSession
from sqlalchemy.orm import sessionmaker

from config import DEFAULT_DATABASE_URL, PROJECT_ROOT
from models import Base, Product, Rating, User

DEFAULT_SEED_JSON = PROJECT_ROOT / 'Databases' / 'json' / 'data.json'


def database_url() -> str:
    return os.environ.get('DATABASE_URL') or DEFAULT_DATABASE_URL


def seed_json_path() -> str:
    return os.environ.get('SEED_JSON') or str(DEFAULT_SEED_JSON)


# Function to load data from a JSON file
def load_data_from_json(filename: str) -> dict[str, Any] | None:
    try:
        with open(filename) as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return None


def insert_data_to_database(Session: sessionmaker[SQLSession], seed_json: str) -> None:
    session = Session()


    loaded_data = load_data_from_json(seed_json)
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


def main() -> None:
    url = database_url()
    seed_json = seed_json_path()
    print(f'Seeding {url} from {seed_json}')
    engine = create_engine(url)
    Base.metadata.create_all(bind=engine)
    insert_data_to_database(sessionmaker(bind=engine), seed_json)


if __name__ == '__main__':
    main()
