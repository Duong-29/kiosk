import qrcode, io, base64

def make_qrcode(link:str):
    qr_img = qrcode.make(link)

    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()

    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    return img_base64