"""
File name:
  image_processor.py

Function:
  Processes selected images, performs file copying, renaming, and moves images into /input.

Dependencies:
  os
  shutil
  tkinter

"""


# image_processor.py

import os
import shutil
from tkinter import messagebox

def process_images(selected_path):
    target_folder = "input"
    valid_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.gif'}
    image_files = []

    # Check if the selected path is a file or a directory
    if not os.path.exists(selected_path):
        print(f"Source path '{selected_path}' does not exist.")
        messagebox.showerror("Error", "Source path does not exist.")
        return None

    # If it's a file, just add it to the list if it has a valid extension
    if os.path.isfile(selected_path):
        if any(selected_path.lower().endswith(ext) for ext in valid_extensions):
            image_files.append(os.path.basename(selected_path))
    else:  # If it's a directory, filter images in the folder by valid extensions
        for filename in os.listdir(selected_path):
            if any(filename.lower().endswith(ext) for ext in valid_extensions):
                image_files.append(filename)

    if not image_files:
        print(f"No valid image files found in '{selected_path}'.")
        messagebox.showerror("Error", "No valid image files found.")
        return None

    print(f"Found {len(image_files)} valid image files in '{selected_path}': {image_files}")

    # Copy and rename images to the target folder
    os.makedirs(target_folder, exist_ok=True)
    print(f"Copying and renaming images to '{target_folder}'...")

    processed_images = []  # List to hold processed images

    for index, filename in enumerate(sorted(image_files), start=1):
        if os.path.isfile(selected_path):  # If it's a single file
            source_path = selected_path
            extension = os.path.splitext(filename)[1]  # Get the original extension
            target_name = f"{index}{extension}"  # Keep the original format
            target_path = os.path.join(target_folder, target_name)
        else:  # If it's a directory
            source_path = os.path.join(selected_path, filename)
            extension = os.path.splitext(filename)[1]  # Get the original extension
            target_name = f"{index}{extension}"  # Keep the original format
            target_path = os.path.join(target_folder, target_name)
        print(f"Attempting to copy from '{source_path}' to '{target_path}'")
        try:
            shutil.copy2(source_path, target_path)
            print(f"Copied '{source_path}' to '{target_path}'")
            processed_images.append(target_name)  # Store the processed image name
        except Exception as e:
            print(f"Error copying '{source_path}' to '{target_path}': {e}")
    return len(image_files)  # Return the list of processed image names
