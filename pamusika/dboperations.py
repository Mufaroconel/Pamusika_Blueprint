# dboperations.py
from datetime import datetime
from models import db
from models import Customer, Order, order_products, Product, CustomerReward, Withdrawal

# from sqlalchemy.orm import joinedload
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete, desc
import uuid
from Pamusika_Investment_Rewards.reward_calculator import calculate_reward


# Function to get all products
def get_all_products():
    return Product.query.all()


# Function to get product by ID
def get_product_by_id(product_id):
    return Product.query.get(product_id)


# Function to add a new product
def add_new_product(
    meta_id, name, cost_price, selling_price, currency, product_category, availability
):
    reward_amount = calculate_reward(cost_price, selling_price)  # Calculate reward
    new_product = Product(
        id=str(uuid.uuid4()),  # Generate a unique UUID
        meta_id=meta_id,
        name=name,
        cost_price=cost_price,
        selling_price=selling_price,
        reward_amount=reward_amount,  # Set reward amount
        currency=currency,
        product_category=product_category,
        availability=availability,
    )
    db.session.add(new_product)
    db.session.commit()
    return new_product


# Function to update an existing product
def update_product(
    product_id,
    meta_id,
    name,
    cost_price,
    selling_price,
    currency,
    product_category,
    availability,
):
    product = Product.query.get(product_id)
    if product:
        product.meta_id = meta_id
        product.name = name
        product.cost_price = cost_price
        product.selling_price = selling_price
        product.reward_amount = calculate_reward(
            cost_price, selling_price
        )  # Recalculate reward
        product.currency = currency
        product.product_category = product_category
        product.availability = availability
        db.session.commit()
    return product


# Function to delete a product by ID
def delete_product_by_id(product_id):
    product = get_product_by_id(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return product


def get_available_products_by_category(db_session):
    """
    Queries the database to fetch available products and group them by category.

    :param db_session: SQLAlchemy session to use for querying.
    :return: Dictionary where keys are product categories and values are lists of meta_ids.
    """
    try:
        # Query products from the database where availability is True
        products = db_session.query(Product).filter_by(availability=True).all()

        # Create a dictionary to group products by category
        catalog_sections = {}
        for product in products:
            if product.product_category not in catalog_sections:
                catalog_sections[product.product_category] = []
            catalog_sections[product.product_category].append(product.meta_id)

        return catalog_sections

    except Exception as e:
        # Optionally, log the exception or raise it to handle it in the calling function
        raise Exception(f"Error fetching products: {str(e)}")


def delete_all_customers():
    with db.session.begin():  # Begin a new database session
        try:
            db.session.query(
                Customer
            ).delete()  # Delete all records in the Customer table
            db.session.commit()  # Commit the transaction
            print("All customer records have been deleted.")
        except Exception as e:
            db.session.rollback()  # Rollback the transaction if there's an error
            print(f"An error occurred: {e}")


def add_customer(
    phone, username, address, surname, name, latitude=None, longitude=None
):
    """Add a new customer to the database and initialize their rewards."""

    # Create a new customer
    new_customer = Customer(
        phone=phone,
        username=username,
        address=address,
        latitude=latitude,
        longitude=longitude,
        surname=surname,
        name=name,
    )

    # Add the new customer to the database session
    db.session.add(new_customer)
    db.session.commit()  # Commit so that the new customer gets a customer ID

    # Initialize the reward for the new customer
    customer_reward = CustomerReward(
        customer_id=new_customer.id,  # Use the newly created customer ID
        reward_amount=0.0,  # Initialize with a default reward amount of 0
    )

    # Add the customer reward to the database session
    db.session.add(customer_reward)
    db.session.commit()  # Commit the reward record

    return new_customer


def add_customer_reward(customer_id, reward_amount=0.0):
    """Add a new reward record for a customer."""
    try:
        # Check if the customer exists
        customer = Customer.query.get(customer_id)
        if not customer:
            print(f"Customer with ID {customer_id} does not exist.")
            return None

        # Create a new CustomerReward record
        new_reward = CustomerReward(
            customer_id=customer.id,  # Use the existing customer ID
            reward_amount=reward_amount,  # Set the initial reward amount
        )

        # Add the new reward to the database session
        db.session.add(new_reward)
        db.session.commit()  # Commit the new record

        print(
            f"Reward record added for customer ID {customer_id} with amount {reward_amount}."
        )
        return new_reward

    except Exception as e:
        db.session.rollback()  # Rollback the session on error
        print(f"Error adding reward for customer ID {customer_id}: {e}")
        return None


def add_to_reward(customer_id, amount):
    """Add to the customer's reward amount."""

    # Find the customer's reward record by customer_id
    customer_reward = CustomerReward.query.filter_by(customer_id=customer_id).first()

    if customer_reward:
        # Add the specified amount to the current reward amount
        customer_reward.reward_amount += amount
        db.session.commit()
        return customer_reward.reward_amount
    else:
        raise ValueError(f"No reward record found for customer ID: {customer_id}")


def subtract_from_reward(customer_id, amount):
    """Subtract from the customer's reward amount."""
    try:
        customer_reward = CustomerReward.query.filter_by(
            customer_id=customer_id
        ).first()

        if not customer_reward:
            return None, f"No reward record found for customer ID: {customer_id}"

        if amount > customer_reward.reward_amount:
            return (
                None,
                f"Insufficient reward balance. Customer ID {customer_id} has only {customer_reward.reward_amount}.",
            )

        customer_reward.reward_amount -= amount
        db.session.commit()
        return customer_reward.reward_amount, None
    except SQLAlchemyError as e:
        db.session.rollback()
        return None, f"An error occurred while subtracting rewards: {str(e)}"


def update_withdrawal_status_to_completed(customer_id):
    try:
        # Find the latest pending withdrawal for the given customer
        last_withdrawal = (
            Withdrawal.query.filter_by(customer_id=customer_id, status="Initiated")
            .order_by(Withdrawal.initiated_at.desc())
            .first()
        )

        # Check if any pending withdrawal was found
        if not last_withdrawal:
            print(f"No pending withdrawals found for customer ID {customer_id}.")
            return False, "No pending withdrawals."

        # Update the status to "Completed"
        last_withdrawal.status = "Completed"
        last_withdrawal.confirmed_at = datetime.now()  # Set the confirmation time

        # Commit the changes to the database
        db.session.commit()

        print(
            f"Withdrawal ID {last_withdrawal.id} marked as 'Completed' for customer ID {customer_id}."
        )
        return True, "Withdrawal status updated to 'Completed'."

    except Exception as e:
        # Roll back the session in case of an error
        db.session.rollback()
        print(f"An error occurred: {str(e)}")
        return False, f"Error: {str(e)}"


def get_withdrawal_by_id(withdrawal_id):
    """Fetch the withdrawal record by ID."""
    try:
        withdrawal = Withdrawal.query.get(withdrawal_id)
        return withdrawal, None
    except SQLAlchemyError as e:
        return None, f"An error occurred while fetching the withdrawal: {str(e)}"


def confirm_withdrawal(withdrawal):
    """Update the withdrawal status."""
    try:
        withdrawal.status = "Confirmed"
        db.session.commit()
        return None
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"An error occurred while confirming the withdrawal: {str(e)}"


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
    """Retrieve all orders, excluding those with status 'Delivered' or 'Cancelled', ordered by creation date in descending order."""
    CustomerAlias = aliased(Customer)

    orders = (
        db.session.query(Order, CustomerAlias.name.label("customer_name"))
        .join(CustomerAlias, Order.customer_id == CustomerAlias.id)
        .filter(Order.status.notin_(["Delivered", "Cancelled"]))
        .order_by(Order.order_date.asc())
        .all()
    )

    return orders


def update_order_status(order_id, new_status):
    """Update the status of an order."""

    # Ensure the new status is valid
    valid_statuses = [
        "Packaging received",
        "Packed",
        "Sent for delivery",
        "Delivered",
        "Cancelled",
    ]

    if new_status not in valid_statuses:
        raise ValueError(
            f"Invalid status: {new_status}. Must be one of {valid_statuses}."
        )

    # Find the order by its ID
    order = Order.query.get(order_id)

    if not order:
        raise ValueError(f"Order with ID {order_id} does not exist.")

    # Update the status
    order.status = new_status

    # Commit the change to the database
    db.session.commit()

    return order


def get_last_pending_order_total(customer_id):
    """
    Retrieve the total amount for the last order with status 'Pending'
    for a specific customer based on their customer_id.
    """

    # Query for the last pending order for the specific customer
    last_pending_order = (
        Order.query.filter_by(status="Pending", customer_id=customer_id)
        .order_by(desc(Order.order_date))
        .first()
    )

    # Check if any pending order was found for the customer
    if not last_pending_order:
        raise ValueError(f"No pending orders found for customer ID {customer_id}.")

    # Return the total amount of the last pending order
    return last_pending_order.total_amount


def get_last_pending_withdrawal(customer_id):
    """
    Retrieve the last pending withdrawal for a specific customer based on their customer_id.
    """

    # Query for the last pending withdrawal for the specific customer
    last_pending_withdrawal = (
        Withdrawal.query.filter_by(status="Pending", customer_id=customer_id)
        .order_by(desc(Withdrawal.initiated_at))
        .first()
    )

    # Check if any pending withdrawal was found for the customer
    if not last_pending_withdrawal:
        raise ValueError(f"No pending withdrawals found for customer ID {customer_id}.")

    # Return the last pending withdrawal object
    return last_pending_withdrawal


def get_filtered_orders(
    order_status=None, customer_name=None, order_id=None, customer_id=None
):
    """Retrieve filtered orders based on provided criteria."""
    # Aliasing Customer table for clearer reference
    CustomerAlias = aliased(Customer)

    # Build the base query, joining Orders with Customers
    query = db.session.query(Order, CustomerAlias.name.label("customer_name")).join(
        CustomerAlias, Order.customer_id == CustomerAlias.id
    )

    # Apply filters based on input parameters
    if order_status:
        query = query.filter(Order.status == order_status)

    if customer_name:
        query = query.filter(CustomerAlias.name.ilike(f"%{customer_name}%"))

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


def add_order(
    db,
    customer_id,
    total_amount,
    reward_amount,
    delivery_address,
    fruits_items,
    vegetables_items,
    product_quantities,
):
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
        reward_amount=reward_amount,
    )

    # Set the fruits and vegetables items
    new_order.set_fruits_items(fruits_items)
    new_order.set_vegetables_items(vegetables_items)

    # Add the order to the session
    db.session.add(new_order)
    db.session.commit()  # Commit to get the order ID

    # Associate products with the order
    for product_id, quantity in product_quantities:
        db.session.execute(
            order_products.insert().values(
                order_id=new_order.id, product_id=product_id, quantity=quantity
            )
        )

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


def add_product(
    id, meta_id, name, price, product_category, currency="USD", availability=True
):
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
        availability=availability,
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


def get_reward_amount_for_last_order(phone):
    try:
        # Find the customer by phone number
        customer = Customer.query.filter_by(phone=phone).first()
        if not customer:
            print("Customer not found.")
            return None  # Return None if the customer is not found

        # Get the customer ID
        customer_id = customer.id

        # Find the last pending order for the customer, sorted by the latest order date
        last_pending_order = (
            Order.query.filter_by(customer_id=customer_id, status="Pending")
            .order_by(Order.order_date.desc())
            .first()
        )
        if not last_pending_order:
            print("No pending orders found for this customer.")
            return None  # Return None if no pending orders are found

        # Return the reward amount from the last pending order
        return last_pending_order.reward_amount

    except SQLAlchemyError as e:
        # Handle the error and rollback if necessary
        print(f"An error occurred: {e}")
        db.session.rollback()
        return None  # Return None on error


def get_total_reward_for_customer(phone):
    try:
        # Find the customer by phone number
        customer = Customer.query.filter_by(phone=phone).first()
        if not customer:
            print("Customer not found.")
            return None  # Return None if the customer is not found

        # Get the customer ID
        customer_id = customer.id

        # Find the reward record for the customer in the CustomerReward table
        customer_reward = CustomerReward.query.filter_by(
            customer_id=customer_id
        ).first()
        if not customer_reward:
            print("No reward record found for this customer.")
            return 0.0  # Return 0 if no reward record is found

        # Return the reward amount
        return customer_reward.reward_amount

    except SQLAlchemyError as e:
        # Handle the error and rollback if necessary
        print(f"An error occurred: {e}")
        db.session.rollback()
        return None  # Return None on error


def initiate_withdrawal(amount, customer_id):
    try:
        # Check if the customer exists
        customer = Customer.query.get(customer_id)
        if not customer:
            print(f"Customer with ID {customer_id} not found.")
            return None

        # Create a new withdrawal record
        new_withdrawal = Withdrawal(
            customer_id=customer_id,
            amount=amount,
            status="Pending",  # Withdrawal is initiated with status Pending
            initiated_at=datetime.now(),
            method="Withdrawal",  # Default method, can be updated based on context
        )

        # Add the new withdrawal to the session and commit to the database
        db.session.add(new_withdrawal)
        db.session.commit()

        print(f"Withdrawal of {amount} initiated for Customer ID {customer_id}.")
        return new_withdrawal  # Return the created withdrawal object

    except SQLAlchemyError as e:
        # Handle any database errors and rollback the transaction
        print(f"An error occurred: {e}")
        db.session.rollback()
        return None  # Return None on error


def get_pending_withdrawals():
    try:
        # Query to fetch all withdrawals with status "Pending"
        pending_withdrawals = Withdrawal.query.filter_by(status="Initiated").all()

        if not pending_withdrawals:
            print("No pending withdrawals found.")
            return []  # Return an empty list if no pending withdrawals are found

        return pending_withdrawals  # Return the list of pending withdrawals

    except SQLAlchemyError as e:
        # Handle any database errors
        print(f"An error occurred: {e}")
        return []  # Return an empty list on error


def update_last_order_status_to_sent(phone):
    try:
        # Find the customer by phone number
        customer = Customer.query.filter_by(phone=phone).first()
        if not customer:
            print("Customer not found.")
            return

        # Get the customer ID
        customer_id = customer.id

        # Find the last order for the customer, sorted by the latest order date
        last_order = (
            Order.query.filter_by(customer_id=customer_id)
            .order_by(Order.order_date.desc())
            .first()
        )
        if not last_order:
            print("No orders found for this customer.")
            return

        # Check if the order status is "Pending"
        if last_order.status == "Pending":
            # Update the order status to "Sent to Packaging"
            last_order.status = "Sent to Packaging"

            # Commit the update to the database
            db.session.commit()

            print("Last order status updated to 'Sent to Packaging' successfully.")
        else:
            print("The last order status is not 'Pending'. No update performed.")

    except SQLAlchemyError as e:
        # Roll back the session if there's an error
        print(f"An error occurred: {e}")
        db.session.rollback()

    except SQLAlchemyError as e:
        # Roll back the session if there's an error
        print(f"An error occurred: {e}")
        db.session.rollback()


def update_latest_pending_order_total(customer_id, new_total):
    try:
        # Find the latest order with status 'Pending' for the customer
        order = (
            Order.query.filter_by(customer_id=customer_id, status="Pending")
            .order_by(Order.order_date.desc())
            .first()
        )

        # If no pending order is found, return an error
        if not order:
            return False, f"No pending orders found for customer ID {customer_id}."

        # Update the total amount
        order.total_amount = new_total

        # Commit the changes to the database
        db.session.commit()

        return True, f"Order ID {order.id} updated with new total: ${new_total:.2f}."
    
    except Exception as e:
        # Roll back in case of error
        db.session.rollback()
        return False, f"Failed to update order total: {str(e)}"


def update_last_withdrawal_status_to_initiated(customer_id):
    try:
        # Find the last pending withdrawal for the customer, sorted by the latest initiation date
        last_withdrawal = (
            Withdrawal.query.filter_by(customer_id=customer_id, status="Pending")
            .order_by(Withdrawal.initiated_at.desc())
            .first()
        )
        if not last_withdrawal:
            print("No pending withdrawals found for this customer.")
            return

        # Update the status to "Initiated" and set the initiated_at timestamp
        last_withdrawal.status = "Initiated"
        last_withdrawal.initiated_at = datetime.now()

        # Commit the update to the database
        db.session.commit()

        print("Last pending withdrawal status updated to 'Initiated' successfully.")

    except SQLAlchemyError as e:
        # Roll back the session if there's an error
        print(f"An error occurred: {e}")
        db.session.rollback()


def cancel_last_order_by_phone(phone):
    try:
        # Find the customer by phone number
        customer = Customer.query.filter_by(phone=phone).first()
        if not customer:
            print("Customer not found.")
            return

        # Get the customer ID
        customer_id = customer.id

        # Find the last pending order for the customer, sorted by the latest order date
        last_order = (
            Order.query.filter_by(customer_id=customer_id, status="Pending")
            .order_by(Order.order_date.desc())
            .first()
        )
        if not last_order:
            print("No pending orders found for this customer.")
            return

        # Update the order status to "Cancelled"
        last_order.status = "Cancelled"

        # Commit the update to the database
        db.session.commit()

        print("Last pending order status updated to 'Cancelled' successfully.")

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
        else:
            print("customer found")
        # Get the customer ID
        customer_id = customer.id

        # Retrieve all orders for this customer where status is not 'Cancelled' or 'Delivered'
        active_orders = (
            Order.query.filter(
                Order.customer_id == customer_id,
                Order.status.notin_(["Cancelled", "Delivered"]),
            )
            .order_by(Order.order_date.desc())
            .all()
        )

        if not active_orders:
            print("no orders found")
            return "No active orders found for this customer."
        else:
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
