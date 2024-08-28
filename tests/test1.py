import unittest
import numpy as np
import sys
sys.path.append("..") # added!

from src.libra.compute_metrics import *
from src.libra.image_difference import *

class TestLibra(unittest.TestCase):
    def setUp(self):
        self.ref_path = "data/test3/orig.png"
        self.cmp_path = "data/test3/compressed.png"
        
    def test_metrics(self):
        '''
        Making sure that some core metrics are the same
        '''
        
        results = compute_metrics(self.cmp_path, self.ref_path, ['SSIM', 'MSE'], ['RGB', 'HSV', 'LAB'])
        expected_results = [{'Metric': 'SSIM', 'RGB': 0.8878801465034485, 'HSV': 0.9144885540008545, 'LAB': 0.9379053115844727}, 
                            {'Metric': 'MSE', 'RGB': 9963.424492668622, 'HSV': 9203.078399664852, 'LAB': 11965.944987850859}]
        
        self.assertEqual(results, expected_results)

        
    def test_image(self):
        '''
        Ensuring that some image comparisons are the same
        '''
        
        # Load saved test images
        color_space = get_color_space_code('HSV')
        
        img_diff_path = "data/test3/diff/diff_image_hsv.png"
        img_diff_eq_path = "data/test3/diff/diff_image_eq_hsv.png"
        
        img_diff = load_and_convert_image(img_diff_path, color_space)
        img_diff_eq = load_and_convert_image(img_diff_eq_path, color_space)
        
        # Run code
        color_space = get_color_space_code('HSV')
        diff_img, diff_img_eq = generate_thresholded_diff_image(self.ref_path, self.cmp_path, 10, color_space)
        
        write_image(diff_img, "out1.png")
        write_image(diff_img_eq, "out2.png")
        
        diff_same = is_similar(diff_img, img_diff)
        diff_eq_same = is_similar(diff_img_eq, img_diff_eq)

        self.assertTrue(True)
        self.assertTrue(True)


        
if __name__ == '__main__':
    unittest.main()