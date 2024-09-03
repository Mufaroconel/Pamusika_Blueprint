# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=True)  # Initially, this can be null
    address = db.Column(db.String(255), nullable=True)  # Initially, this can be null
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    name = db.Column(db.String(100), nullable=True)  # Initially, this can be null
    state = db.Column(db.String(20), nullable=True)  # Initially, this can be null

    def __repr__(self):
        return f"<Customer {self.id} - Phone: {self.phone}, Username: {self.username}, Name: {self.name}, State: {self.state}>"

    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(50), nullable=False, default="Sent to Packaging")
    total_amount = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)

    # Store items as JSON-encoded strings
    fruits_items = db.Column(db.Text, nullable=False)  # JSON-encoded string for fruits
    vegetables_items = db.Column(db.Text, nullable=False)  # JSON-encoded string for vegetables


    # Helper methods to encode and decode JSON data
    def set_fruits_items(self, items):
        """Set the fruits items by encoding them as a JSON string."""
        self.fruits_items = json.dumps(items)
    
    def get_fruits_items(self):
        """Get the fruits items by decoding the JSON string."""
        return json.loads(self.fruits_items)
    
    def set_vegetables_items(self, items):
        """Set the vegetables items by encoding them as a JSON string."""
        self.vegetables_items = json.dumps(items)
    
    def get_vegetables_items(self):
        """Get the vegetables items by decoding the JSON string."""
        return json.loads(self.vegetables_items)
    
    def __repr__(self):
        return f'<Order {self.id} - Status: {self.status}>'




def init_db(app):
        with app.app_context():
            db.create_all()

