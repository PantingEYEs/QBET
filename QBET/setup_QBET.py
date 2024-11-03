import os
import subprocess
import urllib.request
import shutil
import sys

def main():
    # Step 1: Ensure py7zr is installed (if needed for other files)
    try:
        import py7zr
    except ImportError:
        print("Installing py7zr...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "py7zr"])
    
    # Step 2: Change directory to the program root "QBET/start"
    start_path = os.path.join(os.getcwd(), "start")
    if not os.path.exists(start_path):
        print(f"Error: Directory {start_path} does not exist.")
        return
    os.chdir(start_path)

    # Step 3.1: Download the file
    url = "https://github.com/hiroi-sora/Umi-OCR/releases/download/v2.1.4/Umi-OCR_Paddle_v2.1.4.7z.exe"
    file_name = url.split("/")[-1]
    
    print(f"Downloading {file_name}...")
    urllib.request.urlretrieve(url, file_name)

    # Step 3.2: Run the downloaded .exe file to self-extract
    print(f"Running {file_name} to extract contents...")
    subprocess.run([file_name], shell=True)

    # Step 3.3: Move all files from the extracted folder to "QBET/start"
    extracted_folder = "Umi-OCR_Paddle_v2.1.4"
    if os.path.exists(extracted_folder):
        for item in os.listdir(extracted_folder):
            shutil.move(os.path.join(extracted_folder, item), os.getcwd())

    # Step 3.4: Delete the downloaded .exe file and extracted folder
    os.remove(file_name)
    shutil.rmtree(extracted_folder)

    # Step 4.1: Create a virtual environment
    print("Creating virtual environment...")
    subprocess.run(["python3", "-m", "venv", "venv"])

    # Step 4.2: Activate the virtual environment
    activate_script = os.path.join("venv", "Scripts", "activate")
    subprocess.run(activate_script, shell=True)

    # Step 5: Install packages from requirements.txt
    print("Installing packages from requirements.txt...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"])

    # Step 6: Run the main program
    print("Running main program...")
    subprocess.run(["python3", "main.py"])

if __name__ == "__main__":
    main()
