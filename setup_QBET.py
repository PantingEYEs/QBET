import os
import subprocess
import urllib.request
import shutil
import sys
import logging

def check_initialized(start_folder):
    """Check if the Initialized file exists in the start folder."""
    return os.path.isfile(os.path.join(start_folder, 'Initialized'))

def create_initialized_file(start_folder):
    """Create an Initialized file in the start folder."""
    with open(os.path.join(start_folder, 'Initialized'), 'w') as f:
        f.write('Initialized')

def main():
    root_directory = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件的绝对路径
    start_folder = os.path.join(root_directory, 'start')  # 将当前目录与'start'文件夹拼接
    
    if not os.path.exists(start_folder):
        print(f"Directory {start_folder} didn't found.")
        return

    if check_initialized(start_folder):
        start(start_folder)
        return
    
    print("Running main() method for initialization...")

    # Define paths for the items to be checked and deleted
    items_to_delete = [
        "start/UmiOCR-data",
        "start/Umi-OCR.exe",
        "start/venv"
    ]

    # Check each item, and delete if it exists
    for item in items_to_delete:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)  # Delete directory
                print(f"Deleted directory: {item}")
            else:
                os.remove(item)  # Delete file
                print(f"Deleted file: {item}")
        else:
            print(f"{item} does not exist.")

    # Ensure py7zr is installed (if needed for other files)
    try:
        import py7zr  # type: ignore
    except ImportError:
        print("Installing py7zr...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "py7zr"])

    # Change directory to the program root "start"
    if not os.path.exists(start_folder):
        print(f"Error: Directory {start_folder} does not exist.")
        return
    os.chdir(start_folder)

    # Download the file
    url = "https://github.com/hiroi-sora/Umi-OCR/releases/download/v2.1.4/Umi-OCR_Paddle_v2.1.4.7z.exe"
    file_name = url.split("/")[-1]

    print(f"Downloading {file_name}...")
    urllib.request.urlretrieve(url, file_name)

    # Run the downloaded .exe file to self-extract
    print(f"Running {file_name} to extract contents...")
    subprocess.run([file_name], shell=True)
    
    # Step 3.3: Move all files from the extracted folder to "/start"
    extracted_folder = "Umi-OCR_Paddle_v2.1.4"
    if os.path.exists(extracted_folder):
        for item in os.listdir(extracted_folder):
            shutil.move(os.path.join(extracted_folder, item), os.getcwd())

    # Step 3.4: Delete the downloaded .exe file and extracted folder
    os.remove(file_name)
    shutil.rmtree(extracted_folder)

    # Step 4.1: Create a virtual environment
    print("Creating virtual environment...")
    subprocess.run(["python3", "-m", "venv", "venv"], check=True)

    # Step 4.2: Activate the virtual environment
    activate_script = os.path.join("venv", "Scripts", "activate")
    subprocess.run(activate_script, shell=True)

    # Step 5.1: Install packages from requirements.txt with updated pip, setuptools, and wheel
    print("Updating pip, setuptools, and wheel...")
    subprocess.run(["pip", "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)

    # Step 5.2: Install packages from requirements.txt
    print("Installing packages from requirements.txt...")
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing requirements: {e}")
        return

    # Create the Initialized file
    create_initialized_file(start_folder)
    print("Initialization complete.")

    # Run the main program
    subprocess.run(["python3", "main.py"], check=True)

def start(start_folder):
    os.chdir(start_folder)
    activate_script = os.path.join("venv", "Scripts", "activate")
    subprocess.run(activate_script, shell=True)
    subprocess.run(["python3", "main.py"], check=True)

if __name__ == "__main__":
    main()
