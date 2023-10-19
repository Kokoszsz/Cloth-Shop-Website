from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Product, Rating, Base
import json



engine = create_engine("sqlite:///Cloth Shop Website/Databases/mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)


# Function to load data from a JSON file
def load_data_from_json(filename):
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return None
    

def insert_data_to_database(Session):
    session = Session()


    loaded_data = load_data_from_json('Cloth Shop Website/Databases/json/data.json')
    if loaded_data:
        users_data = loaded_data.get("users", [])
        products_data = loaded_data.get("products", [])
        rating_data = loaded_data.get("ratings", [])


    for user in users_data:
        user_obj = User(*user)
        session.add(user_obj)

    for product in products_data:
        product_obj = Product(*product)
        session.add(product_obj)

    for rating in rating_data:
        product_obj = Rating(*rating)
        session.add(product_obj)


    session.commit()
    session.close()

insert_data_to_database(Session)