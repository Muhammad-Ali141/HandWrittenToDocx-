import cv2
import numpy as np
import os

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Denoise then sharpen — better than hard thresholding for handwriting
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(denoised, -1, kernel)

    base, ext = os.path.splitext(image_path)
    processed_path = base + "_processed" + ext
    cv2.imwrite(processed_path, sharpened)
    return processed_path
