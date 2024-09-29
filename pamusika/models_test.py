from dboperations import (
    add_customer,
    get_customer_by_phone,
    add_order,
    update_order_status,
    get_all_orders,
    get_filtered_orders,
    user_exists,
    delete_all_customers,
    query_orders,
    add_product,
    get_product_name_and_category,
    delete_all_orders,
    cancel_last_order_by_phone,
    get_active_orders_by_phone,
    delete_all_order_products,
)
from messages.app_logic_messages import (
    order_packed,
    packaging_received,
    sent_to_packaging,
)
from models import db, Customer, init_db, Order, order_products
from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
import json
from wa_cloud_py import whatsapp
from wa_cloud_py.message_components import ListSection, SectionRow, CatalogSection

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///musikadb.db"  # Use SQLite for simplicity
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secretkey"

db.init_app(app)

migrate = Migrate(app, db)
# user information

# Example data for the order
customer_id = 1
total_amount = 75.0
delivery_address = "123 Main St, Springfield"
fruits_items = [
    {"id": "apple", "quantity": 5, "price": 0.5},
    {"id": "banana", "quantity": 10, "price": 0.2},
]
vegetables_items = [
    {"id": "carrot", "quantity": 7, "price": 0.3},
    {"id": "broccoli", "quantity": 3, "price": 1.5},
]
product_quantities = [
    ("product_id_1", 2),
    ("product_id_2", 5),
]
category_id = "smdx1imjv1"
phone = "263776681617"


def delete_all_customers():
    try:
        # Query all customers
        customers = Customer.query.all()

        if customers:
            for customer in customers:
                db.session.delete(customer)

            # Commit the changes
            db.session.commit()
            print("All customers deleted successfully.")
        else:
            print("No customers found.")
    except Exception as e:
        # Rollback in case of any error
        db.session.rollback()
        print(f"Error deleting customers: {e}")


with app.app_context():
    # delete_all_customers()
    # cancel_last_order_by_phone(phone)
    # orders = get_active_orders_by_phone(phone)

    # print(f"orders type is {type(orders)}")  # Verify if orders are being retrieved correctly.

    # for order in orders :
    #     sent_to_packaging(whatsapp, phone, order, ListSection, SectionRow)

    # for order in orders :
    #     print(order.status)

    # cancel_last_order_by_phone(phone)
    # delete_last_order_by_phone(phone)
    # delete_all_order_products()
    # delete_all_orders()
    # name_category = get_product_name_and_category(category_id)
    # print(name_category.product_category)
    # Assuming the add_product function and
    #  Product model are already defined

# Adding multiple products to the database
#     products = [
#     {"id": "orange01", "meta_id": "smdx1imjv1", "name": "Orange🍊", "price": 0.25, "product_category": "Fruit"},
#     {"id": "pineapple01", "meta_id": "yv12oorgoj", "name": "Pineapple🍍", "price": 0.50, "product_category": "Fruit"},
#     {"id": "tomato01", "meta_id": "0oyglqcnhr", "name": "Tomato🍅", "price": 0.50, "product_category": "Vegetable"},
#     {"id": "carrot01", "meta_id": "aqs54sejq9", "name": "Carrot🥕", "price": 0.50, "product_category": "Vegetable"},
#     {"id": "rape01", "meta_id": "ixxuzk2ll2", "name": "Rape🥬", "price": 0.20, "product_category": "Vegetable"},
#     {"id": "cabbage01", "meta_id": "rq7l4wd0vr", "name": "Cabbage🥬", "price": 0.50, "product_category": "Vegetable"},
#     {"id": "banana01", "meta_id": "19tdnzbn2k", "name": "Banana🍌", "price": 0.10, "product_category": "Fruit"},
#     {"id": "covo01", "meta_id": "kaif9wtpmq", "name": "Covo🥦", "price": 0.20, "product_category": "Vegetable"},
#     {"id": "greenpepper01", "meta_id": "4jenulsjmg", "name": "Green Pepper🫑", "price": 0.20, "product_category": "Vegetable"},
#     {"id": "onion01", "meta_id": "p95w970hrf", "name": "Onion🧅", "price": 0.50, "product_category": "Vegetable"},
# ]


#     for product in products:
#         add_product(
#             id=product["id"],
#             meta_id=product["meta_id"],
#             name=product["name"],
#             price=product["price"],
#             product_category=product["product_category"]  # Pass the category to the function
#         )
#         print(f"Added product: {product['name']} - Category: {product['product_category']}")


# new_order = add_order(
# db=db,
# customer_id=customer_id,
# total_amount=total_amount,
# delivery_address=delivery_address,
# fruits_items=fruits_items,
# vegetables_items=vegetables_items,
# product_quantities=product_quantities
# )
# if new_order:
#     print(f"Order created with ID: {customer_id}")

# orders = query_orders(customer_id=1, status="Sent to Packaging")
# for order in orders:
#     fruits_items_json = order.fruits_items
#     fruits_items = json.loads(fruits_items_json)
#     for item in fruits_items:
#         product_id = item['id']
#         quantity = item['quantity']
#         price = item['price']
#     print(f"{order} {order.total_amount}")

# delete_all_customers()
# user_exist = get_customer_by_phone(phone)
# print(f"Does the user with phone number {user_exist.phone} and name {user_exist.name} exist? {'Yes' if user_exist else 'No'}")


# add_customer = add_customer(phone, username, address, surname, name, latitude=None, longitude=None)
# customer = get_customer_by_phone(phone)
# order = add_order(phone, delivery_address, total_amount, fruits_items, vegetables_items)
# all_orders = get_all_orders()
# order = get_orders(phone)
# if all_orders :
#     for order in all_orders:
#         customer_id = order.customer_id
#         order_status = order.status
#     print (f"order found for {phone}")
# else:
#     print("order not found")
# update_order_status = update_order_status(4, "Packed")
# if customer:
#     """ if the customer is registered,return a greeting and the start of the conversational flow

#     return :

#     """
#     print(f"Customer Found: {customer.name} {customer.surname}, Username: {customer.username}")
# else:
#     """ handle the case where the customer is not registerd
#     notify the user to add their information and register
#     """
#     print("Customer not found.")

# if add_customer:
#     print(f"Customer Added: {add_customer.name} {add_customer.surname}, Username: {add_customer.username}")
# else:
#     print("Customer not added.")

#     from flask import request

#     @app.route("/dashboard")
#     def index():
#         # Get filter parameters from the query string
#         order_status = request.args.get('order_status')
#         customer_name = request.args.get('customer_name')
#         order_id = request.args.get('order_id')
#         customer_id = request.args.get('customer_id')

#         # Fetch filtered orders based on the parameters, or all orders if no filters are applied
#         if any([order_status, customer_name, order_id, customer_id]):
#             orders = get_filtered_orders(order_status, customer_name, order_id, customer_id)
#         else:
#             orders = get_all_orders()

#         # Render the dashboard template with the retrieved orders
#         return render_template("dashboard.html", orders=orders)

#         all_orders = get_all_orders()

#         # for order in all_orders:
#         #     customer = get_customer_by_id(order.customer_id)
#         return render_template("dashboard.html", orders = all_orders)
#         # return order.id


#     @app.route("/update_order_status/<int:order_id>", methods=['POST'])
#     def update_order_status(order_id):
#         data = request.get_json()
#         status = data.get('status')

#         if not status:
#             return jsonify({'error': 'No status provided'}), 400

#         order = Order.query.get_or_404(order_id)
#         order.status = status
#         db.session.commit()

#         return jsonify({'success': True})

#     # def print_order(order):
#     #     if order:
#     #         for order in order:
#                 #  print(f"Order ID: {order.id}")
#                 #  print(f"Order Date: {order.order_date}")
#                 #  print(f"Status: {order.status}")
#                 #  print(f"Fruits: {order.get_fruits_items()}")
#                 #  print(f"Vegetables: {order.get_vegetables_items()}")
#                 #  print(f"Total Amount: {order.total_amount}")
#                 #  print(f"Delivery Address: {order.delivery_address}\n")
#     #     else:
#     #         print("No orders found for this phone number.")

#     # print_order(order)

#     # if update_order_status:
#     #     print(f"Order status updated to: {update_order_status.status}")
#     # else:
#     #     print("Order status not updated.")

# if __name__ == "__main__":
#     app.run(debug=True)
