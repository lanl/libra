import cv2
import numpy as np
import torch

# Use cuda enabled device if available
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def normalize_image(image):
    '''Normalize the image to the range [0, 1]'''
    return image / 255.0

def load_image(image_path):
    """
    Load an image from file and convert to a PyTorch tensor.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to load image from path: {image_path}")
    image = normalize_image(image.astype(np.float32))
    image_tensor = torch.tensor(image).permute(2, 0, 1).unsqueeze(0).float()
    return image_tensor.to(device)
