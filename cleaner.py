import os
import shutil
import subprocess
import csv
from utils import get_supported_files
from PyPDF2 import PdfReader, PdfWriter
from docx import Document
from openpyxl import load_workbook

def clean_metadata(path):
    if os.path.isfile(path):
        files = [path]
    elif os.path.isdir(path):
        files = get_supported_files(path)
    else:
        print("Ruta inválida.")
        return

    for file in files:
        ext = os.path.splitext(file)[1].lower()
        print(f"\n🧽 Limpiando: {file}")
        try:
            if ext == ".pdf":
                clean_pdf(file)
            elif ext == ".docx":
                clean_docx(file)
            elif ext in [".jpg", ".jpeg", ".png"]:
                clean_with_exiftool(file)
            elif ext in [".txt", ".sql"]:
                clean_text_file(file)
            elif ext == ".csv":
                clean_csv(file)
            elif ext == ".xlsx":
                clean_xlsx(file)
            elif ext in [".zip", ".rar"]:
                clean_archive(file)
            else:
                print("   ➤ Formato no compatible para limpieza.")
        except Exception as e:
            print(f"   ⚠️ Error limpiando {file}: {e}")

def clean_pdf(file_path):
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata({})
    output = file_path.replace(".pdf", "_cleaned.pdf")
    with open(output, "wb") as f:
        writer.write(f)
    subprocess.run(["exiftool", "-overwrite_original", "-all=", output], capture_output=True)
    print(f"   ➤ PDF limpiado (PyPDF2 + exiftool): {output}")

def clean_docx(file_path):
    from datetime import datetime
    doc = Document(file_path)
    props = doc.core_properties

    props.author = ""
    props.last_modified_by = ""
    props.comments = ""
    props.title = ""
    props.subject = ""
    props.category = ""
    props.keywords = ""
    props.last_printed = datetime(2000, 1, 1)
    props.created = datetime(2000, 1, 1)
    props.modified = datetime(2000, 1, 1)
    props.revision = 1

    output = file_path.replace(".docx", "_cleaned.docx")
    doc.save(output)
    print(f"   ➤ DOCX limpiado: {output}")

def clean_with_exiftool(file_path):
    result = subprocess.run(["exiftool", "-overwrite_original", "-all=", file_path], capture_output=True)
    if result.returncode == 0:
        print("   ➤ Imagen limpiada con exiftool.")
    else:
        print(f"   ⚠️ Error con exiftool: {result.stderr.decode()}")

def clean_text_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    output = file_path.replace(".txt", "_cleaned.txt").replace(".sql", "_cleaned.sql")
    with open(output, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"   ➤ Texto limpiado: {output}")

def clean_csv(file_path):
    output = file_path.replace(".csv", "_cleaned.csv")
    with open(file_path, newline='', encoding="utf-8", errors="ignore") as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    headers = rows[0]
    cleaned_headers = [h for h in headers if h.lower() not in ["password", "secret", "token", "email"]]
    indices = [i for i, h in enumerate(headers) if h in cleaned_headers]

    with open(output, 'w', newline='', encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(cleaned_headers)
        for row in rows[1:]:
            writer.writerow([row[i] for i in indices])

    print(f"   ➤ CSV limpiado: {output}")

def clean_xlsx(file_path):
    wb = load_workbook(file_path)
    wb.properties.creator = ""
    wb.properties.title = ""
    wb.properties.company = ""
    wb.properties.last_modified_by = ""
    wb.properties.description = ""
    wb.properties.keywords = ""
    wb.properties.subject = ""
    wb.properties.category = ""
    wb.properties.identifier = ""
    output = file_path.replace(".xlsx", "_cleaned.xlsx")
    wb.save(output)
    print(f"   ➤ XLSX limpiado: {output}")

def clean_archive(file_path):
    temp_dir = file_path + "_extracted"
    try:
        shutil.unpack_archive(file_path, temp_dir)
        print(f"   ➤ Archivo descomprimido en: {temp_dir}")
        clean_metadata(temp_dir)
    except Exception as e:
        print(f"   ⚠️ Error descomprimiendo {file_path}: {e}")