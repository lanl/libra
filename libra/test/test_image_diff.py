import unittest
import cv2
import numpy as np
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.image_difference import get_color_space_code, load_and_convert_image, generate_thresholded_diff_image

class TestImageDiff(unittest.TestCase):
    
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
        if os.path.exists('output_diff.png'):
            os.remove('output_diff.png')

    def test_get_color_space_code(self):
        self.assertEqual(get_color_space_code('RGB'), cv2.COLOR_BGR2RGB)
        self.assertEqual(get_color_space_code('HSV'), cv2.COLOR_BGR2HSV)
        self.assertEqual(get_color_space_code('INVALID'), cv2.COLOR_BGR2RGB)

    def test_load_and_convert_image(self):
        image = load_and_convert_image('test_image1.png', cv2.COLOR_BGR2GRAY)
        self.assertEqual(len(image.shape), 2)  # Check if the image is grayscale
        
        with self.assertRaises(FileNotFoundError):
            load_and_convert_image('non_existent_image.png', cv2.COLOR_BGR2GRAY)

    def test_generate_thresholded_diff_image(self):
        generate_thresholded_diff_image(
            'test_image1.png', 
            'test_image2.png', 
            threshold=50, 
            color_space_code=cv2.COLOR_BGR2GRAY, 
            output_path='output_diff.png'
        )
        self.assertTrue(os.path.exists('output_diff.png'))
        
        # Load the output image and check if it is not empty
        output_image = cv2.imread('output_diff.png', cv2.IMREAD_GRAYSCALE)
        self.assertTrue(np.any(output_image))

if __name__ == '__main__':
    unittest.main()
