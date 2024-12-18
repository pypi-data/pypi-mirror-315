import numpy as np
from skimage.metrics import structural_similarity, peak_signal_noise_ratio,mean_squared_error
from skimage import img_as_float
from pytorch_fid import fid_score


def psnr(img1, img2):
    """
    Calculate PSNR between two images of the same dimensions.

    Args:
        img1: numpy array, first image
        img2: numpy array, second image

    Returns:
        PSNR value in dB
    """
    # Ensure the images have the same shape
    if img1.shape != img2.shape:
        raise ValueError("Input images must have the same dimensions.")
    
    # Compute Mean Squared Error (MSE)
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')  # Return infinity if images are identical
    
    # Determine max pixel value based on data type
    if np.issubdtype(img1.dtype, np.integer):
        max_pixel = np.iinfo(img1.dtype).max  # Maximum value for integer types
    elif np.issubdtype(img1.dtype, np.floating):
        max_pixel = 1.0  # For normalized floats (assume [0, 1])
    else:
        raise ValueError("Unsupported image data type.")
    
    # Compute PSNR
    psnr_value = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr_value   

def ssim(img1,img2):
    """
    Calculate SSIM between two images using the SSIM formula.

    Args:
        img1: numpy array, first image
        img2: numpy array, second image

    Returns:
        SSIM value
    """
    # Ensure the images have the same shape
    if img1.shape != img2.shape:
        raise ValueError("Input images must have the same dimensions.")
    
    # Determine max pixel value based on data type
    if np.issubdtype(img1.dtype, np.integer):
        max_pixel = np.iinfo(img1.dtype).max  # Maximum value for integer types
    elif np.issubdtype(img1.dtype, np.floating):
        max_pixel = 1.0  # For normalized floats (assume [0, 1])
    else:
        raise ValueError("Unsupported image data type.")
    
    # Constants for numerical stability
    C1 = (0.01 * max_pixel) ** 2
    C2 = (0.03 * max_pixel) ** 2

    # Means
    mu_x = np.mean(img1)
    mu_y = np.mean(img2)

    # Variances and covariance
    sigma_x = np.var(img1)
    sigma_y = np.var(img2)
    sigma_xy = np.mean((img1 - mu_x) * (img2 - mu_y))

    # SSIM formula
    numerator = (2 * mu_x * mu_y + C1) * (2 * sigma_xy + C2)
    denominator = (mu_x ** 2 + mu_y ** 2 + C1) * (sigma_x + sigma_y + C2)
    ssim_value = numerator / denominator

    return ssim_value

def mse(img1,img2):
    """Returns the Mean Squared Error between two images"""
    return np.mean((img1 - img2)**2)

def fid(real_images_path, fake_images_path):
    """Returns the Frechet Inception Distance between the distributions of real images and artificially generated images"""
    return fid_score.calculate_fid_given_paths([real_images_path, fake_images_path], batch_size=50, device='cuda', dims=2048)

def niqe(img):
    """Returns the Natural Image Quality Evaluator of a artificially generated image"""
    img = img_as_float(img)
    return mse(img, np.zeros_like(img))  # Example using MSE as a placeholder


