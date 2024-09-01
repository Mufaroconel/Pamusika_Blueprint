# dboperations.py
from models import db, Customer, Order
# from sqlalchemy.orm import joinedload
from sqlalchemy.orm import aliased





def add_customer(phone, username, address, surname, name, latitude=None, longitude=None):
    """Add a new customer to the database."""
    new_customer = Customer(
        phone=phone,
        username=username,
        address=address,
        latitude=latitude,
        longitude=longitude,
        surname=surname,
        name=name
    )
    db.session.add(new_customer)
    db.session.commit()
    return new_customer

def get_customer_by_phone(phone):
    """Query a customer by phone number."""
    customer = Customer.query.filter_by(phone=phone).first()
    return customer

def add_order(phone, delivery_address, total_amount, fruits_items, vegetables_items):
    """Add a new order with fruits and vegetables items."""
    customer = Customer.query.filter_by(phone=phone).first()
    customer_id = customer.id
    new_order = Order(
        customer_id=customer_id,
        delivery_address=delivery_address,
        total_amount=total_amount
    )
    
    new_order.set_fruits_items(fruits_items)
    new_order.set_vegetables_items(vegetables_items)
    
    db.session.add(new_order)
    db.session.commit()
    return new_order

def get_orders(phone):
    """Retrieve all orders associated with a given phone number."""
    customer = Customer.query.filter_by(phone=phone).first()
    
    if not customer:
        return None  # or raise an exception, or return an empty list

    # Then, retrieve the orders associated with this customer
    orders = Order.query.filter_by(customer_id=customer.id).all()

    return orders


def get_all_orders():
    """Retrieve all orders, including customer names, ordered by creation date in descending order."""
    # Aliasing Customer table for clearer reference
    CustomerAlias = aliased(Customer)
    
    # Join Order with Customer to get customer details
    orders = db.session.query(Order, CustomerAlias.name.label('customer_name')) \
        .join(CustomerAlias, Order.customer_id == CustomerAlias.id) \
        .order_by(Order.order_date.desc()) \
        .all()
    
    return orders





def update_order_status(order_id, new_status):
    """Update the status of an order."""
    
    # Ensure the new status is valid
    valid_statuses = ["Packaging received", "Packed", "Sent for delivery", "Delivered"]
    
    if new_status not in valid_statuses:
        raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}.")
    
    # Find the order by its ID
    order = Order.query.get(order_id)
    
    if not order:
        raise ValueError(f"Order with ID {order_id} does not exist.")
    
    # Update the status
    order.status = new_status
    
    # Commit the change to the database
    db.session.commit()
    
    return order

def get_filtered_orders(order_status=None, customer_name=None, order_id=None, customer_id=None):
    """Retrieve filtered orders based on provided criteria."""
    # Aliasing Customer table for clearer reference
    CustomerAlias = aliased(Customer)
    
    # Build the base query, joining Orders with Customers
    query = db.session.query(Order, CustomerAlias.name.label('customer_name')) \
        .join(CustomerAlias, Order.customer_id == CustomerAlias.id)
    
    # Apply filters based on input parameters
    if order_status:
        query = query.filter(Order.status == order_status)
    
    if customer_name:
        query = query.filter(CustomerAlias.name.ilike(f'%{customer_name}%'))
    
    if order_id:
        query = query.filter(Order.id == order_id)
    
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    
    # Order by creation date in descending order
    query = query.order_by(Order.order_date.desc())
    
    # Execute the query and return the results
    orders = query.all()
    
    return orders

def user_exists(phone):
    """
    Checks if a user exists in the database based on the provided phone number.
    
    :param phone_number: The phone number of the user to check.
    :return: True if the user exists, False otherwise.
    """
    user = Customer.query.filter_by(phone=phone).first()
    return user is not None