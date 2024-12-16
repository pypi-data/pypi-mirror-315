import cv2
import numpy as np
import tifffile
def frequency_based_noise_reduction(image, low_pass_radius=50, mask_strength=0.5):

    # Convert image to YCrCb (luminance-chrominance) color space
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    luminance = ycrcb[:, :, 0].astype(np.float32) / 255.0

    # Perform 2D FFT on luminance
    dft = np.fft.fft2(luminance)
    dft_shift = np.fft.fftshift(dft)

    # Create low-pass filter mask
    rows, cols = luminance.shape
    crow, ccol = rows // 2, cols // 2

    y, x = np.ogrid[:rows, :cols]
    distance = np.sqrt((x - ccol) ** 2 + (y - crow) ** 2)
    low_pass_mask = distance <= low_pass_radius

    # Apply low-pass filtering
    low_passed_dft = dft_shift * low_pass_mask

    # Apply mask strength for blending
    mask = (distance / np.max(distance)) ** mask_strength
    blended_dft = low_passed_dft * (1 - mask) + dft_shift * mask

    # Inverse FFT to reconstruct the image
    reconstructed_shift = np.fft.ifftshift(blended_dft)
    denoised_luminance = np.fft.ifft2(reconstructed_shift).real

    # Normalize the denoised luminance to [0, 255]
    denoised_luminance = np.clip(denoised_luminance * 255, 0, 255).astype(np.uint8)

    # Replace the original luminance with the denoised luminance
    ycrcb[:, :, 0] = denoised_luminance

    # Convert back to BGR color space
    denoised_color_image = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

    return denoised_color_image

# Load the input image
image = cv2.imread('bck.jpg')
# Apply frequency-based noise reduction
denoised_image = frequency_based_noise_reduction(image, low_pass_radius=120, mask_strength=0.8)

# Display the original and denoised images
cv2.imshow('Original Image', image)
cv2.imshow('Denoised Image', denoised_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the denoised image
cv2.imwrite('denoised_image.jpg', denoised_image)
