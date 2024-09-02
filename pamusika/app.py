from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask.views import MethodView
from wa_cloud_py import WhatsApp
from wa_cloud_py.message_types import MessageStatus, UserMessage, TextMessage, OrderMessage, InteractiveListMessage
from dotenv import load_dotenv
import os
from dboperations import add_customer, get_customer_by_phone, add_order, get_orders, update_order_status, get_all_orders, get_filtered_orders, user_exists
from models import db, Customer, init_db, Order
from messages.app_logic_messages import greet_user_and_select_option, send_catalog, confirm_order, order_confirmed, make_changes, handle_cancellation, sent_to_packaging, packaging_received, order_packed, order_on_way, order_delivered, no_orders, tracking_issue, invalid_option, select_correct_option, request_contact_number, request_user_name, request_address, notify_user_about_support_model
from wa_cloud_py.message_components import ListSection, SectionRow, CatalogSection
from flask_migrate import Migrate

load_dotenv()
wa_access_token = os.getenv("WA_TOKEN")
phone_id = os.getenv("PHONE_ID")
verify_token = os.getenv("VERIFY_TOKEN")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secretkey'

# Initialize the SQLAlchemy object with the app
db.init_app(app)

# Set up Flask-Migrate with the app and db
migrate = Migrate(app, db)

catalog_id = "253006871078558"

phone = "263776681617"
with app.app_context():
    orders = get_orders(phone)  
    if orders :
        for order in orders:
            order_status = order.status
        if order_status == "Sent to Packaging":
            print("Order found sent to packaging")
    else :
        print("order not found")

@app.route("/dashboard")
def index():
    order_status = request.args.get('order_status')
    customer_name = request.args.get('customer_name')
    order_id = request.args.get('order_id')
    customer_id = request.args.get('customer_id')
    
    if any([order_status, customer_name, order_id, customer_id]):
        orders = get_filtered_orders(order_status, customer_name, order_id, customer_id)
    else:
        orders = get_all_orders()

    return render_template("dashboard.html", orders=orders)

whatsapp = WhatsApp(access_token=wa_access_token, phone_number_id=phone_id)
phone = "263776681617"

with app.app_context():
    user_exist = user_exists(phone)
    print(f"Does the user with phone number {phone} exist? {'Yes' if user_exist else 'No'}")

processed_messages = set()
class GroupAPI(MethodView): 
    init_every_request = False

    def __init__(self):
        self.whatsapp = WhatsApp(access_token=wa_access_token, phone_number_id=phone_id)

    def get(self):
        received_verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if received_verify_token == verify_token:
            return challenge, 200   
        else:
            return f"Invalid token received verify token: {received_verify_token} not the same with {verify_token}", 403

    def post(self):
        message = whatsapp.parse(request.data)

        if message.id in processed_messages:
            return "", 200

        processed_messages.add(message.id)

        if isinstance(message, UserMessage):
            phone = message.user.phone_number

            if isinstance(message, TextMessage):
                # message_sent, res = greet_user_and_select_option(whatsapp, phone, ListSection, SectionRow)
                with app.app_context():
                    user = get_customer_by_phone(phone)
                    if user :
                        message_sent, res = greet_user_and_select_option(whatsapp, phone, ListSection, SectionRow)
                    else :
                        message_sent, res = request_user_name(whatsapp, phone)
                        if isinstance(message, TextMessage):
                            message_sent, res = request_contact_number(whatsapp, phone, ListSection, SectionRow)
                            if isinstance(message, TextMessage):
                                message_sent, res = request_address(whatsapp, phone, ListSection, SectionRow)
                                if isinstance(message, TextMessage):
                                    message_sent, res = greet_user_and_select_option(whatsapp, phone, ListSection, SectionRow)
            elif isinstance(message, InteractiveListMessage):
                user_choice = message.reply_id
                if user_choice == "place_order":
                    message_sent, res = send_catalog(phone, catalog_id, whatsapp, CatalogSection)
                elif user_choice == "track_order":
                    with app.app_context():
                        orders = get_orders(phone)  
                        if orders :
                            for order in orders:
                                order_status = order.status
                            if order_status == "Sent to Packaging":
                                message_sent, res = sent_to_packaging(whatsapp, phone, ListSection, SectionRow)
                            elif order_status == "Packaging received":
                                message_sent, res = packaging_received(whatsapp, phone, ListSection, SectionRow)
                            elif order_status == "Packed":
                                message_sent, res = order_packed(whatsapp, phone, ListSection, SectionRow)
                            elif order_status == "Sent for delivery":
                                message_sent, res = order_on_way(whatsapp, phone, ListSection, SectionRow)
                            else :
                                message_sent, res = no_orders(whatsapp, phone, ListSection, SectionRow)
                        else:
                            message_sent, res = no_orders(whatsapp, phone, ListSection, SectionRow)
                elif user_choice == "customer_support":
                    message_sent, res = notify_user_about_support_model(whatsapp, phone, ListSection, SectionRow)
            elif isinstance(message, OrderMessage):
                products = message.products
                message_sent, res = whatsapp.send_text(phone, f"Order confirmed. You have ordered {products}.")
            elif isinstance(message, MessageStatus):
                print(message)
                pass
            pass 
        else:
            print("Unsupported message type")

        return "", 200

app.add_url_rule('/webhook', view_func=GroupAPI.as_view('wa_webhook'))

if __name__ == "__main__":
    app.run(debug=True)
