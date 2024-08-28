import sys
import os

import cv2
import numpy as np
import torch


# Use cuda enabled device if available
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


color_spaces = {
    'RGB': cv2.COLOR_BGR2RGB,
    'HSV': cv2.COLOR_BGR2HSV,
    'HLS': cv2.COLOR_BGR2HLS,
    'LAB': cv2.COLOR_BGR2LAB,
    "XYZ": cv2.COLOR_BGR2XYZ,
    "LUV": cv2.COLOR_BGR2LUV,
    "YCrCb": cv2.COLOR_BGR2YCrCb,
    "YUV": cv2.COLOR_BGR2YUV
}


def load_image(path):
    """
    Load the distorted and reference images.

    Args:
        dist_path (str): Path to the distorted image.
        ref_path (str): Path to the reference image.
    Returns:
        tuple: (distorted image, reference image)
    """
    image = cv2.imread(path)

    if image is None:
        print("Unable to read input images.")
        sys.exit(1)

    return image


def write_image(img, path):
    """
    Write an image out to disk
    
    Args:
        img (cv object): the image
        path (str): Path to write it to
    """
    
    cv2.imwrite(path, img)
    


def load_and_convert_image(image_path, color_space_code=cv2.COLOR_BGR2RGB):
    """
    Load an image from the given path and convert it to the specified color space.

    Args:
        image_path (str): The path to the image file.
        color_space_code (int): The OpenCV color space conversion code.

    Returns:
        numpy.ndarray: The loaded and converted image.

    Raises:
        FileNotFoundError: If the specified image file is not found.
    """
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    return cv2.cvtColor(image, color_space_code)



def get_color_space_code(color_space_name):
    """
    Get the OpenCV color space conversion code for a given color space name.

    Args:
        color_space_name (str): The name of the color space (e.g., 'RGB', 'HSV', 'LAB').

    Returns:
        int: The OpenCV color space conversion code.
    """
    color_spaces = {
        'RGB': cv2.COLOR_BGR2RGB,
        'HSV': cv2.COLOR_BGR2HSV,
        'HLS': cv2.COLOR_BGR2HLS,
        'LAB': cv2.COLOR_BGR2LAB,
        'XYZ': cv2.COLOR_BGR2XYZ,
        'LUV': cv2.COLOR_BGR2LUV,
        'YCrCb': cv2.COLOR_BGR2YCrCb,
        'YUV': cv2.COLOR_BGR2YUV
    }
    
    return color_spaces.get(color_space_name.upper(), cv2.COLOR_BGR2RGB)


def create_output_folder(output_folder_path):
    """
    Create the output folder if it doesn't exist.

    Args:
        output_folder_path (str): Path to the output folder.
    """
    try:
        os.makedirs(output_folder_path, exist_ok=True)
        print(f"Output folder '{output_folder_path}' created.")
    except Exception as e:
        print(f"Error creating output folder '{output_folder_path}': {e}")
        sys.exit(1)
        
        
def normalize_image(image):
    '''Normalize the image to the range [0, 1]'''
    return image / 255.0


def is_similar(img1, img2):
    """ 
    Check if two images are the same
    """
    
    if img1.shape != img2.shape:
        return False
    
    diff = cv2.absdiff(img1, img2)
    print("diff:",cv2.countNonZero(diff))
    return cv2.countNonZero(diff) == 0



def load_tensor_image(image_path):
    """
    Load an image from file and convert to a PyTorch tensor.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to load image from path: {image_path}")
    image = normalize_image(image.astype(np.float32))
    image_tensor = torch.tensor(image).permute(2, 0, 1).unsqueeze(0).float()
    return image_tensor.to(device)