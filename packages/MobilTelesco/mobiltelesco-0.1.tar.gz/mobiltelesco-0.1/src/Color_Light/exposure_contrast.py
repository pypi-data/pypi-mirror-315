import imageio.v3 as iio
import numpy as np
import cv2

def adjust_exposure(img, stops=0):
    scale = 2.0 ** stops
    return img * scale

def adjust_contrast(img, level=0):
    midpoint = 0.5
    strength = level * 5
    return 1 / (1 + np.exp(-strength * (img - midpoint)))  # Sigmoid contrast adjustment

def apply_filter(img, exposure_stops=0, contrast_level=0):
    img = adjust_exposure(img, exposure_stops)
    img = adjust_contrast(img, contrast_level)
    return img

if __name__ == "__main__":
    # Load the image (96-bit TIFF)
    #img = iio.imread('test4.tif')
    img = cv2.imread('bck.jpg')
    # Set exposure and contrast adjustments
    exposure_val = 1.0  # Range -2 to 2
    contrast_val = 0.0  # Range -0.4 to 1.4

    # Apply adjustments
    adjusted_img = apply_filter(img, exposure_stops=exposure_val, contrast_level=contrast_val)

    # Convert back to 96-bit range and save as TIFF
    adjusted_img = (adjusted_img * 526.0).astype(np.float32)
    cv2.imwrite("br_ct2.jpg", adjusted_img)

    # Display image (convert to 8-bit for visualization)
    # display_img = (adjusted_img * 255).astype(np.uint8)
    # cv2.imshow("Adjusted Image", display_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
