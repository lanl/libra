import sys
import os
import unittest
import numpy as np
import cv2


# Add the root directory of the project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.map_computation import compute_ssim_map, compute_mse_map, compute_patchwise_metric, compute_maps

class TestMapComputation(unittest.TestCase):

    def setUp(self):
        # Create sample images for testing
        self.image1 = np.zeros((100, 100, 3), dtype=np.uint8)
        self.image2 = np.zeros((100, 100, 3), dtype=np.uint8)
        self.image2[50:100, 50:100] = 255

        # Save sample images
        cv2.imwrite('test_image1.png', self.image1)
        cv2.imwrite('test_image2.png', self.image2)

    def tearDown(self):
        # Clean up sample images
        os.remove('test_image1.png')
        os.remove('test_image2.png')
        for file in os.listdir('.'):
            if file.startswith('output_diff') and file.endswith('.png'):
                os.remove(file)

    def test_compute_ssim_map(self):
        image1 = cv2.imread('test_image1.png')
        image2 = cv2.imread('test_image2.png')
        ssim_value, ssim_map = compute_ssim_map(image1, image2)
        self.assertTrue(isinstance(ssim_value, float))
        self.assertTrue(isinstance(ssim_map, np.ndarray))
        self.assertEqual(ssim_map.shape, image1.shape[:2])

    def test_compute_mse_map(self):
        image1 = cv2.imread('test_image1.png')
        image2 = cv2.imread('test_image2.png')
        mse_map = compute_mse_map(image1, image2)
        self.assertTrue(isinstance(mse_map, np.ndarray))
        self.assertEqual(mse_map.shape, image1.shape[:2])
        self.assertGreaterEqual(np.max(mse_map), 0)

    def test_compute_patchwise_metric(self):
        def dummy_metric(patch1, patch2):
            return np.mean((patch1 - patch2) ** 2)

        image1 = cv2.imread('test_image1.png')
        image2 = cv2.imread('test_image2.png')
        metric_map = compute_patchwise_metric(image1, image2, 10, 5, dummy_metric)
        self.assertTrue(isinstance(metric_map, np.ndarray))
        self.assertEqual(metric_map.shape, image1.shape[:2])
        self.assertGreaterEqual(np.max(metric_map), 0)

    def test_compute_maps(self):
        image1 = cv2.imread('test_image1.png')
        image2 = cv2.imread('test_image2.png')
        metrics = {
            'SSIM': lambda im1, im2: compute_ssim_map(im1, im2)[0],
            'MSE': compute_mse_map,
            'dummy_metric': lambda im1, im2: compute_patchwise_metric(im1, im2, 10, 5, lambda p1, p2: np.mean((p1 - p2) ** 2))
        }
        color_spaces = ['RGB', 'HSV']
        output_path = 'output_diff'

        compute_maps(image1, image2, metrics, color_spaces, output_path, patch_size=10, step=5)

        for color_space in color_spaces:
            for metric_name in metrics.keys():
                file_path = f"{output_path}_{color_space}_{metric_name}.png"
                self.assertTrue(os.path.exists(file_path))

if __name__ == '__main__':
    unittest.main()
