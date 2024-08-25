
def send_image(phone_number, image_url, whatsapp):
    whatsapp.send_image(
    to=phone_number,
    url=image_url,
    caption="So much wow",
)
