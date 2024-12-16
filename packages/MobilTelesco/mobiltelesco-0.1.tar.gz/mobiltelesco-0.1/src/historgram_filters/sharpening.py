import cv2
import numpy as np
import tifffile
def frequency_based_enhancement_color(
    image, 
    clarity_factor=1.5, 
    sharpening_rate=1.2, 
    detail_factor=1.0, 
    mask_strength=0.5
):
    """
    Enhance an image using frequency-based filtering while preserving color.

    Args:
        image: Input image (BGR format).
        clarity_factor: Strength of mid-frequency enhancement for clarity.
        sharpening_rate: Strength of high-frequency enhancement for sharpening.
        detail_factor: Balance for overall frequency detail control.
        mask_strength: Mask strength for selective frequency modifications.

    Returns:
        Enhanced color image.
    """
    # Convert image to YCrCb (luminance-chrominance) color space
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    luminance = ycrcb[:, :, 0].astype(np.float32) / 255.0

    # Perform 2D FFT on luminance
    dft = np.fft.fft2(luminance)
    dft_shift = np.fft.fftshift(dft)

    # Create frequency masks
    rows, cols = luminance.shape
    crow, ccol = rows // 2, cols // 2

    # Define radii for frequency bands
    low_radius = 30
    high_radius = 100

    # Generate masks
    y, x = np.ogrid[:rows, :cols]
    distance = np.sqrt((x - ccol) ** 2 + (y - crow) ** 2)

    # Low-pass mask
    low_pass_mask = distance <= low_radius

    # High-pass mask
    high_pass_mask = distance >= high_radius

    # Band-pass mask (clarity enhancement)
    band_pass_mask = (distance > low_radius) & (distance < high_radius)

    # Apply frequency filters
    low_pass = dft_shift * low_pass_mask * detail_factor
    high_pass = dft_shift * high_pass_mask * sharpening_rate
    band_pass = dft_shift * band_pass_mask * clarity_factor

    # Combine filtered components
    enhanced_dft = low_pass + band_pass + high_pass

    # Apply mask strength to combine original and enhanced frequencies
    mask = (distance / np.max(distance)) ** mask_strength
    masked_dft = enhanced_dft * (1 - mask) + dft_shift * mask

    # Inverse FFT to reconstruct enhanced luminance
    enhanced_image_shift = np.fft.ifftshift(masked_dft)
    enhanced_luminance = np.fft.ifft2(enhanced_image_shift).real

    # Normalize enhanced luminance to [0, 255]
    enhanced_luminance = np.clip(enhanced_luminance * 255, 0, 255).astype(np.uint8)

    # Replace the original luminance with the enhanced luminance
    ycrcb[:, :, 0] = enhanced_luminance

    # Convert back to BGR color space
    enhanced_color_image = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

    return enhanced_color_image

# Load the input image
image = tifffile.imread('test4.tif')

# Apply frequency-based enhancement
enhanced_color_image = frequency_based_enhancement_color(
    image, 
    clarity_factor=1.1, 
    sharpening_rate=2.0, 
    detail_factor=1.2, 
    mask_strength=1.0
)

# Display the original and enhanced images
cv2.imshow('Original Image', image)
cv2.imshow('Enhanced Color Image', enhanced_color_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the enhanced image
cv2.imwrite('frequency_enhanced_color_image.jpg', enhanced_color_image)
