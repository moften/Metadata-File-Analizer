import os
import mimetypes
import subprocess
import csv
from PyPDF2 import PdfReader
from docx import Document
from openpyxl import load_workbook

SUPPORTED_EXTENSIONS = [
    '.pdf', '.docx', '.txt', '.sql', '.jpg', '.jpeg', '.png',
    '.zip', '.rar', '.csv', '.xlsx'
]

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

        elif ext in ["txt", "sql"]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                print("  • Líneas:", len(content.splitlines()))
                if "password" in content.lower():
                    print("  ⚠️ Posible referencia a 'password' detectada.")
                if "secret" in content.lower():
                    print("  ⚠️ Posible palabra clave 'secret' encontrada.")
                if "token" in content.lower():
                    print("  ⚠️ Se detectó la palabra 'token'.")

        elif ext == "csv":
            with open(file_path, newline='', encoding="utf-8", errors="ignore") as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader, [])
                print("  • Cabeceras:", ", ".join(headers))
                if any(h.lower() in ["password", "secret", "token", "email"] for h in headers):
                    print("  ⚠️ Cabecera sospechosa detectada.")
                row_count = sum(1 for _ in reader)
                print(f"  • Total de filas: {row_count}")

        elif ext == "xlsx":
            wb = load_workbook(file_path, read_only=True)
            props = wb.properties
            print("  • Autor:", props.creator)
            print("  • Título:", props.title)
            print("  • Empresa:", props.company)
            print("  • Última modificación:", props.modified)

        else:
            print("  ⚠️ Formato no soportado para metadatos detallados.")

    except Exception as e:
        print(f"  ⚠️ Error extrayendo metadatos: {e}")