import os
import re
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import pdfplumber
import pandas as pd
import difflib

def find_closest_match(target, options):
    matches = difflib.get_close_matches(target, options, n=1, cutoff=0.6)
    return matches[0] if matches else None

def extract_value_from_pdf(pdf_path, a_value, b_value):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    if not table: continue
                    headers = table[0]
                    b_col_idx = None
                    a_row_idx = None

                    # Fuzzy match B header
                    if headers:
                        b_col_idx = next((i for i, h in enumerate(headers) if find_closest_match(b_value.lower(), [str(h).lower()])), None)

                    # Search A in rows
                    for row_idx, row in enumerate(table):
                        if any(find_closest_match(a_value.lower(), [str(cell).lower()]) for cell in row):
                            a_row_idx = row_idx
                            break

                    if a_row_idx is not None and b_col_idx is not None:
                        try:
                            return table[a_row_idx][b_col_idx]
                        except:
                            return None
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return None

def start_analysis():
    folder_path = filedialog.askdirectory(title="Select Base Folder")
    excel_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx *.xls")])
    column_letter = entry_column.get().strip().upper()

    if not folder_path or not excel_path or not column_letter:
        messagebox.showerror("Missing Input", "Please select folder, Excel file, and input column letter.")
        return

    col_index = ord(column_letter) - ord('A')
    excel_data = pd.read_excel(excel_path)
    results = []

    for root, _, files in os.walk(folder_path):
        folder_name = os.path.basename(root)
        a_value = folder_name.strip()

        # Search matching row in Excel where A is found
        matching_row = excel_data[excel_data.apply(lambda row: a_value.lower() in str(row.values).lower(), axis=1)]
        if matching_row.empty:
            continue

        try:
            b_value = matching_row.iloc[0, col_index]
        except:
            continue

        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                result = extract_value_from_pdf(pdf_path, a_value, str(b_value))
                if result:
                    results.append([a_value, result, os.path.basename(pdf_path)])

    if results:
        output_csv = os.path.join(folder_path, "extracted_table_data.csv")
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Folder Name (A)", "Extracted Value", "PDF File"])
            writer.writerows(results)
        messagebox.showinfo("Done", f"Extraction complete. Saved to {output_csv}")
    else:
        messagebox.showinfo("No Matches", "No matching data was found.")

# GUI Setup
root = tk.Tk()
root.title("PDF Table Extractor Based on Excel")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Enter Excel Column Letter (e.g., U):")
label.grid(row=0, column=0, sticky="w")
entry_column = tk.Entry(frame)
entry_column.grid(row=0, column=1)

btn = tk.Button(frame, text="Start Extraction", command=start_analysis)
btn.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
