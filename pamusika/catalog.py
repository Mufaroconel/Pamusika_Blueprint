from wa_cloud_py import WhatsApp
from wa_cloud_py.message_components import CatalogSection


def send_catalog(phone_number, catalog_id, whatsapp):
    whatsapp.send_catalog_product_list(
    to=phone_number,  # Replace with the actual phone number
    catalog_id= catalog_id,  # Replace with your actual catalog ID
    header="🍎🥦 Available Fresh Produce at Musika 🥕🍊",
    body="🌟 Select a product and add it to your cart 🛒\n\nMusika in Mufakose Magandanga brings you the freshest produce, straight from the farm to your table! 🍅🍍",
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