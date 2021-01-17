import qrcode
import base64
import io

def qr_in_base64(value):
        """Deuelve el código QR del valor, codificado en Base64"""
        qr_image = qrcode.make(value)

        imgBytes = io.BytesIO()

        qr_image.save(imgBytes, format=qr_image.format)

        img_bytes_array = imgBytes.getvalue()

        encoded_qr = base64.b64encode(img_bytes_array).decode()

        return encoded_qr

# def encrypt(value, password):
# """Devuelve la cadena value codificada con la contraseña password"""


# def decrypt(value, password):
# """Devuelve la cadena value decodificada con la contraseña password"""