import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


def generate_qr_code(data):
    """
    Generate a QR code for the given data.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an in-memory file-like object
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    # Generate a filename
    file_name = f'qr_{data}.png'
    content_file = ContentFile(buffer.getvalue(), name=file_name)

    return content_file
