def greet_user_and_select_option(whatsapp, phone_number, ListSection, SectionRow):
    whatsapp.send_interactive_list(
        to=phone_number,
        header="🥭 Welcome to Pamusika!",
        body=(
            "Discover the freshest fruits and vegetables, lovingly sourced from local farms. "
            "Whether you're stocking up on your favorites or exploring new flavors, we have everything you need. "
            "Order now and enjoy farm-fresh produce delivered right to your doorstep. 🥬🍅\n\n"
            "Choose from our options below to get started:\n"
            "1. 🛒 **Place an Order**: Fill your basket with the best fruits and vegetables.\n"
            "2. 🚚 **Track Your Order**: Follow your order’s journey from our market to your home.\n"
            "3. 🛠️ **Customer Support**: Need help? We're here for you."
        ),
        button="Select an Option",
        sections=[
            ListSection(
                title="Your Next Steps",
                rows=[
                    SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                    SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                    SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                ],
            ),
        ],
        footer="#MufakoseHarvest #MagandangaDelights"
    )

def send_catalog(phone_number, catalog_id, whatsapp, CatalogSection):
    whatsapp.send_catalog_product_list(
    to=phone_number,  # Replace with the actual phone number
    catalog_id= catalog_id,  # Replace with your actual catalog ID
    header="🍎🥦 Available Fresh Produce at Musika 🥕🍊",
    body="🌟 Great! Let's get started with placing your order. I'll show you our catalog, and you can pick the items you'd like to buy. 🛒\n\nMusika in Mufakose Magandanga brings you the freshest produce, straight from the farm to your table! 🍅🍍",
    product_sections=[
        CatalogSection(
            title="Fresh Fruits", 
            retailer_product_ids=[
                "smdx1imjv1",  # Orange🍊
                "yv12oorgoj",  # Pineapple🍍
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
                "ddljtudt75",  # Apple🍎
            ]
        ),
    ],
    footer="Enjoy free delivery on all orders today! 🚚"
)
    
def confirm_order(whatsapp, phone_number, ListSection, SectionRow):
    whatsapp.send_interactive_list(
        to=phone_number,
        header="🥭 Confirm Your Order 📝",
        body=(
            "You've selected your items and we're ready to proceed. 🌟\n\n"
            "Would you like to confirm your order, make changes, or cancel? Choose an option below to continue:\n"
            "1. ✅ **Confirm Order**: Proceed with the current selection and finalize your purchase.\n"
            "2. ✏️ **Make Changes**: Review and modify your order before finalizing.\n"
            "3. ❌ **Cancel**: Abort the current order process and start over."
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

def order_confirmed(whatsapp, phone_number, ListSection, SectionRow):
    whatsapp.send_interactive_list(
        to=phone_number,
        header="🎉Order Confirmed!🎉",
         body = (
            "Congratulations! Your order has been successfully confirmed. 🛒🌟\n\n"
            "Our team is now preparing your fresh produce for delivery. 🚚🍅\n\n"
            "You can track your order’s journey or reach out to customer support for any assistance:\n\n"
            "1. 🚚 **Track Your Order**: Stay updated on your order's progress.\n"
            "2. 🛠️ **Customer Support**: Get help with any questions or concerns.\n\n"
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
                ],
            ),
        ],
        footer="#MufakoseHarvest #MagandangaDelights"
    )
def make_changes(phone_number, catalog_id, whatsapp, CatalogSection):
    whatsapp.send_catalog_product_list(
    to=phone_number,  
    catalog_id= catalog_id, 
    header="🍎🥦 Available Fresh Produce at Musika 🥕🍊",
    body="🌟 No worries! Let's make those changes to your order. 🛒\n\nMusika in Mufakose Magandanga brings you the freshest produce, straight from the farm to your table! 🍅🍍",
    product_sections=[
        CatalogSection(
            title="Fresh Fruits", 
            retailer_product_ids=[
                "smdx1imjv1",  # Orange🍊
                "yv12oorgoj",  # Pineapple🍍
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
                "ddljtudt75",  # Apple🍎
            ]
        ),
    ],
    footer="Enjoy free delivery on all orders today! 🚚"
)
    

def handle_cancellation(whatsapp, phone_number, ListSection, SectionRow):
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
                ],
            ),
        ],
        footer="#MufakoseHarvest #MagandangaDelights"
    )

def sent_to_packaging(whatsapp, phone_number, ListSection, SectionRow):
    whatsapp.send_interactive_list(
        to=phone_number,
        header="📦 Order Status",
        body="📦 Your order is curently being sent to packaging. It will be on its way soon! 🚚",
        button="Select an Option",
        sections=[
            ListSection(
                title="Your Next Steps",
                rows=[
                    SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                    SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                    SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                ],
            ),
        ],
        footer="#MufakoseHarvest #MagandangaDelights"
    )


def packaging_received(whatsapp, phone_number, ListSection, SectionRow):
    whatsapp.send_interactive_list(
        to=phone_number,
        header="📦 Order Status",
        body="🎉 Good news! Your order has been received by packaging. 🛠️",
        button="Select an Option",
        sections=[
            ListSection(
                title="Your Next Steps",
                rows=[
                    SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                    SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                    SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                ],
            ),
        ],
        footer="#MufakoseHarvest #MagandangaDelights"
    )

def order_packed(whatsapp, phone_number, ListSection, SectionRow):
    whatsapp.send_interactive_list(
        to=phone_number,
        header="📦 Order Status",
        body="📦 Your order is packed and ready for delivery. Hang tight! 🚚",
        button="Select an Option",
        sections=[
            ListSection(
                title="Your Next Steps",
                rows=[
                    SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                    SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                    SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                ],
            ),
        ],
        footer="#MufakoseHarvest #MagandangaDelights"
    )


def order_on_way(whatsapp, phone_number, ListSection, SectionRow):
    whatsapp.send_interactive_list(
        to=phone_number,
        header="📦 Order Status",
        body="🚚 Your order is on the way! It should arrive shortly. 🌟",
        button="Select an Option",
        sections=[
            ListSection(
                title="Your Next Steps",
                rows=[
                    SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                    SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                    SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                ],
            ),
        ],
        footer="#MufakoseHarvest #MagandangaDelights"
    )

def order_delivered(whatsapp, phone_number, ListSection, SectionRow):
    whatsapp.send_interactive_list(
        to=phone_number,
        header="📦 Order Status",
        body="🎉 Your order has been delivered! Enjoy your purchase. 😊",
        button="Select an Option",
        sections=[
            ListSection(
                title="Your Next Steps",
                rows=[
                    SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                    SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                    SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                ],
            ),
        ],
        footer="#MufakoseHarvest #MagandangaDelights"
    )

def no_orders(whatsapp, phone_number, ListSection, SectionRow):
    whatsapp.send_interactive_list(
        to=phone_number,
        header="📦 Order Status",
        body = (
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
                ],
            ),
        ],
        footer="#MufakoseHarvest #MagandangaDelights"
    )

def tracking_issue(whatsapp, phone_number, ListSection, SectionRow):
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
                ],
            ),
        ],
        footer="#MufakoseHarvest #MagandangaDelights"
    )

def invalid_option(whatsapp, phone_number, ListSection, SectionRow):
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
                ],
            ),
        ],
        footer="#MufakoseHarvest #MagandangaDelights"
    )

def select_correct_option(whatsapp, phone_number, ListSection, SectionRow):
    # Greet the user and prompt them to select an option
    whatsapp.send_interactive_list(
        to=phone_number,
        header="🔍 Take your time to select the correct option",
        body=(
            "Discover the freshest fruits and vegetables, lovingly sourced from local farms. "
            "Whether you're stocking up on your favorites or exploring new flavors, we have everything you need. "
            "Order now and enjoy farm-fresh produce delivered right to your doorstep. 🥬🍅\n\n"
            "Choose from our options below to get started:\n"
            "1. 🛒 **Place an Order**: Fill your basket with the best fruits and vegetables.\n"
            "2. 🚚 **Track Your Order**: Follow your order’s journey from our market to your home.\n"
            "3. 🛠️ **Customer Support**: Need help? We're here for you."
        ),
        button="Select an Option",
        sections=[
            ListSection(
                title="Your Next Steps",
                rows=[
                    SectionRow(id="place_order", title="Place an Order", description="Pick from our freshest selection of fruits and vegetables."),
                    SectionRow(id="track_order", title="Track Your Order", description="Stay updated on your delivery's progress."),
                    SectionRow(id="customer_support", title="Customer Support", description="We’re here to assist with any questions."),
                ],
            ),
        ],
        footer="#MufakoseHarvest #MagandangaDelights"
    )
