import requests
import customtkinter as ctk
import re
import os
import sys
import shutil
from tkinter import messagebox

API_URL = f"https://api.github.com/repos/MafiaMasinescu/Homework-App/releases/latest"

#check_down = ctk.CTkButton(app, text="Check Version", command=lambda: check_update())
#check_down.pack()
#down_but = ctk.CTkButton(app, text="Download Update", command=lambda: download())
#down_but.pack()

app_path =  __file__  # Get path of current script/exe

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
    global latest_version , app_path
    
    if latest_version is None:
        print("Failed to check for updates.")
        return
        
    update_url = f"https://github.com/MafiaMasinescu/Homework-App/releases/latest/download/Homework-App.exe"
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

