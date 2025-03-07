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
import random
from werkzeug.security import check_password_hash, generate_password_hash

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
    begin_withdrawal,
    update_product_availability,
    add_product_availability,
    get_products_by_region,
    get_product_availability_by_product_id,
)
from models import (
    db,
    Customer,
    init_db,
    Order,
    db_session,
    CustomerReward,
    Withdrawal,
    Employee,
    Product,
)
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
    send_withdrawal_success_message,
    send_otp_via_whatsapp,
)
from wa_cloud_py.message_components import ListSection, SectionRow, CatalogSection
from Pamusika_Investment_Rewards.reward_calculator import calculate_reward

# from wa_cloud_py.components.messages import ListSection, SectionRow, CatalogSection # latest version 0.1.7
from flask_migrate import Migrate
from flask import flash, url_for, redirect
from location_restriction import validate_address
from functools import wraps
from datetime import timedelta
from flask_socketio import SocketIO, emit
from validate_amount import validate_withdrawal_amount
import string

load_dotenv()
wa_access_token = os.getenv("WA_TOKEN")
phone_id = os.getenv("PHONE_ID")
verify_token = os.getenv("VERIFY_TOKEN")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///musikatest_0_db.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = (
# "postgresql://uep1bjqsmff4ei:paa7a7cf74e5bb627a7d1ab512cc06d2cc8be231f249e7a9936a8ed8307a2bd24@cfv89ambqptmdb.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d26o11i55bsuha"
# )
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


@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")


@app.route("/send_otp", methods=["POST"])
def send_otp():
    email = request.form["email"]
    employee_phone = request.form["phone"]
    region = request.form["region"]

    # Generate a unique OTP (e.g., 6-digit number)
    otp = "".join(random.choices(string.digits, k=6))

    # Send the OTP to your WhatsApp number
    send_otp_via_whatsapp(otp, whatsapp, email, region)

    # Hash the OTP before saving it (as a password)
    hashed_password = generate_password_hash(otp)

    # Save the user with the hashed password (you may want to check if the user already exists)
    new_user = Employee(
        username=email,
        password_hash=hashed_password,
        phone=employee_phone,
        region=region,
    )  # Adjust phone as needed
    db.session.add(new_user)
    db.session.commit()

    flash(
        "Agent created successfully! An OTP has been sent to the recruiter for verification.",
        "success",
    )

    return redirect(
        url_for("login")
    )  # Redirect to login or another page after sending OTP


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    user_id = session.get("user_id")  # Get user ID from session
    if not user_id:
        flash("You need to log in first.", "danger")
        return redirect(url_for("login"))  # Redirect to login if not logged in

    if request.method == "POST":
        old_password = request.form["oldPassword"]
        new_password = request.form["newPassword"]
        confirm_password = request.form["confirmPassword"]

        user = Employee.query.get(user_id)  # Fetch the user from the database

        if user and check_password_hash(user.password_hash, old_password):
            if new_password == confirm_password:
                user.password_hash = generate_password_hash(new_password)
                db.session.commit()  # Save the new password to the database
                flash("Your password has been changed successfully!", "success")
                return redirect(
                    url_for("dashboard")
                )  # Redirect to dashboard or another page
            else:
                flash("New passwords do not match.", "danger")
        else:
            flash("Old password is incorrect.", "danger")

    return render_template("change_password.html")


# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Query the Employee model to find the user by username
        employee = Employee.query.filter_by(username=username).first()

        if employee and check_password_hash(employee.password_hash, password):
            session.permanent = True
            session["user_id"] = employee.id  # Store user ID in session
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
    # Fetching the logged-in user's information
    user_id = session.get("user_id")  # Assuming user ID is stored in session
    employee = Employee.query.get(user_id)  # Fetch the employee details
    employee_region = employee.region
    if any([order_status, customer_name, order_id, customer_id]):
        orders = get_filtered_orders(order_status, customer_name, order_id, customer_id)
    else:
        orders = get_all_orders(employee_region)  # Fetch all orders

    # Users section
    users = Customer.query.filter_by(region=employee.region).all()
    total_users = len(users)

    # Products section
    products = get_products()

    return render_template(
        "dashboard.html",
        orders=orders,
        users=users,
        total_users=total_users,
        products=products,
        employee=employee,  # Pass employee details to the template
    )


@app.route("/products", methods=["GET", "POST"])
@login_required
def manage_products():
    user_id = session.get("user_id")  # Get user ID from session
    employee = Employee.query.get(user_id)  # Fetch employee details
    employee_region = employee.region  # Get the region of the logged-in employee

    if request.method == "POST":
        product_id = request.form.get("product_id")
        meta_id = request.form.get("meta_id")
        name = request.form.get("name")
        cost_price = float(request.form.get("cost_price"))
        selling_price = float(request.form.get("selling_price"))
        currency = request.form.get("currency", "USD")
        product_category = request.form.get("product_category")
        availability = True if request.form.get("availability") else False
        quantity = int(request.form.get("quantity", 0))  # Default to 0 if not provided
        reward_amount = calculate_reward(cost_price, selling_price)

        if product_id:  # Update existing product
            updated_product = update_product(
                product_id,
                meta_id,
                name,
                cost_price,
                selling_price,
                currency,
                product_category,
            )

            if updated_product:
                flash(f"Product '{name}' updated successfully.", "success")
                print("Proceeding to update the product availability")

                # Update ProductAvailability for this product in the employee's region
                print(
                    f"reward {reward_amount} availability {availability} quantity {quantity}"
                )
                update_product_availability(
                    updated_product.id,
                    employee_region,
                    reward_amount,
                    availability,
                    quantity,
                )
                print("Product availability updated successfully.")

            else:
                flash(f"Failed to update product '{name}'.", "danger")

        else:  # Add new product or record availability for existing product
            existing_product = Product.query.filter_by(meta_id=meta_id).first()
            if existing_product:
                add_product_availability(
                    existing_product.id,
                    employee_region,
                    reward_amount,
                    availability,
                    quantity,
                )
                flash(
                    f"Availability record added for existing product '{existing_product.name}'!",
                    "success",
                )
            else:
                new_product = add_new_product(
                    meta_id,
                    name,
                    cost_price,
                    selling_price,
                    currency,
                    product_category,
                )
                if new_product:
                    add_product_availability(
                        new_product.id,
                        employee_region,
                        reward_amount,
                        availability,
                        quantity,
                    )
                    flash(f"Product '{name}' added successfully!", "success")
                else:
                    flash(f"Error adding product '{name}'.", "danger")

        return redirect(url_for("manage_products"))

    results = get_products_by_region(employee_region)
    return render_template("manage_products.html", results=results)


@app.route("/rewards")
@login_required
def view_rewards():
    """View the list of all rewards for customers."""
    user_id = session.get("user_id")  # Assuming user ID is stored in session
    employee = Employee.query.get(user_id)  # Fetch the employee details
    employee_region = employee.region

    rewards = (
        db.session.query(CustomerReward)
        .join(Customer)
        .filter(Customer.region == employee_region)
        .all()
    )
    pending_withdrawals = get_pending_withdrawals()  # Fetch pending withdrawals

    # Fetch customer addresses for each withdrawal
    for withdrawal in pending_withdrawals:
        customer = Customer.query.get(withdrawal.customer_id)  # Get customer by ID
        withdrawal.address = (
            customer.address if customer else "Address not found"
        )  # Add address to withdrawal

    return render_template(
        "rewards.html", rewards=rewards, pending_withdrawals=pending_withdrawals
    )


@app.route("/withdrawal_confirmation/<int:customer_id>", methods=["POST"])
def withdrawal_confirmation(customer_id):
    # Call the function to update withdrawal status to "Completed" directly
    success, message = update_withdrawal_status_to_completed(customer_id)
    phone = get_customer_by_id(customer_id).phone
    name = get_customer_by_id(customer_id).name
    amount = message
    # Handle the outcome of the function
    if success:
        send_withdrawal_success_message(
            whatsapp,
            phone,
            name,
            amount,
            ListSection,
            SectionRow,
        )
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
    customer = get_customer_by_id(customer_id)
    phone = customer.phone
    fullname = customer.name
    address = customer.address
    balance = get_total_reward_for_customer(phone)
    if balance >= 1:
        print(balance)
        if float(withdrawal_amount) < balance:
            print(withdrawal_amount)
            begining_withdrawal = begin_withdrawal(withdrawal_amount, customer_id)
            if begining_withdrawal:
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
                return redirect(
                    url_for("view_rewards")
                )  # Redirect to the withdrawal page
        else:
            flash("Insufficient balance to initiate withdrawal.", "danger")
            return redirect(url_for("view_rewards"))
    else:
        flash("Withdrawal amount should be greater than 1.", "danger")
        return redirect(url_for("view_rewards"))


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
                        update_customer_state(phone, "confirming_profile")
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
                        is_valid, suggestion, region = validate_address(
                            address
                        )  # Update to capture region
                        if is_valid:
                            user.address = address
                            user.region = region
                            update_customer_state(phone, "confirming_profile")

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
                        amount_validator = validate_withdrawal_amount(
                            amount, whatsapp, phone
                        )
                        if amount_validator:
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
                                        begin_withdrawal(amount, customer_id)
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
                user = get_customer_by_phone(phone)
                customer_region = user.region
                result = send_catalog(
                    phone,
                    catalog_id,
                    whatsapp,
                    CatalogSection,
                    db_session,
                    customer_region,
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
                    whatsapp.send_text(
                        to="263711475883",
                        body=f"Hi {username}, you have a new withdrawal order from {phone}. Check your dashboard for more details. https://musika-d2fb0b8da611.herokuapp.com/rewards",
                    )
                    update_customer_state(phone, None)
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
                        body=f"Hi {username}, you have a new order from {phone}. Check your dashboard for more details. https://musika-d2fb0b8da611.herokuapp.com/order/{order_id}",
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
                            body=f"Hi {username}, you have a new order from {phone}. Check your dashboard for more details. https://musika-d2fb0b8da611.herokuapp.com/order/{order_id}",
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
                        body=f"Hi {username}, you have a new order from {phone}. Check your dashboard for more details. https://musika-d2fb0b8da611.herokuapp.com/order/{order_id}",
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
                    print("orders", orders)

                    if not orders or isinstance(orders, str):
                        result = no_orders(whatsapp, phone, ListSection, SectionRow)
                        if result:
                            message_sent, res = result
                        else:
                            message_sent, res = None, None
                    else:
                        print("Order found")
                        try:
                            # Check if 'orders' is iterable
                            for order in orders:
                                order_status = order.status
                                print(
                                    f"Processing order ID: {order.id}, Status: {order_status}"
                                )  # Debugging output

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
                                    print("sent to packagin", order_on_way)
                                elif order_status == "Sent for delivery":
                                    message_sent, res = order_on_way(
                                        whatsapp, phone, order, ListSection, SectionRow
                                    )

                                # Check if a message was sent
                                if message_sent is None:
                                    print(
                                        f"Failed to send message for Order ID: {order.id}"
                                    )

                        except TypeError:
                            # Handle the case where 'orders' is not iterable (e.g., it's a single order)
                            order = orders
                            order_status = (
                                order.status
                            )  # Assuming it's a single order object
                            print(
                                f"Processing single order ID: {order.id}, Status: {order_status}"
                            )  # Debugging output

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

                            # Check if a message was sent
                            if message_sent is None:
                                print(
                                    f"Failed to send message for Order ID: {order.id}"
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
                    print(name_category.id)
                if name_category is not None:
                    product_availability = get_product_availability_by_product_id(
                        name_category.id
                    )
                    print(product_availability)
                    reward_amount = product_availability.reward_amount
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
                print("order executed")
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
                print("result for confirm order with payment", result)
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
                print("result for order amount restriction", result)

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
    # app.run(debug=False)
    port = int(os.getenv("PORT", 8000))
    gunicorn.run(app, host="0.0.0.0", port=port)

    with app.app_context():
        db.create_all()
