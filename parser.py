import os
import re
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import pygame
import time
import subprocess
# Function to show splash screen
def show_splash():
    splash_image_path = "intro.png"
    sound_path = "introsound.mp3"
    
    if not os.path.exists(splash_image_path):
        print("Warning: Splash image not found. Skipping splash screen.")
        return
    
    splash_root = tk.Toplevel()
    splash_root.overrideredirect(True)
    
    # Load splash image
    splash_image = Image.open(splash_image_path)
    splash_photo = ImageTk.PhotoImage(splash_image)
    splash_label = tk.Label(splash_root, image=splash_photo)
    splash_label.image = splash_photo
    splash_label.pack()
    
    # Center splash screen
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    img_width, img_height = splash_image.size
    x = (screen_width - img_width) // 2
    y = (screen_height - img_height) // 2
    splash_root.geometry(f"{img_width}x{img_height}+{x}+{y}")
    
    # Play intro sound if available
    if os.path.exists(sound_path):
        pygame.mixer.init()
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    else:
        print("Warning: Intro sound not found. Skipping sound.")
    
    # Fade in effect
    for alpha in range(0, 255, 10):
        splash_root.attributes('-alpha', alpha / 255)
        splash_root.update()
        time.sleep(0.05)
    
    time.sleep(2)
    
    # Fade out effect
    for alpha in range(255, -1, -10):
        splash_root.attributes('-alpha', alpha / 255)
        splash_root.update()
        time.sleep(0.05)
    
    splash_root.destroy()
show_splash()

# GUI Setup
root = tk.Tk()
root.title("Data_Scouter")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=10)

#scan_button = tk.Button(frame, text="Select Directory and Scan PDFs", command=scan_pdfs_in_directory)
#scan_button.pack()

result_text = scrolledtext.ScrolledText(root, width=70, height=20)
result_text.pack(pady=10)

root.mainloop()
subprocess.Popen(["python", "Main.py"])
