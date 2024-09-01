# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    surname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return (f"<Order {self.id} - Date: {self.order_date}, Status: {self.status}, "
                f"Total Amount: {self.total_amount}, Delivery Address: {self.delivery_address}, "
                f"Fruits: {self.fruits_items}, Vegetables: {self.vegetables_items}>")
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    status = db.Column(db.String(50), nullable=False, default="Sent to Packaging")
    total_amount = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)
    
    # Store items as JSON-encoded strings
    fruits_items = db.Column(db.Text, nullable=False)  # JSON-encoded string
    vegetables_items = db.Column(db.Text, nullable=False)  # JSON-encoded string

    def __repr__(self):
        return f'<Order {self.id} - Status: {self.status}>'

    # Helper methods to encode and decode JSON data
    def set_fruits_items(self, items):
        self.fruits_items = json.dumps(items)
    
    def get_fruits_items(self):
        return json.loads(self.fruits_items)
    
    def set_vegetables_items(self, items):
        self.vegetables_items = json.dumps(items)
    
    def get_vegetables_items(self):
        return json.loads(self.vegetables_items)



def init_db(app):
        with app.app_context():
            db.create_all()

