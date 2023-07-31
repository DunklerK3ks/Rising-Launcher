import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import threading
import tkinter.ttk as ttk
import zipfile

def start_garrys_mod(connect_to_server=False):
    gmod_path = r"C:\Program Files (x86)\Steam\steamapps\common\GarrysMod"
    hl2_exe_path = os.path.join(gmod_path, "hl2.exe")

    if not os.path.exists(hl2_exe_path):
        messagebox.showerror("Fehler", "Die 'hl2.exe' von Garry's Mod wurde nicht gefunden.")
        return

    try:
        subprocess.run(hl2_exe_path, shell=True)
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Starten von Garry's Mod: {e}")
    else:
        print("Garry's Mod wurde gestartet.")

    if connect_to_server:
        server_ip = "84.200.229.4"
        server_port = "27030"
        server_url = f"steam://connect/{server_ip}:{server_port}"
        os.system(f'start "" "{server_url}"')

def download_image(url, save_path):
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def load_background_image():
    bg_image_url = "https://cdn.discordapp.com/attachments/1103265415569883156/1135662533202677820/BgV3.png"
    save_path = "background_image.png"
    download_image(bg_image_url, save_path)
    return save_path

def load_logo_image():
    logo_url = "https://cdn.discordapp.com/attachments/787365474316320768/1135634515411349615/pageLogo-9e52900a1.png"
    save_path = "logo_image.png"
    download_image(logo_url, save_path)
    return save_path

def download_zip_and_install(url, save_path, target_folder, progress_var):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192

    with open(save_path, 'wb') as f:
        for data in response.iter_content(chunk_size=block_size):
            f.write(data)
            progress_var.set(min(100, progress_var.get() + block_size * 100 // total_size))

    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        zip_ref.extractall(target_folder)

    os.remove(save_path)

def download_and_install_zip():
    url = "https://cdn.discordapp.com/attachments/787365474316320768/1135703263010893886/pokemon_swep_-_rock_1273472995.zip"
    filename = os.path.basename(url)
    save_path = os.path.join(os.path.expanduser('~'), filename)
    target_folder = os.path.join(r"C:\Program Files (x86)\Steam\steamapps\common\GarrysMod\garrysmod\addons")

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.grid(row=5, column=0, padx=10, pady=10, columnspan=2, sticky="we")

    download_thread = threading.Thread(target=download_zip_and_install, args=(url, save_path, target_folder, progress_var))
    download_thread.start()

    messagebox.showinfo("Download gestartet", "Der Download wurde gestartet.\nBitte warten Sie, bis der Vorgang abgeschlossen ist.")

    download_thread.join()

    messagebox.showinfo("Erfolg", f"Das ZIP wurde erfolgreich installiert in: {target_folder}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rising Phoenix Launcher")

    # Setzen des benutzerdefinierten Fenster-Icons
    logo_path = load_logo_image()
    if os.path.exists(logo_path):
        root.iconphoto(True, tk.PhotoImage(file=logo_path))

    # Hintergrundbild für den Dark Mode
    bg_image_path = load_background_image()
    if os.path.exists(bg_image_path):
        bg_image = Image.open(bg_image_path)
        root.geometry(f"{bg_image.width}x{bg_image.height}")
        root.resizable(0, 0)  # Verhindert das Ändern der Fenstergröße
        bg_image_tk = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=bg_image_tk)
        bg_label.place(x=0, y=0)
    else:
        print("Hintergrundbild nicht gefunden.")

    # Stil für die Buttons
    button_style = {"font": ("Helvetica", 16, "bold"), "fg": "white", "bg": "#191919", "borderwidth": 0, "activebackground": "#404040"}

    # Jedi vs Sith Button weiter unten und auf der linken Seite
    jedi_vs_sith_button = tk.Button(root, text="", command=lambda: start_garrys_mod(True), height=0, width=0, **button_style)
    jedi_vs_sith_button.grid(row=2, column=0, padx=25, pady=40, columnspan=2)

    # Größerer Start-Button im Dark Mode
    launch_button = tk.Button(root, text="Jedi vs Sith", command=lambda: start_garrys_mod(True), height=3, width=20, **button_style)
    launch_button.grid(row=3, column=0, padx=10, pady=20, columnspan=2)

    # Größerer Start-Button im Dark Mode
    launch_button = tk.Button(root, text="Clone Wars RP", command=download_and_install_zip, height=3, width=20, **button_style)
    launch_button.grid(row=4, column=0, padx=10, pady=20, columnspan=2)

    root.mainloop()
