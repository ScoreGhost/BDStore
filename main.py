# This file contains the main application code for the Flask API.

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Cart, db, User, Address, Product, CartItem, Order

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

@api.route("/carts", methods=["GET"])
def get_carts():
    """
    Retrieve all carts from the database and return them in JSON format.
    """
    carts = session.query(Cart).all()

    carritos_en_formato_diccionario = []

    for cart in carts:
        cart_dict = {
            "id": cart.id,
            "creationdate": cart.creation_date,
        }
        carritos_en_formato_diccionario.append(cart_dict)

    return jsonify(carritos_en_formato_diccionario)

@api.route("/carts/<int:id>", methods=["DELETE"])
def delete_carts(id):
    """
    Delete a new carts in the database with the provided data.
    """
    search_cart = session.query(Cart).get(id)
    session.delete(search_cart)
    session.commit()
    return jsonify({"message": "Cart deleted successfully"}), 201


@api.route("/carts/<int:id>", methods=["GET"])
def get_carts_by(id):
    """
    Get a new carts ID in the database with the provided data.
    """
    search_cart = session.query(Cart).get(id)
    
    return jsonify(search_cart.serialize()), 200

@api.route("/carts/<int:id>/items", methods=["POST"])
def add_carts_item(id):
    """
    Adds items to carts in the database with the provided data.
    """
    search_cart = session.query(Cart).get(id)
    data = request.get_json()
    product_id = data.get("product_id")
    search_product = session.query(Product).get(product_id)
    quantity = data.get("quantity")
    new_cart_item = CartItem(quantity=quantity,cart=search_cart,products=search_product)
    session.add(new_cart_item)
    session.commit()
    return jsonify({"message": "Cart has items added successfully"}), 201


@api.route("/carts/<int:id>/items/<int:item_id>", methods=["DELETE"])
def delete_carts_items_by(id,item_id):
    """
    Delete a carts items in the database with the provided data.
    """
    search_cart_item = session.query(CartItem).get(item_id)
    session.delete(search_cart_item)
    session.commit()
    return jsonify({"message": "Cart item deleted successfully"}), 201

@api.route("/carts", methods=["POST"])
def create_cart():
    """
    Create a new products in the database with the provided data.
    """
    data = request.get_json()
    new_cart = Cart()
    session.add(new_cart)
    session.commit()
    return jsonify({"message": "Cart created successfully"}), 201

@api.route("/orders", methods=["POST"])
def create_orders():
    """
    Create a new orders in the database with the provided data.
    """
    data = request.get_json()
    cart_id = data.get("cart_id")
    search_cart = session.query(Cart).get(cart_id)
    total = search_cart.gettotal()
    new_order = Order(total_ammount=total, status="pending", client_info="Lucho")
    session.add(new_order)
    session.commit()
    return jsonify({"message": "Order created successfully"}), 201

@api.route("/orders", methods=["GET"])
def get_orders():
    """
    Retrieve all orders from the database and return them in JSON format.
    """
    orders = session.query(Order).all()

    ordenes_en_formato_diccionario = []

    for order in orders:
        order_dict = {
            "id": order.id,
            "client_info": order.client_info,
            "total_ammount": order.total_ammount
            
        }
        ordenes_en_formato_diccionario.append(order_dict)

    return jsonify(ordenes_en_formato_diccionario)

@api.route("/orders/<int:id>", methods=["GET"])
def search_single_order_by_(id):
    """
   Search an existing order in the database with the provided data.
    """
    # Step 1: Get the order to update
    order = session.query(Order).get(id)

    # Step 2: Check if the order exists
    if not order:
        return jsonify({"message": "Order not found"}), 404
    
    order_dict = {
            "id": order.id,
            "client_info": order.client_info,
            "total_ammount": order.total_ammount,
            "status": order.status
        }

    return jsonify(order_dict)

@api.route("/orders/<int:id>", methods=["PUT"])
def update_order(id):
    """
    Update an existing order in the database with the provided data.
    """
    # Step 1: Get the order to update
    order_to_update = session.query(Order).get(id)

    # Step 2: Check if the order exists
    if not order_to_update:
        return jsonify({"message": "Order not found"}), 404

    # Step 3: Get the updated data from the request
    data = request.get_json()

    # Step 4: Update the product fields
    if "status" in data:
        order_to_update.status = data["status"]
    

    # Step 5: Commit the changes to the database
    session.commit()

    # Step 6: Return a success message
    return jsonify({"message": "order updated successfully"}), 200




@api.route("/products/<int:id>", methods=["DELETE"])
def delete_products(id):
    """
    Delete a new products in the database with the provided data.
    """
    search_product = session.query(Product).get(id)
    session.delete(search_product)
    session.commit()
    return jsonify({"message": "Product deleted successfully"}), 201

@api.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    """
    Update an existing product in the database with the provided data.
    """
    # Step 1: Get the product to update
    product_to_update = session.query(Product).get(id)

    # Step 2: Check if the product exists
    if not product_to_update:
        return jsonify({"message": "Product not found"}), 404

    # Step 3: Get the updated data from the request
    data = request.get_json()

    # Step 4: Update the product fields
    if "name" in data:
        product_to_update.name = data["name"]
    if "price" in data:
        product_to_update.price = data["price"]
    if "description" in data:
        product_to_update.description = data["description"]
    if "stock" in data:
        product_to_update.stock = data["stock"]
    if "lenght" in data:
        product_to_update.lenght = data["lenght"]
    if "color" in data:
        product_to_update.color = data["color"]

    # Step 5: Commit the changes to the database
    session.commit()

    # Step 6: Return a success message
    return jsonify({"message": "Product updated successfully"}), 200

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

@api.route("/products/<int:id>", methods=["GET"])
def search_single_product_by_(id):
    """
   Search an existing product in the database with the provided data.
    """
    # Step 1: Get the product to update
    product = session.query(Product).get(id)

    # Step 2: Check if the product exists
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    product_dict = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "stock": product.stock,
            "lenght": product.lenght,
            "color": product.color,
        }

    return jsonify(product_dict)



if __name__ == "__main__":
    api.run(port=5000, debug=True)
