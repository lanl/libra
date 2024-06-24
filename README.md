# Visualization Quality Assessment: Libra


### Overview
This is a subset of the original Visualization Quality Assessment that focuses exclusively on evaluation. This project provides tools to compute various image quality assessment (IQA) metrics, both full-reference and no-reference. The metrics are designed to evaluate the quality of images by comparing them to reference images (full-reference) or without any reference (no-reference). This project supports a wide range of metrics, suitable for different use cases in image processing and computer vision.

## Features
- **Compute Image Quality Assesment Metrics**: Assessment quality with multiple full and no reference metrics
- **Multiple Color Spaces**: Support for different color spaces (e.g., RGB, HSV) to assess image quality in various domains.
- **Heatmaps Generation**: Generate metric maps visualizing the spatial distribution of metric values across the image
- **Image Difference**: Generate thresholded difference images to highlight significant differences between two images
- **Configurable via JSON**: Flexible configuration through JSON files for specifying image paths, metrics, color spaces, and output options.

## Installation
1. Clone Repository
```
git clone git@github.com:lanl/vizStudy.git
```
2. Install Dependencies
```sh
pip install opencv-python-headless numpy matplotlib scikit-image torch piq pyiqa ImageHash
```
or 
```
conda install conda-forge::pytorch
conda install piq -c photosynthesis-team -c conda-forge -c PyTorch
conda install conda-forge::image-quality
conda install pandas
```

## Usage

### Set up json configuration

The JSON configuration file should contain the following keys:

- **reference_image_path (str)**: Path to the reference image.
- **distorted_image_path (str)**: Path to the distorted image.
- **output_directory (str)**: Path to the output directory where the CSV file and metric maps will be saved.
- **output_filename (str, optional)**: Name of the output CSV file (default: "metrics.csv").
- **generate_metrics (bool, optional)**: Flag to generate metrics (default: False).
- **generate_maps (bool, optional)**: Flag to generate metric maps (default: False).
- **generate_image_difference (bool, optional)**: Flag to generate thresholded difference images (default: False).
- **difference_threshold (int, optional)**: Threshold value for generating thresholded difference images (default: 10).
- **metrics (list of str, optional)**: List of metrics to compute.
- **color_spaces (list of str, optional)**: List of color spaces to use for computing metrics (default: ["RGB"]).
- **map_window_size (int, optional)**: Window size for computing metric maps (default: 161).
- **map_step_size (int, optional)**: Step size for computing metric maps (default: 50).

---

Here is an example of the JSON configuration:

```json
{
    "reference_image_path": "/ref_path",
    "distorted_image_path": "/dist_path",
    "output_directory": "/out_path",
    "output_filename": "metrics.csv",
    "generate_metrics": false,
    "generate_maps": true,
    "generate_image_difference":true,
    "difference_threshold": 100,
    "metrics": ["SSIM", "VSI", "GMSD", "MSE", "DSS"],
    "color_spaces": ["RGB", "HSV"],
    "map_window_size": 150,
    "map_step_size": 30
}

```
Run following command to compute:
```
python main.py <config-path>
```

## Example Usage

This example evaluates the visualization quality of isotropic turbulence dataset subjected to tensor compression with a maximum Peak Signal-to-Noise Ratio (PSNR) of 40. The assessment focuses on how effectively the tensor compression retains the visual fidelity of the turbulence data.

**References**\
**Dataset**: https://klacansky.com/open-scivis-datasets/\
**Compression Technique**: https://github.com/rballester/tthresh

<table>
  <tr>
    <td style="text-align: center;">
      <p style="font-weight: bold;">Reference Image</p>
      <img src="./data/test/orig.png" alt="Example 1" style="width: 400px; height: auto;">
    </td>
    <td style="text-align: center;">
      <p style="font-weight: bold;">Compressed Image (PSNR: 40)</p>
      <img src="./data/test/compressed.png" alt="Example 2" style="width: 400px; height: auto;">
    </td>
  </tr>
</table>


### Image Quality Maps
### RGB Color Space
<img src="./data/test/map_RGB.png" alt="Example 2" style="max-width: 100%; height: auto;">

### HSV Color Space
<img src="./data/test/map_HSV.png" alt="Example 2" style="max-width: 100%; height: auto;">


### Compatible Color Spaces




| **Color Space** | **Description**                                                                                                         | **Reference**                                                                                             |
|-----------------|-------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| RGB             | Standard color space with three primary colors: Red, Green, and Blue. Commonly used in digital images and displays.    |(https://en.wikipedia.org/wiki/RGB_color_model)                                            |
| HSV             | Stands for Hue, Saturation, and Value. Often used in image processing and computer vision because it separates color.    | (https://en.wikipedia.org/wiki/HSL_and_HSV)                                                |
| HLS             | Stands for Hue, Lightness, and Saturation. Similar to HSV but with a different way of representing colors.              | (https://en.wikipedia.org/wiki/HSL_and_HSV)                                                |
| LAB             | Consists of three components: Lightness (L*), a* (green to red), and b* (blue to yellow). Mimics human vision.           | (https://en.wikipedia.org/wiki/CIELAB_color_space)                                         |
| XYZ             | A linear color space derived from the CIE 1931 color matching functions. Basis for many other color spaces.             | (https://en.wikipedia.org/wiki/CIE_1931_color_space)                                       |
| LUV             | Similar to LAB but with a different chromaticity component. Used in color difference calculations and image analysis.   | (https://en.wikipedia.org/wiki/CIELUV)                                                     |
| YCbCr           | Color space used in video compression. Separates the image into luminance (Y) and chrominance (Cb and Cr) components.   | (https://en.wikipedia.org/wiki/YCbCr)                                                    |
| YUV             | Used in analog television and some digital video formats. Separates image into luminance (Y) and chrominance (U and V). | (https://en.wikipedia.org/wiki/YUV)                                                        |


## Image Quality Assesment Metrics

### Full Reference Metrics


Based on open source PIQ implementation (https://github.com/photosynthesis-team/piq)

| Metric       | Description                                                                 | Value Ranges                                          | Reference Link                                            |
|--------------|-----------------------------------------------------------------------------|------------------------------------------------------|-----------------------------------------------------------|
| MSE          | Measures the average squared difference between the reference and test images. | Range: [0, ∞). Lower MSE indicates higher similarity.               | https://en.wikipedia.org/wiki/Mean_squared_error |
| SSIM         | Assesses the structural similarity between images considering luminance, contrast, and structure. | Range: [-1, 1]. Higher values indicate better similarity. | https://en.wikipedia.org/wiki/Structural_similarity |
| PSNR         | Represents the ratio between the maximum possible power of a signal and the power of corrupting noise. | Range: [0, ∞) dB. Higher values indicate better image quality.    | https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio |
| FSIM         | Evaluates image quality based on feature similarity considering phase congruency and gradient magnitude. | Range: [0, 1]. Higher values indicate better feature similarity. | https://ieeexplore.ieee.org/document/5705575 |
| MS-SSIM      | Extension of SSIM that evaluates image quality at multiple scales.          | Range: [0, 1]. Higher values indicate better structural similarity. | https://en.wikipedia.org/wiki/Multi-scale_structural_similarity |
| VSI          | Measures image quality based on visual saliency.                            | Range: [0, 1]. Higher values indicate better visual similarity. | https://ieeexplore.ieee.org/document/6873260 |
| SR-SIM       | Assesses image quality using spectral residual information.                 | Range: [0, 1]. Higher values indicate better visual similarity.                           | https://ieeexplore.ieee.org/document/6467149 |
| MS-GMSD      | Evaluates image quality based on gradient magnitude similarity across multiple scales. | Range: [0, ∞). Lower values indicate higher similarity.     | https://ieeexplore.ieee.org/document/7952357 |
| LPIPS        | Uses deep learning models to assess perceptual similarity.                  | Range: [0, 1]. Lower values indicate higher similarity. | https://arxiv.org/abs/1801.03924 |
| PieAPP       | Deep learning-based metric for perceptual image quality.                    | Range: [0, 1]. Lower values indicate higher quality.      | https://arxiv.org/abs/1806.02067|
| DISTS        | Combines deep learning features to evaluate image quality based on structure and texture similarity. | Range: [0, 1]. Lower values indicate higher similarity.                    | https://arxiv.org/abs/2004.07728|
| MDSI         | Measures image quality based on mean deviation similarity index.            | Range: [0, ∞). Lower values indicate better quality.                | https://arxiv.org/abs/1608.07433|
| DSS          | Computes image quality using a detailed similarity structure.               | Range: [0, 1]. Higher values indicate better similarity.                  | https://ieeexplore.ieee.org/document/7351172 |
| IW-SSIM      | Information-weighted SSIM that emphasizes important regions in images.      | Range: [0, 1]. Higher values indicate better structural similarity. | https://ece.uwaterloo.ca/~z70wang/publications/IWSSIM.pdf |
| VIFp         | Measures image quality based on visual information fidelity.                | Range: [0, 1]. Higher values indicate better preservation of information. | https://ieeexplore.ieee.org/document/1576816 |
| GMSD         | Gradient Magnitude Similarity Deviation metric for assessing image quality. | Range: [0, ∞). Lower values indicate higher similarity.             | https://arxiv.org/abs/1308.3052 |
| HaarPSI      | Uses Haar wavelet-based perceptual similarity index to evaluate image quality. | Range: [0, 1]. Higher values indicate better perceptual similarity. | https://arxiv.org/abs/1607.06140 |




### No Reference Metrics

Implementation bassed on (https://github.com/chaofengc/IQA-PyTorch)
| **Metric** | **Description**                                                                                                                     | **Value Ranges**                                      | **Reference**                                                                                   |
|------------|-------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| BRISQUE    | Blind/Referenceless Image Spatial Quality Evaluator (BRISQUE) uses natural scene statistics to measure image quality.               | Range: [0, 100]. Lower values indicate better quality. | https://live.ece.utexas.edu/research/Quality/BRISQUE_release.zip |
| CLIP-IQA   | Image quality metric that utilizes the CLIP model to assess the visual quality of images based on their similarity to predefined text prompts.         | Range: [0, 1]. Higher values indicate better quality. | https://arxiv.org/abs/2207.12396 |
| NIQE       | Natural Image Quality Evaluator. It assesses image quality based on statistical features derived from natural scene statistics. | Range: [0, 100]. Lower values indicate better quality. | Mittal, A., Soundararajan, R., & Bovik, A. C. (2013). Making a “completely blind” image quality analyzer. IEEE Signal Processing Letters, 20(3), 209-212. |
| MUSIQ      | Multi-Scale Image Quality. An advanced metric that evaluates image quality across multiple scales to better capture perceptual quality. | Range: [0, 1]. Higher values indicate better quality. | Ke, J., Li, Q., & Min, X. (2021). MUSIQ: Multi-scale image quality assessment. IEEE Transactions on Image Processing, 30, 1363-1376. |
| NIMA       | Neural Image Assessment. A deep learning-based model that predicts the aesthetic and technical quality of images. | Range: [0, 10]. Higher values indicate better quality. | Talebi, H., & Milanfar, P. (2018). NIMA: Neural image assessment. IEEE Transactions on Image Processing, 27(8), 3998-4011. |


### Perceptual Hashing (pHash) : 

pHash is a technique used for image retrieval and near-duplicate detection by generating a compact hash value that represents the perceptual content of an image. It calculates a hash based on the entire image, enabling comparisons to identify visually similar images. However, pHash does not directly measure perceptual image quality in terms of fidelity or distortion.

Learn more about pHash on (https://en.wikipedia.org/wiki/Perceptual_hashing).


This program is open source under the BSD-3 License.
Redistribution and use in source and binary forms, with or without modification, are permitted
provided that the following conditions are met:

1.Redistributions of source code must retain the above copyright notice, this list of conditions and
the following disclaimer.
 
2.Redistributions in binary form must reproduce the above copyright notice, this list of conditions
and the following disclaimer in the documentation and/or other materials provided with the
distribution.
 
3.Neither the name of the copyright holder nor the names of its contributors may be used to endorse
or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
