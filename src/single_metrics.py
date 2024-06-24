'''Contains modules to compare two images and a metric quantifying the difference''' 

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def compute_mse(im1, im2):
    # convert to hsv (hue:color, saturation:?, value:intensity or grayscale)
    hsv_img1 = cv2.cvtColor(im1, cv2.COLOR_BGR2HSV)
    hsv_img2 = cv2.cvtColor(im2, cv2.COLOR_BGR2HSV)

    err = np.sum((im1.astype("float") - hsv_img2.astype("float")) ** 2)
    err /= float(hsv_img1.shape[0] * hsv_img1.shape[1])
    return err


def compute_ssim(im1, im2):
    '''Compute SSIM: SSIM works on grayscale, so use value/intensity chanel of hsv'''
    
    # is SSIM on hsv valid???
    hsv_img1 = cv2.cvtColor(im1, cv2.COLOR_BGR2HSV)
    hsv_img2 = cv2.cvtColor(im2, cv2.COLOR_BGR2HSV)

    # split
    hsv_img1_split = cv2.split(hsv_img1)
    hsv_img2_split = cv2.split(hsv_img2)

    # compute SSIM
    return ssim(hsv_img1_split[2], hsv_img2_split[2])