import numpy as np
from metrics_library.image_quality import psnr, ssim, mse

def test_psnr():
    img1 = np.ones((256, 256), dtype=np.uint8) * 255
    img2 = np.zeros((256, 256), dtype=np.uint8)
    assert psnr(img1, img2) == float('inf')

def test_ssim():
    img1 = np.ones((256, 256), dtype=np.uint8)
    img2 = np.ones((256, 256), dtype=np.uint8)
    assert ssim(img1, img2) == 1.0

def test_mse():
    img1 = np.array([0, 0, 0])
    img2 = np.array([1, 1, 1])
    assert mse(img1, img2) == 1
