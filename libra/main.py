"""
This script computes various image quality assessment (IQA) metrics between a distorted image and a reference image.
It takes a configuration file as input, which specifies the paths to the distorted and reference images, the output
folder, the metrics to compute, and other settings. The computed metrics are saved in a CSV file in the output folder.

Usage:
   python compute_metrics.py <path_to_config_file>

Configuration File Format:
The configuration file should be a JSON file with the following keys:
   "dist_path" (str): Path to the distorted image.
   "ref_path" (str): Path to the reference image.
   "output_folder" (str): Path to the output folder where the CSV file will be saved.
   "output_csv" (str, optional): Name of the output CSV file (default: "metrics.csv").
   "generate_maps" (bool, optional): Flag to generate metric maps (default: False).
   "map_metrics" (list of str, optional): List of metrics for which to generate maps.
   "color_spaces" (list of str, optional): List of color spaces to use for computing metrics (default: ["RGB"]).
   "patch_size" (int, optional): Patch size for computing metric maps (default: 161).
   "step_size" (int, optional): Step size for computing metric maps (default: 50).

"""

import os
import sys
import json
import argparse
import cv2
import pandas as pd
import warnings
import numpy as np
from utils.metrics import *
from utils.image_preprocess import *
from utils.map_computation import compute_maps
from utils.image_difference import *


# define possible metrics
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

# define possible color spaces

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


def read_config(config_path):
    """
    Read and validate the configuration file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Configuration dictionary.
    """
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(
            f"Error: Configuration file '{config_path}' is not a valid JSON file.")
        sys.exit(1)


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


def load_images(dist_path, ref_path):
    """
    Load the distorted and reference images.

    Args:
        dist_path (str): Path to the distorted image.
        ref_path (str): Path to the reference image.
    Returns:
        tuple: (distorted image, reference image)
    """
    dist_image = cv2.imread(dist_path)
    ref_image = cv2.imread(ref_path)

    if dist_image is None or ref_image is None:
        print("Unable to read input images.")
        sys.exit(1)

    return dist_image, ref_image


def compute_metrics(dist_image, ref_image, selected_metrics, color_spaces_to_use):
    """
    Compute the specified IQA metrics for the given images and color spaces.

    Args:
        dist_image (numpy.ndarray): Distorted image.
        ref_image (numpy.ndarray): Reference image.
        selected_metrics (dict): Dictionary of selected metrics and their functions.
        color_spaces_to_use (list): List of color spaces to use for computing metrics.

    Returns:
        list: List of dictionaries containing metric results for each color space.
    """
    results = []
    for metric_name, metric_fn in selected_metrics.items():
        metric_result = {'Metric': metric_name}
        for color_space_name in color_spaces_to_use:
            try:
                color_space_code = color_spaces[color_space_name]
                dist_image_converted = cv2.cvtColor(
                    dist_image, color_space_code)
                ref_image_converted = cv2.cvtColor(ref_image, color_space_code)
                if metric_name in ["BRISQUE", "NIQE", "MUSIQ", "NIMA", "CLIPIQA"]:
                    metric_result[color_space_name] = metric_fn(
                        dist_image_converted)
                else:
                    metric_result[color_space_name] = metric_fn(
                        dist_image_converted, ref_image_converted)
            except Exception as e:
                print(
                    f"Error computing {metric_name} for {color_space_name}: {e}")
        results.append(metric_result)

    return results


# def main(config_path):
def main(argv):
    """
    Main function to compute IQA metrics and save the results.

    Args:
        config_path (str): Path to the configuration file.
    """
    
    # Suppress all warnings
    warnings.filterwarnings("ignore")

    if (sys.argv[1].endswith(".json")):
        # Read JSON
        config_path = sys.argv[1]

        # set config dict
        config = read_config(config_path)

        dist_path = config.get("distorted_image_path")
        ref_path = config.get("reference_image_path")
        output_folder_path = config.get("output_directory", "out")
        output_csv_name = config.get("output_filename", "metrics.csv")
        generate_maps = config.get("generate_maps", False)
        generate_metrics = config.get("generate_metrics", False)
        map_metrics = config.get("metrics", [])
        color_spaces_to_use = config.get("color_spaces", ["RGB"])
        window_size = config.get("map_window_size", 161)
        step_size = config.get("map_step_size", 50)
        generate_image_difference = config.get("generate_image_difference", False)
        difference_threshold = config.get("difference_threshold", 10)
    else:
        # Set some defaults
        output_folder_path = "out"
        output_csv_name = "metrics.csv"
        generate_maps = False
        generate_metrics = False
        map_metrics = []
        color_spaces_to_use = ["RGB"]
        window_size = 161
        step_size = 50
        generate_image_difference = False
        difference_threshold = 10
        
        # Process Command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('-r', '--ref', type=str, required=True, help='Refrence image')
        parser.add_argument('-c', '--comparison', type=str, required=True, help='Comparison image')
        parser.add_argument('-o', '--output_directory', type=str, default='out', help='Output directory')
        
        args = parser.parse_args()
        


    # Chcek for required fields
    if not dist_path or not ref_path or not output_folder_path:
        print("Missing required fields in the configuration file.")
        sys.exit(1)

    create_output_folder(output_folder_path)

    # load images and metrics
    dist_image, ref_image = load_images(dist_path, ref_path)
    selected_metrics = {metric: metrics[metric]
                        for metric in map_metrics if metric in metrics}

    # Compute metric if flag is on
    if generate_metrics:
        print("Computing metrics...")
        results = compute_metrics(
            dist_image, ref_image, selected_metrics, color_spaces_to_use)

        results_df = pd.DataFrame(results)
        csv_path = os.path.join(output_folder_path, output_csv_name)
        results_df.to_csv(csv_path, index=False)
        print(f"Results saved to {csv_path}")

        # Compute maps if flag is on
    if generate_maps:
        print("Computing Metric Maps...")
        compute_maps(dist_image, ref_image, selected_metrics, color_spaces_to_use,
                     os.path.join(output_folder_path, "map"), window_size, step_size)

        # compute diff if flag is on
    if generate_image_difference:
        print("Computing image difference...")
        for color_space_name in color_spaces_to_use:
            color_space = get_color_space_code(color_space_name)
            diff_output_path = os.path.join(
                output_folder_path, f"diff_image_{color_space_name.lower()}.png")
            generate_thresholded_diff_image(
                dist_path, ref_path, difference_threshold, color_space, diff_output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compute_metrics.py <config_file>")
        sys.exit(1)

    # config_path = sys.argv[1]
    # main(config_path)
    main(sys.argv)
