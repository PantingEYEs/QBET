"""
File name:
  file_validator.py

Function:
  Validates if the necessary dependencies and folders are present in the project structure.

Dependencies:
  os
  sys
  tkinter
  importlib

"""


# file_validator.py

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox
from importlib import util

# Required directories and files
REQUIRED_DIRS = ["output", "input", "temp"]
REQUIRED_PACKAGES = ["PIL", "cv2", "numpy"]

def check_directories():
    # Ensure that essential directories exist. Create if missing.
    missing_dirs = [dir_name for dir_name in REQUIRED_DIRS if not os.path.exists(dir_name)]
    return missing_dirs

def create_directories(directories):
    # Create specified directories if they do not exist.
    for dir_name in directories:
        os.makedirs(dir_name, exist_ok=True)
    print(f"Created missing directories: {', '.join(directories)}")

def check_packages():
    # Check if required Python packages are installed.
    missing_packages = []
    for package in REQUIRED_PACKAGES:
        if util.find_spec(package) is None:
            missing_packages.append(package)
    return missing_packages

def install_packages(packages):
    # Automatically install missing packages using pip.
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *packages])
        print(f"Successfully installed: {', '.join(packages)}")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install some packages: {', '.join(packages)}")
        return False

def validate_setup():
    # Validates the environment setup and installs missing dependencies if needed.
    missing_dirs = check_directories()
    missing_packages = check_packages()

    # Create missing directories
    if missing_dirs:
        create_directories(missing_dirs)
        # Show a message box if directories were missing
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showinfo("Directory Check", f"Created missing directories: {', '.join(missing_dirs)}")

    # Install missing packages
    if missing_packages:
        print(f"Missing packages detected: {', '.join(missing_packages)}")
        if not install_packages(missing_packages):
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            messagebox.showerror("Dependency Check", "Failed to install some packages. Please try manually.")
            return False  # Indicate that setup is not complete
    else:
        print("All dependencies and folders are in place.")

    return True  # Indicate successful setup

if __name__ == "__main__":
    if not validate_setup():
        print("Setup validation failed. Exiting.")
    else:
        print("Setup validation successful.")
