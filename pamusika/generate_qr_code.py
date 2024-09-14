import qrcode

# Create an instance of QRCode
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Add data to the QRCode instance
url = f'https://wa.me/{263717432471}?text={"hi"}'
qr.add_data(url)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill='black', back_color='white')

# Save the image to a file
img.save('/Users/macbook/Desktop/WA_Cloud/Pamusika_Blueprint/pamusika/pamusika_qr_code.png')

