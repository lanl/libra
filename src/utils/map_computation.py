"""
This module provides functions to compute various image quality assessment (IQA) metrics
and generate metric maps for the given images and color spaces.

The computed metric values and maps can be used for evaluating the quality of images
and detecting differences between them.
"""


import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim

def compute_ssim_map(im1, im2):

    """
    Compute the Structural Similarity Index (SSIM) and its corresponding map between two images.

    Args:
        image1 (numpy.ndarray): The first input image.
        image2 (numpy.ndarray): The second input image.

    Returns:
        tuple: A tuple containing the SSIM value (float) and the SSIM map (numpy.ndarray).
    """
      
    hsv_img1 = cv2.cvtColor(im1, cv2.COLOR_BGR2HSV)
    hsv_img2 = cv2.cvtColor(im2, cv2.COLOR_BGR2HSV)

    ssim_value, ssim_map = ssim(hsv_img1[:, :, 2], hsv_img2[:, :, 2], full=True)
    return ssim_value, ssim_map

def compute_mse_map(im1, im2, patch_size=161, step=50):
    """
    Compute the Mean Squared Error (MSE) map between two images by evaluating MSE on patches.

    Args:
        image1 (numpy.ndarray): The first input image.
        image2 (numpy.ndarray): The second input image.
        patch_size (int, optional): The size of the patches to compute MSE on. Default is 161.
        step_size (int, optional): The step size between patches. Default is 50.

    Returns:
        numpy.ndarray: The MSE map between the two images.
    """

    h, w, _ = im1.shape
    mse_map = np.zeros((h, w))

    for i in range(0, h - patch_size + 1, step):
        for j in range(0, w - patch_size + 1, step):
            patch1 = im1[i:i+patch_size, j:j+patch_size, :]
            patch2 = im2[i:i+patch_size, j:j+patch_size, :]
            err = np.sum((patch1.astype("float") - patch2.astype("float")) ** 2)
            err /= float(patch1.shape[0] * patch1.shape[1] * patch1.shape[2])
            mse_map[i:i+patch_size, j:j+patch_size] = err

    return mse_map

def compute_patchwise_metric(im1, im2, patch_size, step, metric_fn):
    """
    Compute a quality metric map by evaluating the given metric function on patches of the images.

    Args:
        image1 (numpy.ndarray): The first input image.
        image2 (numpy.ndarray): The second input image (can be None for no-reference metrics).
        patch_size (int): The size of the patches to compute the metric on.
        step_size (int): The step size between patches.
        metric_fn (callable): The metric function to compute the quality metric.

    Returns:
        numpy.ndarray: The quality metric map between the two images (or for the single image in case of no-reference metrics).
    """

    h, w, _ = im1.shape
    metric_map = np.zeros((h, w))

    for i in range(0, h - patch_size + 1, step):
        for j in range(0, w - patch_size + 1, step):
            patch1 = im1[i:i+patch_size, j:j+patch_size, :]

            if im2 is not None:
                patch2 = im2[i:i+patch_size, j:j+patch_size, :]
                try:
                    metric_value = metric_fn(patch1, patch2)
                    metric_map[i:i+patch_size, j:j+patch_size] = metric_value
                except Exception as e:
                    print(f"Error computing metric on patch ({i}, {j}): {e}")
            else:
                try:
                    metric_value = metric_fn(patch1)
                    metric_map[i:i+patch_size, j:j+patch_size] = metric_value
                except Exception as e:
                    print(f"Error computing no-reference metric on patch ({i}, {j}): {e}")

    return metric_map

def compute_maps(img1, img2, metrics, color_spaces, output_path, patch_size=161, step=50):
    """
    Generate metric maps for the given images, metrics, and color spaces, and save them to files.

    Args:
        image1 (numpy.ndarray): The first input image.
        image2 (numpy.ndarray): The second input image.
        metrics (dict): A dictionary containing the metric names and corresponding metric functions.
        color_spaces (list): A list of color space names to generate metric maps for.
        output_path (str): The base path for saving the generated metric maps.
        patch_size (int, optional): The size of the patches to compute the metrics on. Default is 161.
        step_size (int, optional): The step size between patches. Default is 50.
    """

    
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    for color_space in color_spaces:
        fig, axes = plt.subplots(1, len(metrics), figsize=(5*len(metrics), 5))

        if color_space == "RGB":
            img1_cs = img1
            img2_cs = img2
        else:
            img1_cs = cv2.cvtColor(img1, getattr(cv2, f"COLOR_BGR2{color_space}"))
            img2_cs = cv2.cvtColor(img2, getattr(cv2, f"COLOR_BGR2{color_space}"))

        for jdx, (metric_name, metric_fn) in enumerate(metrics.items()):
            ax = axes[jdx] if len(metrics) > 1 else axes
            try:
                if metric_name == "SSIM":
                    ssim_value, ssim_map = compute_ssim_map(img1_cs, img2_cs)
                    im = ax.imshow(ssim_map, cmap='gray')
                    ax.set_title(f'SSIM')
                elif metric_name == "MSE":
                    mse_map = compute_mse_map(img1_cs, img2_cs)
                    im = ax.imshow(mse_map, cmap='hot')
                    ax.set_title(f'MSE')
                elif metric_name in ["BRISQUE", "NIQE", "MUSIQ", "NIMA", "CLIPIQA"]:
                    # No-reference metrics, compute on img1 only
                    metric_map = compute_patchwise_metric(img1_cs, None, patch_size, step, metric_fn)
                    im = ax.imshow(metric_map, cmap='viridis')
                    ax.set_title(f'{metric_name}')
                else:
                    # Full-reference metrics
                    metric_map = compute_patchwise_metric(img1_cs, img2_cs, patch_size, step, metric_fn)
                    im = ax.imshow(metric_map, cmap='viridis')
                    ax.set_title(f'{metric_name}')

                ax.axis('off')
                cbar = plt.colorbar(im, ax=ax)
                cbar.set_label(f'{metric_name} Value')
            except Exception as e:
                print(f"Error generating {metric_name} Map for {color_space} color space: {e}")

        plt.tight_layout()
        plt.savefig(f"{output_path}_{color_space}.png")
        print(f"Maps generation completed for {color_space} color space.")