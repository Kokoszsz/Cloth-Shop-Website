from database import User

def insert_data(Session):
    session = Session()

    users_data = [
        (1, "test", "123", "test123@gmail.com"),
        (2, "pigir", "12313", "pigir@gmail.com"),
        (3, "test123", "test123", "test123@tets123.com")
    ]



    for user in users_data:
        user_obj = User(*user)
        session.add(user_obj)

    session.commit()

    session.close()