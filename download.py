import requests
import customtkinter as ctk
import re
import json

ver = 1.01

app = ctk.CTk()
app.geometry("800x600")
api_url = "https://raw.githubusercontent.com/MafiaMasinescu/Proiect-Facultate-I/main/utils.py"
check_down = ctk.CTkButton(app, text="Check ver", command=lambda: check_update())

check_down.pack()
down_but = ctk.CTkButton(app, text="Download", command=lambda: download())
down_but.pack()

def check_update():
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.text
    pattern = "api_url"
    result = re.search(pattern, data)
    if result:
        start = data.rfind('\n', 0, result.start()) + 1
        end = data.find('\n', result.end())
        if end == -1:
            end = len(data)
        print(data[start+17:end])

def download():
    print("Downloading...")
    

app.mainloop()