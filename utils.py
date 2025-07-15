import os
import mimetypes
import subprocess
from PyPDF2 import PdfReader
from docx import Document

SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.txt', '.sql', '.jpg', '.jpeg', '.png', '.zip', '.rar']

def get_supported_files(folder_path):
    matched_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                matched_files.append(os.path.join(root, file))
    return matched_files

def print_file_info(file_path):
    name = os.path.basename(file_path)
    size = os.path.getsize(file_path)
    mtype = mimetypes.guess_type(file_path)[0]
    print(f"📄 {name} - {round(size/1024, 2)} KB - Tipo: {mtype or 'Desconocido'}")

def show_metadata_details(file_path):
    ext = file_path.lower().split(".")[-1]

    print(f"\n📂 Metadatos de: {file_path}")

    try:
        if ext == "pdf":
            reader = PdfReader(file_path)
            meta = reader.metadata
            for key, value in meta.items():
                print(f"  • {key}: {value}")

        elif ext == "docx":
            doc = Document(file_path)
            props = doc.core_properties
            for attr in dir(props):
                if not attr.startswith("_") and not callable(getattr(props, attr)):
                    value = getattr(props, attr)
                    if value:
                        print(f"  • {attr}: {value}")

        elif ext in ["jpg", "jpeg", "png"]:
            result = subprocess.run(["exiftool", file_path], capture_output=True, text=True)
            print(result.stdout)

        else:
            print("  ⚠️ Formato no soportado para metadatos detallados.")

    except Exception as e:
        print(f"  ⚠️ Error extrayendo metadatos: {e}")