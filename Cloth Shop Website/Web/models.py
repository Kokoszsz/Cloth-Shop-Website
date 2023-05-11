from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "accounts"

    id = Column('id', Integer, primary_key = True)
    name = Column('name', String)
    password = Column('password', String)
    email = Column('email', String)

    def __init__(self, id, name, password, email):
        self.id = id
        self.name= name
        self.password = password
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'email': self.email
        }

    def __repr__(self):
        return f"({self.id}), ({self.name}), ({self.password}), ({self.email})"
        
    
class Product(Base):
    __tablename__ = "products"

    id = Column('id', Integer, primary_key = True)
    name = Column('name', String)
    cost_to_show = Column('cost', String)
    cloth_cathegory = Column('cloth_cathegory', String)
    gender = Column('gender', String)
    image = Column('image', String)

    def __init__(self, id, name, cost_to_show, cloth_cathegory, gender, image):
        self.id = id
        self.name= name
        self.cost_to_show = cost_to_show
        self.cost = float(cost_to_show)
        self.cloth_cathegory = cloth_cathegory
        self.gender = gender
        self.image = image

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cost_to_show': self.cost_to_show,
            'cloth_cathegory': self.cloth_cathegory,
            'gender': self.gender,
            'image': self.image
        }

    def __repr__(self):
        return f"({self.id})"
    