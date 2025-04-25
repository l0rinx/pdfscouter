import os
import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import csv
import re
import subprocess

def analyze_pdfs(base_dir, folder_keyword, search_text, unit):
    results = []

    folder_keyword = folder_keyword.lower()
    search_text = search_text.lower()
    unit = unit.lower()
    search_terms = search_text.split()

    for root, _, files in os.walk(base_dir):
        folder_name = os.path.basename(root).lower()
        if folder_keyword not in folder_name:
            continue

        for file in files:
            if not file.lower().endswith(".pdf"):
                continue

            pdf_path = os.path.join(root, file)
            try:
                doc = fitz.open(pdf_path)
                for page in doc:
                    lines = page.get_text("text").split("\n")
                    for line in lines:
                        lower_line = line.lower()
                        normalized_line = re.sub(r'[^\w\s]', '', lower_line)
                        if all(term in normalized_line for term in search_terms):
                            segments = re.split(r"[,.]", line)
                            for segment in segments:
                                numbers = re.findall(r"\b\d+(?:[.,]\d+)?\b", segment)
                                if numbers and (unit in lower_line or unit == ""):
                                    for number in numbers:
                                        results.append([pdf_path, line, number])
            except Exception as e:
                print(f"Error reading {pdf_path}: {e}")

    if results:
        output_path = os.path.join(base_dir, "pdf_analysis_results.csv")
        try:
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["PDF Path", "Matched Line", "Extracted Number"])
                writer.writerows(results)
            messagebox.showinfo("Success", f"Results saved to {output_path}")
        except PermissionError:
            messagebox.showerror("Error", "Cannot write results file. Make sure it is not open or write-protected.")
    else:
        messagebox.showinfo("Done", "No matching data found.")

def start_analysis():
    base_dir = entry_dir.get()
    folder_keyword = entry_folder_keyword.get()
    search_text = entry_search_text.get()
    unit = entry_unit.get()

    if not all([base_dir, folder_keyword, search_text]):
        messagebox.showerror("Input Error", "Please fill in all required fields.")
        return

    analyze_pdfs(base_dir, folder_keyword, search_text, unit)

def browse_folder():
    selected = filedialog.askdirectory()
    if selected:
        entry_dir.delete(0, tk.END)
        entry_dir.insert(0, selected)

def launch_external_program():
    try:
        subprocess.Popen(["python", "3input_basic.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch finalbuild.py:\n{e}")


def launch_external_program2():
    try:
        subprocess.Popen(["python", "imagebaseds.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch finalbuild.py:\n{e}")

root = tk.Tk()
root.title("PDF Folder Analyzer")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Directory browser
tk.Label(frame, text="Select Base Folder:").grid(row=0, column=0, sticky="w")
entry_dir = tk.Entry(frame, width=50)
entry_dir.grid(row=0, column=1)
tk.Button(frame, text="Browse", command=browse_folder).grid(row=0, column=2)

# Folder keyword
tk.Label(frame, text="Folder name must contain:").grid(row=1, column=0, sticky="w")
entry_folder_keyword = tk.Entry(frame, width=50)
entry_folder_keyword.grid(row=1, column=1, columnspan=2)

# Search text
tk.Label(frame, text="Text to search in PDF:").grid(row=2, column=0, sticky="w")
entry_search_text = tk.Entry(frame, width=50)
entry_search_text.grid(row=2, column=1, columnspan=2)

# Unit
tk.Label(frame, text="Unit (optional):").grid(row=3, column=0, sticky="w")
entry_unit = tk.Entry(frame, width=50)
entry_unit.grid(row=3, column=1, columnspan=2)

# Analyze button
tk.Button(frame, text="Analyze PDFs", command=start_analysis).grid(row=4, column=1, pady=10)

# Launch external program button
tk.Button(frame, text="1stFinder", command=launch_external_program).grid(row=5, column=1, pady=5)

# Launch external program button
tk.Button(frame, text="Image_based_Finder", command=launch_external_program2).grid(row=5, column=1, pady=5)


root.mainloop()
