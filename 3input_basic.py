import os
import csv
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
def analyze_pdfs(directory, lambda_str, alyx, gravity_gun, output_file):
    results = []
    
    lambda_str = lambda_str.lower()
    alyx = alyx.lower()
    gravity_gun = gravity_gun.lower()
    
    found_matching_folder = False
    
    for root, _, files in os.walk(directory):
        if lambda_str in os.path.basename(root).lower():
            found_matching_folder = True
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_path = os.path.join(root, file)
                    with fitz.open(pdf_path) as doc:
                        for page in doc:
                            text = page.get_text("text")
                            if not text.strip():  # Check if text extraction failed
                                print(f"Warning: No text extracted from {pdf_path}, consider using OCR.")
                                continue
                            
                            lines = text.split("\n")
                            
                            for line in lines:
                                lower_line = line.lower()
                                numbers = [word for word in line.split() if word.replace('.', '', 1).replace(',', '', 1).isdigit()]
                                
                                if numbers:
                                    if gravity_gun in lower_line and alyx in lower_line:
                                        print(f"Checking line: {line}")  # Debug print
                                        print(f"Found match in {pdf_path}: {line} -> Numbers: {numbers}")  # Debug print
                                        for num in numbers:
                                            results.append([pdf_path, line, num])
                                    elif alyx in lower_line:
                                        print(f"Found Alyx match in {pdf_path}: {line} -> Numbers: {numbers}")  # Debug print
                                        for num in numbers:
                                            results.append([pdf_path, line, num])
    
    if not found_matching_folder:
        messagebox.showwarning("No Matching Folders", f"No folders containing '{lambda_str}' were found.")
        return
    
    if results:
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["PDF Path", "Line", "Extracted Number"])
            writer.writerows(results)
        messagebox.showinfo("Success", f"Analysis complete! Results saved to {output_file}")
    else:
        messagebox.showwarning("No Results", "No matching data found in the PDFs.")

def select_directory():
    folder_selected = filedialog.askdirectory()
    entry_directory.delete(0, tk.END)
    entry_directory.insert(0, folder_selected)

def start_analysis():
    directory = entry_directory.get()
    lambda_str = entry_lambda.get()
    alyx = entry_alyx.get()
    gravity_gun = entry_gravity_gun.get()
    output_file = os.path.join(directory, "pdf_analysis_results.csv")
    
    if not directory or not lambda_str or not alyx or not gravity_gun:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    analyze_pdfs(directory, lambda_str, alyx, gravity_gun, output_file)

# GUI Setup
root = tk.Tk()
root.title("PDF Analysis Tool")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Directory selection
label_directory = tk.Label(frame, text="Select Folder:")
label_directory.grid(row=0, column=0, sticky="w")
entry_directory = tk.Entry(frame, width=50)
entry_directory.grid(row=0, column=1)
button_browse = tk.Button(frame, text="Browse", command=select_directory)
button_browse.grid(row=0, column=2)

# Input fields
label_lambda = tk.Label(frame, text="SUpplier:")
label_lambda.grid(row=1, column=0, sticky="w")
entry_lambda = tk.Entry(frame, width=50)
entry_lambda.grid(row=1, column=1, columnspan=2)

label_alyx = tk.Label(frame, text="Unit:")
label_alyx.grid(row=2, column=0, sticky="w")
entry_alyx = tk.Entry(frame, width=50)
entry_alyx.grid(row=2, column=1, columnspan=2)

label_gravity_gun = tk.Label(frame, text="txt to look for:")
label_gravity_gun.grid(row=3, column=0, sticky="w")
entry_gravity_gun = tk.Entry(frame, width=50)
entry_gravity_gun.grid(row=3, column=1, columnspan=2)

# Start analysis button
button_start = tk.Button(frame, text="Analyze PDFs", command=start_analysis)
button_start.grid(row=4, column=1, pady=10)


def launch_external_program2():
    try:
        subprocess.Popen(["python", "imagebased.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch finalbuild.py:\n{e}")
        # Launch external program button
tk.Button(frame, text="Image_based_Finder", command=launch_external_program2).grid(row=5, column=1, pady=5)

root.mainloop()
