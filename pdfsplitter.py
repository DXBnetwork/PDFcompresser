from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
 


import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askdirectory

def split_pdf_by_size(input_pdf, output_folder):
    input_pdf = Path(input_pdf)
    output_folder = Path(output_folder)
    # Convert size to bytes
    max_size_bytes = 10 * 1024 * 1024
    # Create output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)
    # Read the input PDF
    reader = PdfReader(input_pdf)
    total_pages = len(reader.pages)
    part_number = 1
    writer = PdfWriter()
    for page_number in range(total_pages):
        writer.add_page(reader.pages[page_number])
        # Save the file if it exceeds the size limit
        temp_path = output_folder / f"part_{part_number}.pdf"
        with temp_path.open(mode="wb") as temp_file:
            writer.write(temp_file)
            temp_file_size = temp_path.stat().st_size
        if temp_file_size >= max_size_bytes:
            part_number += 1
            writer = PdfWriter()
    # Save any remaining pages
    if writer.pages:
        final_path = output_folder / f"part_{part_number}.pdf"
        with final_path.open(mode="wb") as final_file:
            writer.write(final_file)
    print(f"PDF has been split into parts under 12 MB each in {output_folder}.")
 
if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Open the file dialog to select a file
    file_path = filedialog.askopenfilename(title='Select File') # Changed from askdirectory
    input_pdf = file_path
    output_folder = "output_pdfs"
    # Maximum size of each split PDF in MB
    split_pdf_by_size(input_pdf, output_folder)
