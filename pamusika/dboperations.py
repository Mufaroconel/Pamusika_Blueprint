# dboperations.py
from models import db
from models import Customer, Order, order_products, Product
# from sqlalchemy.orm import joinedload
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete

def delete_all_customers():
    with db.session.begin():  # Begin a new database session
        try:
            db.session.query(Customer).delete()  # Delete all records in the Customer table
            db.session.commit()  # Commit the transaction
            print("All customer records have been deleted.")
        except Exception as e:
            db.session.rollback()  # Rollback the transaction if there's an error
            print(f"An error occurred: {e}")

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

def add_customer_with_phone(phone):
    customer = Customer(phone=phone, state="collecting_name")
    db.session.add(customer)
    db.session.commit()
    return customer

def update_customer_name(phone, name):
    customer = Customer.query.filter_by(phone=phone).first()
    if customer:
        customer.name = name
        customer.state = "collecting_username"
        db.session.commit()
    return customer

def update_customer_username(phone, username):
    customer = Customer.query.filter_by(phone=phone).first()
    if customer:
        customer.username = username
        customer.state = "collecting_address"
        db.session.commit()
    return customer

def update_customer_address(phone, address, latitude=None, longitude=None):
    customer = Customer.query.filter_by(phone=phone).first()
    if customer:
        customer.address = address
        customer.latitude = latitude
        customer.longitude = longitude
        customer.state = None  # Registration completed
        db.session.commit()
    return customer

def get_customer_by_phone(phone):
    """Query a customer by phone number."""
    customer = Customer.query.filter_by(phone=phone).first()
    return customer

def get_all_orders():
    """Retrieve all orders, including customer names, ordered by creation date in descending order."""
    CustomerAlias = aliased(Customer)

    orders = db.session.query(Order, CustomerAlias.name.label('customer_name')) \
        .join(CustomerAlias, Order.customer_id == CustomerAlias.id) \
        .order_by(Order.order_date.desc()) \
        .all()
    
    return orders

def update_order_status(order_id, new_status):
    """Update the status of an order."""
    
    # Ensure the new status is valid
    valid_statuses = ["Packaging received", "Packed", "Sent for delivery", "Delivered", "Cancelled"]
    
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

def add_order(db, customer_id, total_amount, delivery_address, fruits_items, vegetables_items, product_quantities):
    """
    Adds a new order to the database with associated products.
    
    Args:
        db: SQLAlchemy database instance.
        customer_id (int): The ID of the customer placing the order.
        total_amount (float): The total amount of the order.
        delivery_address (str): The address for order delivery.
        fruits_items (list): List of fruits items to be included in the order.
        vegetables_items (list): List of vegetables items to be included in the order.
        product_quantities (list of tuples): Each tuple contains (product_id, quantity).
        
    Returns:
        Order: The created Order object.
    """
    # Create a new Order instance
    new_order = Order(
        customer_id=customer_id,
        total_amount=total_amount,
        delivery_address=delivery_address,
    )
    
    # Set the fruits and vegetables items
    new_order.set_fruits_items(fruits_items)
    new_order.set_vegetables_items(vegetables_items)
    
    # Add the order to the session
    db.session.add(new_order)
    db.session.commit()  # Commit to get the order ID
    
    # Associate products with the order
    for product_id, quantity in product_quantities:
        db.session.execute(order_products.insert().values(
            order_id=new_order.id,
            product_id=product_id,
            quantity=quantity
        ))
    
    # Commit the changes to the database
    db.session.commit()
    
    return new_order

def query_orders(order_id=None, customer_id=None, status=None):
    """
    Query orders from the database based on the provided filters.

    :param order_id: The ID of the order to retrieve (optional).
    :param customer_id: The ID of the customer whose orders to retrieve (optional).
    :param status: The status of the orders to retrieve (optional).
    :return: A list of Order objects matching the query.
    """
    query = Order.query
    
    if order_id:
        query = query.filter_by(id=order_id)
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    if status:
        query = query.filter_by(status=status)
    
    return query.all()

def add_product(id, meta_id, name, price, product_category, currency='USD', availability=True):
    """
    Add a new product to the Product table.

    :param id: Internal product ID (string)
    :param meta_id: Meta-specific ID for referencing (string)
    :param name: Name of the product (string)
    :param price: Price of the product (float)
    :param product_category: Category of the product (string)
    :param currency: Currency of the price (string, default 'USD')
    :param availability: Availability status (boolean, default True)
    """
    # Create a new Product instance with the given parameters
    new_product = Product(
        id=id,
        meta_id=meta_id,
        name=name,
        price=price,
        product_category=product_category,
        currency=currency,
        availability=availability
    )
    
    # Add the new product to the session and commit the transaction
    db.session.add(new_product)
    db.session.commit()

    return new_product

def get_products():
    """
    Retrieve all products from the Product table.
    
    :return: List of products
    """
    # Query the Product table for all records
    products = Product.query.all()
    return products

def get_product_name_and_category(meta_id):
    """
    Returns the product name and product category based on the meta_id.

    :param meta_id: The meta_id of the product (string)
    :return: A tuple containing the product name and category, or None if the product is not found
    """
    # Query the Product table to find the product with the given meta_id
    name_category = Product.query.filter_by(meta_id=meta_id).first()
    
    if name_category:
        return name_category
    else:
        return None

def cancel_last_order_by_phone(phone):
    try:
        # Find the customer by phone number
        customer = Customer.query.filter_by(phone=phone).first()
        if not customer:
            print("Customer not found.")
            return

        # Get the customer ID
        customer_id = customer.id

        # Find the last order for the customer, sorted by the latest order date
        last_order = Order.query.filter_by(customer_id=customer_id).order_by(Order.order_date.desc()).first()
        if not last_order:
            print("No orders found for this customer.")
            return

        # Update the order status to "Cancelled"
        last_order.status = "Cancelled"

        # Commit the update to the database
        db.session.commit()

        print("Last order status updated to 'Cancelled' successfully.")

    except SQLAlchemyError as e:
        # Roll back the session if there's an error
        print(f"An error occurred: {e}")
        db.session.rollback()

def get_active_orders_by_phone(phone):
    """Fetch all orders where the status is neither 'Cancelled' nor 'Delivered'."""
    try:
        # Find the customer by phone number
        customer = Customer.query.filter_by(phone=phone).first()
        if not customer:
            print("customer not found")
            return "Customer not found."
        else :
            print("customer found")
        # Get the customer ID
        customer_id = customer.id

        # Retrieve all orders for this customer where status is not 'Cancelled' or 'Delivered'
        active_orders = Order.query.filter(
            Order.customer_id == customer_id,
            Order.status.notin_(["Cancelled", "Delivered"])
        ).order_by(Order.order_date.desc()).all()

        if not active_orders:
            print("no orders found")
            return "No active orders found for this customer."
        else :
            print("orders found")
        # Return the list of active orders
        return active_orders

    except SQLAlchemyError as e:
        # Handle the database error
        print(f"An error occurred: {e}")
        return "An error occurred while fetching the active orders."

def delete_all_orders():
    """
    Delete all records from the Order table.
    """
    try:
        # Fetch all orders
        orders = Order.query.all()

        # Delete each order
        for order in orders:
            db.session.delete(order)
        
        # Commit the changes
        db.session.commit()
        print("All orders have been deleted.")
    except Exception as e:
        db.session.rollback()  # Rollback if something goes wrong
        print(f"Error deleting orders: {e}")

def delete_all_order_products():
    """Deletes all rows from the order_products table."""
    try:
        # Create the delete statement for the 'order_products' table
        db.session.execute(delete(order_products))
        db.session.commit()  # Commit the transaction to apply the changes
        print("All rows deleted successfully from the order_products table.")
    except Exception as e:
        db.session.rollback()  # Rollback in case of any error
        print(f"Error occurred while deleting rows: {str(e)}")