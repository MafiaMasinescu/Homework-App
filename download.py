import requests
import customtkinter as ctk
import re
import os
import sys
import shutil
from tkinter import messagebox
import time
import psutil

API_URL = f"https://api.github.com/repos/MafiaMasinescu/Homework-App/releases/latest"

#check_down = ctk.CTkButton(app, text="Check Version", command=lambda: check_update())
#check_down.pack()
#down_but = ctk.CTkButton(app, text="Download Update", command=lambda: download())
#down_but.pack()


if getattr(sys, 'frozen', False):
    app_path = sys.executable
else:
    app_path = os.path.abspath(__file__)

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
        
        for proc in psutil.process_iter(['pid', 'name']):
            if "main.exe" in proc.info['name'].lower():
                print(f"Terminating process {proc.info['name']} (PID {proc.info['pid']})...")
                psutil.Process(proc.info['pid']).terminate()
                time.sleep(2)
        
        # Replace old file with new update
        os.replace(update_file, app_path)
        print("Update successful! Restarting...")

        # Restart script or executable
        os.execv(app_path, sys.argv)
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

