from dboperations import add_customer, get_customer_by_phone, add_order, get_orders, update_order_status, get_all_orders, get_filtered_orders
from models import db, Customer, init_db, Order
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'secretkey'

db.init_app(app)
init_db(app)

# user information
phone = "0711475883"
# username = "Mrewwe"
# address = "6ds9 Jirewi Cfsfreascent Mufakose, Harare"
# surname = "Nyewakudyfdsa"
# name = "Mfdsweufaro"

# order information
# usage in a view function or script
# fruits_items = [
#     {"item_name": "Apples", "quantity": 3, "price": 1.50},
#     {"item_name": "Bananas", "quantity": 6, "price": 2.00}
# ]

# vegetables_items = [
#     {"item_name": "Carrots", "quantity": 2, "price": 1.20},
#     {"item_name": "Spinach", "quantity": 1, "price": 2.50}
# ]
# delivery_address = "69 Jiri Crescent Mufakose Harare"
# total_amount = 6.20


with app.app_context():
    # add_customer = add_customer(phone, username, address, surname, name, latitude=None, longitude=None)
    # customer = get_customer_by_phone(phone)
    # order = add_order(phone, delivery_address, total_amount, fruits_items, vegetables_items)
    order = get_orders(phone)
    update_order_status = update_order_status(4, "Packed")
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

    from flask import request

    @app.route("/dashboard")
    def index():
        # Get filter parameters from the query string
        order_status = request.args.get('order_status')
        customer_name = request.args.get('customer_name')
        order_id = request.args.get('order_id')
        customer_id = request.args.get('customer_id')
        
        # Fetch filtered orders based on the parameters, or all orders if no filters are applied
        if any([order_status, customer_name, order_id, customer_id]):
            orders = get_filtered_orders(order_status, customer_name, order_id, customer_id)
        else:
            orders = get_all_orders()

        # Render the dashboard template with the retrieved orders
        return render_template("dashboard.html", orders=orders)

        all_orders = get_all_orders()

        # for order in all_orders:
        #     customer = get_customer_by_id(order.customer_id)
        return render_template("dashboard.html", orders = all_orders)
        # return order.id


    @app.route("/update_order_status/<int:order_id>", methods=['POST'])
    def update_order_status(order_id):
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return jsonify({'error': 'No status provided'}), 400

        order = Order.query.get_or_404(order_id)
        order.status = status
        db.session.commit()
        
        return jsonify({'success': True})

    # def print_order(order):
    #     if order:
    #         for order in order:
                #  print(f"Order ID: {order.id}")
                #  print(f"Order Date: {order.order_date}")
                #  print(f"Status: {order.status}")
                #  print(f"Fruits: {order.get_fruits_items()}")
                #  print(f"Vegetables: {order.get_vegetables_items()}")
                #  print(f"Total Amount: {order.total_amount}")
                #  print(f"Delivery Address: {order.delivery_address}\n")
    #     else:
    #         print("No orders found for this phone number.")
    
    # print_order(order)

    # if update_order_status:
    #     print(f"Order status updated to: {update_order_status.status}")
    # else:
    #     print("Order status not updated.")

if __name__ == "__main__":
    app.run(debug=True)