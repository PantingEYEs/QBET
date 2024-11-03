"""
File name:
  output_generator.py

Function:
  Generates the QB.md file in the /output folder, handles image sorting, renaming, and numbering.

Dependencies:
  os
  datetime

"""

#it cannot generation a QB.md   !!!

# output_generator.py

import os
import shutil
from datetime import datetime

class OutputGenerator:
    def __init__(self, root_dir):
        """
        Initializes the OutputGenerator.
        
        :param root_dir: The root directory of the project where 'input' and 'output' folders are located.
        """
        self.root_dir = root_dir
        self.input_dir = os.path.join(root_dir, "input")
        self.output_dir = os.path.join(root_dir, "output")
        self.qb_md_path = os.path.join(self.output_dir, "QB.md")
        self.supported_formats = (".jpg", ".jpeg", ".png", ".heic", ".gif")

        # Ensure the output directory and QB.md file exist
        os.makedirs(self.output_dir, exist_ok=True)
        self._initialize_qb_md()

    def _initialize_qb_md(self):
        """
        Initializes the QB.md file in the output directory if it doesn't already exist.
        """
        if not os.path.exists(self.qb_md_path):
            with open(self.qb_md_path, "w") as qb_md_file:
                qb_md_file.write("# Image Selection Log\n\n")
            print(f"QB.md file created at {self.qb_md_path}")

    def generate_sorted_images(self, selected_folder):
        """
        Copies, sorts, and renames images from the selected folder into the input directory.
        
        :param selected_folder: The folder containing images to process.
        :return: The number of images processed.
        """
        # Ensure input directory exists and is cleared before processing
        os.makedirs(self.input_dir, exist_ok=True)
        for file in os.listdir(self.input_dir):
            os.remove(os.path.join(self.input_dir, file))

        # Find and copy supported images, sorting by modification time
        images = [
            os.path.join(selected_folder, file) 
            for file in os.listdir(selected_folder) 
            if file.lower().endswith(self.supported_formats)
        ]
        images.sort(key=os.path.getmtime)

        # Copy images to input folder and rename them sequentially
        for i, image_path in enumerate(images, start=1):
            new_name = f"{i}{os.path.splitext(image_path)[1].lower()}"
            destination = os.path.join(self.input_dir, new_name)
            shutil.copy2(image_path, destination)
            print(f"Copied {image_path} to {destination}")

        # Write the number of images selected in QB.md
        self._update_qb_md(len(images))
        return len(images)

    def _update_qb_md(self, image_count):
        """
        Updates the QB.md file with the total number of selected images.
        
        :param image_count: The number of images processed and stored in the input folder.
        """
        with open(self.qb_md_path, "a") as qb_md_file:
            qb_md_file.write(f"{image_count} images selected.\n\n")
        print(f"Updated QB.md with image count: {image_count}")
