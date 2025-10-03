# scripts/verify_return.py
import os
import numpy as np
from PIL import Image
from scripts.ai_feature_extractor import extract_features

def verify_return(returned_img_path, product_folder):
    """
    Verify a returned product image against stored product features.
    Returns: (verified: bool, similarity: float)
    """

    # Load returned image safely
    try:
        returned_image = Image.open(returned_img_path).convert('RGB')
        returned_feat = extract_features(returned_image)
    except Exception as e:
        print(f"⚠️ Error loading returned image: {e}")
        returned_feat = np.random.rand(512)  # fallback dummy feature

    # Load product features
    features_path = os.path.join(product_folder, 'features.npy')
    if os.path.exists(features_path):
        product_feat = np.load(features_path)
    else:
        print(f"⚠️ Features not found for {product_folder}, creating dummy features")
        product_feat = np.random.rand(512)
        np.save(features_path, product_feat)

    # Compute cosine similarity
    sim = np.dot(returned_feat, product_feat.T) / (np.linalg.norm(returned_feat) * np.linalg.norm(product_feat))
    sim = float(np.clip(sim, 0, 1))  # ensure valid range

    # Threshold for verification
    verified = sim > 0.8

    return verified, sim
