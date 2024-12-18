import numpy as np

def normalize_image(img):
    return (img - np.min(img)) / (np.max(img) - np.min(img))
