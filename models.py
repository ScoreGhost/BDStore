# This file contains the SQLAlchemy models for the Flask API.

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship
import datetime

db = declarative_base()

class User(db):
    """
    Represents a user in the database.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return f"<User(name={self.name}, fullname={self.fullname}, nickname={self.nickname})>"

class Address(db):
    """
    Represents an address in the database.
    """
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)

    # Foreign key to the User table
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="addresses")

    def __repr__(self):
        return f"<Address(email_address={self.email_address})>"

class Product(db):
    """
    Represents the products in the database.
    """
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(String)
    description = Column(String)
    stock = Column(Integer)
    lenght = Column(Integer)
    color = Column(String)

    def __repr__(self):
        return f"<User(name={self.name},price={self.price},description={self.description},stock={self.stock},lenght={self.lenght},color={self.color} ,)>"
    
class Cart(db):
    """
    Represents the cart of the buyer in the database.
    """
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    creation_date = Column(Date, default=datetime.datetime.utcnow)  # Automatically set the creation date

    def __repr__(self):
        return f"<Cart(creation_date={self.creation_date}, relation_cart_item={self.relation_cart_item})>"
    
class CartItem(db):
    """
    Represents the CartItems of the buyer in the database.
    """
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)

    cart_id = Column(Integer, ForeignKey("cart.id"))
    cart = relationship(Cart, backref="cart_items")

    products_id = Column(Integer, ForeignKey("products.id"))
    products = relationship(Product)

    def __repr__(self):
        return f"<CartItem(relation_cart={self.relation_cart}, relation_product={self.relation_product}, quantity={self.quantity})>"    
    
class Order(db):
    """
    Represents the Order of the buyer in the database.
    """
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    creation_date = Column(Date, default=datetime.datetime.utcnow)
    total_ammount = Column(Integer)
    status = Column(String)
    client_info = Column(String)
    
    def __repr__(self):
        return f"<Order(creation_date={self.creation_date},total_ammount={self.total_ammount},status={self.status},client_info={self.client_info},relation_info{self.relation_info})>"

class OrderItem(db):
    """
    Represents the Order Items of the buyer in the database.
    """
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    price = Column(Integer)

    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship(Order, backref="order_items")

    products_id = Column(Integer, ForeignKey("products.id"))
    products = relationship(Product)

    def __repr__(self):
        return f"<Order(relation_order={self.relation_order},relation_product={self.relation_product},quantity={self.quantity},price={self.price})>"

if __name__ == "__main__":
    dildo_mario = Product(name="MarioPP",price=100, description="Plumbers best PP for your pleasure", stock=20,lenght=16, color="red and blue")


    