import json


def request_user_name(whatsapp, phone_number):
    try:
        # Send the text requesting the user's full name
        whatsapp.send_text(
            to=phone_number,
            body=(
                "🏷️ Let's get you registered! Please provide the following details to complete your registration:\n\n"
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
                "🏠 Finally, please provide your delivery address."
            ),
        )
        # Return True and success message on successful execution
        return True, "Request for delivery address sent successfully."
    
    except Exception as e:
        # Catch any exception and return False with the error message
        return False, f"Failed to request delivery address: {str(e)}"

def confirm_user_details(whatsapp, phone_number, name, address, ListSection, SectionRow):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="🔍 Confirm Your Details",
            body=(
                f"Hi {name},\n\n"
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
                        SectionRow(id="confirm_user_details", title="Confirm", description="Confirm user information."),
                        SectionRow(id="edit_details", title="Edit Details", description="Update your name or address."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
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
                "🎉 You have successfully registered an account with Pamusika! We're thrilled to have you with us. "
                "Now, it's time to explore our offerings:\n\n"
                "Discover the freshest fruits and vegetables, lovingly sourced from local farms. "
                "Whether you're stocking up on your favorites or exploring new flavors, we have everything you need. "
                "Order now and enjoy farm-fresh produce delivered right to your doorstep. 🥬🍅\n\n"
                "Choose from our options below to get started:\n"
                "1. 🛒 *Place an Order*: Fill your basket with the best fruits and vegetables.\n"
                "2. 🚚 *Track Your Order*: Follow your order’s journey from our market to your home.\n"
                "3. 🛠️ *Customer Support*: Need help? We're here for you."
                "4. 🛠️ *Profile*: View and Edit Your Details"
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
        )
        return True, "Interactive list sent successfully."
    except Exception as e:
        return False, f"Failed to send interactive list: {str(e)}"



def greet_user_and_select_option(whatsapp, phone, ListSection, SectionRow):
    try:
        # Construct and send the interactive list message
        whatsapp.send_interactive_list(
            to=phone,
            header="🥭 Welcome to Pamusika!",
            body=(
                "Discover the freshest fruits and vegetables, lovingly sourced from local farms. "
                "Whether you're stocking up on your favorites or exploring new flavors, we have everything you need. "
                "Order now and enjoy farm-fresh produce delivered right to your doorstep. 🥬🍅\n\n"
                "Choose from our options below to get started:\n"
                "1. 🛒 *Place an Order*: Fill your basket with the best fruits and vegetables.\n"
                "2. 🚚 *Track Your Order*: Follow your order’s journey from our market to your home.\n"
                "3. 🛠️ *Customer Support*: Need help? We're here for you.\n"
                "4. 🧑‍💼 *Profile*: View and Edit Your Details"
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User Profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
        )
        # If successful, return True and a success message
        return True, "Message sent successfully."
    
    except Exception as e:
        # If there's an error, return False and the error message
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
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
        )
        return True, "Interactive list sent successfully."
    except Exception as e:
        return False, f"Failed to send interactive list: {str(e)}"


def send_catalog(phone_number, catalog_id, whatsapp, CatalogSection):
    try:
        # Send the catalog product list message
        whatsapp.send_catalog_product_list(
            to=phone_number,  # Recipient's phone number
            catalog_id=catalog_id,  # The catalog ID to display
            header="🍎🥦 Available Fresh Produce at Musika 🥕🍊",
            body=(
                "🌟 Great! Let's get started with placing your order. I'll show you our catalog, and you can pick the items you'd like to buy. 🛒\n\n"
                "Musika in Mufakose Magandanga brings you the freshest produce, straight from the farm to your table! 🍅🍍"
            ),
            product_sections=[
                CatalogSection(
                    title="Fresh Fruits", 
                    retailer_product_ids=[
                        "smdx1imjv1",  # Orange🍊
                        "yv12oorgoj",  # Pineapple🍍
                        "ddljtudt75",  # Apple🍎
                        "19tdnzbn2k",  # Banana🍌
                    ]
                ),
                CatalogSection(
                    title="Vegetables", 
                    retailer_product_ids=[
                        "0oyglqcnhr",  # Tomato🍅
                        "aqs54sejq9",  # Carrot🥕
                        "ixxuzk2ll2",  # Rape🥬
                        "rq7l4wd0vr",  # Cabbage🥬
                        "kaif9wtpmq",  # Covo🥦
                        "4jenulsjmg",  # Green Pepper🫑
                        "p95w970hrf",  # Onion🧅
                    ]
                ),
            ],
            footer="Enjoy free delivery on all orders today! 🚚"
        )
        # If successful, return True and a success message
        return True, "Catalog sent successfully."
    
    except Exception as e:
        # If there's an error, return False and the error message
        return False, f"Failed to send catalog: {str(e)}"

    
def confirm_order(whatsapp, phone_number, ListSection, SectionRow, total_amount, fruits_items, vegetables_items, product_quantities, customer_id, delivery_address):
    try:
        # Convert lists of items into formatted strings
        fruits_items_str = "\n".join([f"{item['product']} * {item['quantity']} @{item['price']} each" for item in fruits_items])
        vegetables_items_str = "\n".join([f"{item['product']} * {item['quantity']} @{item['price']} each" for item in vegetables_items])

        # Send the interactive list for order confirmation
        whatsapp.send_interactive_list(
            to=phone_number,
            header="🥭 Confirm Your Order 📝",
            body=(
                f"Here's a summary of your order:\n\n"
                f"Customer ID: {customer_id}\n\n"
                f"Total Amount: ${total_amount:.2f}\n\n"
                f"Delivery Address: {delivery_address}\n\n"
                f"Fruits Items:\n{fruits_items_str}\n\n"
                f"Vegetables Items:\n{vegetables_items_str}\n\n"
                "Would you like to confirm your order, make changes, or cancel? Choose an option below to continue:\n"
                "1. ✅ *Confirm Order*: Proceed with the current selection and finalize your purchase.\n"
                "2. ✏️ *Make Changes*: Review and modify your order before finalizing.\n"
                "3. ❌ *Cancel*: Abort the current order process and start over."
            ),
            button="Select an Option",
            sections=[
                ListSection(
                    title="Order Confirmation",
                    rows=[
                        SectionRow(id="confirm_order", title="Confirm Order", description="Finalize and place your order."),
                        SectionRow(id="edit_order", title="Make Changes", description="Modify your selection before finalizing."),
                        SectionRow(id="cancel_order", title="Cancel", description="Abort the order process and restart."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
        )
        # Return True and success message on successful execution
        return True, "Order confirmation message sent successfully."

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
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
        )
        return True, "Order confirmation message sent successfully."
    except Exception as e:
        return False, f"Failed to send order confirmation message: {str(e)}"

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
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User Profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
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
                    retailer_product_ids=["smdx1imjv1", "yv12oorgoj", "19tdnzbn2k"]
                ),
                CatalogSection(
                    title="Vegetables", 
                    retailer_product_ids=["0oyglqcnhr", "aqs54sejq9", "ixxuzk2ll2", "rq7l4wd0vr", 
                                          "kaif9wtpmq", "4jenulsjmg", "p95w970hrf", "ddljtudt75"]
                ),
            ],
            footer="Enjoy free delivery on all orders today! 🚚"
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
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
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
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
        )
        return True, "Packaging status message sent successfully."
    except Exception as e:
        return False, f"Failed to send packaging status message: {str(e)}"


def packaging_received(whatsapp, phone_number, order, ListSection, SectionRow):
    try:
        # Format fruits and vegetables
        fruits = format_items(order.fruits_items) if order.fruits_items else "No fruits"
        vegetables = format_items(order.vegetables_items) if order.vegetables_items else "No vegetables"
        
        # Send WhatsApp message
        whatsapp.send_interactive_list(
            to=phone_number,
            header="📦 Order Status",
            body=f"🎉 Good news! Your order (ID: {order.order_id}) has been received by packaging. 🛠️\n\n"
                 f"🧾 *Total Amount*: ${order.total_amount}\n"
                 f"📅 *Order Date*: {order.order_date}\n"
                 f"🍎 *Fruits*: {fruits}\n"
                 f"🥦 *Vegetables*: {vegetables}",
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
        )
        return True, "Packaging received status message sent successfully."
    except Exception as e:
        return False, f"Failed to send packaging received message: {str(e)}"


def order_packed(whatsapp, phone_number, order, ListSection, SectionRow):
    try:
        # Format fruits and vegetables
        fruits = format_items(order.fruits_items) if order.fruits_items else "No fruits"
        vegetables = format_items(order.vegetables_items) if order.vegetables_items else "No vegetables"
        
        # Send WhatsApp message
        whatsapp.send_interactive_list(
            to=phone_number,
            header="📦 Order Status",
            body=f"📦 Your order (ID: {order.order_id}) is packed and ready for delivery. Hang tight! 🚚\n\n"
                 f"🧾 *Total Amount*: ${order.total_amount}\n"
                 f"📅 *Order Date*: {order.order_date}\n"
                 f"🍎 *Fruits*: {fruits}\n"
                 f"🥦 *Vegetables*: {vegetables}",
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
        )
        return True, "Packed order status message sent successfully."
    except Exception as e:
        return False, f"Failed to send packed order message: {str(e)}"


def order_on_way(whatsapp, phone_number, order, ListSection, SectionRow):
    try:
        # Format fruits and vegetables
        fruits = format_items(order.fruits_items) if order.fruits_items else "No fruits"
        vegetables = format_items(order.vegetables_items) if order.vegetables_items else "No vegetables"
        
        # Send WhatsApp message
        whatsapp.send_interactive_list(
            to=phone_number,
            header="📦 Order Status",
            body=f"🚚 Your order (ID: {order.order_id}) is on the way! It should arrive shortly. 🌟\n\n"
                 f"🧾 *Total Amount*: ${order.total_amount}\n"
                 f"📅 *Order Date*: {order.order_date}\n"
                 f"🍎 *Fruits*: {fruits}\n"
                 f"🥦 *Vegetables*: {vegetables}",
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
        )
        return True, "Order on the way status message sent successfully."
    except Exception as e:
        return False, f"Failed to send order on the way message: {str(e)}"


def order_delivered(whatsapp, phone_number, order, ListSection, SectionRow):
    try:
        # Format fruits and vegetables
        fruits = format_items(order.fruits_items) if order.fruits_items else "No fruits"
        vegetables = format_items(order.vegetables_items) if order.vegetables_items else "No vegetables"
        
        # Send WhatsApp message
        whatsapp.send_interactive_list(
            to=phone_number,
            header="📦 Order Status",
            body=f"🎉 Your order (ID: {order.order_id}) has been delivered! Enjoy your purchase. 😊\n\n"
                 f"🧾 *Total Amount*: ${order.total_amount}\n"
                 f"📅 *Order Date*: {order.order_date}\n"
                 f"🍎 *Fruits*: {fruits}\n"
                 f"🥦 *Vegetables*: {vegetables}",
            button="Select an Option",
            sections=[
                ListSection(
                    title="Your Next Steps",
                    rows=[
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
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
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
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
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
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
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
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
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                        SectionRow(id="user_profile", title="User profile", description="View and Edit Your Details."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
        )
    except Exception as e:
        print(f"Error sending select correct option message: {e}")

def send_user_profile(whatsapp, phone_number, name, address, ListSection, SectionRow):
    try:
        whatsapp.send_interactive_list(
            to=phone_number,
            header="🛠️ Your Profile",
            body=(
                f"Hi {name},\n\n"
                f"Here are your current details:\n"
                f"*Full Name*: {name}\n"
                f"*Address*: {address}\n\n"
                "What would you like to do next?"
            ),
            button="Choose an Option",
            sections=[
                ListSection(
                    title="Profile Actions",
                    rows=[
                        SectionRow(id="edit_details", title="Edit Details", description="Update your name or address."),
                        SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                        SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                        SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                    ],
                ),
            ],
            footer="#MufakoseHarvest #MagandangaDelights"
        )
    except Exception as e:
        print(f"Error sending user profile message: {e}")
