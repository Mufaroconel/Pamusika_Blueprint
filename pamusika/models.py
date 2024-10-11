# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
db_session = db.session


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    name = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(20), nullable=True)
    region = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return (
            f"<Customer {self.id} - Phone: {self.phone}, "
            f"Username: {self.username}, Name: {self.name}, "
            f"State: {self.state}, Region: {self.region}>"
        )


class Product(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    meta_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="USD")
    product_category = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return (
            f"<Product {self.name} - Category: {self.product_category} - "
            f"Meta ID: {self.meta_id} - Cost Price: {self.cost_price} - "
            f"Selling Price: {self.selling_price} - "
            f"Available: {self.availability}>"
        )


class ProductAvailability(db.Model):
    __tablename__ = "product_availability"

    id = db.Column(db.String(50), primary_key=True)
    product_id = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    reward_amount = db.Column(db.Float, default=0.0)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return (
            f"<ProductAvailability Product ID: {self.product_id} - Region: {self.region} - "
            f"Available: {self.availability} - Quantity: {self.quantity} - "
            f"Reward Amount: {self.reward_amount}>"
        )


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    total_amount = db.Column(db.Float, nullable=True)
    delivery_address = db.Column(db.String(255), nullable=True)

    # New fields to store rewards
    reward_amount = db.Column(
        db.Float, nullable=False, default=0.0
    )  # Total reward earned for this order
    date = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )  # Date when reward was earned

    # Relationship to access products in this order
    products = db.relationship("Product", secondary="order_products", backref="orders")

    def __repr__(self):
        # Create a list of product names and quantities
        product_details = []
        for product in self.products:  # Accessing related products
            product_details.append(
                f"{product.name}"
            )  # Assuming 'name' is an attribute of Product

        # Join product details into a string
        products_str = ", ".join(product_details) if product_details else "No products"

        return (
            f"<Order {self.id} - Status: {self.status}, Customer ID: {self.customer_id}, "
            f"Order Date: {self.order_date}, Total: {self.total_amount}, "
            f"Delivery Address: {self.delivery_address}, Reward Amount: {self.reward_amount}, "
            f"Date: {self.date}, Products: [{products_str}]>"
        )


order_products = db.Table(
    "order_products",
    db.Column("order_id", db.Integer, db.ForeignKey("order.id"), primary_key=True),
    db.Column(
        "product_id", db.String(50), db.ForeignKey("product.id"), primary_key=True
    ),
    db.Column("quantity", db.Integer, nullable=False),
)


###


class CustomerReward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    reward_amount = db.Column(db.Float, nullable=False, default=0.0)

    customer = db.relationship("Customer", backref=db.backref("rewards", lazy=True))

    def __repr__(self):
        return f"<CustomerReward {self.id} - Customer ID: {self.customer_id}, Reward Amount: {self.reward_amount}>"


class Withdrawal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)  # Amount to be withdrawn
    status = db.Column(
        db.String(50), nullable=False, default="Pending"
    )  # Pending, Confirmed, etc.
    initiated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )  # Time of initiation
    confirmed_at = db.Column(
        db.DateTime, nullable=True
    )  # Time of confirmation (nullable since not confirmed yet)
    method = db.Column(
        db.String(50), nullable=False, default="Payment"
    )  # Initiation method (e.g., Payment, Withdrawal)

    # Relationship to Customer
    customer = db.relationship("Customer", backref=db.backref("withdrawals", lazy=True))

    def __repr__(self):
        return (
            f"<Withdrawal {self.id} - Customer ID: {self.customer_id}, "
            f"Amount: {self.amount}, Status: {self.status}, "
            f"Initiated At: {self.initiated_at}, Confirmed At: {self.confirmed_at}, "
            f"Method: {self.method}>"
        )


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # Store hashed password
    phone = db.Column(db.String(15), unique=True, nullable=False)
    region = db.Column(db.String(100), nullable=True)  # New field for region

    def __repr__(self):
        return (
            f"<Employee {self.id} - Username: {self.username}, "
            f"Phone: {self.phone}, Region: {self.region}>"
        )

    def set_password(self, password):
        """Hash the password for secure storage."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)


def init_db(app):
    with app.app_context():
        db.create_all()
