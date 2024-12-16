import cv2
import numpy as np
import tifffile as tiff

# Load the image (standard 8-bit or 16-bit image)
image = tiff.imread('test2.tif')

def apply_drago_tone_mapping(image, gamma=1.2, saturation=0.8):
    """Apply Drago's tone mapping to an image for HDR effects."""
    # Normalize the image to [0, 1] range
    image_float = image.astype(np.float32) / 65536.0

    # Calculate luminance (grayscale) using the standard formula
    luminance = 0.2126 * image_float[:, :, 2] + 0.7152 * image_float[:, :, 1] + 0.0722 * image_float[:, :, 0]
    
    # Apply logarithmic compression to the luminance
    log_luminance = np.log1p(luminance)
    log_luminance /= np.max(log_luminance)  # Normalize

    # Apply Gaussian blur for local contrast enhancement
    blurred_luminance = cv2.GaussianBlur(log_luminance, (1, 1), 0)

    # Enhance the local contrast
    enhanced_luminance = log_luminance / (blurred_luminance + 1e-5)

    # Apply gamma correction
    enhanced_luminance = np.power(enhanced_luminance, gamma)

    # Clip the enhanced luminance to [0, 1]
    enhanced_luminance = np.clip(enhanced_luminance, 0, 1)

    # Reconstruct the image by applying enhanced luminance to each channel
    tone_mapped_image = np.zeros_like(image_float)
    for i in range(3):  # Loop over BGR channels
        tone_mapped_image[:, :, i] = image_float[:, :, i] * enhanced_luminance

    # Apply saturation adjustment
    tone_mapped_image *= saturation

    # Clip the result to [0, 1]
    tone_mapped_image = np.clip(tone_mapped_image, 0, 65535)

    # Convert back to [0, 255] range for display
    return (tone_mapped_image * 255).astype(np.uint8)

# Apply Drago's Tone Mapping
tone_mapped_image = apply_drago_tone_mapping(image, gamma=0.3, saturation=10)

# Show original and tone-mapped images
cv2.imshow('Original Image', image)
cv2.imshow('Drago Tone Mapped Image', tone_mapped_image)

# Wait for key press and close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the tone-mapped image
cv2.imwrite('drago_tone_mapped_image.jpg', tone_mapped_image)
