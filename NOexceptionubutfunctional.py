import os
import re
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Function to search for numerical values and their weight-related terms
def find_weight_in_text(text, is_schneider=False):
    results = []
    weight_terms = ["kg", "kilogrammes", "kilograms", "grammes", "grams", "g"]
    
    if is_schneider:
        for term in weight_terms:
            pattern = rf"(\d+[\.,]?\d*)\s*({term})"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).replace(',', '.')
                unit = match.group(2).lower()
                results.append((value, unit))
                break
    else:
        for term in weight_terms:
            pattern = rf"(\d+[\.,]?\d*)\s*({term})"
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                value = match[0].replace(',', '.')
                unit = match[1].lower()
                results.append((value, unit))
    
    return results

# Function to scan PDFs in a selected directory
def scan_pdfs_in_directory():
    directory = filedialog.askdirectory()
    if not directory:
        return
    
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Folder Name, Value, Term\n")
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                folder_name = os.path.basename(root)
                text = extract_text_from_pdf(pdf_path)
                is_schneider = "schneider" in text.lower()
                results = find_weight_in_text(text, is_schneider)
                
                if results:
                    for value, term in results:
                        result_text.insert(tk.END, f"{folder_name}, {value}, {term}\n")
                else:
                    result_text.insert(tk.END, f"{folder_name}, , No relevant weight terms found\n")
                result_text.insert(tk.END, '-' * 40 + "\n")
    
    messagebox.showinfo("Scan Complete", "PDF scanning is complete.")

# GUI Setup
root = tk.Tk()
root.title("PDF Scanner")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=10)

scan_button = tk.Button(frame, text="Select Directory and Scan PDFs", command=scan_pdfs_in_directory)
scan_button.pack()

result_text = scrolledtext.ScrolledText(root, width=70, height=20)
result_text.pack(pady=10)

root.mainloop()
