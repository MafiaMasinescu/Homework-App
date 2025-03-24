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

def get_latest_version():
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
    global app_path
    update_url = f"https://github.com/MafiaMasinescu/Homework-App/releases/latest/download/main.exe"
    response = requests.get(update_url, stream=True)
    if response.status_code == 200:
        backup_file = app_path + ".bak"
        update_file = app_path + ".new"
        shutil.copy(app_path, backup_file)
        print(f"Backup created: {backup_file}")
        with open(update_file, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
                
        def update_batch():
            batch_path = os.path.join(os.path.dirname(app_path), "update.bat")
            batch_script = f"""@echo off
            echo Updating application...
            echo Waiting for application to close...
            taskkill /F /IM main.exe /T
            timeout /t 2 /nobreak
            echo Deleting old executable...
            del "main.exe"
            timeout /t 1 /nobreak
            echo Renaming new update...
            rename "main.exe.new" "main.exe"
            echo Starting new version...
            start "" "main.exe"
            exit"""
            with open(batch_path, "w") as batch_file:
                batch_file.write(batch_script)

            return batch_path
        batch_file = update_batch()        
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

