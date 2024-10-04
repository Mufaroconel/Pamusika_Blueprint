# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()
db_session = db.session


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    username = db.Column(
        db.String(100), unique=True, nullable=True
    )  # Initially, this can be null
    address = db.Column(db.String(255), nullable=True)  # Initially, this can be null
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    name = db.Column(db.String(100), nullable=True)  # Initially, this can be null
    state = db.Column(db.String(20), nullable=True)  # Initially, this can be null

    def __repr__(self):
        return f"<Customer {self.id} - Phone: {self.phone}, Username: {self.username}, Name: {self.name}, State: {self.state}>"


class Product(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    meta_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    reward_amount = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(3), nullable=False, default="USD")
    availability = db.Column(db.Boolean, nullable=False, default=True)
    product_category = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return (
            f"<Product {self.name} - Category: {self.product_category} - "
            f"Meta ID: {self.meta_id} - Cost Price: {self.cost_price} - "
            f"Selling Price: {self.selling_price} - Reward: {self.reward_amount} {self.currency} - "
            f"Available: {self.availability}>"
        )


# class Order(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
#     order_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
#     status = db.Column(db.String(50), nullable=False, default="Pending")
#     total_amount = db.Column(db.Float, nullable=True)
#     delivery_address = db.Column(db.String(255), nullable=True)

#     # Store items as JSON-encoded strings
#     fruits_items = db.Column(db.Text, nullable=True)  # JSON-encoded string for fruits
#     vegetables_items = db.Column(
#         db.Text, nullable=True
#     )  # JSON-encoded string for vegetables

#     # New fields to store rewards
#     reward_amount = db.Column(
#         db.Float, nullable=False, default=0.0
#     )  # Total reward earned for this order
#     date = db.Column(
#         db.DateTime, nullable=False, default=datetime.now
#     )  # Date when reward was earned

#     def set_fruits_items(self, items):
#         """Set the fruits items by encoding them as a JSON string."""
#         self.fruits_items = json.dumps(items)

#     def get_fruits_items(self):
#         """Get the fruits items by decoding the JSON string."""
#         return json.loads(self.fruits_items)

#     def set_vegetables_items(self, items):
#         """Set the vegetables items by encoding them as a JSON string."""
#         self.vegetables_items = json.dumps(items)

#     def get_vegetables_items(self):
#         """Get the vegetables items by decoding the JSON string."""
#         return json.loads(self.vegetables_items)

#     def __repr__(self):
#         return (
#             f"<Order {self.id} - Status: {self.status}, Customer ID: {self.customer_id}, "
#             f"Order Date: {self.order_date}, Total: {self.total_amount}, "
#             f"Delivery Address: {self.delivery_address}, Reward Amount: {self.reward_amount}, "
#             f"Date: {self.date}>"
#         )


# order_products = db.Table(
#     "order_products",
#     db.Column("order_id", db.Integer, db.ForeignKey("order.id"), primary_key=True),
#     db.Column(
#         "product_id", db.String(50), db.ForeignKey("product.id"), primary_key=True
#     ),
#     db.Column("quantity", db.Integer, nullable=False),
# )

###


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
            product_details.append(f"{product.name}")  # Assuming 'name' is an attribute of Product

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


def init_db(app):
    with app.app_context():
        db.create_all()
