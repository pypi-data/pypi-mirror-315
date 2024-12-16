import numpy as np
import cv2
import tifffile as tiff

def load_image(image_path: str):
    """
    Load an image using OpenCV.

    Args:
        image_path (str): Path to the image file.

    Returns:
        np.ndarray: Loaded image array.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    return img

def get_min_max(image: np.ndarray):
    """
    Calculate the minimum and maximum pixel values in the image.

    Args:
        image (np.ndarray): Input image.

    Returns:
        tuple: Minimum and maximum pixel values.
    """
    return np.min(image), np.max(image)

def normalize_and_scale(image: np.ndarray, scale_max: int = 65535):
    """
    Normalize and scale the image to a specified range.

    Args:
        image (np.ndarray): Input image.
        scale_max (int): Maximum value for scaling. Default is 65535.

    Returns:
        np.ndarray: Scaled image.
    """
    min_val, max_val = get_min_max(image)
    normalized = (image - min_val) / (max_val - min_val)
    scaled = np.uint32(normalized * scale_max)
    return scaled, min_val, max_val

def apply_linear_transformation(image: np.ndarray, alpha: float, beta: float, min_val: int, max_val: int):
    """
    Apply a linear transformation to the image using alpha and beta.

    Args:
        image (np.ndarray): Input image.
        alpha (float): Scaling factor.
        beta (float): Offset value.
        min_val (int): Minimum value of the original image.
        max_val (int): Maximum value of the original image.

    Returns:
        np.ndarray: Transformed image.
    """
    transformed = np.clip(alpha * image + beta, min_val, max_val)
    return transformed

def save_image(image: np.ndarray, output_path: str):
    """
    Save an image as a TIFF file.

    Args:
        image (np.ndarray): Image to save.
        output_path (str): Path to save the TIFF file.
    """
    tiff.imwrite(output_path, image)

def display_images(original: np.ndarray, transformed: np.ndarray):
    """
    Display the original and transformed images.

    Args:
        original (np.ndarray): Original image.
        transformed (np.ndarray): Transformed image.
    """
    cv2.imshow('Original', original)
    cv2.imshow('Transformed', transformed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def process_image(image_path: str, output_path: str, alpha: float, beta: float):
    """
    Full processing pipeline for an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the transformed image.
        alpha (float): Scaling factor for linear transformation.
        beta (float): Offset value for linear transformation.
    """
    img = load_image(image_path)
    scaled_img, min_val, max_val = normalize_and_scale(img)
    transformed_img = apply_linear_transformation(scaled_img, alpha, beta, min_val, max_val)
    save_image(transformed_img, output_path)
    display_images(img, transformed_img)

# Example usage
if __name__ == "__main__":
    # Replace 'bck.jpg' and 'new_light.tif' with your input/output paths
    image_path = 'bck.jpg'
    output_path = 'new_light.tif'
    alpha = float(input('* Enter alpha [1/max - 1.0]: '))
    beta = float(input('* Enter beta [<1.0]: '))
    
    process_image(image_path, output_path, alpha, beta)
