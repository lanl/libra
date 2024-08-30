from .utils import *
from .metrics import *


def compute_metrics(dist_path, ref_path, map_metrics, color_spaces_to_use):
    """
    Compute the specified IQA metrics for the given images and color spaces.

    Args:
        dist_path (str): Path of distorted image.
        ref_path (str): Path of reference image.
        selected_metrics (list): List of metrics to use e.g. ['SSIM', 'MSE'].
        color_spaces_to_use (list): List of color spaces to use for computing metrics e.g. ['HSV','LAB']

    Returns:
        list: List of dictionaries containing metric results for each color space.
    """
    dist_image = load_image(dist_path)
    ref_image = load_image(ref_path)
    
    selected_metrics = {metric: metrics[metric]
                        for metric in map_metrics if metric in metrics}
    
    results = []
    for metric_name, metric_fn in selected_metrics.items():
        metric_result = {'Metric': metric_name}
        for color_space_name in color_spaces_to_use:
            try:
                color_space_code = color_spaces[color_space_name]
                dist_image_converted = cv2.cvtColor(dist_image, color_space_code)
                ref_image_converted = cv2.cvtColor(ref_image, color_space_code)
                if metric_name in ["BRISQUE", "NIQE", "MUSIQ", "NIMA", "CLIPIQA"]:
                    metric_result[color_space_name] = metric_fn(dist_image_converted)
                else:
                    metric_result[color_space_name] = metric_fn(dist_image_converted, ref_image_converted)
            except Exception as e:
                print(
                    f"Error computing {metric_name} for {color_space_name}: {e}")
        results.append(metric_result)

    return results


def compute_metric(dist_path, ref_path, metric_name, color_space_name):
    """
    Compute the specified IQA metrics for the given images and color spaces.

    Args:
        dist_path (str): Path of distorted image.
        ref_path (str): Path of reference image.
        metric_name (str): metrics to use e.g. 'SSIM'.
        color_spaces (str): Color spaces to use for computing metrics e.g. 'LAB'

    Returns:
        list: List of dictionaries containing metric results for each color space.
    """
    dist_image = load_image(dist_path)
    ref_image = load_image(ref_path)
    

    if metric_name in metrics:
        metric_fn = metrics[metric_name]
        
        color_space_code = color_spaces[color_space_name]
        dist_image_converted = cv2.cvtColor(dist_image, color_space_code)
        ref_image_converted  = cv2.cvtColor(ref_image, color_space_code)
    
        if metric_name in ["BRISQUE", "NIQE", "MUSIQ", "NIMA", "CLIPIQA"]:
            result = metric_fn(dist_image_converted)
        else:
            result = metric_fn(dist_image_converted, ref_image_converted)

        return result
    else:
        return float("nan")
    
    
    
def list_metrics():
    """
    Returns:
        all the supported metrics
    """
    return metrics.keys()


def list_colorspaces():
    """
    Returns:
        all the supported color spaces
    """
    return color_spaces.keys()


def __dir__():
    return ["compute_metrics", "compute_metric", "list_metrics", "list_colorspaces"]
