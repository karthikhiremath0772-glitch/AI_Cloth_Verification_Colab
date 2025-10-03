# scripts/generate_qr.py
import os
import qrcode

def generate_qr_for_product(product_name, product_folder):
    """
    Generate a QR code for a given product.
    Returns the path to the QR image.
    """

    # Ensure product folder exists
    if not os.path.exists(product_folder):
        os.makedirs(product_folder)
        print(f"📁 Created product folder: {product_folder}")

    # QR code content (can be product name or any identifier)
    qr_content = f"Product:{product_name}"

    # Generate QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code
    qr_path = os.path.join(product_folder, "qr.png")
    img.save(qr_path)

    print(f"✅ QR code saved for {product_name} at {qr_path}")
    return qr_path
