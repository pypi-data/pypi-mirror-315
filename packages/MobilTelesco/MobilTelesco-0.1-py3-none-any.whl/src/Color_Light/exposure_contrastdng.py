import cv2
import numpy as np
from process_raw import DngFile

# Load DNG file
dng_path = "img.dng"
dng = DngFile.read(dng_path)
print(dng.bit)

# Postprocess image (demosaicing)
rgb1 = dng.postprocess()  # Demosaicing with rawpy
cv2.imwrite("rgb1.jpg", rgb1[:, :, ::-1])

# Demosaicing with gamma correction
rgb2 = dng.demosaicing(poww=1)
cv2.imwrite("rgb2.jpg", rgb2[:, :, ::-1])

# Exposure adjustment
def adjust_exposure(img, stops=0):
    scale = 2.0 ** stops
    img = img.astype(np.float32) * scale
    img = np.clip(img, 0, 255)
    return img.astype(np.uint8)

# Contrast adjustment
def adjust_contrast(img, level=0):
    img = img.astype(np.float32) / 255.0      
    midpoint = 0.5
    strength = level * 5
    img = 1 / (1 + np.exp(-strength * (img - midpoint)))
    img = np.clip(img * 255, 0, 255)
    return img.astype(np.uint8)

# Apply exposure and contrast adjustments
def apply_filter(img, exposure_stops=0, contrast_level=0):
    img = adjust_exposure(img, exposure_stops)
    img = adjust_contrast(img, contrast_level)
    return img

if __name__ == "__main__":
    # Load the image to be adjusted
    img = cv2.imread("rgb2.jpg")

    # Set exposure and contrast values
    exposure_value = 0.25  # Range -2 to 2
    contrast_value = 0.95  # Range -0.4 to 1.4

    # Apply adjustments
    adjusted_img = apply_filter(img, exposure_stops=exposure_value, contrast_level=contrast_value)

    # Save adjusted image and DNG file
    # cv2.imshow("Adjusted Image", adjusted_img)
    cv2.waitKey(0)

    # Save DNG with original data
    DngFile.save("C:/Users/HP/Desktop/Mobiltelesco/out.dng", dng.raw, bit=dng.bit, pattern=dng.pattern)

    # Print DNG file details
    print(dng.bit)
    print(dng.pattern)
    print(dng.raw)
