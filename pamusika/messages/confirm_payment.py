from wa_cloud_py.message_components import ReplyButton, ImageHeader

def confirm_payment(whatsapp, phone_number):
    whatsapp.send_interactive_buttons(
    to=phone_number,
    header=ImageHeader(url="https://images.unsplash.com/photo-1622618760546-8e443f8a909b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c2hpYmElMjBpbnV8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60"),
    body="🛒 Confirm Your Purchase at Musika",
    footer="⚠️ Please note: All payments are non-refundable.",
    buttons=[
      ReplyButton(id="confirm", title="Confirm"),
      ReplyButton(id="cancel", title="Cancel"),
    ],
  )