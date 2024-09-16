from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask.views import MethodView
from wa_cloud_py import WhatsApp
from wa_cloud_py.messages.types import MessageStatus, UserMessage, TextMessage, OrderMessage, InteractiveListMessage
# from wa_cloud_py.message_types import MessageStatus, UserMessage, TextMessage, OrderMessage, InteractiveListMessage
from dotenv import load_dotenv
import os
from dboperations import add_customer, get_customer_by_phone, add_order, update_order_status, get_all_orders, get_filtered_orders, user_exists, add_customer_with_phone, update_customer_name, update_customer_username, update_customer_address, get_products, get_product_name_and_category, cancel_last_order_by_phone, get_active_orders_by_phone, update_last_order_status_to_sent
from models import db, Customer, init_db, Order, db_session
from messages.app_logic_messages import greet_user_and_select_option, send_catalog, confirm_order, order_confirmed, make_changes, handle_cancellation, sent_to_packaging, packaging_received, order_packed, order_on_way, order_delivered, no_orders, tracking_issue, invalid_option, select_correct_option, request_user_name, request_address, notify_user_about_support_model, confirm_user_details, registration_successful, send_user_profile, order_cancelled, notify_unavailable_service, notify_address_suggestion, order_amount_restriction
# from wa_cloud_py.message_components import ListSection, SectionRow, CatalogSection
from wa_cloud_py.components.messages import ListSection, SectionRow, CatalogSection
from flask_migrate import Migrate
from flask import flash, url_for, redirect
from location_restriction import validate_address
from functools import wraps
from datetime import timedelta
from flask_socketio import SocketIO, emit

load_dotenv()
wa_access_token = os.getenv("WA_TOKEN")
phone_id = os.getenv("PHONE_ID")
verify_token = os.getenv("VERIFY_TOKEN")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mumsikadatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secretkey'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=12)
socketio = SocketIO(app)

migrate = Migrate(app, db)
db.init_app(app)
init_db(app)
catalog_id = "253006871078558"

valid_username = 'admin'
valid_password = 'password'

def login_required(f):
    """A decorator to protect routes that require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Please log in to access this page.", 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == valid_username and password == valid_password:
            session.permanent = True
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
 
@app.route("/dashboard")
@login_required
def dashboard():
    order_status = request.args.get('order_status')
    customer_name = request.args.get('customer_name')
    order_id = request.args.get('order_id')
    customer_id = request.args.get('customer_id')
    
    if any([order_status, customer_name, order_id, customer_id]):
        orders = get_filtered_orders(order_status, customer_name, order_id, customer_id)
    else:
        orders = get_all_orders()

    # users section
    users = Customer.query.all()
    total_users = len(users)

    # products section
    products = get_products()
    return render_template("dashboard.html", orders=orders, users = users, total_users=total_users, products = products)


@app.route('/order/<int:order_id>', methods=['GET'])
@login_required
def order_details(order_id):
    # Fetch the order details by ID
    order = Order.query.get_or_404(order_id)
    
    # You might also want to fetch customer details, depending on your use case
    customer = Customer.query.get(order.customer_id)
    
    return render_template('order_details.html', order=order, customer=customer)

@app.route('/order/<int:order_id>/update-status', methods=['POST'])
@login_required
def order_status_update(order_id):
    # Fetch the order by ID
    order = Order.query.get_or_404(order_id)
    
    # Update the order status from the form submission
    new_status = request.form.get('status')
    if new_status:
        order.status = new_status
        db.session.commit()
        flash(f"Order {order_id} status updated to {new_status}", 'success')
    
    return redirect(url_for('order_details', order_id=order_id))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

whatsapp = WhatsApp(access_token=wa_access_token, phone_number_id=phone_id)

def update_customer_state(phone, state):
    user = get_customer_by_phone(phone)
    if user:
        user.state = state
        db.session.commit()

processed_messages = set()
class GroupAPI(MethodView): 
    init_every_request = False

    def __init__(self):
        self.whatsapp = WhatsApp(access_token=wa_access_token, phone_number_id=phone_id)

    def get(self):
        received_verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if received_verify_token == verify_token:
            return challenge, 200   
        else:
            return f"Invalid token received verify token: {received_verify_token} not the same with {verify_token}", 403

    def post(self):
        message = whatsapp.parse(request.data)

        if message.id in processed_messages:
            return "", 200

        processed_messages.add(message.id)

        if isinstance(message, UserMessage):
            phone = message.user.phone_number
            username = message.user.name
            with app.app_context():
                user = get_customer_by_phone(phone)

                if isinstance(message, TextMessage):

                    if not user:
                        add_customer_with_phone(phone)
                        update_customer_state(phone, "collecting_name")
                        result = request_user_name(whatsapp, username, phone)
                        if result :
                            message_sent, res = result
                        else :
                            message_sent, res = None
                    elif user.state == "collecting_name":
                        user.name = message.body
                        update_customer_state(phone, "collecting_address")
                        result = request_address(whatsapp, phone)
                        if result :
                            message_sent, res = result
                        else :
                            message_sent, res = None
                    elif user.state == "collecting_address":
                        address = message.body
                        is_valid, suggestion = validate_address(address)
                        if is_valid:
                            user.address = address
                            update_customer_state(phone, "confirming_user_profile")
                            name = user.name
                            address = user.address
                            message_sent, res = confirm_user_details(whatsapp, phone,username, name, address, ListSection, SectionRow)
                        else :
                            if suggestion:
                                message_sent, res = notify_address_suggestion(whatsapp, phone, suggestion)
                            else :
                                message_sent, res = notify_unavailable_service(whatsapp, phone)
                                message_sent, res = request_address(whatsapp, phone)
                                update_customer_state(phone, "collecting_address")
                    else:
                        result = greet_user_and_select_option(whatsapp, phone, username, ListSection, SectionRow)
                        if result :
                            message_sent, res = result
                        else :
                            message_sent, res = None
                               
        if isinstance(message, InteractiveListMessage):
            user_choice = message.reply_id
            if user_choice == "confirm_user_details":
                update_customer_state(phone, None)
                db.session.commit()
                registration_successful(whatsapp, phone, ListSection, SectionRow)
            elif user_choice == "user_profile":
                with app.app_context():
                    user = get_customer_by_phone(phone)
                    name = user.name
                    address = user.address
                    send_user_profile(whatsapp, phone, name, address, ListSection, SectionRow)
            elif user_choice == "edit_details":
                update_customer_state(phone, "collecting_name")
                result = request_user_name(whatsapp, username, phone)
                if result :
                    message_sent, res = result
                else :
                    message_sent, res = None
            elif user_choice == "place_order":
                result = send_catalog(phone, catalog_id, whatsapp, CatalogSection, db_session)
                if result:
                    message_sent, res = result
                else :
                    message_sent, res = None
            if user_choice == "confirm_order":
                update_last_order_status_to_sent(phone)
                order_confirmed(whatsapp, phone, ListSection, SectionRow)
            elif user_choice == "cancel_order":
                # Update the order status to cancelled
                cancel_last_order_by_phone(phone)
                result = order_cancelled(whatsapp, phone, ListSection, SectionRow)
                print("cancelled")
                if result:
                    message_sent, res = result
                else:
                    message_sent, res = None

            elif user_choice == "edit_order" :
                cancel_last_order_by_phone(phone)
                result = send_catalog(phone, catalog_id, whatsapp, CatalogSection, db_session)
                if result:
                    message_sent, res = result
                else :
                    message_sent, res = None

            elif user_choice == "track_order":
                with app.app_context():
                    orders = get_active_orders_by_phone(phone)
                    if not orders or isinstance(orders, str):
                        result = no_orders(whatsapp, phone, ListSection, SectionRow)
                        if result:
                            message_sent, res = result
                        else :
                            message_sent, res = None, None
                    else :
                        try:
                            # Check if 'orders' is iterable
                            for order in orders:
                                order_status = order.status
                                if order_status == "Packed":
                                    message_sent, res = order_packed(whatsapp, phone, order, ListSection, SectionRow)
                                elif order_status == "Packaging received":
                                    message_sent, res = packaging_received(whatsapp, phone, order, ListSection, SectionRow)
                                elif order_status == "Sent to Packaging":
                                    message_sent, res = sent_to_packaging(whatsapp, phone, order, ListSection, SectionRow)
                                elif order_status == "Sent for delivery":
                                    message_sent, res = order_on_way(whatsapp, phone, order, ListSection, SectionRow)

                        except TypeError:
                            # Handle the case where 'orders' is not iterable (e.g., it's a single order)
                            order = orders
                            order_status = order.status  # Assuming it's a single order object
                            if order_status == "Sent to Packaging":
                                message_sent, res = sent_to_packaging(whatsapp, phone, order, ListSection, SectionRow)
                            elif order_status == "Packaging received":
                                message_sent, res = packaging_received(whatsapp, phone, order, ListSection, SectionRow)
                            elif order_status == "Packed":
                                message_sent, res = order_packed(whatsapp, phone, order, ListSection, SectionRow)
                            elif order_status == "Sent for delivery":
                                message_sent, res = order_on_way(whatsapp, phone, order, ListSection, SectionRow)
            elif user_choice == "customer_support":
                message_sent, res = notify_user_about_support_model(whatsapp, phone, ListSection, SectionRow)

        elif isinstance(message, OrderMessage):
            products = message.products
            # from db get cusstomer id, delivery address
            with app.app_context():
                customer = get_customer_by_phone(phone)
                customer_id = customer.id
                delivery_address = customer.address
            # from order message get total_amount, fruit_items
            #   '' vegetable items, product items
            total_amount = 0.0
            fruits_items = []
            vegetables_items = []
            product_quantities = []

            for product in products:
              # Calculate the total for this product
              item_total = product.price * product.quantity
              total_amount += item_total
              category_id = product.id
              with app.app_context():
                  name_category = get_product_name_and_category(category_id)
              if name_category is not None :
                  if name_category.product_category == 'Fruit':
                      fruits_items.append({
                          "product": name_category.name,
                          "quantity": product.quantity,
                          "price": product.price
                      })
                  elif name_category.product_category == 'Vegetable':
                      vegetables_items.append({
                          "product": name_category.name,
                          "quantity": product.quantity,
                          "price": product.price
                      })
              
              # Add to product_quantities
              product_quantities.append((product.id, product.quantity))
            with app.app_context():
                def execute_order():
                    add_order(
                        db=db,
                        customer_id=customer_id,
                        total_amount=total_amount,
                        delivery_address=delivery_address,
                        fruits_items=fruits_items,
                        vegetables_items=vegetables_items,
                        product_quantities=product_quantities
                        )

                    socketio.emit('new_order', {
                        'customer_id': customer_id,
                        'total_amount': total_amount,
                        'delivery_address': delivery_address,
                        'fruits_items': fruits_items,
                        'vegetables_items': vegetables_items
                    })
                if total_amount >= 0.50:
                    execute_order()  
                    result = confirm_order(whatsapp, phone, ListSection, SectionRow, total_amount, fruits_items, vegetables_items, product_quantities, customer_id, delivery_address)
                else :
                    result = order_amount_restriction(whatsapp, phone, ListSection, SectionRow, total_amount, fruits_items, vegetables_items, product_quantities, customer_id, delivery_address)
                

                if result:
                    message_sent, res = result
                else:
                    message_sent, res = None

        elif isinstance(message, MessageStatus):
            print(message)
            pass
    
        else:
             print("Unsupported message type")
            
        return "", 200
    
        
app.add_url_rule('/webhook', view_func=GroupAPI.as_view('wa_webhook'))

# if __name__ == "__main__":
    # app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

    with app.app_context():
            db.create_all()
