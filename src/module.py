import logging
from datetime import datetime
import cv2

from .single_metrics import *
from .img_comp import *

log_name = ""


def compare_images(img1_name, img2_name):
    # log
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_name = "comparison_" + current_datetime + ".log"
    logging.basicConfig(filename=log_name, level=logging.DEBUG)

    print("image 1: ", img1_name)
    print("image 2: ", img2_name)

    # read
    im1 = cv2.imread(img1_name)
    im2 = cv2.imread(img2_name)

    logging.info(f"image 1:{img1_name}, width:{im1.shape[1]}, height:{im1.shape[0]}")
    logging.info(f"image 2:{img2_name}, width:{im2.shape[1]}, height:{im2.shape[0]}")


    # Compute metrics
    metric_ssim = compute_ssim(im1, im2)
    metric_mse = compute_mse(im1, im2)
    diff_img = img_diff(im1, im2)
    cv2.imwrite("diff_img.png", diff_img) 
    
    logging.info(f"ssim: {metric_ssim}")
    logging.info(f"mse: {metric_mse}")

    print(f"ssim: {metric_ssim}")
    print(f"mse: {metric_mse}")
    print(f"diff image saved at: diff_img.png")

