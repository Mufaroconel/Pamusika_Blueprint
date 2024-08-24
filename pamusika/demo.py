from wa_cloud_py import WhatsApp
from wa_cloud_py.message_components import ListSection, SectionRow
from catalog import send_catalog
from payment_method import which_payment_method
from confirm_payment import confirm_payment
from text_messages import GreetingMessages, InformationalMessages, ConfirmationMessages, ErrorMessages, PromotionalMessages


whatsapp = WhatsApp(access_token="EAFhvAtxZBbY4BO3v8S8e0pa4NlJZAqo37oqYfx6wKp0deuuJ86j3v0aZC1ETAPZBZBNUvMccDhlfW4A8Bue4fGzmWKZAMCbCGDmBMPrp06IafBaHeRpOyZCvRemSICJ8hqmqAU0xEb0F2Bk0zWuwhZBVZCluTUSgTRop7XRCNIebY2aQGCmiI2ICnffZBZCYzNm6Y2awHEP63tcxsoGn28sNRcZD", phone_number_id="228270780366581")
phone_number = "0776681617"
message_body = "Hello?"
catalog_id = "253006871078558"

# whatsapp.send_text(to="0776681617", body="Hello world!")
# whatsapp.send_text(to="0734635133", body="Msoro bhangue")
# whatsapp.send_location(to="0776681617", name="My Locations", address="Harare", latitude=-17.8728918070979, longitude=30.935103469966368)


# whatsapp.send_reaction(to=phone_number, message_id="wami.dabc123", emoji="😲")
# whatsapp.send_image(
#   to=phone_number,
#   url="https://images.unsplash.com/photo-1622618760546-8e443f8a909b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c2hpYmElMjBpbnV8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
#   caption="So much wow",
# )

whatsapp.send_text(to=phone_number, body=InformationalMessages.informational_message_5())


# confirm_payment(whatsapp, phone_number)
# which_payment_method(whatsapp, phone_number)
# send_catalog(phone_number, catalog_id, whatsapp)