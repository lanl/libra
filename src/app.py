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

import libra as libra


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
    
    parser.add_argument('-m', '--metrics', type=str, required=False, default="SSIM", help='metrics to use e.g SSIM')
    parser.add_argument('-d', '--imgdiff', required=False, action="store_true", help='generate image diff')
    parser.add_argument('-p', '--mapdiff', required=False, action="store_true", help='generate image diff map')
    
    #parser.add_argument('-o', '--output_directory', type=str, required=False, default="", help='Output directory')
    
    parser.add_argument('-ds', '--diffcolspace', type=str, required=False, default="RGB", help='opencv color space to use for difference; default is JET')
    parser.add_argument('-dc', '--diffcolormap', type=str, required=False, default="JET", help='color map for map difference')
    parser.add_argument('-dt', '--diffthreshold', type=float, default=10, help='Theshold difference')
    
    parser.add_argument('-pc', '--mapcolormap', type=str, required=False, default="gray", help='matplotlib color map for map difference, default is gray')
    parser.add_argument('-pw', '--windowsize', type=int, default=11, help='Window Size for map')
    parser.add_argument('-ps', '--stepsize', type=int, default=5, help='Step Size for map')
    
    
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
        map_colormap = config.get("map_colormap", "gray")
        diff_colormap = config.get("diff_colormap", "JET") 
        
    else:
        generate_metrics = False
        if '-m' in sys.argv or '--metric' in sys.argv:
            generate_metrics = True
        
        generate_maps = args.mapdiff
        generate_image_difference = args.imgdiff
        
        
        ref_path = args.ref
        dist_path = args.comparison
        
        map_metrics = [args.metrics]   
        color_spaces_to_use = [args.diffcolspace]
        difference_threshold = args.diffthreshold
        window_size = args.windowsize
        step_size = args.stepsize
        map_colormap = args.mapcolormap
        diff_colormap = args.diffcolormap
        
        
    options =  generate_metrics or generate_maps or generate_image_difference
    if options == False:
        generate_metrics = True
        map_metrics = ['SSIM']
        color_spaces_to_use = ['LAB']
        print('No option was selected, we will default to using SSIM for comaparing the images in the LAB color space')

        
    
    if run_mode == "JSON":
        libra.create_output_folder(output_folder_path)


    # Compute metric if flag is on
    if generate_metrics:
        if run_mode == "CMD":
            result = libra.compute_metric(dist_path, ref_path, map_metrics[0], color_spaces_to_use[0])
            print(result)
        else:
            print("Computing metrics...")
            
            results = []
            for metric_name in map_metrics:
                metric_result = {'Metric': metric_name}            
                for color_space_name in color_spaces_to_use:
                    metric_result[color_space_name] = libra.compute_metric(dist_path, ref_path, metric_name, color_space_name)
                    
                results.append(metric_result)
                
            results_df = pd.DataFrame(results)
                
            csv_path = os.path.join(output_folder_path, output_csv_name)
            results_df.to_csv(csv_path, index=False)
            print(f"Results saved to {csv_path}")


    # compute diff if flag is on
    if generate_image_difference:
        if run_mode == "CMD":
            color_space_name = color_spaces_to_use[0]
            heatmap, heatmap_eq = libra.diff_images(dist_path, ref_path, difference_threshold, color_space_name, diff_colormap)
            
            # Save the images
            diff_output_path = os.path.join(f"diff_image_{color_space_name.lower()}.png")
            libra.write_image(heatmap, diff_output_path)
        
            eq_output_path = diff_output_path.replace("diff_image_", "diff_image_eq_")
            libra.write_image(heatmap_eq, eq_output_path)
            
            print(f"Difference images saved to {diff_output_path} and {eq_output_path}")
            
        else:
            print("Computing image difference...")
            
            for color_space_name in color_spaces_to_use:
                heatmap, heatmap_eq = libra.diff_images(dist_path, ref_path, difference_threshold, color_space_name, diff_colormap)

                # Save the images
                diff_output_path = os.path.join(output_folder_path, f"diff_image_{color_space_name.lower()}.png")
                libra.write_image(heatmap, diff_output_path)
        
                eq_output_path = diff_output_path.replace("diff_image_", "diff_image_eq_")
                libra.write_image(heatmap_eq, eq_output_path)
                
                print(f"Thresholded difference image for {color_space_name} saved to {diff_output_path}")


    # Compute maps if flag is on
    if generate_maps:
        if run_mode == "CMD":
            color_space_name = color_spaces_to_use[0]
            metric_name = map_metrics[0]
            
            plt = libra.compute_map(dist_path, ref_path, metric_name, color_space_name, window_size, step_size, map_colormap)
            plt.savefig(f"map_{color_space_name}_{metric_name}.png")
            plt.close()
            
            print(f"Difference map saved to map_{color_space_name}_{metric_name}.png")
            
        else:
            print("Computing Metric Maps...")
            
            for color_space in color_spaces_to_use:
                for metric_name in map_metrics:
                    plt = libra.compute_map(dist_path, ref_path, metric_name, color_space, window_size, step_size, map_colormap)
                    
                    output_path = os.path.join(output_folder_path, "map")
                    plt.savefig(f"{output_path}_{color_space}_{metric_name}.png")
                    plt.close()
                    
                    print(f"Difference map for colorspace {color_space} and metric {metric_name} saved to {output_path}_{color_space}_{metric_name}.png")



if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.argv.append('-h')

    main(sys.argv)
