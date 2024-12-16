import os
import pyexiv2
import pandas as pd

def extract_exif(image_path):
    """Extract EXIF metadata from the given image file using pyexiv2."""
    try:
        metadata = pyexiv2.ImageMetadata(image_path)
        metadata.read()

        exif_data = {key: metadata[key] for key in metadata.exif_keys}
        return exif_data
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
        return None

def save_exif_to_csv(image_folder):
    """Save EXIF data of all DNG files in the folder to a CSV file."""
    data = []

    # Iterate over all files in the directory
    for filename in os.listdir(image_folder):
        if filename.lower().endswith('.dng'):
            file_path = os.path.join(image_folder, filename)
            metadata = extract_exif(file_path)

            if metadata:
                metadata['Filename'] = filename  # Add filename for reference
                data.append(metadata)

    if data:
        # Convert the data to a DataFrame and save to CSV
        df = pd.DataFrame(data)
        csv_path = os.path.join(image_folder, 'image_metadata.csv')
        df.to_csv(csv_path, index=False)
        print(f"Metadata saved to image_metadata.csv in {image_folder}")
    else:
        print("No DNG files found or no EXIF data available.")

# Example usage
image_folder = r'C:\Users\HP\Desktop\Mobiltelesco'  # Replace with your folder path
save_exif_to_csv(image_folder)
