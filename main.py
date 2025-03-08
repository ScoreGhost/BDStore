# This file contains the main application code for the Flask API.

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from models import db, User, Address,Product

from flask import Flask, request, jsonify
from addreses import address_api
from session import session

# Create a new Flask application
api = Flask(__name__)
# Register the address_api blueprint
api.register_blueprint(address_api)


@api.route("/users", methods=["GET"])
def get_users():
    """
    Retrieve all users from the database and return them in JSON format.
    """
    users = session.query(User).all()

    usuarios_en_formato_diccionario = []

    for user in users:
        user_dict = {
            "id": user.id,
            "name": user.name,
            "fullname": user.fullname,
            "nickname": user.nickname,
        }
        usuarios_en_formato_diccionario.append(user_dict)

    return jsonify(usuarios_en_formato_diccionario)

@api.route("/users", methods=["POST"])
def create_user():
    """
    Create a new user in the database with the provided data.
    """
    data = request.get_json()
    new_user = User(name=data["name"], fullname=data["fullname"], nickname=data["nickname"])
    session.add(new_user)
    session.commit()
    return jsonify({"message": "User created successfully"}), 201

@api.route("/products", methods=["POST"])
def create_products():
    """
    Create a new products in the database with the provided data.
    """
    data = request.get_json()
    new_product = Product(name=data["name"], price=data["price"], description=data["description"], stock=data["stock"], lenght=data["lenght"], color=data["color"])
    session.add(new_product)
    session.commit()
    return jsonify({"message": "Product created successfully"}), 201

@api.route("/products", methods=["GET"])
def get_products():
    """
    Retrieve all products from the database and return them in JSON format.
    """
    products = session.query(Product).all()

    productos_en_formato_diccionario = []

    for product in products:
        product_dict = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "stock": product.stock,
            "lenght": product.lenght,
            "color": product.color,
        }
        productos_en_formato_diccionario.append(product_dict)

    return jsonify(productos_en_formato_diccionario)

if __name__ == "__main__":
    api.run(port=5000, debug=True)
