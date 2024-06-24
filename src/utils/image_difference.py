"""
This module provides functions to compare two images and generate a thresholded difference image.

It supports various color spaces and allows for comparing specific color channels.
The thresholded difference image highlights the significant differences between the two images.
"""

import cv2
import numpy as np

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

def load_and_convert_image(image_path, color_space_code):
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
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    return cv2.cvtColor(image, color_space_code)

def generate_thresholded_diff_image(image1_path, image2_path, threshold, color_space_code, output_path, color_channels=None):
    """
    Load two images, convert them to the specified color space, calculate the difference,
    and apply a threshold to highlight significant differences. Save the result to a file.

    Args:
        image1_path (str): The path to the first image file.
        image2_path (str): The path to the second image file.
        threshold (int): The threshold value to apply for highlighting differences.
        color_space_code (int): The OpenCV color space conversion code.
        output_path (str): The path to save the thresholded difference image.
        color_channels (tuple or None, optional): A tuple specifying the color channels to use for calculating the difference.
            If None, all color channels are used.

    Raises:
        FileNotFoundError: If either of the input image files is not found.
    """
    # Load and convert images
    image1 = load_and_convert_image(image1_path, color_space_code)
    image2 = load_and_convert_image(image2_path, color_space_code)

    if color_channels is None:
        # Calculate the absolute difference between the images
        difference = cv2.absdiff(image1, image2)
    else:
        # Calculate the absolute difference between specific color channels
        image1_channels = cv2.split(image1)
        image2_channels = cv2.split(image2)
        difference = cv2.absdiff(image1_channels[color_channels], image2_channels[color_channels])

    # Apply threshold to get binary mask of differences
    _, thresholded_diff = cv2.threshold(difference, threshold, 255, cv2.THRESH_BINARY)

    # Save the thresholded difference image
    cv2.imwrite(output_path, thresholded_diff)
    print(f"Thresholded difference image saved to {output_path}")