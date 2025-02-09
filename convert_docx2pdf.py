
import glob
import os
from docx2pdf import convert

folder_path = ""  # Path to the folder containing the .docx files
docx_files = glob.glob(os.path.join(folder_path, "*.docx"))

for docx_file in docx_files:
    base_name = os.path.splitext(docx_file)[0]
    pdf_file = base_name + ".pdf"

    try:
        convert(docx_file, pdf_file)
        print(f"Succeed: {docx_file} → {pdf_file}")
    except Exception as e:
        print(f"Fail: {docx_file}, Error: {e}")
