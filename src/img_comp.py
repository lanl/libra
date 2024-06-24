'''Contains modules to compare two images and return the difference''' 
import cv2

def img_diff(im1, im2):
    return cv2.subtract(im1, im2)
    