# cleaner.py

import os
import shutil
import subprocess
from utils import get_supported_files

from PyPDF2 import PdfReader, PdfWriter
from docx import Document

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
            elif ext in [".zip", ".rar"]:
                clean_archive(file)
            else:
                print("   ➤ Formato no compatible para limpieza.")
        except Exception as e:
            print(f"   ⚠️ Error limpiando {file}: {e}")

def clean_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata({})
        output = file_path.replace(".pdf", "_cleaned.pdf")
        with open(output, "wb") as f:
            writer.write(f)
        print(f"   ➤ PDF limpiado: {output}")
    except Exception as e:
        print(f"   ⚠️ Error limpiando PDF: {e}")

def clean_docx(file_path):
    try:
        doc = Document(file_path)
        output = file_path.replace(".docx", "_cleaned.docx")
        doc.save(output)
        print(f"   ➤ DOCX limpiado: {output}")
    except Exception as e:
        print(f"   ⚠️ Error limpiando DOCX: {e}")

def clean_with_exiftool(file_path):
    result = subprocess.run(["exiftool", "-overwrite_original", "-all=", file_path], capture_output=True)
    if result.returncode == 0:
        print("   ➤ Imagen limpiada con exiftool.")
    else:
        print(f"   ⚠️ Error con exiftool: {result.stderr.decode()}")

def clean_text_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        output = file_path.replace(".txt", "_cleaned.txt").replace(".sql", "_cleaned.sql")
        with open(output, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"   ➤ Texto limpiado: {output}")
    except Exception as e:
        print(f"   ⚠️ Error limpiando texto: {e}")

def clean_archive(file_path):
    temp_dir = file_path + "_extracted"
    try:
        shutil.unpack_archive(file_path, temp_dir)
        print(f"   ➤ Archivo descomprimido en: {temp_dir}")
        clean_metadata(temp_dir)  # Limpieza recursiva
    except Exception as e:
        print(f"   ⚠️ Error descomprimiendo {file_path}: {e}")