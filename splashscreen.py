import os
import re
import fitz  # bestlibrary for FUCKING SURREEEE LFGGG
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import pygame
import time
import subprocess
import sys
#SPLASHSCREENDISPLAY
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


# Function to extract text from a PDF file

#scan pdf in th GUI
#
#def scan_pdfs_in_directory():
#    directory = filedialog.askdirectory()
#    if not directory:
#        return
    
#    result_text.delete(1.0, tk.END)
#    result_text.insert(tk.END, "Folder Name, Value, Term\n")
    
#    for root, _, files in os.walk(directory):


#slashsccreenbe4 the GUI
show_splash()

# stup gui
root = tk.Tk()
root.title("Data_Scouter")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=10)

root.mainloop()
import sys
subprocess.run([sys.executable, "3input_basic.py"])

try:
    subprocess.Popen(["python", "3input_basic.py"])
except Exception as e:
    messagebox.showerror("Error", f"Failed to launch finalbuild.py: {e}")