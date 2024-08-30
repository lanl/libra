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
import pandas as pd
import warnings
import numpy as np
from datetime import datetime

from libra.map_computation import compute_map
from libra.image_difference import diff_images
from libra.compute_metrics import *
from libra.utils import *
from libra.metrics import *



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



def main(argv):
    """
    Main function to compute IQA metrics and save the results.

    Args:
        config_path (str): Path to the configuration file.
    """
    
    # Suppress all warnings
    warnings.filterwarnings("ignore")
    
    
    # Process Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--json', type=str, required=False, help='JSON Input file')
    
    required_arg = True
    if '-j' in sys.argv or '--json' in sys.argv:
        required_arg = False
    
    parser.add_argument('-r', '--ref', type=str, required=required_arg, help='Refrence image')
    parser.add_argument('-c', '--comparison', type=str, required=required_arg, help='Comparison image')
    parser.add_argument('-m', '--metrics', nargs='+', required=required_arg, default=[], help='metrics to use e.g SSIM')
    
    parser.add_argument('-o', '--output_directory', type=str, required=False, default="", help='Output directory')
    parser.add_argument('-d', '--imgdiff', required=False, action="store_true", help='generate image diff')
    parser.add_argument('-s', '--diffcolspace', nargs='+', required=False, default=['RGB'], help='color space to use for diff')
    parser.add_argument('-t', '--diffthreshold', type=float, default=10, help='Theshold difference')
    parser.add_argument('-p', '--mapdiff', required=False, action="store_true", help='generate image diff map')
    
    args = parser.parse_args()
    run_mode = "CMD"
    if args.json is not None:
        run_mode = "JSON"
    
    #if (sys.argv[1].endswith(".json")):
    if run_mode == "JSON":
        # Read JSON
        config_path = args.json

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
        window_size = config.get("map_window_size", 11)
        step_size = config.get("map_step_size", 50)
        generate_image_difference = config.get("generate_image_difference", False)
        difference_threshold = config.get("difference_threshold", 10)
        
    else:
        
        # Set some defaults
        output_csv_name = "metrics.csv"
        generate_maps = False
        generate_metrics = True
        window_size = 11
        step_size = 50
        
        ref_path = args.ref
        dist_path = args.comparison
        map_metrics = args.metrics
                  
        generate_image_difference = args.imgdiff
        color_spaces_to_use = args.diffcolspace
        difference_threshold = args.diffthreshold
        generate_maps = args.mapdiff
        
        if args.output_directory == "":
            now = datetime.now()
            dt_string = now.strftime("%Y_%m_%d__%H_%M")
            output_folder_path = "output-" + dt_string
        else:
            output_folder_path = args.output_directory


    # Check for required fields
    if not dist_path or not ref_path or not output_folder_path:
        print("Missing required fields in the configuration file.")
        sys.exit(1)

    create_output_folder(output_folder_path)


    # Compute metric if flag is on
    if generate_metrics:
        print("Computing metrics...")
        results = compute_metrics(dist_path, ref_path, map_metrics, color_spaces_to_use)

        results_df = pd.DataFrame(results)
        if run_mode == "CMD":
            print(results_df)
        csv_path = os.path.join(output_folder_path, output_csv_name)
        results_df.to_csv(csv_path, index=False)
        print(f"Results saved to {csv_path}")

    # Compute maps if flag is on
    if generate_maps:
        print("Computing Metric Maps...")

        for color_space in color_spaces_to_use:
            for metric_name in map_metrics:
                plt = compute_map(dist_path, ref_path, metric_name, color_space, window_size, step_size)
                
                output_path = os.path.join(output_folder_path, "map")
                plt.savefig(f"{output_path}_{color_space}_{metric_name}.png")
                plt.close()
                

    # compute diff if flag is on
    if generate_image_difference:
        print("Computing image difference...")
        
        for color_space_name in color_spaces_to_use:
            
            heatmap, heatmap_eq = diff_images(dist_path, ref_path, difference_threshold, color_space_name)

            # Save the images
            diff_output_path = os.path.join(output_folder_path, f"diff_image_{color_space_name.lower()}.png")
            write_image(heatmap, diff_output_path)
    
            eq_output_path = diff_output_path.replace("diff_image_", "diff_image_eq_")
            write_image(heatmap_eq, eq_output_path)
            
            print(f"Thresholded difference image saved to {diff_output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compute_metrics.py <config_file>")
        sys.exit(1)

    main(sys.argv)
