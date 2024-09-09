from wa_cloud_py import WhatsApp
from dotenv import load_dotenv
import os
from wa_cloud_py.message_components import ListSection, SectionRow
from messages.payment_method import which_payment_method
from messages.confirm_payment import confirm_payment
from messages.text_messages import GreetingMessages, InformationalMessages, ConfirmationMessages, ErrorMessages, PromotionalMessages
from messages.send_image import send_image
from messages.app_logic_messages import greet_user_and_select_option, send_catalog, confirm_order,order_confirmed,make_changes, handle_cancellation,sent_to_packaging, packaging_received, order_packed, order_on_way, order_delivered, no_orders, tracking_issue, invalid_option, select_correct_option
from wa_cloud_py.message_components import CatalogSection


load_dotenv()
wa_access_token = os.getenv("WA_TOKEN")
phone_id = os.getenv("PHONE_ID")
whatsapp = WhatsApp(access_token=wa_access_token, phone_number_id=phone_id)
phone_number = "0776681617"
# phone_number = "0782849634"
# phone_number = "0711475883"
catalog_id = "253006871078558"
image_url = "https://images.unsplash.com/photo-1622618760546-8e443f8a909b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c2hpYmElMjBpbnV8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60"




# greet_user_and_select_option(whatsapp, phone_number, ListSection, SectionRow)
# send_catalog(phone_number, catalog_id, whatsapp, CatalogSection)
# confirm_order(whatsapp, phone_number, ListSection, SectionRow)
# order_confirmed(whatsapp, phone_number, ListSection, SectionRow)
# make_changes(phone_number, catalog_id, whatsapp, CatalogSection)
# handle_cancellation(whatsapp, phone_number)

# sent_to_packaging(whatsapp, phone_number, ListSection, SectionRow)
# packaging_received(whatsapp, phone_number, ListSection, SectionRow)
# order_packed(whatsapp, phone_number, ListSection, SectionRow)
# order_on_way(whatsapp, phone_number, ListSection, SectionRow)
# order_delivered(whatsapp, phone_number, ListSection, SectionRow)
# no_orders(whatsapp, phone_number, ListSection, SectionRow)
# tracking_issue(whatsapp, phone_number, ListSection, SectionRow)
# invalid_option(whatsapp, phone_number, ListSection, SectionRow)
# select_correct_option(whatsapp, phone_number, ListSection, SectionRow)

