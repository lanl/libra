import unittest
import numpy as np
import sys
import os
sys.path.append("..")

from src.libra.compute_metrics import *
from src.libra.image_difference import *
from src.libra.map_computation import *

class TestLibra(unittest.TestCase):
    def setUp(self):
        self.ref_path = "data/test/orig.png"
        self.cmp_path = "data/test/compressed.png"
        
        
    def test_metrics(self):
        '''
        Making sure that some core metrics are the same
        '''
        
        results = compute_metrics(self.cmp_path, self.ref_path, ['SSIM', 'MSE'], ['RGB', 'HSV', 'LAB'])
        expected_results = [{'Metric': 'SSIM', 'RGB': 0.8878801465034485, 'HSV': 0.9144885540008545, 'LAB': 0.9379053115844727}, 
                            {'Metric': 'MSE', 'RGB': 9963.424492668622, 'HSV': 9203.078399664852, 'LAB': 11965.944987850859}]
        
        self.assertEqual(results, expected_results)

        
    def test_image_comparison(self):
        '''
        Ensuring that some image comparisons are the same
        '''
        
        # Load saved test differences
        img_diff_path    = "data/test/diff/diff_image_hsv.png"
        img_diff_eq_path = "data/test/diff/diff_image_eq_hsv.png"
        
        img_diff = load_image(img_diff_path)
        img_diff_eq = load_image(img_diff_eq_path)
        
        # Compute Diff
        diff_img, diff_img_eq = diff_images(self.ref_path, self.cmp_path, 10, 'HSV')
        
    
        self.assertTrue( is_same(diff_img, img_diff) )
        self.assertTrue( is_same(diff_img_eq, img_diff_eq) )


    def test_map_computation(self):
        '''
        Ensure that map computation has not changed
        '''
        
        # Load saved maps
        color_space = get_color_space_code('RGB')
        map_hsv_mse_path  = "data/test/map/map_HSV_MSE.png"
        map_hsv_ssim_path = "data/test/map/map_HSV_SSIM.png"
        
        map_hsv_mse  = load_image(map_hsv_mse_path)
        map_hsv_ssim = load_image(map_hsv_ssim_path)
        
        # Compute Maps
        plt_mse  = compute_map(self.cmp_path, self.ref_path, 'MSE', 'HSV', patch_size=11, step=50)
        plt_mse.savefig(f"./temp_hsv_mse.png")
        plt_mse.close()
        
        plt_ssim = compute_map(self.cmp_path, self.ref_path, 'SSIM', 'HSV', patch_size=11, step=50)
        plt_ssim.savefig(f"./temp_hsv_ssim.png")
        plt_ssim.close()
        
        # Reload and compare
        map_hsv_mse_computed  = load_image("./temp_hsv_mse.png")
        map_hsv_ssim_computed = load_image("./temp_hsv_ssim.png")
        
        os.remove("./temp_hsv_mse.png")
        os.remove("./temp_hsv_ssim.png")
        
        self.assertTrue( is_same(map_hsv_mse, map_hsv_mse_computed) )
        self.assertTrue( is_same(map_hsv_ssim, map_hsv_ssim_computed) )
        
        
if __name__ == '__main__':
    unittest.main()
    
    
# In tests folder:
# python -m unittest test.py -v