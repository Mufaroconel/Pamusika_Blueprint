from wa_cloud_py import whatsapp
from wa_cloud_py.message_components import ListSection, SectionRow

whatsapp = WhatsApp(access_token="EAFhvAtxZBbY4BO3v8S8e0pa4NlJZAqo37oqYfx6wKp0deuuJ86j3v0aZC1ETAPZBZBNUvMccDhlfW4A8Bue4fGzmWKZAMCbCGDmBMPrp06IafBaHeRpOyZCvRemSICJ8hqmqAU0xEb0F2Bk0zWuwhZBVZCluTUSgTRop7XRCNIebY2aQGCmiI2ICnffZBZCYzNm6Y2awHEP63tcxsoGn28sNRcZD", phone_number_id="228270780366581")
phone_number = "0776681617"
message_body = "Hello?"
whatsapp.send_interactive_list(
  to=phone_number,
  header="Payment options",
  body="Select a payment option 🧾",
  button="Options",
  sections=[
    ListSection(
      title="Mobile money 📱",
      rows=[
        SectionRow(id="pay_with_ecocash", title="EcoCash", description="Pay with EcoCash"),
        SectionRow(id="pay_with_onemoney", title="OneMoney", description="Pay with OneMoney")
      ],
    ),
    ListSection(
      title="Bank transfer 💳",
      rows=[
        SectionRow(id="pay_with_visa", title="Visa"),
        SectionRow(id="pay_with_mastercard", title="MasterCard"),
      ],
    ),
  ],
)