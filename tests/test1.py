import unittest
import sys
sys.path.append("..") # added!

from src.libra.compute_metrics import *


def main(argv):
    ref_path = "data/test3/orig.png"
    cmp_path = "data/test3/compressed.png"
    
    results = compute_metrics(cmp_path, ref_path, ['SSIM'], ['RGB'])
    print(results)

if __name__ == "__main__":
    main(sys.argv)