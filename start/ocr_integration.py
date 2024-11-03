"""
File name:
  ocr_integration.py

Function:
  Integrates the OCR command to process cropped images, handles OCR output text saving to QB.md.

Dependencies:
  subprocess
  os

"""

# ocr_integration.py

import os
import subprocess

# Set the root directory as a configurable variable
ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')  # Assuming QBET_V1.0 as root directory
TEMP_DIR = os.path.join(ROOT_DIR, 'temp')

def run_ocr(image_number):
    """
    Run the OCR command using the provided image number.

    Args:
        image_number (int): The number of the image being processed.

    Returns:
        None
    """
    image_path = os.path.join(TEMP_DIR, str(image_number), "Q.png")
    output_path = os.path.join(TEMP_DIR, str(image_number), "Q.txt")
    
    # Construct the OCR command
    command = f'umi-ocr --path "{image_path}" --output "{output_path}"'
    print(f"Executing command: {command}")
    
    try:
        # Execute the command
        subprocess.run(command, shell=True, check=True)
        print(f"OCR completed for image {image_number}. Output saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"OCR failed for image {image_number}. Error: {e}")

def batch_run_ocr(image_numbers):
    """
    Run OCR for a batch of images.

    Args:
        image_numbers (list of int): List of image numbers to process.

    Returns:
        None
    """
    for image_number in image_numbers:
        run_ocr(image_number)

# Example usage
if __name__ == "__main__":
    # Example batch processing of images with IDs 1, 2, and 3
    example_image_numbers = [1, 2, 3]
    batch_run_ocr(example_image_numbers)
