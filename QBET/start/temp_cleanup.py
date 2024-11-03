"""
File name:
  temp_cleanup.py

Function:
  Clears the /temp folder when moving to the next question.

Dependencies:
  os
  shutil

"""

import os
import shutil

def clean_temp_folder(folder_path):
    """
    Clean the temporary folder by deleting all image files.

    Args:
        folder_path (str): The path to the temporary folder.

    Returns:
        None
    """
    if os.path.exists(folder_path):
        # List all files in the temporary folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                # Remove the file
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                # If there are directories, remove them
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Deleted directory: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    else:
        print(f"The folder {folder_path} does not exist.")

# Example usage
if __name__ == "__main__":
    # Specify the path to the temp folder
    temp_folder_path = "temp"
    clean_temp_folder(temp_folder_path)
