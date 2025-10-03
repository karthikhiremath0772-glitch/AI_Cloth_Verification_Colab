import numpy as np
from PIL import Image

def extract_features(image):
    """
    Accepts a PIL Image object.
    Returns a 512-d feature vector (dummy).
    Ensures non-zero vectors to avoid NaN in similarity.
    """
    # Ensure RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize
    image = image.resize((224, 224))
    
    # Convert to array and normalize
    arr = np.array(image) / 255.0
    
    # Flatten and take first 512 elements
    features = arr.flatten()[:512]
    
    # Add tiny epsilon to avoid zero vectors
    features += 1e-6
    
    return features
