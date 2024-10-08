"""
This module provides functions to compute various image quality assessment (IQA) metrics
and generate metric maps for the given images and color spaces.

The computed metric values and maps can be used for evaluating the quality of images
and detecting differences between them.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

from .utils import *
from .metrics import *



def compute_ssim_map(im1, im2):
    from skimage.metrics import structural_similarity as ssim
    """
    Compute the Structural Similarity Index (SSIM) and its corresponding map between two images.

    Args:
        im1 (numpy.ndarray): The first input image.
        im2 (numpy.ndarray): The second input image.

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
        im1 (numpy.ndarray): The first input image.
        im2 (numpy.ndarray): The second input image.
        patch_size (int, optional): The size of the patches to compute MSE on. Default is 161.
        step (int, optional): The step size between patches. Default is 50.

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
        im1 (numpy.ndarray): The first input image.
        im2 (numpy.ndarray): The second input image (can be None for no-reference metrics).
        patch_size (int): The size of the patches to compute the metric on.
        step (int): The step size between patches.
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



def compute_map(dist_path, ref_path, metric_name='SSIM', color_space='HSV', patch_size=161, step=50, colormap='gray'):
    """
    Generate metric maps for the given images, metrics, and color spaces, and save them to files.

    Args:
        dist_path (str): Path of distorted image.
        ref_path (str): Path of reference image.
        metric (str): metric name
        color_space (str): name of the color space
        patch_size (int, optional): The size of the patches to compute the metrics on. Default is 161.
        step (int, optional): The step size between patches. Default is 50.
        colormap (str, optional) : Name of the colormap to show the difference in matplotlib
        
    Return:
        plot (matplotlib)
    """
    img1 = load_image(dist_path)
    img2 = load_image(ref_path)
    
    
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    
    if color_space == "RGB":
        img1_cs = img1
        img2_cs = img2
    else:
        img1_cs = cv2.cvtColor(img1, getattr(cv2, f"COLOR_BGR2{color_space}"))
        img2_cs = cv2.cvtColor(img2, getattr(cv2, f"COLOR_BGR2{color_space}"))

    metric_fn = metrics['MSE']
    
    plt.figure()
    try:
        if metric_name == "SSIM":
            ssim_value, ssim_map = compute_ssim_map(img1_cs, img2_cs)
            im = plt.imshow(ssim_map, cmap=colormap)
            plt.title(f'SSIM ({color_space})')
        elif metric_name == "MSE":
            mse_map = compute_mse_map(img1_cs, img2_cs)
            im = plt.imshow(mse_map, cmap=colormap)
            plt.title(f'MSE ({color_space})')
        elif metric_name in ["BRISQUE", "NIQE", "MUSIQ", "NIMA", "CLIPIQA"]:
            # No-reference metrics, compute on img1 only
            metric_map = compute_patchwise_metric(img1_cs, None, patch_size, step, metric_fn)
            im = plt.imshow(metric_map, cmap=colormap)
            plt.title(f'{metric_name} ({color_space})')
        else:
            # Full-reference metrics
            metric_map = compute_patchwise_metric(img1_cs, img2_cs, patch_size, step, metric_fn)
            im = plt.imshow(metric_map, cmap=colormap)
            plt.title(f'{metric_name} ({color_space})')

        plt.axis('off')
        cbar = plt.colorbar(im)
        cbar.set_label(f'{metric_name} Value')
        
        # Add text annotation at the bottom of the plot
        plt.figtext(0.5, 0.01, f"Patch Size: {patch_size}, Step Size: {step}",
                    wrap=True, horizontalalignment='center', fontsize=10)

        plt.tight_layout()
        #print(f"Map generation completed for {metric_name} in {color_space} color space.")

    except Exception as e:
        print(f"Error generating {metric_name} Map for {color_space} color space: {e}")
            
    return plt


def __dir__():
    return ["compute_map"]