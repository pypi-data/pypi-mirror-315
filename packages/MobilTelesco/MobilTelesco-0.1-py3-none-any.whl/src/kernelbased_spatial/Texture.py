import cv2
import numpy as np
import tifffile
# Load the image (assuming it's an 8-bit or 16-bit image)
image = tifffile.imread('test4.tif')

# Function to sharpen the image (for texture enhancement)
def enhance_texture(image, strength=1.5):
    # Create a kernel for sharpening (high-pass filter)
    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]])
    
    # Apply the kernel using convolution
    sharpened_image = cv2.filter2D(image, -1, kernel)
    
    # Adjust the strength of sharpening
    sharpened_image = cv2.addWeighted(image, 1.0, sharpened_image, strength, 0)
    
    return sharpened_image
def enhance_clarity(image, edge_strength=1.5, blend_factor=0.5):
    """
    Enhances the clarity of an image by focusing on edge contrast.

    Args:
    - image: Input image (BGR format).
    - edge_strength: Strength of edge contrast enhancement.
    - blend_factor: Blending factor between the original and enhanced edges.

    Returns:
    - clarity_image: Image with enhanced clarity.
    """
    # Convert image to grayscale to detect edges
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect edges using the Laplacian operator
    edges = cv2.Laplacian(gray_image, cv2.CV_64F)
    
    # Normalize edges to [0, 1] range for blending
    edges = cv2.normalize(edges, None, 0, 1, cv2.NORM_MINMAX)
    
    # Amplify the edges for clarity
    amplified_edges = np.clip(edges * edge_strength, 0, 1)
    
    # Convert amplified edges back to BGR for blending with the original image
    amplified_edges_bgr = cv2.merge([amplified_edges] * 3)
    
    # Enhance the original image by blending with amplified edges
    image_float = image.astype(np.float32) / 255.0
    clarity_image = cv2.addWeighted(image_float, 1 - blend_factor, amplified_edges_bgr, blend_factor, 0, dtype=cv2.CV_64F)
    
    # Scale back to [0, 255] range
    clarity_image = np.clip(clarity_image * 255, 0, 255).astype(np.uint8)
    
    return clarity_image

# Function to dehaze the image
def dehaze(image, strength=1.0):
    # Convert to float32
    image_float = image.astype(np.float32) / 255.0
    
    # Increase global contrast and adjust brightness (remove haze)
    image_float = np.clip(image_float * (1 + strength), 0, 1)
    
    # Apply local contrast enhancement
    enhanced_contrast = cv2.equalizeHist((image_float[:, :, 0] * 255).astype(np.uint8))
    
    # Rebuild the image using enhanced contrast
    for i in range(3):
        image_float[:, :, i] = np.clip(image_float[:, :, i] * enhanced_contrast / 255.0, 0, 1)
    
    # Convert back to [0, 255] range
    return (image_float * 255).astype(np.uint8)

# Apply texture enhancement (sharpening), clarity enhancement, and dehaze in sequence
texture_enhanced = enhance_texture(image, strength=1)
clarity_enhanced = enhance_clarity(texture_enhanced, edge_strength=2, blend_factor=-0.1)
dehaze_enhanced = dehaze(clarity_enhanced, strength=0.8)
# Show the final image after applying all effects
cv2.imshow('Final texture Enhanced Image',texture_enhanced)
cv2.imshow('Final clarity Enhanced Image',dehaze_enhanced)
#cv2.imshow('Original Image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the final enhanced image
tifffile.imwrite('final_enhanced_image.tif', dehaze_enhanced)