from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Product, Base



engine = create_engine("sqlite:///Cloth Shop Website/Databases/mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

def insert_data_to_database(Session):
    session = Session()





    users_data = [
        (1, "test", "123", "test123@gmail.com"),
        (2, "pigir", "12313", "pigir@gmail.com"),
        (3, "test123", "test123", "test123@tets123.com")
    ]

    products_data = [
        (1, "Great T-shirt", "34", "t_shirt", "male", "grey_t_shirt.jpg"),
        (2, "Brown T-Shirt", "54", "t_shirt", "male", "borwn_t_shirt.png"),
        (3, "Red T-shirt", "37", "t_shirt", "male", "another_red_t_shirt.jpg"),
        (4, "Red T-shirt Extra", "69.99", "t_shirt", "male", "red_t_shirt.png"),
        (5, "Black Shirt", "56.99", "shirt", "female", "black_shirt.png"),
        (6, "Pink Shirt", "49.99", "shirt", "female", "pink_blouse.png"),
        (7, "Standard Jeans", "59.99", "jeans", "female", "jeans.jpg"),
        (8, "Jeans Extra", "79.99", "jeans", "female", "a_few_jeans.jpeg"),
        (9, "Male Jeans", "56.99", "jeans", "male", "more_jeans.jpg")
    ]

    for user in users_data:
        user_obj = User(*user)
        session.add(user_obj)

    for product in products_data:
        product_obj = Product(*product)
        session.add(product_obj)


    session.commit()
    session.close()

insert_data_to_database(Session)