import cv2
import numpy as np

# Load the color image
image = cv2.imread('bck.jpg')

# Check if the image was loaded correctly
if image is None:
    print("Error: Image not found.")
    exit()

# Function to apply optimized S-Curve with weights to each channel of a color image
def apply_weighted_s_curve_color(image, w_r=1.0, w_g=1.0, w_b=1.0):
    # Split the image into Red, Green, and Blue channels
    b, g, r = cv2.split(image)
    
    # Function to apply S-Curve transformation to a single channel
    def apply_s_curve_channel(channel):
        # Flatten the channel to 1D array for statistical calculation
        flattened_channel = channel.flatten()
        
        # Calculate the mean and standard deviation for the channel
        mu = np.mean(flattened_channel)  # Midpoint
        sigma = np.std(flattened_channel)  # Spread (sharpness)
        
        # Normalize the channel to [0, 1]
        channel_normalized = channel / 255.0
        
        # Apply the S-Curve transformation
        s_curve = 1 / (1 + np.exp(-(channel_normalized - mu / 255.0) / (sigma / 255.0)))  # Sigmoid function
        
        # Scale back to [0, 255] and convert to uint8
        channel_s_curve = np.uint8(np.clip(s_curve * 255, 0, 255))
        
        return channel_s_curve
    
    # Apply the S-Curve transformation to each channel
    r_s_curve = apply_s_curve_channel(r)
    g_s_curve = apply_s_curve_channel(g)
    b_s_curve = apply_s_curve_channel(b)
    
    # Apply the weights to each channel's transformed result
    r_weighted = np.uint8(np.clip(w_r * r_s_curve, 0, 255))
    g_weighted = np.uint8(np.clip(w_g * g_s_curve, 0, 255))
    b_weighted = np.uint8(np.clip(w_b * b_s_curve, 0, 255))
    
    # Merge the weighted channels back into one image
    image_weighted = cv2.merge([b_weighted, g_weighted, r_weighted])
    
    return image_weighted

# Apply the weighted S-Curve transformation to the color image with specified weights
w_r = 0.7  # Weight for Red channel
w_g = 1.0  # Weight for Green channel
w_b = 1.5  # Weight for Blue channel

weighted_s_curve_image = apply_weighted_s_curve_color(image, w_r=w_r, w_g=w_g, w_b=w_b)

# Show the original and transformed images
cv2.imshow('Original Image', image)
cv2.imshow('Weighted S-Curve Image', weighted_s_curve_image)

# Wait until a key is pressed, then close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the transformed image
cv2.imwrite('weighted_s_curve_color_image.jpg', weighted_s_curve_image)
