from wa_cloud_py.message_components import ListSection, SectionRow


def which_payment_method(whatsapp, phone_number):
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
        title="On delivery 💳",
        rows=[
          SectionRow(id="pay_with_cash", title="Cash"),
          SectionRow(id="pay_with_credit_card", title="Credit Card"),
        ],
      ),
    ],
  )