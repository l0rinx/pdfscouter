import os
import csv
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pdfplumber

def analyze_pdfs(directory, lambda_list, alyx_list, gravity_gun_list, output_file, exclude_list):
    results = []

    lambda_list = [l.lower() for l in lambda_list]
    alyx_list = [a.lower() for a in alyx_list]
    gravity_gun_list = [g.lower() for g in gravity_gun_list]
    exclude_list = [e.lower() for e in exclude_list]

    found_matching_folder = False

    for root, _, files in os.walk(directory):
        folder_name = os.path.basename(root).lower()
        if folder_name in exclude_list:
            continue

        if any(lambda_str in folder_name for lambda_str in lambda_list):
            found_matching_folder = True
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_path = os.path.join(root, file)
                    doc = fitz.open(pdf_path)
                    found_value = False

                    for page in doc:
                        lines = page.get_text("text").split("\n")
                        for line in lines:
                            lower_line = line.lower()
                            words = line.split()
                            numbers = [w for w in words if any(c.isdigit() for c in w)]

                            if numbers:
                                for alyx, gravity_gun in zip(alyx_list, gravity_gun_list):
                                    if gravity_gun in lower_line and alyx in lower_line:
                                        results.append([pdf_path, line, numbers[0]])
                                        found_value = True
                                        break
                                    elif alyx in lower_line:
                                        results.append([pdf_path, line, numbers[0]])
                                        found_value = True
                                        break
                                    elif gravity_gun in lower_line:
                                        results.append([pdf_path, line, numbers[0]])
                                        found_value = True
                                        break
                            if found_value:
                                break
                        if found_value:
                            break

    if not found_matching_folder:
        messagebox.showwarning("No Matching Folders", f"No folders containing any of: {', '.join(lambda_list)} were found.")
        return

    if results:
        try:
            with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["PDF Path", "Line", "Extracted Number"])
                writer.writerows(results)
            messagebox.showinfo("Success", f"Analysis complete! Results saved to {output_file}")
        except PermissionError:
            messagebox.showerror("Permission Denied", f"Cannot write to the file: {output_file}. Please close it if open or choose a different folder.")
    else:
        messagebox.showwarning("No Results", "No matching data found in the PDFs.")

def analyze_pdfs_from_tables(directory, lambda_list, alyx_list, gravity_gun_list, output_file, exclude_list):
    results = []

    lambda_list = [l.lower() for l in lambda_list]
    alyx_list = [a.lower() for a in alyx_list]
    gravity_gun_list = [g.lower() for g in gravity_gun_list]
    exclude_list = [e.lower() for e in exclude_list]

    found_matching_folder = False

    for root, _, files in os.walk(directory):
        folder_name = os.path.basename(root).lower()
        if folder_name in exclude_list:
            continue

        if any(lambda_str in folder_name for lambda_str in lambda_list):
            found_matching_folder = True
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_path = os.path.join(root, file)
                    with pdfplumber.open(pdf_path) as pdf:
                        found_value = False

                        for page in pdf.pages:
                            tables = page.extract_tables()
                            for table in tables:
                                for row in table:
                                    line = ' '.join([cell for cell in row if cell])
                                    lower_line = line.lower()
                                    numbers = [cell for cell in row if cell and cell.replace('.', '', 1).replace(',', '', 1).isdigit()]

                                    if numbers:
                                        for alyx, gravity_gun in zip(alyx_list, gravity_gun_list):
                                            if gravity_gun in lower_line and alyx in lower_line:
                                                results.append([pdf_path, line, numbers[0]])
                                                found_value = True
                                                break
                                            elif alyx in lower_line:
                                                results.append([pdf_path, line, numbers[0]])
                                                found_value = True
                                                break
                                            elif gravity_gun in lower_line:
                                                results.append([pdf_path, line, numbers[0]])
                                                found_value = True
                                                break
                                    if found_value:
                                        break
                                if found_value:
                                    break
                            if found_value:
                                break

    if not found_matching_folder:
        messagebox.showwarning("No Matching Folders", f"No folders containing any of: {', '.join(lambda_list)} were found.")
        return

    if results:
        try:
            with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["PDF Path", "Line", "Extracted Number"])
                writer.writerows(results)
            messagebox.showinfo("Success", f"Analysis complete! Results saved to {output_file}")
        except PermissionError:
            messagebox.showerror("Permission Denied", f"Cannot write to the file: {output_file}. Please close it if open or choose a different folder.")
    else:
        messagebox.showwarning("No Results", "No matching data found in the PDFs.")

# GUI Setup
root = tk.Tk()
root.title("PDF Analysis Tool")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# === Tabs ===
tabs = [tk.Frame(notebook) for _ in range(2)]
labels = ["Line-Based Analysis", "Table-Based Analysis"]
callbacks = [analyze_pdfs, analyze_pdfs_from_tables]

for tab, label in zip(tabs, labels):
    notebook.add(tab, text=label)

for tab, callback in zip(tabs, callbacks):
    frame = tk.Frame(tab)
    frame.pack(padx=10, pady=10)

    entry_directory = tk.Entry(frame, width=50)
    dynamic_entries = []
    exclude_entries = []

    def browse_directory(entry=entry_directory):
        folder_selected = filedialog.askdirectory()
        entry.delete(0, tk.END)
        entry.insert(0, folder_selected)

    def add_input_group():
        row = len(dynamic_entries) + 1

        label_lambda = tk.Label(frame, text=f"Name of the Supplier:")
        label_lambda.grid(row=row * 3 - 2, column=0, sticky="w")
        entry_lambda = tk.Entry(frame, width=50)
        entry_lambda.grid(row=row * 3 - 2, column=1, columnspan=2)

        label_alyx = tk.Label(frame, text=f"HINT:")
        label_alyx.grid(row=row * 3 - 1, column=0, sticky="w")
        entry_alyx = tk.Entry(frame, width=50)
        entry_alyx.grid(row=row * 3 - 1, column=1, columnspan=2)

        label_gravity_gun = tk.Label(frame, text=f"Unit:")
        label_gravity_gun.grid(row=row * 3, column=0, sticky="w")
        entry_gravity_gun = tk.Entry(frame, width=50)
        entry_gravity_gun.grid(row=row * 3, column=1, columnspan=2)

        dynamic_entries.append((entry_lambda, entry_alyx, entry_gravity_gun))

    def add_exclude_entry():
        row = 3 * len(dynamic_entries) + len(exclude_entries) + 2
        entry = tk.Entry(frame, width=40)
        entry.grid(row=row, column=1)
        exclude_entries.append(entry)

    tk.Label(frame, text="Select Folder:").grid(row=0, column=0, sticky="w")
    entry_directory.grid(row=0, column=1)
    tk.Button(frame, text="Browse", command=browse_directory).grid(row=0, column=2)

    add_input_group()
    tk.Button(frame, text="Add Another Input Set", command=add_input_group).grid(row=100, column=1, pady=5)

    tk.Label(frame, text="Exclude Folder Named:").grid(row=101, column=0, sticky="w")
    entry_exclude = tk.Entry(frame, width=40)
    entry_exclude.grid(row=101, column=1)
    exclude_entries.append(entry_exclude)
    tk.Button(frame, text="+", command=add_exclude_entry).grid(row=101, column=2)

    def run_analysis():
        directory = entry_directory.get()
        lambda_list = [entry[0].get() for entry in dynamic_entries if entry[0].get()]
        alyx_list = [entry[1].get() for entry in dynamic_entries if entry[1].get()]
        gravity_gun_list = [entry[2].get() for entry in dynamic_entries if entry[2].get()]
        exclude_list = [e.get() for e in exclude_entries if e.get()]

        output_file = os.path.join(directory, "pdf_analysis_results.csv")

        if not directory or not lambda_list or not alyx_list or not gravity_gun_list:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        callback(directory, lambda_list, alyx_list, gravity_gun_list, output_file, exclude_list)

    tk.Button(frame, text="Analyze PDFs", command=run_analysis).grid(row=102, column=1, pady=10)

root.mainloop()
