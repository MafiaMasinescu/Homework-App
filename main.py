import datetime
start_time = datetime.datetime.now()
from PIL import Image
import customtkinter as ctk
import os
import sys
import download
from tkinter import messagebox
import subprocess

build = 0.99
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
app = ctk.CTk()
app.title("Login")
app.minsize(800, 600)
app.maxsize(800, 600)
app.resizable(False, False)

def add_to_exclusions():
    """Adds the current executable to Windows Defender exclusion list."""    
    exe_path = os.path.abspath(sys.executable)  # Get full path of the EXE
    command = f'powershell -Command "Add-MpPreference -ExclusionPath \'{exe_path}\'"'
    
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully added to exclusions: {exe_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to add exclusion: {e}")
        return

def LoginFrame():

    if getattr(sys, 'frozen', False):  # Check if running as a bundled app
        image_path = os.path.join(sys._MEIPASS, 'images/pattern.png')
    else:
        image_path = os.path.join(os.path.dirname(__file__), 'images/pattern.png')
    
    # Load and create CTkImage
    img = Image.open(image_path)
    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
    background_img = ctk.CTkLabel(master=app, image=ctk_img, text="")
    background_img.pack(fill="both", expand=True)

    if getattr(sys, 'frozen', False):  # Check if running as a bundled app
        image_path = os.path.join(sys._MEIPASS, 'images/settings.png')
    else:
        image_path = os.path.join(os.path.dirname(__file__), 'images/settings.png')
    settings_img = Image.open(image_path)
    settings_img = settings_img.resize((25, 25))
    ctk_settings_img = ctk.CTkImage(light_image=settings_img, dark_image=settings_img, size=(settings_img.width, settings_img.height))
    settings = ctk.CTkButton(master=app, image= ctk_settings_img , text="" , command=lambda: settings() , bg_color="black" , fg_color="gray" , width=10, height=5 ,)
    settings.place(x = 730 , y = 10)

    def settings():
        settings_overlay = ctk.CTkFrame(master=app, fg_color="black")
        settings_overlay.place(relx=0, rely=0, relwidth=1, relheight=1) 
        app.configure(bg="black")
        back_button = ctk.CTkButton(master=app, text="Back",
                                    command=lambda: return_to_login(),
                                    bg_color="black",
                                    fg_color="black",
                                    width=15, height=10,)
        back_button.place(x=10, y=5)
        def return_to_login():
            settings_overlay.destroy()
            back_button.destroy()
            download_button.destroy()
            currver.destroy()
            check_update.destroy()
        
        def check_for_update():
            latest_version = download.get_latest_version(build)
            if latest_version > build:
                download_button.place(relx = 0.5 , rely = 0.6 , anchor="center")
                currver.place(relx = 0.5 , rely = 0.5 , anchor="center")
                currver.configure(text=f"Current Version: {build} | Latest Version: {latest_version}")
            else:
                messagebox.showinfo("No Update", "No new updates available.")
                
        check_update = ctk.CTkButton(master=app , text="Check for updates" ,
                                    command=lambda: check_for_update(),
                                    bg_color="black" , fg_color="black" , width=25, height=15 ,)
        check_update.place(relx = 0.5 , rely = 0.4 , anchor="center")
        currver = ctk.CTkLabel(master=app, text=f"Current Version: {build}", bg_color="black", fg_color="black")
        currver.place(relx = 0.5 , rely = 0.5 , anchor="center")
        download_button = ctk.CTkButton(master=app , text="Download update" ,
                                    command=lambda: download.download(build),
                                    bg_color="black" , fg_color="black" , width=25, height=15 ,)

    print("Time taken to load: ", datetime.datetime.now() - start_time)

if __name__ == "__main__":
    LoginFrame()
    app.mainloop()