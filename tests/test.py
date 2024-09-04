import unittest
import numpy as np
import sys
import os
sys.path.append("..")

import src.libra as libra

class TestLibra(unittest.TestCase):
    def setUp(self):
        self.ref_path = "data/test/orig.png"
        self.cmp_path = "data/test/compressed.png"
        
        
    def test_metrics(self):
        '''
        Making sure that some core metrics are the same
        '''
        precomputed_results = [0.8878801465034485, 0.9144885540008545, 0.9379053115844727, 9963.424492668622, 9203.078399664852, 11965.944987850859]
        results = []
        metric_names = ['SSIM', 'MSE']
        colorspace_names = ['RGB', 'HSV', 'LAB']
        for metric_name in metric_names:
            for colorspace_name in colorspace_names:
                results.append( libra.compute_metric(self.cmp_path, self.ref_path, metric_name, colorspace_name) )

        self.assertTrue(results == precomputed_results)

        
    def test_image_comparison(self):
        '''
        Ensuring that some image comparisons are the same
        '''
        
        # Load saved test differences
        img_diff_path    = "data/test/diff/diff_image_hsv.png"
        img_diff_eq_path = "data/test/diff/diff_image_eq_hsv.png"
        
        img_diff = libra.load_image(img_diff_path)
        img_diff_eq = libra.load_image(img_diff_eq_path)
        
        # Compute Diff
        diff_img, diff_img_eq = libra.diff_images(self.ref_path, self.cmp_path, 10, 'HSV')
        
    
        self.assertTrue( libra.is_same(diff_img, img_diff) )
        self.assertTrue( libra.is_same(diff_img_eq, img_diff_eq) )


    def test_map_computation(self):
        '''
        Ensure that map computation has not changed
        '''
        
        # Load saved maps
        color_space = libra.get_color_space_code('RGB')
        map_hsv_mse_path  = "data/test/map/map_HSV_MSE.png"
        map_hsv_ssim_path = "data/test/map/map_HSV_SSIM.png"
        
        map_hsv_mse  = libra.load_image(map_hsv_mse_path)
        map_hsv_ssim = libra.load_image(map_hsv_ssim_path)
        
        # Compute Maps
        plt_mse  = libra.compute_map(self.cmp_path, self.ref_path, 'MSE', 'HSV', patch_size=11, step=50)
        plt_mse.savefig(f"temp_hsv_mse.png")
        plt_mse.close()
        
        plt_ssim = libra.compute_map(self.cmp_path, self.ref_path, 'SSIM', 'HSV', patch_size=11, step=50)
        plt_ssim.savefig(f"temp_hsv_ssim.png")
        plt_ssim.close()
        
        # Reload and compare
        map_hsv_mse_computed  = libra.load_image("temp_hsv_mse.png")
        map_hsv_ssim_computed = libra.load_image("temp_hsv_ssim.png")
        
        os.remove("temp_hsv_mse.png")
        os.remove("temp_hsv_ssim.png")
        
        self.assertTrue( libra.is_same(map_hsv_mse, map_hsv_mse_computed) )
        self.assertTrue( libra.is_same(map_hsv_ssim, map_hsv_ssim_computed) )
        
        
if __name__ == '__main__':
    unittest.main()
    
    
# In tests folder:
# python -m unittest test.py -v