import requests
import os
import sys
import shutil
from tkinter import messagebox
import subprocess

API_URL = f"https://api.github.com/repos/MafiaMasinescu/Homework-App/releases/latest"

if getattr(sys, 'frozen', False):
    app_path = sys.executable
else:
    app_path = os.path.abspath(__file__)

bat_path = os.path.join(os.path.dirname(app_path), "update.bat")
if os.path.exists(bat_path):
    os.remove(bat_path)

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

        def batch_update():
            """Batch file to replace old file with new update."""
            batch_file = os.path.join(os.path.dirname(app_path), "update.bat")
            with open(batch_file, "w") as f:
                f.write(f'@echo off\n')
                f.write(f'taskkill /f /im main.exe\n')
                f.write(f'timeout /t 2 /nobreak >nul\n')
                f.write(f'move /y "{update_file}" "{app_path}"\n')  
                #f.write(f'del /f "{app_path}"\n')
                #f.write(f'rename "{update_file}" "main.exe"\n')
                f.write(f'start "" "{app_path}"\n')
                f.write(f'del /f "%~f0"\n')

        batch_update()
        subprocess.Popen(["cmd", "/c", bat_path], creationflags=subprocess.CREATE_NO_WINDOW)
        sys.exit(0)
       # for proc in psutil.process_iter(['pid', 'name']):
       #     if "main.exe" in proc.info['name'].lower():
       #         print(f"Terminating process {proc.info['name']} (PID {proc.info['pid']})...")
       #         psutil.Process(proc.info['pid']).terminate()
       #         time.sleep(2)
       # 
       # # Replace old file with new update
       # os.replace(update_file, app_path)
       # print("Update successful! Restarting...")
#
       # # Restart script or executable
       # os.execv(app_path, sys.argv)
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

