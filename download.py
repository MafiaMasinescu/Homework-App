import requests
import os
import sys
import shutil
from tkinter import messagebox

API_URL = f"https://api.github.com/repos/MafiaMasinescu/Homework-App/releases/latest"


if getattr(sys, 'frozen', False):
    app_path = sys.executable
else:
    app_path = os.path.abspath(__file__)
print(f"App Path: {app_path}")
def get_latest_version(ver):
    """Fetches the latest version from GitHub API."""
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            latest_version = response.json()["tag_name"]  # Format: "v1.1"
            return float(latest_version.lstrip("v"))  # Remove 'v' and convert to float
        else:
            messagebox.showerror("Error", f"Failed to fetch version: {response.status_code}")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching version: {e}")
        return None

def download(ver):
    """Downloads and updates the script or executable."""
    global app_path

    update_url = f"https://github.com/MafiaMasinescu/Homework-App/releases/latest/download/main.exe"
    response = requests.get(update_url, stream=True)
    if response.status_code == 200:
        backup_file = app_path + ".bak"
        update_file = app_path + ".new"

        # Backup current file
        shutil.copy(app_path, backup_file)
        print(f"Backup created: {backup_file}")

        # Save new update
        with open(update_file, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        
        print(f"Update downloaded: {update_file}")
        
        def update_batch():
            batch_path = os.path.join(os.path.dirname(app_path), "update.bat")
            log_file = os.path.join(os.path.dirname(app_path), "update_log.txt")

            batch_script = f"""@echo off
echo Updating application... > "update_log.txt"
echo Timestamp: %date% %time% >> "update_log.txt"

echo Waiting for application to close... >> "update_log.txt"
taskkill /F /IM main.exe /T >> "update_log.txt" 2>&1
if %ERRORLEVEL% NEQ 0 echo Warning: Process termination returned code: %ERRORLEVEL% >> "update_log.txt"
timeout /t 2 /nobreak >> "update_log.txt"

echo Deleting old executable... >> "update_log.txt"
if exist "main.exe" (
    echo Old executable found, size: >> "update_log.txt"
    for %%I in ("main.exe") do echo %%~zI bytes >> "update_log.txt"
    del "main.exe" >> "update_log.txt" 2>&1
    if %ERRORLEVEL% NEQ 0 echo Error deleting old executable: %ERRORLEVEL% >> "update_log.txt"
) else (
    echo Warning: Old executable not found >> "update_log.txt"
)
timeout /t 1 /nobreak >> "update_log.txt"

echo Checking for update file... >> "update_log.txt"
if exist "main.exe.new" (
    echo Update file found, size: >> "update_log.txt"
    for %%I in ("main.exe.new") do echo %%~zI bytes >> "update_log.txt"
) else (
    echo ERROR: Update file not found! >> "update_log.txt"
    echo Update failed. >> "update_log.txt"
    pause
    exit /b 1
)

echo Renaming new update... >> "update_log.txt"
rename "main.exe.new" "main.exe" >> "update_log.txt" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error renaming file: %ERRORLEVEL% >> "update_log.txt"
    echo Update failed. >> "update_log.txt"
    pause
    exit /b 1
)

echo Verifying new executable exists... >> "update_log.txt"
if not exist "main.exe" (
    echo ERROR: New executable doesn't exist after rename! >> "update_log.txt"
    echo Update failed. >> "update_log.txt"
    pause
    exit /b 1
)

echo Directory listing: >> "update_log.txt"
dir >> "update_log.txt"

echo Environment PATH: >> "update_log.txt"
echo %PATH% >> "update_log.txt"

echo Starting new version... >> "update_log.txt"
echo Current directory: %CD% >> "update_log.txt"
start "" "main.exe" >> "update_log.txt" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error starting main.exe: %ERRORLEVEL% >> "update_log.txt"
    echo You may need to start the application manually. >> "update_log.txt"
) else (
    echo Application started successfully. >> "update_log.txt"
)
timeout /t 2 >> "update_log.txt"

echo Cleaning up... >> "update_log.txt"
if exist "main.exe.bak" (
    del "main.exe.bak" >> "update_log.txt" 2>&1
    if %ERRORLEVEL% NEQ 0 echo Warning: Could not delete backup file: %ERRORLEVEL% >> "update_log.txt"
)
echo Update completed at %date% %time%. >> "update_log.txt"

echo Update process finished. See update_log.txt for details.
timeout /t 5
exit"""

            with open(batch_path, "w") as batch_file:
                batch_file.write(batch_script)

            return batch_path


        # Create and execute the update batch file
        batch_file = update_batch()
        print(f"Update script created: {batch_file}")
        print("Executing update script and closing application...")
        
        # Start the batch file and exit the current process
        os.startfile(batch_file)
        sys.exit(0)
    else:
        messagebox.showerror("Error", f"Failed to download update: {response.status_code}")

def check_update(currver):
    """Checks if a new version is available."""
    latest_version = get_latest_version(currver)
    if latest_version:
        print(f"Current Version: {currver}, Latest Version: {latest_version}")
        if latest_version > currver:
            print("New version available!")
            return True
        else:
            print("You're up-to-date.")
            return False
    else:
        messagebox.ERROR("Error", "Failed to check for updates.")

