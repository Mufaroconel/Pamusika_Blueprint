import json
from dboperations import get_available_products_by_category


def request_user_name(whatsapp, username, phone):
    try:
        # Send the text requesting the user's full name
        whatsapp.send_text(
            to=phone,
            body=(
                f"🏷️Hi {username} Let's get you registered! Please provide the following details to complete your registration:\n\n"
                "1. *Full Name*: Please reply with your full name."
            ),
        )
        # Return True and success message on successful execution
        return True, "Request for user name sent successfully."

    except Exception as e:
        # Catch any exception and return False with the error message
        return False, f"Failed to request user name: {str(e)}"


def request_address(whatsapp, phone_number):
    try:
        # Send the text requesting the user's delivery address
        whatsapp.send_text(
            to=phone_number,
            body=(
                "🏠 Please provide your delivery address.\n\n"
                "To ensure accurate processing, please enter your address in the following format:\n"
                "1. House Number\n"
                "2. Street Name\n"
                "3. Suburb\n\n"
                "For example:\n"
                "69 Jiri Crescent, Mufakose\n\n"
                "Thank you!"
            ),
        )
        # Return True and success message on successful execution
        return True, "Request for delivery address sent successfully."

    except Exception as e:
        # Catch any exception and return False with the error message
        return False, f"Failed to request delivery address: {str(e)}"


def notify_address_suggestion(whatsapp, phone_number, suggestion):
    try:
        # Send a message suggesting the corrected address to the user
        whatsapp.send_text(
            to=phone_number,
            body=(
                f"🚨 It seems like there might be an error in the address you provided. "
                f"Did you mean **{suggestion}**? 🏠\n"
                "Please check and confirm or provide your correct address so we can assist you better."
            ),
        )
        # Return True and success message on successful execution
        return True, "Address suggestion sent successfully."

    except Exception as e:
        # Catch any exception and return False with the error message
        return False, f"Failed to send address suggestion: {str(e)}"


def notify_unavailable_service(whatsapp, phone_number):
    try:
        # Send the text notifying the user that services may be unavailable or address incorrect
        whatsapp.send_text(
            to=phone_number,
            body=(
                "🚫 It seems that the address you provided may be incorrect or services are not yet available in your area. "
                "Please double-check your address and try again. We're expanding soon, so stay tuned!"
            ),
        )
        # Return True and success message on successful execution
        return True, "Notification about service availability sent successfully."

    except Exception as e:
        # Catch any exception and return False with the error message
        return False, f"Failed to notify about service unavailability: {str(e)}"


def confirm_user_details(
    whatsapp, phone_number, username, name, address, ListSection, SectionRow
):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="🔍 Confirm Your Details",
            body=(
                f"Hi {username},\n\n"
                f"Please confirm that your details are correct:\n"
                f"*Full Name*: {name}\n"
                f"*Address*: {address}\n\n"
                "If everything looks good, please select an option below to continue:\n"
                "1. 🛒 *Confirm Registration*: Confirm your registration and proceed to place an order.\n"
                "2. 📝 *Edit Details*: Update your name or address.\n"
                "3. 🛠️ *Customer Support*: Get help from our support team."
                "4. 🛠️ *Profile*: View and Edit Your Details"
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="confirm_user_details",
                            title="Confirm",
                            description="Confirm user information.",
                        ),
                        SectionRow(
                            id="edit_details",
                            title="Edit Details",
                            description="Update your name or address.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
        return True, "Interactive list sent successfully."
    except Exception as e:
        return False, f"Failed to send interactive list: {str(e)}"


def registration_successful(whatsapp, phone_number, ListSection, SectionRow):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="🥭 Welcome to Pamusika!",
            body=(
                "🎉 You've successfully registered with Pamusika! We're excited to have you onboard. "
                "Now, explore our fresh produce straight from local farms. Order today and get it delivered to your doorstep. 🥬🍅\n\n"
                "Here’s what you can do next:\n"
                "1. 🛒 *Place an Order*: Select fresh fruits and vegetables.\n"
                "2. 🚚 *Track Your Order*: Check the status of your delivery.\n"
                "3. 🛠️ *Customer Support*: Get help if needed.\n"
                "4. 🛠️ *Profile*: View or update your details."
            ),
            button="Choose an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Browse fresh fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Track your delivery status.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="Need assistance? We're here to help.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User profile",
                            description="View and update your account details.",
                        ),
                    ],
                ),
            ],
        )
        return True, "Interactive list sent successfully."
    except Exception as e:
        return False, f"Failed to send interactive list: {str(e)}"


def greet_user_and_select_option(whatsapp, phone, username, ListSection, SectionRow):
    try:
        # Send an interactive list message
        whatsapp.send_interactive_list(
            to=phone,
            header=f"Hello {username} 🥭 Welcome to Pamusika!",
            body=(
                "Explore fresh fruits and vegetables from local farms, delivered to your doorstep. 🥬🍅\n\n"
                "Choose an option to get started:\n"
                "1. 🛒 *Place an Order*: Shop fresh produce.\n"
                "2. 🚚 *Track Your Order*: Follow your delivery.\n"
                "3. 🛠️ *Customer Support*: Get help if needed.\n"
                "4. 🧑‍💼 *Profile*: View and update your details."
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Shop fresh fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Track your delivery status.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="Get assistance if needed.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User Profile",
                            description="View or update your details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
        # Return True if successful
        return True, "Message sent successfully."

    except Exception as e:
        # Return False and error message if an exception occurs
        return False, f"Failed to send message: {str(e)}"


def notify_user_about_support_model(whatsapp, phone_number, ListSection, SectionRow):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="💬Customer Support!",
            body=(
                "⚠️ *Please Note:*\n\n"
                "Our customer support LLM model or agent is still under training, and we're continually working to improve its performance. "
                "We appreciate your understanding and patience as we strive to provide the best possible service.\n\n"
                "For any urgent issues, feel free to reach out to our human support team, who are always ready to assist you."
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Pick from our freshest selection of fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Stay updated on your delivery's progress.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User profile",
                            description="View and Edit Your Details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
        return True, "Interactive list sent successfully."
    except Exception as e:
        return False, f"Failed to send interactive list: {str(e)}"


def send_catalog(phone_number, catalog_id, whatsapp, CatalogSection, db_session):
    try:
        # Get available products grouped by category using the helper function
        catalog_sections = get_available_products_by_category(db_session)

        # Create CatalogSection dynamically from the product categories and meta IDs
        product_sections = [
            CatalogSection(title=category, retailer_product_ids=meta_ids)
            for category, meta_ids in catalog_sections.items()
        ]

        # Send the catalog product list message
        whatsapp.send_catalog_product_list(
            to=phone_number,  # Recipient's phone number
            catalog_id=catalog_id,  # The catalog ID to display
            header="🍎🥦 Available Fresh Produce at Musika 🥕🍊",
            body=(
                "🌟 Great! Let's get started with placing your order. I'll show you our catalog, and you can pick the items you'd like to buy. 🛒\n\n"
                "Musika in Mufakose Magandanga brings you the freshest produce, straight from the farm to your table! 🍅🍍"
            ),
            product_sections=product_sections,
            footer="Enjoy free delivery on all orders today! 🚚",
        )

        # Return True if successful
        return True, "Catalog sent successfully."

    except Exception as e:
        # Handle the exception and return the error
        return False, f"Failed to send catalog: {str(e)}"


def confirm_order_with_payment(
    whatsapp,
    phone_number,
    ListSection,
    SectionRow,
    total_amount,
    total_reward,
    fruits_items,
    vegetables_items,
    product_quantities,
    username,
    delivery_address,
):
    try:
        # Convert lists of items into formatted strings
        fruits_items_str = "\n".join(
            [
                f"{item['product']} * {item['quantity']} @{item['price']} each"
                for item in fruits_items
            ]
        )
        vegetables_items_str = "\n".join(
            [
                f"{item['product']} * {item['quantity']} @{item['price']} each"
                for item in vegetables_items
            ]
        )

        # Send the interactive list for order confirmation with payment method selection
        whatsapp.send_interactive_list(
            to=phone_number,
            header="🥭 Confirm Your Order",
            body=(
                f"Hi {username},\n\n"
                f"Here is a summary of your order:\n\n"
                f"Total Amount: ${total_amount:.2f}\n"
                f"Total Reward Balance: ${total_reward:.2f}\n\n"
                f"Delivery Address: {delivery_address}\n\n"
                f"Fruits Items:\n{fruits_items_str}\n\n"
                f"Vegetables Items:\n{vegetables_items_str}\n\n"
                "Please confirm your order and select a payment method to proceed."
            ),
            button="Select Payment",
            sections=[
                ListSection(
                    title="Payment Options",
                    rows=[
                        SectionRow(
                            id="pay_with_cash",
                            title="Cash on Delivery",  # 19 characters
                            description="Pay with cash on delivery.",
                        ),
                        SectionRow(
                            id="pay_with_rewards",
                            title="Use Rewards",  # Shortened to 11 characters
                            description="Use your rewards balance.",
                        ),
                        SectionRow(
                            id="edit_order",
                            title="Make Changes",  # 12 characters
                            description="Modify your order before confirming.",
                        ),
                        SectionRow(
                            id="cancel_order",
                            title="Cancel Order",  # 12 characters
                            description="Abort the order and restart.",
                        ),
                    ],
                ),
            ],
            footer="Please select a payment method.",
        )
        # Return True and success message on successful execution
        return True, "Order confirmation with payment method sent successfully."

    except Exception as e:
        # Catch any exception and return False with the error message
        return False, f"Failed to send order confirmation: {str(e)}"


def order_confirmed(whatsapp, phone_number, ListSection, SectionRow):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="🎉Order Confirmed!🎉",
            body=(
                "Congratulations! Your order has been successfully confirmed. 🛒🌟\n\n"
                "Our team is now preparing your fresh produce for delivery. 🚚🍅\n\n"
                "You can track your order’s journey or reach out to customer support for any assistance:\n\n"
                "2. 🚚 *Track Your Order*: Stay updated on your order's progress.\n"
                "3. 🛠️ *Customer Support*: Get help with any questions or concerns.\n\n"
                "4. 🛠️ *Profile*: View and Edit Your Details"
                "Thank you for choosing Pamusika - your source of farm-fresh goodness! 🥭🥦"
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Pick from our freshest selection of fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Stay updated on your delivery's progress.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User profile",
                            description="View and Edit Your Details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
        return True, "Order confirmation message sent successfully."
    except Exception as e:
        return False, f"Failed to send order confirmation message: {str(e)}"


def withdrawal_initiated(whatsapp, phone_number, ListSection, SectionRow):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="💵 Withdrawal Initiated!",
            body=(
                "Your withdrawal request has been successfully initiated. 🏦💰\n\n"
                "Our team is processing your request, and your cash will be delivered to your doorstep soon. 🚚💵\n\n"
                "You can manage your account or reach out to customer support for any assistance:\n\n"
                "1. 🏠 *View Profile*: Manage your personal details.\n"
                "2. 🛠️ *Customer Support*: Get help with any questions or concerns.\n\n"
                "Thank you for banking with us!"
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="user_profile",
                            title="User Profile",
                            description="Manage your personal details.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                    ],
                ),
            ],
            footer="Your cash will be delivered shortly. 🏦💵",
        )
        return True, "Withdrawal initiation message sent successfully."
    except Exception as e:
        return False, f"Failed to send withdrawal initiation message: {str(e)}"


def order_amount_restriction(
    whatsapp,
    phone_number,
    ListSection,
    SectionRow,
    total_amount,
    fruits_items,
    vegetables_items,
    product_quantities,
    customer_id,
    delivery_address,
):
    try:
        # Convert lists of items into formatted strings
        fruits_items_str = "\n".join(
            [
                f"{item['product']} * {item['quantity']} @{item['price']} each"
                for item in fruits_items
            ]
        )
        vegetables_items_str = "\n".join(
            [
                f"{item['product']} * {item['quantity']} @{item['price']} each"
                for item in vegetables_items
            ]
        )

        # Send the interactive list for order confirmation
        whatsapp.send_interactive_list(
            to=phone_number,
            header="🚫 Purchase Restriction 🚫",
            body=(
                f"Here's a summary of your order:\n\n"
                f"Customer ID: {customer_id}\n\n"
                f"Total Amount: ${total_amount:.2f}\n\n"
                f"Delivery Address: {delivery_address}\n\n"
                f"Fruits Items:\n{fruits_items_str}\n\n"
                f"Vegetables Items:\n{vegetables_items_str}\n\n"
                "Unfortunately, you cannot purchase items priced less than 50 cents.\n "
                "Please review your order and make necessary adjustments before proceeding.\n\n"
                "1. ✏️ *Make Changes*: Review and modify your order before finalizing.\n"
                "2. ❌ *Cancel*: Abort the current order process and start over."
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Order Confirmation",
                    rows=[
                        SectionRow(
                            id="edit_order",
                            title="Make Changes",
                            description="Modify your selection before finalizing.",
                        ),
                        SectionRow(
                            id="cancel_order",
                            title="Cancel",
                            description="Abort the order process and restart.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
        # Return True and success message on successful execution
        return True, "Order confirmation message sent successfully."

    except Exception as e:
        # Catch any exception and return False with the error message
        return False, f"Failed to send order confirmation: {str(e)}"


def order_cancelled(whatsapp, phone_number, ListSection, SectionRow):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="🚫 Order Cancelled 🚫",
            body=(
                "Your order has been successfully cancelled. 🙏\n\n"
                "If you have any questions or need assistance, please reach out to our customer support team.\n\n"
                "You can still place a new order or view your profile:\n\n"
                "1. 🛒 *Place an Order*: Pick from our freshest selection of fruits and vegetables.\n"
                "2. 👀 *User Profile*: View and Edit Your Details."
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Pick from our freshest selection of fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Stay updated on your delivery's progress.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User Profile",
                            description="View and Edit Your Details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
        return True, "Order cancellation message sent successfully."
    except Exception as e:
        return False, f"Failed to send order cancellation message: {str(e)}"


def make_changes(phone_number, catalog_id, whatsapp, CatalogSection):
    try:
        whatsapp.send_catalog_product_list(
            to=phone_number,
            catalog_id=catalog_id,
            header="🍎🥦 Available Fresh Produce at Musika 🥕🍊",
            body="🌟 No worries! Let's make those changes to your order. 🛒\n\nMusika in Mufakose Magandanga brings you the freshest produce, straight from the farm to your table! 🍅🍍",
            product_sections=[
                CatalogSection(
                    title="Fresh Fruits",
                    retailer_product_ids=["smdx1imjv1", "yv12oorgoj", "19tdnzbn2k"],
                ),
                CatalogSection(
                    title="Vegetables",
                    retailer_product_ids=[
                        "0oyglqcnhr",
                        "aqs54sejq9",
                        "ixxuzk2ll2",
                        "rq7l4wd0vr",
                        "kaif9wtpmq",
                        "4jenulsjmg",
                        "p95w970hrf",
                        "ddljtudt75",
                    ],
                ),
            ],
            footer="Enjoy free delivery on all orders today! 🚚",
        )
        return True, "Product catalog sent successfully."
    except Exception as e:
        return False, f"Failed to send product catalog: {str(e)}"


def handle_cancellation(whatsapp, phone_number, ListSection, SectionRow):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="📦 Order Status",
            body="❌ Your order has been canceled. If you change your mind, feel free to start over. 🌟🛒",
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Pick from our freshest selection of fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Stay updated on your delivery's progress.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User profile",
                            description="View and Edit Your Details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
        return True, "Cancellation message sent successfully."
    except Exception as e:
        return False, f"Failed to send cancellation message: {str(e)}"


def format_items(items):
    """Helper function to format items for display."""
    formatted_items = ""
    for item in items:
        formatted_items += f"{item['product']} (x{item['quantity']}) - ${item['price'] * item['quantity']}\n"
    return formatted_items.strip()


def sent_to_packaging(whatsapp, phone_number, order, ListSection, SectionRow):
    try:
        # Decode fruits and vegetables from JSON
        fruits = json.loads(order.fruits_items)
        vegetables = json.loads(order.vegetables_items)

        # Format the items
        fruits_formatted = format_items(fruits)
        vegetables_formatted = format_items(vegetables)

        whatsapp.send_interactive_list(
            to=phone_number,
            header="📦 Order Status",
            body=(
                f"📦 Your order (ID: {order.id}) currently being sent to packaging. It will be on its way soon! 🚚\n\n"
                f"🧾 *Total Amount*: ${order.total_amount}\n"
                f"📅 *Order Date*: {order.order_date}\n"
                f"🍎 *Fruits*:\n{fruits_formatted or 'No fruits ordered'}\n"
                f"🥦 *Vegetables*:\n{vegetables_formatted or 'No vegetables ordered'}"
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Pick from our freshest selection of fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Stay updated on your delivery's progress.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User profile",
                            description="View and Edit Your Details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
        return True, "Packaging status message sent successfully."
    except Exception as e:
        return False, f"Failed to send packaging status message: {str(e)}"


def packaging_received(whatsapp, phone_number, order, ListSection, SectionRow):
    try:
        # Decode fruits and vegetables from JSON
        fruits = json.loads(order.fruits_items)
        vegetables = json.loads(order.vegetables_items)

        # Format fruits and vegetables
        fruits = format_items(fruits) if order.fruits_items else "No fruits"
        vegetables = (
            format_items(vegetables) if order.vegetables_items else "No vegetables"
        )

        # Send WhatsApp message
        whatsapp.send_interactive_list(
            to=phone_number,
            header="📦 Order Status",
            body=f"🎉 Good news! Your order (ID: {order.id}) has been received by packaging. 🛠️\n\n"
            f"🧾 *Total Amount*: ${order.total_amount}\n"
            f"📅 *Order Date*: {order.order_date}\n"
            f"🍎 *Fruits*: {fruits}\n"
            f"🥦 *Vegetables*: {vegetables}",
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Pick from our freshest selection of fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Stay updated on your delivery's progress.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User profile",
                            description="View and Edit Your Details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
        return True, "Packaging received status message sent successfully."
    except Exception as e:
        return False, f"Failed to send packaging received message: {str(e)}"


def order_packed(whatsapp, phone_number, order, ListSection, SectionRow):
    try:
        # Decode fruits and vegetables from JSON
        fruits = json.loads(order.fruits_items)
        vegetables = json.loads(order.vegetables_items)

        # Format fruits and vegetables
        fruits = format_items(fruits) if order.fruits_items else "No fruits"
        vegetables = (
            format_items(vegetables) if order.vegetables_items else "No vegetables"
        )

        # Send WhatsApp message
        whatsapp.send_interactive_list(
            to=phone_number,
            header="📦 Order Status",
            body=(
                f"📦 Your order (ID: {order.id}) is packed and ready for delivery. Hang tight! 🚚\n\n"
                f"🧾 *Total Amount*: ${order.total_amount}\n"
                f"📅 *Order Date*: {order.order_date}\n"
                f"🍎 *Fruits*: {fruits}\n"
                f"🥦 *Vegetables*: {vegetables}"
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Pick from our freshest selection of fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Stay updated on your delivery's progress.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User Profile",
                            description="View and Edit Your Details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
        return True, "Packed order status message sent successfully."
    except Exception as e:
        return False, f"Failed to send packed order message: {str(e)}"


def order_on_way(whatsapp, phone_number, order, ListSection, SectionRow):
    try:
        # Decode fruits and vegetables from JSON
        fruits = json.loads(order.fruits_items)
        vegetables = json.loads(order.vegetables_items)

        # Format fruits and vegetables
        fruits = format_items(fruits) if order.fruits_items else "No fruits"
        vegetables = (
            format_items(vegetables) if order.vegetables_items else "No vegetables"
        )

        # Send WhatsApp message
        whatsapp.send_interactive_list(
            to=phone_number,
            header="📦 Order Status",
            body=f"🚚 Your order (ID: {order.id}) is on the way! It should arrive shortly. 🌟\n\n"
            f"🧾 *Total Amount*: ${order.total_amount}\n"
            f"📅 *Order Date*: {order.order_date}\n"
            f"🍎 *Fruits*: {fruits}\n"
            f"🥦 *Vegetables*: {vegetables}",
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Pick from our freshest selection of fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Stay updated on your delivery's progress.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User profile",
                            description="View and Edit Your Details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
        return True, "Order on the way status message sent successfully."
    except Exception as e:
        return False, f"Failed to send order on the way message: {str(e)}"


def order_delivered(
    whatsapp, phone_number, order, new_reward_balance, ListSection, SectionRow
):
    try:
        # Decode fruits and vegetables from JSON
        fruits = json.loads(order.fruits_items)
        vegetables = json.loads(order.vegetables_items)

        # Format fruits and vegetables
        fruits = format_items(fruits) if order.fruits_items else "No fruits"
        vegetables = (
            format_items(vegetables) if order.vegetables_items else "No vegetables"
        )

        # Send WhatsApp message
        whatsapp.send_interactive_list(
            to=phone_number,
            header="📦 Order Status",
            body=f"🎉 Your order (ID: {order.id}) has been delivered! Enjoy your purchase. 😊\n\n"
            f"🧾 *Total Amount*: ${order.total_amount}\n"
            f"📅 *Order Date*: {order.order_date}\n"
            f"🍎 *Fruits*: {fruits}\n"
            f"🥦 *Vegetables*: {vegetables}\n\n"
            f" Your new reward balance is: *${new_reward_balance:.2f}*",
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Pick from our freshest selection of fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Stay updated on your delivery's progress.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User profile",
                            description="View and Edit Your Details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
        return True, "Order delivered status message sent successfully."
    except Exception as e:
        return False, f"Failed to send order delivered message: {str(e)}"


def no_orders(whatsapp, phone_number, ListSection, SectionRow):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="📦 Order Status",
            body=(
                "🤔 Hmm, it looks like you don't have any orders at the moment.\n"
                "🛒 Do you wish to make any purchases or need assistance with something else?\n"
                "📞 You can always start by placing an order or contacting customer support."
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Pick from our freshest selection of fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Stay updated on your delivery's progress.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User profile",
                            description="View and Edit Your Details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
    except Exception as e:
        print(f"Error sending no orders message: {e}")


def tracking_issue(whatsapp, phone_number, ListSection, SectionRow):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="📦 Order Status",
            body="🤔 Hmm, I couldn't track your order right now. Please try again later.",
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Pick from our freshest selection of fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Stay updated on your delivery's progress.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User profile",
                            description="View and Edit Your Details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
    except Exception as e:
        print(f"Error sending tracking issue message: {e}")


def invalid_option(whatsapp, phone_number, ListSection, SectionRow):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="📦 Order Status",
            body="🚨 Oops! It seems like there was an error. Please select a valid option: order placement, order tracking, or customer support.",
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Pick from our freshest selection of fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Stay updated on your delivery's progress.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User profile",
                            description="View and Edit Your Details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
    except Exception as e:
        print(f"Error sending invalid option message: {e}")


def select_correct_option(whatsapp, phone_number, ListSection, SectionRow):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="🔍 Take your time to select the correct option",
            body=(
                "Discover the freshest fruits and vegetables, lovingly sourced from local farms. "
                "Whether you're stocking up on your favorites or exploring new flavors, we have everything you need. "
                "Order now and enjoy farm-fresh produce delivered right to your doorstep. 🥬🍅\n\n"
                "Choose from our options below to get started:\n"
                "1. 🛒 *Place an Order*: Fill your basket with the best fruits and vegetables.\n"
                "2. 🚚 *Track Your Order*: Follow your order’s journey from our market to your home.\n"
                "3. 🛠️ *Customer Support*: Need help? We're here for you.\n"
                "4. 🛠️ *Profile*: View and Edit Your Details"
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Pick from our freshest selection of fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Stay updated on your delivery's progress.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User profile",
                            description="View and Edit Your Details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
    except Exception as e:
        print(f"Error sending select correct option message: {e}")


def send_user_profile(
    whatsapp,
    phone_number,
    username,
    name,
    total_rewards_earned,
    address,
    ListSection,
    SectionRow,
):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="🛠️ Your Profile",
            body=(
                f"Hi {username},\n\n"
                f"Here are your current details:\n"
                f"*Full Name*: {name}\n"
                f"*Address*: {address}\n\n"
                f"Here are your total rewards earned: "
                f"*${total_rewards_earned:.2f}*\n"
                "What would you like to do next?"
            ),
            button="Choose an Option",
            sections=[
                ListSection(
                    title="Profile Actions",
                    rows=[
                        SectionRow(
                            id="edit_details",
                            title="Edit Details",
                            description="Update your name or address.",
                        ),
                        SectionRow(
                            id="withdraw_reward",
                            title="Withdraw Reward",
                            description="Initiate a reward withdrawal request.",
                        ),
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Pick from our freshest selection of fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Stay updated on your delivery's progress.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="We’re here to assist with any questions.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
    except Exception as e:
        print(f"Error sending user profile message: {e}")


def insufficient_balance_notification(
    whatsapp, phone_number, username, reward_balance, ListSection, SectionRow
):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="⚠️ Insufficient Balance",
            body=(
                f"Hi { username },\n\n"
                "Sorry!! You have insufficient balance to proceed with the withdrawal.\n"
                f"Your current balance is *${reward_balance:.2f}.*\n"
                "Buy more with Musika and earn more rewards to qualify for a withdrawal.\n\n"
                "Please enter a valid withdrawal amount or choose from the options below:"
            ),
            button="Choose an Option",
            sections=[
                ListSection(
                    title="Account Options",
                    rows=[
                        SectionRow(
                            id="exit_withdrawal",
                            title="Exit Withdrawal",
                            description="Cancel the withdrawal process.",
                        ),
                        SectionRow(
                            id="check_balance",
                            title="Check Balance",
                            description="View your current balance.",
                        ),
                    ],
                ),
            ],
            footer="Thank you for using our service!",
        )
        return True, "Insufficient balance message sent successfully."
    except Exception as e:
        return False, f"Failed to send insufficient balance message: {str(e)}"


import math


def insufficient_balance_for_order_notification(
    whatsapp,
    phone_number,
    username,
    reward_balance,
    total_order_amount,
    ListSection,
    SectionRow,
):
    try:
        # Calculate amounts
        amount_with_rewards = min(reward_balance, total_order_amount)
        amount_with_cash = total_order_amount - amount_with_rewards

        # Round down to 1 decimal place for rewards
        amount_with_rewards = math.floor(amount_with_rewards * 10) / 10
        # Round up to 1 decimal place for cash
        amount_with_cash = total_order_amount - amount_with_rewards

        whatsapp.send_interactive_list(
            to=phone_number,
            header="⚠️ Insufficient Balance for Payment",
            body=(
                f"Hi {username},\n\n"
                "Unfortunately, your rewards balance is insufficient to fully pay for your order.\n"
                f"Your current rewards balance is *${reward_balance:.2f}*.\n"
                f"The total amount due for your order is *${total_order_amount:.2f}*.\n\n"
                "Here's how you can pay:\n"
                f"- Use rewards to pay *${amount_with_rewards:.1f}*.\n"
                f"- Pay the remaining *${amount_with_cash:.1f}* in cash upon delivery.\n\n"
                "Please choose one of the options below to proceed:"
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Payment Options",
                    rows=[
                        SectionRow(
                            id="pay_with_rewards_and_delivery",
                            title="Pay with Rewards",
                            description="Use rewards & cash on delivery.",
                        ),
                        SectionRow(
                            id="pay_cash_on_delivery",
                            title="Cash on Delivery",
                            description="Full payment on delivery.",
                        ),
                        SectionRow(
                            id="edit_order",
                            title="Change Order",
                            description="Modify your order.",
                        ),
                        SectionRow(
                            id="cancel_order",
                            title="Cancel Order",
                            description="Abort the order.",
                        ),
                    ],
                ),
            ],
            footer="Thank you for shopping with us!",
        )
        return True, "Insufficient balance notification sent successfully."
    except Exception as e:
        return False, f"Failed to send insufficient balance notification: {str(e)}"


def insufficient_reward_balance(
    whatsapp,
    phone_number,
    username,
    balance,
    ListSection,
    SectionRow,
):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="⚠️ Insufficient Rewards Balance",
            body=(
                f"Hi {username},\n\n"
                "Unfortunately, your rewards balance is insufficient to pay for your order.\n"
                f"Your current rewards balance is *${balance:.2f}*.\n"
                # f"The total amount due for your order is *${total_order_amount:.2f}*.\n\n"
                # f"You will need to pay the remaining amount of *${amount_with_cash:.1f}* in cash upon delivery.\n\n"
                "Please choose one of the options below to proceed:"
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Payment Options",
                    rows=[
                        SectionRow(
                            id="pay_with_cash",
                            title="Cash on Delivery",
                            description="Full payment on delivery.",
                        ),
                        SectionRow(
                            id="edit_order",
                            title="Change Order",
                            description="Modify your order.",
                        ),
                        SectionRow(
                            id="cancel_order",
                            title="Cancel Order",
                            description="Abort the order.",
                        ),
                    ],
                ),
            ],
            footer="Thank you for shopping with us!",
        )
        return True, "Insufficient balance notification sent successfully."
    except Exception as e:
        return False, f"Failed to send insufficient balance notification: {str(e)}"


def minimum_withdrawal_warning(
    whatsapp, phone_number, username, ListSection, SectionRow
):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="⚠️ Minimum Withdrawal",
            body=(
                f"Hi {username},\n\n"
                "Sorry!! The minimum withdrawal amount is *$1*.\n"
                "Buy more with Musika and earn more rewards to qualify for a withdrawal.\n\n"
                "Please enter a valid amount or choose from the options below:"
            ),
            button="Choose an Option",
            sections=[
                ListSection(
                    title="Withdrawal Options",
                    rows=[
                        SectionRow(
                            id="exit_withdrawal",
                            title="Exit Withdrawal",
                            description="Cancel the withdrawal process.",
                        ),
                        SectionRow(
                            id="check_balance",
                            title="Check Balance",
                            description="View your current balance.",
                        ),
                    ],
                ),
            ],
            footer="Thank you for using our service!",
        )
        return True, "Minimum withdrawal warning sent successfully."
    except Exception as e:
        return False, f"Failed to send minimum withdrawal warning: {str(e)}"


def exit_withdrawal_message(whatsapp, phone, username, ListSection, SectionRow):
    try:
        # Send an interactive list message
        whatsapp.send_interactive_list(
            to=phone,
            header=f"Goodbye {username} 👋",
            body=(
                "You have successfully exited the withdrawal process.\n\n"
                "You can still purchase fresh fruits and vegetables using the options below:\n"
                "1. 🛒 *Place an Order*: Shop fresh produce.\n"
                "2. 🚚 *Track Your Order*: Follow your delivery.\n"
                "3. 🛠️ *Customer Support*: Get help if needed.\n"
                "4. 🧑‍💼 *Profile*: View and update your details."
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(
                            id="place_order",
                            title="Place an Order",
                            description="Shop fresh fruits and vegetables.",
                        ),
                        SectionRow(
                            id="track_order",
                            title="Track Your Order",
                            description="Track your delivery status.",
                        ),
                        SectionRow(
                            id="customer_support",
                            title="Customer Support",
                            description="Get assistance if needed.",
                        ),
                        SectionRow(
                            id="user_profile",
                            title="User Profile",
                            description="View or update your details.",
                        ),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights",
        )
        # Return True if successful
        return True, "Exit withdrawal message sent successfully."

    except Exception as e:
        # Return False and error message if an exception occurs
        return False, f"Failed to send exit withdrawal message: {str(e)}"


def confirm_withdrawal_message(
    whatsapp,
    phone_number,
    username,
    address,
    amount,
    ListSection,
    SectionRow,
):
    try:
        # Keep the structure similar to the working function
        whatsapp.send_interactive_list(
            to=phone_number,
            header="💵 Confirm Withdrawal",
            body=(
                f"Hi {username},\n\n"
                f"Withdraw *${amount}*?\n\n"
                "Delivery address for cash:\n"
                f"*{address}*\n\n"
            ),
            button="Choose an Option",
            sections=[
                ListSection(
                    title="Next Steps",
                    rows=[
                        SectionRow(
                            id="confirm_withdrawal",
                            title="Confirm",
                            description="Confirm withdrawal.",
                        ),
                        SectionRow(
                            id="edit_address",
                            title="Edit Address",
                            description="Change address.",
                        ),
                        SectionRow(
                            id="edit_amount",
                            title="Edit Amount",
                            description="Change withdrawal amount.",
                        ),
                    ],
                ),
            ],
            footer="Ensure address and amount are correct.",
        )
        return True, "Confirmation message sent successfully."
    except Exception as e:
        return False, f"Failed to send confirmation message: {str(e)}"


def rewards_balance(whatsapp, phone_number, username, balance, ListSection, SectionRow):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="💵 Your Current Balance",
            body=(
                f"Hi {username},\n\n"
                f"Your current balance is *${balance:.2f}*.\n\n"
                "Please enter an amount that is within your available balance to proceed with the withdrawal.\n\n"
            ),
            button="Choose an Option",
            sections=[
                ListSection(
                    title="Withdrawal Options",
                    rows=[
                        SectionRow(
                            id="exit_withdrawal",
                            title="Exit Withdrawal",
                            description="Cancel the withdrawal process.",
                        ),
                    ],
                ),
            ],
            footer="Ensure the amount is within your balance to avoid issues.",
        )
        return True, "Balance notification sent successfully."
    except Exception as e:
        return False, f"Failed to send balance notification: {str(e)}"


def send_edit_user_details_prompt(
    whatsapp, phone_number, username, name, address, ListSection, SectionRow
):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="📝 Update Your Details",
            body=(
                f"Hi {username},\n\n"
                "You have chosen to update your details.\n"
                "What would you like to update?\n\n"
                f"*Current Name*: {name}\n"
                f"*Current Address*: {address}\n\n"
                "Please choose an option below to edit your name or address:"
            ),
            button="Choose an Option",
            sections=[
                ListSection(
                    title="Update Options",
                    rows=[
                        SectionRow(
                            id="edit_name",
                            title="Edit Name",
                            description="Change your name.",
                        ),
                        SectionRow(
                            id="edit_address",
                            title="Edit Address",
                            description="Update your delivery address.",
                        ),
                    ],
                ),
            ],
            footer="Ensure the correct details for successful transactions.",
        )
        return True, "Edit details prompt sent successfully."
    except Exception as e:
        return False, f"Failed to send edit details prompt: {str(e)}"


def send_payment_method_prompt(
    whatsapp, phone_number, username, ListSection, SectionRow
):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="💳 Choose Payment Method",
            body=(
                f"Hi {username},\n\n"
                "Please select a payment method for your transaction:\n\n"
                "You can either pay with *Cash on Delivery* or use your *Rewards Balance*.\n\n"
                "Choose an option below to proceed:"
            ),
            button="Select Payment Method",
            sections=[
                ListSection(
                    title="Payment Options",
                    rows=[
                        SectionRow(
                            id="cash_on_delivery",
                            title="Cash on Delivery",
                            description="Pay with cash when your order is delivered.",
                        ),
                        SectionRow(
                            id="rewards_balance",
                            title="Use Rewards Balance",
                            description="Use your available rewards balance for this transaction.",
                        ),
                    ],
                ),
            ],
            footer="Select your preferred payment method to continue.",
        )
        return True, "Payment method prompt sent successfully."
    except Exception as e:
        return False, f"Failed to send payment method prompt: {str(e)}"
