from flask import Flask, request
from wa_cloud_py import WhatsApp
from wa_cloud_py.message_types import TextMessage, UserMessage, MessageStatus

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    whatsapp = WhatsApp(access_token="EAFhvAtxZBbY4BO3v8S8e0pa4NlJZAqo37oqYfx6wKp0deuuJ86j3v0aZC1ETAPZBZBNUvMccDhlfW4A8Bue4fGzmWKZAMCbCGDmBMPrp06IafBaHeRpOyZCvRemSICJ8hqmqAU0xEb0F2Bk0zWuwhZBVZCluTUSgTRop7XRCNIebY2aQGCmiI2ICnffZBZCYzNm6Y2awHEP63tcxsoGn28sNRcZD", phone_number_id="228270780366581")
    message = whatsapp.parse(request.data)

    if isinstance(message, UserMessage):
        if isinstance(message, TextMessage):
            # Process text message
            whatsapp.send_text(to=message.user.phone_number, text="Received your message!")

    elif isinstance(message, MessageStatus):
        # Handle message status updates
        print(f"Message status: {message}")

    return "OK", 200

if __name__ == '__main__':
    app.run(port=8080)
