# dboperations.py
from datetime import datetime
from models import db
from models import (
    Customer,
    Order,
    order_products,
    Product,
    CustomerReward,
    Withdrawal,
    ProductAvailability,
)

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
    meta_id, name, cost_price, selling_price, currency, product_category
):
    new_product = Product(
        id=str(uuid.uuid4()),  # Generate a unique ID for the product
        meta_id=meta_id,
        name=name,
        cost_price=cost_price,
        selling_price=selling_price,
        currency=currency,
        product_category=product_category,
    )

    try:
        db.session.add(new_product)
        db.session.commit()
        return new_product
    except Exception as e:
        db.session.rollback()
        print(f"Error adding product: {e}")
        return None


def add_product_availability(product_id, region, reward_amount, availability, quantity):
    new_availability = ProductAvailability(
        id=str(uuid.uuid4()),  # Generate a unique ID for the availability record
        product_id=product_id,
        region=region,
        reward_amount=reward_amount,
        availability=availability,
        quantity=quantity,
    )

    try:
        db.session.add(new_availability)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error adding product availability: {e}")


def get_products_by_region(employee_region):
    """Retrieve all products available in the specified region,
    along with their reward amounts from ProductAvailability."""

    # Fetch all product availability records for the specified region
    available_products = ProductAvailability.query.filter_by(
        region=employee_region
    ).all()

    if not available_products:
        print(f"No products found for region: {employee_region}")
        return []  # Return an empty list instead of None

    # Extract product IDs from the availability records
    product_ids = [availability.product_id for availability in available_products]

    # Fetch products corresponding to those IDs
    products = Product.query.filter(Product.id.in_(product_ids)).all()

    # Create a mapping of product_id to availability details
    reward_map = {
        availability.product_id: {
            "reward_amount": availability.reward_amount,
            "availability": availability.availability,
            "quantity": availability.quantity,
            "region": availability.region,  # Include region here
        }
        for availability in available_products
    }

    # Combine product data with reward information
    results = []
    for product in products:
        reward_info = reward_map.get(
            product.id,
            {
                "reward_amount": 0,
                "availability": False,
                "quantity": 0,
                "region": employee_region,
            },
        )

        results.append(
            {
                "product": product,
                **reward_info,  # Unpack the dictionary to add its keys and values
            }
        )

    return results


# Function to update an existing product
def update_product(
    product_id,
    meta_id,
    name,
    cost_price,
    selling_price,
    currency,
    product_category,
):
    product = Product.query.get(product_id)

    if not product:
        print(f"Product with ID {product_id} not found.")
        return None  # Explicitly return None if product is not found

    # Update fields
    product.meta_id = meta_id
    product.name = name
    product.cost_price = cost_price
    product.selling_price = selling_price
    product.currency = currency
    product.product_category = product_category

    try:
        db.session.commit()  # Commit changes to the database
        print(f"Product '{name}' updated successfully.")
        return product  # Return updated product
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        print(f"Error updating product: {e}")
        return None  # Return None on failure


def update_product_availability(
    product_id, region, reward_amount, availability, quantity
):
    availability_record = ProductAvailability.query.filter_by(
        product_id=product_id, region=region
    ).first()

    if availability_record:
        availability_record.availability = availability  # Update availability status
        availability_record.quantity = quantity  # Update quantity
        availability_record.reward_amount = reward_amount

        try:
            db.session.commit()  # Commit changes to the database
            print(
                f"Updated availability for Product ID: {product_id} in Region: {region}"
            )
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"Error updating product availability: {e}")
    else:
        print(
            f"No availability record found for Product ID: {product_id} in Region: {region}"
        )


# Function to delete a product by ID
def delete_product_by_id(product_id):
    product = get_product_by_id(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return product


def get_available_products_by_category(db_session, customer_region):
    """
    Queries the database to fetch available products based on their region.

    :param db_session: SQLAlchemy session to use for querying.
    :param customer_region: The region for which to check product availability.
    :return: Dictionary where keys are product categories and values are lists of product meta_ids.
    """
    try:
        # Query ProductAvailability for the specified region where availability is True
        available_products = (
            db_session.query(ProductAvailability)
            .filter_by(region=customer_region, availability=True)
            .all()
        )

        # Create a dictionary to group products by category
        catalog_sections = {}

        # Fetch product details for each available product
        for availability in available_products:
            product = (
                db_session.query(Product).filter_by(id=availability.product_id).first()
            )
            if product:
                # Group products by their category
                if product.product_category not in catalog_sections:
                    catalog_sections[product.product_category] = []
                catalog_sections[product.product_category].append(product.meta_id)

        return catalog_sections

    except Exception as e:
        # Optionally, log the exception or raise it to handle it in the calling function
        raise Exception(f"Error fetching products: {str(e)}")


# db_operations.py


def get_product_details(meta_id):
    """Fetch product name, price, and reward amount based on meta_id."""
    try:
        # Fetch product from Product table using meta_id
        product = Product.query.filter_by(meta_id=meta_id).first()

        if product:
            # Fetch availability from ProductAvailability table
            availability = ProductAvailability.query.filter_by(
                product_id=product.id
            ).first()

            return {
                "name": product.name,
                "price": product.selling_price,  # Assuming this is the correct field for selling price
                "reward_amount": availability.reward_amount if availability else 0.0,
            }

        return None  # Return None if the product is not found

    except Exception as e:
        print(f"Error fetching product details: {str(e)}")
        return None  # Return None in case of an error


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
        # Find the last pending withdrawal for the customer, sorted by the latest initiation date
        last_withdrawal = (
            Withdrawal.query.filter_by(customer_id=customer_id, status="Initiated")
            .order_by(Withdrawal.initiated_at.desc())
            .first()
        )

        if not last_withdrawal:
            print(f"No initiated withdrawals found for this customer {customer_id}.")
            return False, "No pending withdrawals found for this customer."

        # Store the amount before updating the status
        withdrawal_amount = (
            last_withdrawal.amount
        )  # Assuming 'amount' is a field in your Withdrawal model

        # Update the status to "Completed" and set the initiated_at timestamp
        last_withdrawal.status = "Completed"
        last_withdrawal.completed_at = (
            datetime.now()
        )  # You might want to track when it was completed

        # Commit the update to the database
        db.session.commit()

        print("Last pending withdrawal status updated to 'Completed' successfully.")
        return True, withdrawal_amount  # Return the amount of the completed withdrawal

    except Exception as e:
        print(f"Error updating withdrawal status: {e}")
        return False, "An error occurred while updating the withdrawal status."

    except SQLAlchemyError as e:
        # Roll back the session if there's an error
        print(f"An error occurred: {e}")
        db.session.rollback()


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


def get_customer_by_id(customer_id):
    """Query a customer by ID."""
    customer = Customer.query.get(customer_id)
    return customer


def get_all_orders(employee_region):
    """Retrieve all orders from customers in the same region as the logged-in employee,
    excluding those with status 'Delivered' or 'Cancelled', ordered by creation date in ascending order."""

    CustomerAlias = aliased(Customer)

    orders = (
        db.session.query(Order, CustomerAlias.name.label("customer_name"))
        .join(CustomerAlias, Order.customer_id == CustomerAlias.id)
        .filter(CustomerAlias.region == employee_region)  # Filter by employee's region
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
    product_quantities,  # Removed fruits_items and vegetables_items
):
    """
    Adds a new order to the database with associated products.

    Args:
        db: SQLAlchemy database instance.
        customer_id (int): The ID of the customer placing the order.
        total_amount (float): The total amount of the order.
        delivery_address (str): The address for order delivery.
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

    # Add the order to the session
    db.session.add(new_order)
    db.session.commit()  # Commit to get the order ID

    # Associate products with the order
    for (
        meta_id,
        quantity,
    ) in product_quantities:  # Assuming product_quantities now contains meta_ids
        # Ensure that the product exists in the database before adding
        product = Product.query.filter_by(meta_id=meta_id).first()  # Query by meta_id
        if product:
            # Add the product association with its quantity
            db.session.execute(
                order_products.insert().values(
                    order_id=new_order.id,
                    product_id=product.id,
                    quantity=quantity,  # Use product.id for association
                )
            )
        else:
            print(f"Product with meta ID {meta_id} does not exist.")
    # Commit the changes to the database
    db.session.commit()

    return new_order


def get_order_products(order_id):
    """
    Query the order_products table to retrieve products associated with a specific order.

    Args:
        order_id (int): The ID of the order for which to retrieve products.

    Returns:
        list: A list of dictionaries containing product details and quantities.
    """
    # Query the order_products association table
    results = db.session.execute(
        db.select(order_products).where(order_products.c.order_id == order_id)
    ).fetchall()

    # Prepare a list to hold product details
    order_products_details = []

    for result in results:
        product_id = result.product_id
        quantity = result.quantity

        # Fetch product details using the product_id
        product = Product.query.filter_by(
            id=product_id
        ).first()  # Assuming 'id' is the primary key

        if product:
            # Fetch availability to get reward amount
            availability = ProductAvailability.query.filter_by(
                product_id=product.id
            ).first()
            reward_amount = (
                availability.reward_amount if availability else 0.0
            )  # Default to 0 if not found

            order_products_details.append(
                {
                    "product_id": product.id,
                    "name": product.name,
                    "price": product.selling_price,  # Assuming this is the correct field for selling price
                    "quantity": quantity,
                    "reward_amount": reward_amount,
                }
            )
        else:
            print(f"Product with ID {product_id} not found.")

    return order_products_details


def query_orders(
    order_id=None, customer_id=None, status=None, start_date=None, end_date=None
):
    """
    Query orders from the database based on the provided filters.

    :param order_id: The ID of the order to retrieve (optional).
    :param customer_id: The ID of the customer whose orders to retrieve (optional).
    :param status: The status of the orders to retrieve (optional).
    :param start_date: The start date for filtering orders (optional).
    :param end_date: The end date for filtering orders (optional).
    :return: A list of Order objects matching the query.
    """
    query = Order.query

    if order_id:
        query = query.filter_by(id=order_id)
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    if status:
        query = query.filter_by(status=status)

    # Filter by order date range if provided
    if start_date:
        query = query.filter(Order.order_date >= start_date)
    if end_date:
        query = query.filter(Order.order_date <= end_date)

    return query.all()


##


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


def get_product_availability_by_product_id(product_id):
    """
    Retrieve the ProductAvailability record for a given product_id.

    :param product_id: The ID of the product to look up.
    :return: ProductAvailability object or None if not found.
    """
    try:
        # Query the ProductAvailability table for the specified product_id
        availability_record = (
            db.session.query(ProductAvailability)
            .filter_by(product_id=product_id)
            .first()
        )

        return availability_record  # Returns None if not found

    except Exception as e:
        print(f"Error fetching product availability: {str(e)}")
        return None  # Return None in case of an error


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


def get_reward_amount_for_order(order_id):
    try:
        # Find the order by order_id
        order = Order.query.filter_by(id=order_id).first()
        if not order:
            print("Order not found.")
            return None  # Return None if the order is not found

        # Return the reward amount for the specified order
        return order.reward_amount

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
            status="Initiated",  # Withdrawal is initiated with status Pending
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


def begin_withdrawal(amount, customer_id):
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


def update_last_order_status_to_sent_and_return_id(phone):
    try:
        # Find the customer by phone number
        customer = Customer.query.filter_by(phone=phone).first()
        if not customer:
            print("Customer not found.")
            return None

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
            return None

        # Check if the order status is "Pending"
        if last_order.status == "Pending":
            # Update the order status to "Sent to Packaging"
            last_order.status = "Sent to Packaging"

            # Commit the update to the database
            db.session.commit()

            print("Last order status updated to 'Sent to Packaging' successfully.")
            # Return the order ID of the updated order
            return last_order.id
        else:
            print("The last order status is not 'Pending'. No update performed.")
            return None

    except SQLAlchemyError as e:
        # Roll back the session if there's an error
        print(f"An error occurred: {e}")
        db.session.rollback()
        return None


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
