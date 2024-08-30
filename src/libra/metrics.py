import cv2
import numpy as np
import torch
import piq
import pyiqa
import torchvision.transforms as transforms
from PIL import Image
from piq import CLIPIQA

from .utils import *


def preprocess_image(image):
    '''Normalize the image to the range [0, 1] and convert to a PyTorch tensor'''
    image = image.astype(np.float32) / 255.0
    image_tensor = torch.tensor(image).permute(2, 0, 1).unsqueeze(0).float()
    return image_tensor

############## FULL REFERENCE METRICS ##########################

def compute_mse(im1, im2):
    # convert to hsv (hue:color, saturation:?, value:intensity or grayscale)
    hsv_img1 = cv2.cvtColor(im1, cv2.COLOR_BGR2HSV)
    hsv_img2 = cv2.cvtColor(im2, cv2.COLOR_BGR2HSV)

    err = np.sum((im1.astype("float") - hsv_img2.astype("float")) ** 2)
    err /= float(hsv_img1.shape[0] * hsv_img1.shape[1])
    return err

def compute_ssim(im1, im2):
    '''Compute SSIM'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    index = piq.ssim(img1_torch, img2_torch)
    return index.item()

def compute_fsim(im1, im2):
    '''Compute FSIM'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    index = piq.fsim(img1_torch, img2_torch, data_range=img1_torch.max() - img1_torch.min())
    return index.item()

def compute_vifp(im1, im2):
    '''Compute VIFp'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    index = piq.vif_p(img1_torch, img2_torch)
    return index.item()

def compute_iw_ssim(im1, im2):
    '''Compute IW_SSIM'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    index = piq.information_weighted_ssim(img1_torch, img2_torch)
    return index.item()

def compute_ms_ssim(im1, im2):
    '''Compute MS-SSIM'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    index = piq.multi_scale_ssim(img1_torch, img2_torch)
    return index.item()

def compute_psnr(im1, im2):
    '''Compute PSNR'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    index = piq.psnr(img1_torch, img2_torch)
    return index.item()

def compute_haarpsi(im1, im2):
    '''Compute HaarPSI'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    index = piq.haarpsi(img1_torch, img2_torch)
    return index.item()

def compute_vsi(im1, im2):
    '''Compute VSI'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    index = piq.vsi(img1_torch, img2_torch)
    return index.item()

def compute_srsim(im1, im2):
    '''Compute SR-SIM'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    index = piq.srsim(img1_torch, img2_torch)
    return index.item()

def compute_gmsd(im1, im2):
    '''Compute GMSD'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    index = piq.gmsd(img1_torch, img2_torch)
    return index.item()

def compute_msgmsd(im1, im2):
    '''Compute MS-GMSD'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    index = piq.multi_scale_gmsd(img1_torch, img2_torch)
    return index.item()

def compute_lpips(im1, im2):
    '''Compute LPIPS'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    lpips_index = piq.LPIPS(replace_pooling=True)(img1_torch, img2_torch)
    return lpips_index.item()

def compute_pieapp(im1, im2):
    '''Compute PieAPP'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    pieapp_index = piq.PieAPP()(img1_torch, img2_torch)
    return pieapp_index.item()

def compute_dists(im1, im2):
    '''Compute DISTS'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    dists_index = piq.DISTS()(img1_torch, img2_torch)
    return dists_index.item()

def compute_mdsi(im1, im2):
    ''' Compute MDSI'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    mdsi_index = piq.mdsi(img1_torch, img2_torch)
    return mdsi_index.item()

def compute_dss(im1, im2):
    '''Compute DSS'''
    img1_torch = preprocess_image(im1)
    img2_torch = preprocess_image(im2)
    dss_index = piq.dss(img1_torch, img2_torch)
    return dss_index.item()

def compute_phash(img1, img2):
    """Compute the perceptual hash (pHash) of two images and return the Hamming distance."""

    from imagehash import phash
    from PIL import Image
    try:
        # Convert NumPy arrays to PIL Images (assuming they are already in RGB format)
        img1_pil = Image.fromarray(img1)
        img2_pil = Image.fromarray(img2)
        
        # Compute pHash
        phash1 = phash(img1_pil)
        phash2 = phash(img2_pil)
        
        # Calculate Hamming distance
        distance = phash1 - phash2
        return distance
    except Exception as e:
        print(f"Error computing pHash: {e}")
        return None



##################### NO REFERENCE METRICS ###########################################

# Use cuda enabled device if available
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def convert_to_tensor(image):
    """
    Converts an OpenCV image to a PyTorch tensor.
    """
    image = preprocess_image(image)
    return image.to(device)

def compute_brisque(image):
    """
    Computes the BRISQUE score for the given image.
    """
    image = convert_to_tensor(image)
    model = pyiqa.create_metric('brisque', device=device).eval()
    with torch.no_grad():
        score = model(image)
    return score.item()

def compute_niqe(image):
    """
    Computes the NIQE score for the given image.
    """
    image = convert_to_tensor(image)
    model = pyiqa.create_metric('niqe', device=device).eval()
    with torch.no_grad():
        score = model(image)
    return score.item()

def compute_musiq(image):
    """
    Computes the MUSIQ score for the given image.
    """
    image = convert_to_tensor(image)
    model = pyiqa.create_metric('musiq', device=device).eval()
    with torch.no_grad():
        score = model(image)
    return score.item()

def compute_nima(image):
    """
    Computes the NIMA score for the given image.
    """
    image = convert_to_tensor(image)
    model = pyiqa.create_metric('nima', device=device).eval()
    with torch.no_grad():
        score = model(image)
    return score.item()

def compute_clip_iqa(image):
    """
    Computes the CLIPIQA score for the given image.
    """
    image = convert_to_tensor(image)
    clip_iqa = CLIPIQA(data_range=1.0)  # Set data_range to 1.0 because image is normalized

    # Compute the CLIPIQA score
    score = clip_iqa(image).item()
    return score



metrics = {
    'MSE': compute_mse,
    'SSIM': compute_ssim,
    'FSIM': compute_fsim,
    'MS-SSIM': compute_ms_ssim,
    'PSNR': compute_psnr,
    'VSI': compute_vsi,
    'SR-SIM': compute_srsim,
    'MS-GMSD': compute_msgmsd,
    'LPIPS': compute_lpips,
    'PieAPP': compute_pieapp,
    'DISTS': compute_dists,
    "MDSI": compute_mdsi,
    "DSS": compute_dss,
    "IW-SSIM": compute_iw_ssim,
    "VIFp": compute_vifp,
    "GMSD": compute_gmsd,
    "HaarPSI": compute_haarpsi,
    "BRISQUE": compute_brisque,
    "NIQE": compute_niqe,
    "MUSIQ": compute_musiq,
    "NIMA": compute_nima,
    "CLIPIQA": compute_clip_iqa,
    "PHASH": compute_phash
}