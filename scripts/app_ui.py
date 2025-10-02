
import streamlit as st
import os
from PIL import Image
from scripts.verify_return import verify_return  # Use your existing verify_return function

PRODUCTS_PATH = "/content/drive/MyDrive/AI_Cloth_Verification/products"
RETURNED_PATH = "/content/drive/MyDrive/AI_Cloth_Verification/returned"

st.title("🧵 AI Cloth Verification Tool")

# Upload Original Images
st.header("Step 1: Upload Original Cloth Images")
uploaded_front = st.file_uploader("Upload Front Image", type=["jpg", "png", "webp"], key="front")
uploaded_back = st.file_uploader("Upload Back Image", type=["jpg", "png", "webp"], key="back")
uploaded_tag = st.file_uploader("Upload Tag Image", type=["jpg", "png", "webp"], key="tag")

if uploaded_front and uploaded_back and uploaded_tag:
    st.success("✅ Original images uploaded successfully!")
    st.write("Now you can generate QR code linked to this cloth.")

# Generate QR
st.header("Step 2: Generate QR Code")
cloth_name = st.text_input("Enter Cloth Name (unique ID)")

if st.button("Generate QR"):
    if cloth_name and uploaded_front and uploaded_back and uploaded_tag:
        cloth_dir = os.path.join(PRODUCTS_PATH, cloth_name)
        os.makedirs(os.path.join(cloth_dir, "front"), exist_ok=True)
        os.makedirs(os.path.join(cloth_dir, "back"), exist_ok=True)
        os.makedirs(os.path.join(cloth_dir, "tag"), exist_ok=True)

        Image.open(uploaded_front).save(os.path.join(cloth_dir, "front", "front1.jpg"))
        Image.open(uploaded_back).save(os.path.join(cloth_dir, "back", "back1.jpg"))
        Image.open(uploaded_tag).save(os.path.join(cloth_dir, "tag", "tag1.jpg"))

        from scripts.generate_qr import generate_qr
        generate_qr(cloth_name, cloth_dir)

        st.success(f"✅ QR code generated and saved for {cloth_name}!")

# Upload Returned Cloth
st.header("Step 3: Upload Returned Cloth Image")
returned_img_file = st.file_uploader("Upload Returned Cloth", type=["jpg", "png", "webp"], key="returned")

if returned_img_file:
    returned_img_path = os.path.join(RETURNED_PATH, returned_img_file.name)
    Image.open(returned_img_file).save(returned_img_path)
    st.success(f"✅ Returned cloth image saved as {returned_img_file.name}")

    if st.button("Verify Cloth"):
        result, similarity = verify_return(returned_img_path)
        st.subheader("Verification Result")
        st.write(f"Similarity: {similarity:.2f}%")
        if result:
            st.success("✅ ORIGINAL PRODUCT")
        else:
            st.error("❌ FAKE PRODUCT")
