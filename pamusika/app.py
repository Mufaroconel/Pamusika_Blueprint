from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    session,
    flash,
)
from flask_sqlalchemy import SQLAlchemy
from flask.views import MethodView
from wa_cloud_py import WhatsApp
import math

# from wa_cloud_py.messages.types import MessageStatus, UserMessage, TextMessage, OrderMessage, InteractiveListMessage # latest version 0.1.7
from wa_cloud_py.message_types import (
    MessageStatus,
    UserMessage,
    TextMessage,
    OrderMessage,
    InteractiveListMessage,
)
from dotenv import load_dotenv
import os
from dboperations import (
    add_customer,
    get_customer_by_phone,
    add_order,
    update_order_status,
    get_all_orders,
    get_filtered_orders,
    user_exists,
    add_customer_with_phone,
    update_customer_name,
    update_customer_username,
    update_customer_address,
    get_products,
    get_product_name_and_category,
    cancel_last_order_by_phone,
    get_active_orders_by_phone,
    update_last_order_status_to_sent_and_return_id,
    get_all_products,
    add_new_product,
    update_product,
    delete_product_by_id,
    add_to_reward,
    subtract_from_reward,
    get_reward_amount_for_last_order,
    add_customer_reward,
    get_total_reward_for_customer,
    initiate_withdrawal,
    get_pending_withdrawals,
    subtract_from_reward,
    confirm_withdrawal,
    get_withdrawal_by_id,
    get_last_pending_order_total,
    update_last_withdrawal_status_to_initiated,
    get_last_pending_withdrawal,
    update_withdrawal_status_to_completed,
    update_latest_pending_order_total,
    get_customer_by_id,
    get_reward_amount_for_order,
    get_order_products,
)
from models import db, Customer, init_db, Order, db_session, CustomerReward, Withdrawal
from messages.app_logic_messages import (
    greet_user_and_select_option,
    send_catalog,
    confirm_order_with_payment,
    order_confirmed,
    make_changes,
    handle_cancellation,
    sent_to_packaging,
    packaging_received,
    order_packed,
    order_on_way,
    order_delivered,
    no_orders,
    tracking_issue,
    invalid_option,
    select_correct_option,
    request_user_name,
    request_address,
    notify_user_about_support_model,
    confirm_user_details,
    registration_successful,
    send_user_profile,
    order_cancelled,
    notify_unavailable_service,
    notify_address_suggestion,
    order_amount_restriction,
    insufficient_balance_notification,
    minimum_withdrawal_warning,
    exit_withdrawal_message,
    confirm_withdrawal_message,
    rewards_balance,
    send_edit_user_details_prompt,
    insufficient_balance_for_order_notification,
    withdrawal_initiated,
    insufficient_reward_balance,
)
from wa_cloud_py.message_components import ListSection, SectionRow, CatalogSection

# from wa_cloud_py.components.messages import ListSection, SectionRow, CatalogSection # latest version 0.1.7
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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///musikatestdb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secretkey"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)
socketio = SocketIO(app)

migrate = Migrate(app, db)
db.init_app(app)
init_db(app)
catalog_id = "253006871078558"

valid_username = "admin"
valid_password = "password"


def login_required(f):
    """A decorator to protect routes that require login"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    return redirect(url_for("login"))


# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == valid_username and password == valid_password:
            session.permanent = True
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/dashboard")
@login_required
def dashboard():
    order_status = request.args.get("order_status")
    customer_name = request.args.get("customer_name")
    order_id = request.args.get("order_id")
    customer_id = request.args.get("customer_id")

    if any([order_status, customer_name, order_id, customer_id]):
        orders = get_filtered_orders(order_status, customer_name, order_id, customer_id)
    else:
        orders = get_all_orders()

    # users section
    users = Customer.query.all()
    total_users = len(users)

    # products section
    products = get_products()
    return render_template(
        "dashboard.html",
        orders=orders,
        users=users,
        total_users=total_users,
        products=products,
    )


@app.route("/products", methods=["GET", "POST"])
@login_required
def manage_products():
    if request.method == "POST":
        product_id = request.form.get("product_id")
        meta_id = request.form.get("meta_id")
        name = request.form.get("name")
        cost_price = float(request.form.get("cost_price"))
        selling_price = float(request.form.get("selling_price"))
        currency = request.form.get("currency", "USD")
        product_category = request.form.get("product_category")
        availability = True if request.form.get("availability") else False

        if product_id:  # Update existing product
            product = update_product(
                product_id,
                meta_id,
                name,
                cost_price,
                selling_price,
                currency,
                product_category,
                availability,
            )
            if product:
                flash(
                    f"Product '{name}' updated successfully. Reward: {product.reward_amount} {currency}.",
                    "success",
                )
            else:
                flash(f"Product with ID {product_id} not found.", "danger")
        else:  # Add new product
            new_product = add_new_product(
                meta_id,
                name,
                cost_price,
                selling_price,
                currency,
                product_category,
                availability,
            )
            flash(
                f"Product '{name}' added successfully. Reward: {new_product.reward_amount} {currency}.",
                "success",
            )

        return redirect(url_for("manage_products"))

    # GET request, render the template with all products
    products = get_all_products()
    return render_template("manage_products.html", products=products)


@app.route("/rewards")
@login_required
def view_rewards():
    """View the list of all rewards for customers."""
    rewards = CustomerReward.query.all()  # Fetch all customer rewards
    pending_withdrawals = get_pending_withdrawals()
    return render_template(
        "rewards.html", rewards=rewards, pending_withdrawals=pending_withdrawals
    )


@app.route("/withdrawal_confirmation/<int:customer_id>", methods=["POST"])
def withdrawal_confirmation(customer_id):
    # Call the function to update withdrawal status to "Completed" directly
    success, message = update_withdrawal_status_to_completed(customer_id)

    # Handle the outcome of the function
    if success:
        flash("Withdrawal status updated to 'Initiated' successfully.", "success")
    else:
        flash(message or "Failed to update withdrawal status.", "danger")

    # Redirect to the appropriate route
    return redirect(url_for("view_rewards"))  # Adjust this route if needed


# Route to update a specific customer's reward
@app.route("/rewards/update/<int:customer_id>", methods=["POST"])
@login_required
def update_reward(customer_id):
    """Update the reward for a specific customer."""
    new_reward_amount = float(request.form["reward_amount"])

    # Find the reward record for the customer
    customer_reward = CustomerReward.query.filter_by(customer_id=customer_id).first()

    if customer_reward:
        # Update the reward amount
        customer_reward.reward_amount = new_reward_amount
        db.session.commit()
        flash(
            f"Reward for Customer {customer_id} updated to {new_reward_amount}.",
            "success",
        )
    else:
        flash(f"No reward record found for Customer {customer_id}.", "danger")

    return redirect(url_for("view_rewards"))


@app.route("/initiate_withdrawal", methods=["POST"])
@login_required
def initialize_withdrawal():
    customer_id = request.form["customer_id"]
    withdrawal_amount = request.form["withdrawal_amount"]
    intiating_withdrawal = initiate_withdrawal(withdrawal_amount, customer_id)
    customer = get_customer_by_id(customer_id)
    phone = customer.phone
    fullname = customer.name
    address = customer.address
    if intiating_withdrawal:
        flash(f"Withdrawal initiated for Customer {customer_id}.", "success")
        confirm_withdrawal_message(
            whatsapp,
            phone,
            fullname,
            address,
            withdrawal_amount,
            ListSection,
            SectionRow,
        )
        return redirect(url_for("view_rewards"))  # Redirect to the withdrawal page


@app.route("/products/delete/<product_id>", methods=["POST"])
@login_required
def delete_product(product_id):
    product = delete_product_by_id(product_id)
    if product:
        flash(f"Product '{product.name}' deleted successfully.", "success")
    else:
        flash(f"Product with ID {product_id} not found.", "danger")

    return redirect(url_for("manage_products"))


@app.route("/order/<int:order_id>", methods=["GET"])
@login_required
def order_details(order_id):
    # Fetch the order details by ID
    order = Order.query.get_or_404(order_id)

    # Fetch customer details
    customer = Customer.query.get(order.customer_id)

    # Fetch associated products for the order
    order_products = get_order_products(order.id)  # Use the new function

    return render_template(
        "order_details.html",
        order=order,
        customer=customer,
        order_products=order_products,
    )


@app.route("/order/<int:order_id>/update-status", methods=["POST"])
@login_required
def order_status_update(order_id):
    # Fetch the order by ID
    order = Order.query.get_or_404(order_id)

    # Update the order status from the form submission
    new_status = request.form.get("status")
    if new_status:
        if order.status == "Delivered":
            pass
        else:
            order.status = new_status
            db.session.commit()
            customer_id = order.customer_id
            phone = get_customer_by_id(customer_id).phone
            if order.status == "Packed":
                message_sent, res = order_packed(
                    whatsapp, phone, order, ListSection, SectionRow
                )
            elif order.status == "Packaging received":
                message_sent, res = packaging_received(
                    whatsapp, phone, order, ListSection, SectionRow
                )
            elif order.status == "Sent to Packaging":
                message_sent, res = sent_to_packaging(
                    whatsapp, phone, order, ListSection, SectionRow
                )
            elif order.status == "Sent for delivery":
                message_sent, res = order_on_way(
                    whatsapp, phone, order, ListSection, SectionRow
                )
            elif order.status == "Delivered":
                customer_order_reward = get_reward_amount_for_order(order_id)
                add_to_reward(customer_id, customer_order_reward)
                new_reward_balance = get_total_reward_for_customer(phone)
                message_sent, res = order_delivered(
                    whatsapp, phone, order, new_reward_balance, ListSection, SectionRow
                )
            elif order.status == "Cancelled":
                message_sent, res = order_cancelled(
                    whatsapp, phone, ListSection, SectionRow
                )

        flash(f"Order {order_id} status updated to {new_status}", "success")

    return redirect(url_for("order_details", order_id=order_id))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


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
            return (
                f"Invalid token received verify token: {received_verify_token} not the same with {verify_token}",
                403,
            )

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
                        new_customer = add_customer_with_phone(phone)
                        if new_customer:
                            update_customer_state(phone, "collecting_name")
                            reward = add_customer_reward(
                                new_customer.id, reward_amount=0.0
                            )
                            if reward:
                                print(
                                    f"CustomerReward successfully added for customer ID {new_customer.id}."
                                )
                            else:
                                print(
                                    f"Failed to add CustomerReward for customer ID {new_customer.id}."
                                )
                        result = request_user_name(whatsapp, username, phone)
                        if result:
                            message_sent, res = result
                        else:
                            message_sent, res = None
                    elif user.state == "collecting_name":
                        user.name = message.body
                        update_customer_state(phone, "collecting_address")
                        result = request_address(whatsapp, phone)
                        if result:
                            message_sent, res = result
                        else:
                            message_sent, res = None
                    elif user.state == "editing_name":
                        user.name = message.body
                        update_customer_state(phone, "confirming_user_profile")
                        name = user.name
                        address = user.address
                        message_sent, res = confirm_user_details(
                            whatsapp,
                            phone,
                            username,
                            name,
                            address,
                            ListSection,
                            SectionRow,
                        )
                    elif user.state == "collecting_address":
                        address = message.body
                        is_valid, suggestion = validate_address(address)
                        if is_valid:
                            user.address = address
                            update_customer_state(phone, "confirming_user_profile")
                            name = user.name
                            address = user.address
                            message_sent, res = confirm_user_details(
                                whatsapp,
                                phone,
                                username,
                                name,
                                address,
                                ListSection,
                                SectionRow,
                            )
                        else:
                            if suggestion:
                                message_sent, res = notify_address_suggestion(
                                    whatsapp, phone, suggestion
                                )
                            else:
                                message_sent, res = notify_unavailable_service(
                                    whatsapp, phone
                                )
                                message_sent, res = request_address(whatsapp, phone)
                                update_customer_state(phone, "collecting_address")
                    elif user.state == "withdraw_reward":
                        amount = message.body
                        balance = get_total_reward_for_customer(phone)
                        customer = get_customer_by_phone(phone)
                        address = customer.address
                        if customer:
                            customer_id = customer.id
                            print(customer_id, address)
                            if float(amount) < 1:
                                minimum_withdrawal_warning(
                                    whatsapp,
                                    phone,
                                    username,
                                    ListSection,
                                    SectionRow,
                                )
                            else:
                                if balance >= float(amount):
                                    initiate_withdrawal(amount, customer_id)
                                    confirm_withdrawal_message(
                                        whatsapp,
                                        phone,
                                        username,
                                        address,
                                        amount,
                                        ListSection,
                                        SectionRow,
                                    )
                                    print("withdrawal message sent")
                                else:
                                    reward_balance = get_total_reward_for_customer(
                                        phone
                                    )
                                    print(reward_balance)
                                    insufficient_balance_notification(
                                        whatsapp,
                                        phone,
                                        username,
                                        reward_balance,
                                        ListSection,
                                        SectionRow,
                                    )
                        else:
                            print("no customer found")
                    elif user.state == "confirm_withdraw":
                        whatsapp.send_text(to=phone, body="withdrawal confirmed")
                        update_customer_state(phone, None)
                    else:
                        result = greet_user_and_select_option(
                            whatsapp, phone, username, ListSection, SectionRow
                        )
                        if result:
                            message_sent, res = result
                        else:
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
                    total_rewards_earned = get_total_reward_for_customer(phone)

                    send_user_profile(
                        whatsapp,
                        phone,
                        username,
                        name,
                        total_rewards_earned,
                        address,
                        ListSection,
                        SectionRow,
                    )
            elif user_choice == "edit_details":
                user = get_customer_by_phone(phone)
                name = user.name
                address = user.address
                result = send_edit_user_details_prompt(
                    whatsapp,
                    phone,
                    username,
                    name,
                    address,
                    ListSection,
                    SectionRow,
                )
                if result:
                    message_sent, res = result
                else:
                    message_sent, res = None
            elif user_choice == "edit_name":
                request_user_name(whatsapp, username, phone)
                update_customer_state(phone, "editing_name")
                pass
            elif user_choice == "edit_address":
                request_address(whatsapp, phone)
                update_customer_state(phone, "collecting_address")
            elif user_choice == "edit_amount":
                whatsapp.send_text(to=phone, body="Please Enter amount to withdraw")
            elif user_choice == "place_order":
                result = send_catalog(
                    phone, catalog_id, whatsapp, CatalogSection, db_session
                )
                if result:
                    message_sent, res = result
                else:
                    message_sent, res = None
            elif user_choice == "confirm_withdrawal":
                balance = get_total_reward_for_customer(phone)
                customer_id = get_customer_by_phone(phone).id
                withdrawal_amount = get_last_pending_withdrawal(customer_id).amount
                print(balance)
                print(withdrawal_amount)
                if balance >= withdrawal_amount:
                    subtract_from_reward(customer_id, withdrawal_amount)
                    update_last_withdrawal_status_to_initiated(customer_id)
                    withdrawal_initiated(whatsapp, phone, ListSection, SectionRow)
                else:
                    insufficient_balance_for_order_notification(
                        whatsapp,
                        phone,
                        username,
                        balance,
                        withdrawal_amount,
                        ListSection,
                        SectionRow,
                    )
            elif user_choice == "pay_with_cash":
                customer_reward = get_reward_amount_for_last_order(phone)
                order_id = update_last_order_status_to_sent_and_return_id(phone)
                if order_id:
                    print(customer_reward)
                    customer = get_customer_by_phone(phone)
                    if customer:
                        customer_id = customer.id
                    else:
                        print("customer not found")
                    if customer_reward:
                        print(customer_reward)
                        total_reward = customer_reward
                        # add_to_reward(customer_id, total_reward)
                        print("updated succesfully")
                    else:
                        print("reward not found")

                    order_confirmed(whatsapp, phone, ListSection, SectionRow)
                    whatsapp.send_text(
                        to="263711475883",
                        body=f"Hi {username}, you have a new order from {phone}. Check your dashboard for more details. https://0gvvb2gw-5000.uks1.devtunnels.ms/order/{order_id}",
                    )
                else:
                    pass
            elif user_choice == "pay_with_rewards":
                balance = get_total_reward_for_customer(phone)
                customer_id = get_customer_by_phone(phone).id
                total_amount = get_last_pending_order_total(customer_id)
                print(balance)
                print(total_amount)
                if balance < 1:
                    insufficient_reward_balance(
                        whatsapp,
                        phone,
                        username,
                        balance,
                        ListSection,
                        SectionRow,
                    )
                elif balance >= total_amount:
                    subtract_from_reward(customer_id, total_amount)
                    new_customer_reward = get_reward_amount_for_last_order(phone)
                    # add_to_reward(customer_id, new_customer_reward)
                    order_id = update_last_order_status_to_sent_and_return_id(phone)
                    if order_id:
                        order_confirmed(whatsapp, phone, ListSection, SectionRow)
                        whatsapp.send_text(
                            to="263711475883",
                            body=f"Hi {username}, you have a new order from {phone}. Check your dashboard for more details. https://0gvvb2gw-5000.uks1.devtunnels.ms/order/{order_id}",
                        )
                else:
                    insufficient_balance_for_order_notification(
                        whatsapp,
                        phone,
                        username,
                        balance,
                        total_amount,
                        ListSection,
                        SectionRow,
                    )
            elif user_choice == "pay_with_rewards_and_delivery":
                balance = get_total_reward_for_customer(phone)
                rounded_balance = math.floor(balance * 10) / 10
                customer_id = get_customer_by_phone(phone).id
                total_amount = get_last_pending_order_total(customer_id)
                new_total = total_amount - rounded_balance
                update_latest_pending_order_total(customer_id, new_total)
                subtract_from_reward(customer_id, rounded_balance)

                order_id = update_last_order_status_to_sent_and_return_id(phone)
                if order_id:
                    order_confirmed(whatsapp, phone, ListSection, SectionRow)
                    whatsapp.send_text(
                        to="263711475883",
                        body=f"Hi {username}, you have a new order from {phone}. Check your dashboard for more details. https://0gvvb2gw-5000.uks1.devtunnels.ms/order/{order_id}",
                    )
                    print(new_customer_reward)
                    print(rounded_balance, total_amount)
                else:
                    pass
            elif user_choice == "cancel_order":
                # Update the order status to cancelled
                cancel_last_order_by_phone(phone)
                result = order_cancelled(whatsapp, phone, ListSection, SectionRow)
                print("cancelled")
                if result:
                    message_sent, res = result
                else:
                    message_sent, res = None

            elif user_choice == "edit_order":
                cancel_last_order_by_phone(phone)
                result = send_catalog(
                    phone, catalog_id, whatsapp, CatalogSection, db_session
                )
                if result:
                    message_sent, res = result
                else:
                    message_sent, res = None

            elif user_choice == "track_order":
                with app.app_context():
                    orders = get_active_orders_by_phone(phone)
                    if not orders or isinstance(orders, str):
                        result = no_orders(whatsapp, phone, ListSection, SectionRow)
                        if result:
                            message_sent, res = result
                        else:
                            message_sent, res = None, None
                    else:
                        try:
                            # Check if 'orders' is iterable
                            for order in orders:
                                order_status = order.status
                                if order_status == "Packed":
                                    message_sent, res = order_packed(
                                        whatsapp, phone, order, ListSection, SectionRow
                                    )
                                elif order_status == "Packaging received":
                                    message_sent, res = packaging_received(
                                        whatsapp, phone, order, ListSection, SectionRow
                                    )
                                elif order_status == "Sent to Packaging":
                                    message_sent, res = sent_to_packaging(
                                        whatsapp, phone, order, ListSection, SectionRow
                                    )
                                elif order_status == "Sent for delivery":
                                    message_sent, res = order_on_way(
                                        whatsapp, phone, order, ListSection, SectionRow
                                    )

                        except TypeError:
                            # Handle the case where 'orders' is not iterable (e.g., it's a single order)
                            order = orders
                            order_status = (
                                order.status
                            )  # Assuming it's a single order object
                            if order_status == "Sent to Packaging":
                                message_sent, res = sent_to_packaging(
                                    whatsapp, phone, order, ListSection, SectionRow
                                )
                            elif order_status == "Packaging received":
                                message_sent, res = packaging_received(
                                    whatsapp, phone, order, ListSection, SectionRow
                                )
                            elif order_status == "Packed":
                                message_sent, res = order_packed(
                                    whatsapp, phone, order, ListSection, SectionRow
                                )
                            elif order_status == "Sent for delivery":
                                message_sent, res = order_on_way(
                                    whatsapp, phone, order, ListSection, SectionRow
                                )
            elif user_choice == "customer_support":
                message_sent, res = notify_user_about_support_model(
                    whatsapp, phone, ListSection, SectionRow
                )
            elif user_choice == "withdraw_reward":
                whatsapp.send_text(to=phone, body="Please Enter amount to withdraw")
                update_customer_state(phone, "withdraw_reward")
            elif user_choice == "exit_withdrawal":
                update_customer_state(phone, None)
                exit_withdrawal_message(
                    whatsapp, phone, username, ListSection, SectionRow
                )
                print("withdrawal exited")
            elif user_choice == "check_balance":
                balance = get_total_reward_for_customer(phone)
                rewards_balance(
                    whatsapp, phone, username, balance, ListSection, SectionRow
                )

        elif isinstance(message, OrderMessage):
            products = message.products
            # Get customer ID and delivery address from the database
            with app.app_context():
                customer = get_customer_by_phone(phone)
                if customer is None:
                    print("Customer not found.")
                    return  # Handle customer not found scenario appropriately
                customer_id = customer.id
                delivery_address = customer.address

            # Initialize totals and product quantities
            total_amount = 0.0
            total_reward = 0.0
            product_quantities = []

            for product in products:
                # Calculate the total for this product
                item_total = product.price * product.quantity
                total_amount += item_total

                category_id = product.id
                with app.app_context():
                    name_category = get_product_name_and_category(category_id)

                if name_category is not None:
                    reward_amount = name_category.reward_amount
                    item_reward_total = reward_amount * product.quantity
                    total_reward += item_reward_total

                    # Add to product_quantities (now includes all products)
                    product_quantities.append((product.id, product.quantity))

            # Function to execute order creation and emit event
            def execute_order():
                add_order(
                    db=db,
                    customer_id=customer_id,
                    total_amount=total_amount,
                    delivery_address=delivery_address,
                    product_quantities=product_quantities,  # Only using this now
                    reward_amount=total_reward,
                )

                socketio.emit(
                    "new_order",
                    {
                        "customer_id": customer_id,
                        "total_amount": total_amount,
                        "delivery_address": delivery_address,
                        "product_quantities": product_quantities,  # Send all products as quantities
                    },
                )

            if total_amount >= 1.00:
                execute_order()
                result = confirm_order_with_payment(
                    whatsapp,
                    phone,
                    ListSection,
                    SectionRow,
                    total_amount,
                    total_reward,
                    product_quantities,  # Send only product quantities now
                    username,
                    delivery_address,
                )
            else:
                result = order_amount_restriction(
                    whatsapp,
                    phone,
                    ListSection,
                    SectionRow,
                    total_amount,
                    product_quantities,  # Send only product quantities now
                    customer_id,
                    delivery_address,
                )

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


app.add_url_rule("/webhook", view_func=GroupAPI.as_view("wa_webhook"))

if __name__ == "__main__":
    app.run(debug=True)

    with app.app_context():
        db.create_all()
