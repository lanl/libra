from .utils import *
from .metrics import *

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


def compute_metrics(dist_path, ref_path, map_metrics, color_spaces_to_use):
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