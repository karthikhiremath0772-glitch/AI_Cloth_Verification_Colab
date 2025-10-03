import streamlit as st
import os
from PIL import Image
from scripts.generate_qr import generate_qr_for_product
from scripts.verify_return import verify_return  # make sure this returns (bool, similarity)

# Base directory
BASE_DIR = '/content/drive/MyDrive/AI_Cloth_Verification'

st.title('👕 AI Cloth Verification Tool')

# Menu
menu = ['Generate QR', 'Verify Return']
choice = st.sidebar.selectbox('Menu', menu)

# -------------------- Generate QR --------------------
if choice == 'Generate QR':
    st.subheader('Generate QR for a Product')
    product_name = st.text_input('Enter Product Name (e.g. red_tshirt)')

    if st.button('Generate QR'):
        if not product_name:
            st.error("❌ Please enter a product name")
        else:
            product_folder = os.path.join(BASE_DIR, 'products', product_name)
            qr_path = generate_qr_for_product(product_name, product_folder)
            st.success(f'✅ QR Code generated: {qr_path}')
            st.image(qr_path, caption='Generated QR Code')

# -------------------- Verify Return --------------------
elif choice == 'Verify Return':
    st.subheader('Verify Returned Product')
    product_name = st.text_input('Enter Product Name (e.g. red_tshirt)')
    uploaded_file = st.file_uploader('Upload Return Image', type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None and st.button('Verify'):
        if not product_name:
            st.error("❌ Please enter a product name")
        else:
            # Save uploaded return image
            returned_folder = os.path.join(BASE_DIR, 'returned')
            os.makedirs(returned_folder, exist_ok=True)
            return_path = os.path.join(returned_folder, uploaded_file.name)
            with open(return_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())

            # Check if product exists
            product_folder = os.path.join(BASE_DIR, 'products', product_name)
            if not os.path.exists(product_folder):
                st.error("❌ Product folder not found!")
            else:
                try:
                    result, score = verify_return(return_path, product_folder)
                    if result:
                        st.success(f'✅ Verified! Similarity: {score:.2f}')
                    else:
                        st.error(f'❌ Verification Failed. Similarity: {score:.2f}')
                except Exception as e:
                    st.error(f"❌ Verification error: {str(e)}")
