import datetime
start_time = datetime.datetime.now()
from PIL import Image
import customtkinter as ctk
import os
import sys

build = 1
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

def LoginFrame():
    app = ctk.CTk()
    app.title("Login")
    app.minsize(800, 600)
    app.maxsize(800, 600)
    app.resizable(False, False)

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
        

    print("Time taken to load: ", datetime.datetime.now() - start_time)
    app.mainloop()

if __name__ == "__main__":
    LoginFrame()