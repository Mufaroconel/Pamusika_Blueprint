from wa_cloud_py import WhatsApp
from wa_cloud_py.message_types import MessageStatus, UserMessage, TextMessage, OrderMessage
from flask import request, Flask, render_template
from flask.views import MethodView
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from dboperations import get_all_orders

load_dotenv()
wa_access_token = os.getenv("WA_TOKEN")
phone_id = os.getenv("PHONE_ID")
verify_token = os.getenv("VERIFY_TOKEN")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route("/dashboard")
def index():
    all_orders = get_all_orders()
    return render_template("dashboard.html", orders=all_orders)

class GroupAPI(MethodView):
    init_every_request = False

    def get(self):
        # Verify token for webhook
        received_verify_token = request.args.get("hub.verify_token")  # Renamed to received_verify_token
        challenge = request.args.get("hub.challenge")

        if received_verify_token == "something_secure_and_unique":
            return challenge, 200
        else:
            return f"Invalid token received verify token: {received_verify_token} not the same with {verify_token}", 403

    def post(self):
        whatsapp = WhatsApp(access_token=wa_access_token, phone_number_id=phone_id)  # Using wa_access_token
        message = whatsapp.parse(request.data)

        # Check if the message was sent by a user
        if isinstance(message, UserMessage):

            # Process text message
            if isinstance(message, TextMessage):
               message_sent, res = whatsapp.send_text(
                   to=message.user.phone_number,
                   body="Hello World",
               )

            # Process order
            if isinstance(message, OrderMessage):
                pass

        # Print status of message you sent to the user
        elif isinstance(message, MessageStatus):
            print(message)

        # Handle unsupported message types
        else:
            print("Unsupported message type")

        return "", 200

# Add the route for the webhook
app.add_url_rule('/webhook', view_func=GroupAPI.as_view('wa_webhook'))

if __name__ == "__main__":
    app.run(debug=True)
