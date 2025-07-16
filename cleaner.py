import os
import shutil
import csv
import json
import zipfile
import tempfile
from datetime import datetime
from pathlib import Path
from utils import (
    extract_metadata,
    save_cleaned_file,
    is_supported_file,
    get_supported_files,
    get_mime_type,
    ensure_clean_dir,
    is_mac_junk_file
)
from docx import Document
from PyPDF2 import PdfReader, PdfWriter
import openpyxl


def review_metadata(path):
    files = get_supported_files(path)
    if not files:
        print("⚠️ No se encontraron archivos compatibles.")
        return

    print(f"\n🧾 Archivos encontrados: {len(files)}")
    for f in files:
        print(f"📄 {os.path.basename(f)} - {os.path.getsize(f) / 1024:.2f} KB - Tipo: {get_mime_type(f)}")
        metadata = extract_metadata(f)
        if metadata:
            print(f"\n📂 Metadatos de: {f}")
            for k, v in metadata.items():
                print(f"  • {k}: {v}")
        else:
            print(f"  ⚠️ No se pudieron extraer metadatos de: {f}")


def clean_metadata(file_path):
    ext = Path(file_path).suffix.lower()
    try:
        if ext == ".pdf":
            clean_pdf(file_path)
        elif ext == ".docx":
            clean_docx(file_path)
        elif ext == ".xlsx":
            clean_xlsx(file_path)
        elif ext == ".json":
            clean_json(file_path)
        elif ext == ".csv":
            clean_csv(file_path)
        elif ext == ".txt":
            clean_txt(file_path)
        elif ext == ".zip":
            clean_zip(file_path)
        elif ext == ".xml":
            clean_xml(file_path)
        else:
            print(f"   ⚠️ Tipo de archivo no soportado: {file_path}")
    except Exception as e:
        print(f"   ⚠️ Error limpiando {os.path.basename(file_path)}: {e}")


def clean_pdf(path):
    reader = PdfReader(path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata({})
    cleaned_path = ensure_clean_dir(path)
    with open(cleaned_path, "wb") as f:
        writer.write(f)
    print(f"   ✅ PDF limpio: {cleaned_path}")


def clean_docx(path):
    doc = Document(path)
    props = doc.core_properties
    props.author = ""
    props.last_modified_by = ""
    props.comments = ""
    props.revision = "1"
    props.modified = datetime.now()
    props.created = datetime.now()
    cleaned_path = ensure_clean_dir(path)
    doc.save(cleaned_path)
    print(f"   ✅ DOCX limpio: {cleaned_path}")


def clean_xlsx(path):
    wb = openpyxl.load_workbook(path)
    if hasattr(wb, 'properties'):
        wb.properties.creator = ""
        wb.properties.lastModifiedBy = ""
    cleaned_path = ensure_clean_dir(path)
    wb.save(cleaned_path)
    print(f"   ✅ XLSX limpio: {cleaned_path}")


def clean_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    cleaned_path = ensure_clean_dir(path)
    with open(cleaned_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"   ✅ JSON limpio: {cleaned_path}")


def clean_csv(path):
    cleaned_path = ensure_clean_dir(path)
    with open(path, "r") as infile, open(cleaned_path, "w") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            writer.writerow(row)
    print(f"   ✅ CSV limpio: {cleaned_path}")


def clean_txt(path):
    cleaned_path = ensure_clean_dir(path)
    with open(path, "r") as infile, open(cleaned_path, "w") as outfile:
        for line in infile:
            outfile.write(line)
    print(f"   ✅ TXT limpio: {cleaned_path}")


def clean_xml(path):
    cleaned_path = ensure_clean_dir(path)
    with open(path, "r", encoding="utf-8", errors="ignore") as infile:
        content = infile.read()
    with open(cleaned_path, "w", encoding="utf-8") as outfile:
        outfile.write(content)
    print(f"   ✅ XML limpio: {cleaned_path}")
    
def clean_zip(path):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_ref.extractall(temp_dir)

            # Borrar basura de macOS antes de procesar
            for root, dirs, files in os.walk(temp_dir, topdown=False):
                for name in files:
                    if is_mac_junk_file(name):
                        os.remove(os.path.join(root, name))
                for name in dirs:
                    full_path = os.path.join(root, name)
                    if is_mac_junk_file(name) or not os.listdir(full_path):
                        shutil.rmtree(full_path, ignore_errors=True)

            # Limpiar archivos internos
            all_files = get_supported_files(temp_dir)
            for f in all_files:
                print(f"\n🧽 Limpiando: {f}")
                clean_metadata(f)

            # Crear carpeta de salida
            cleaned_zip_path = Path(path).parent / "cleaned" / f"{Path(path).stem}_cleaned.zip"
            cleaned_zip_path.parent.mkdir(exist_ok=True, parents=True)
            shutil.make_archive(str(cleaned_zip_path).replace('.zip', ''), 'zip', temp_dir)
            print(f"   ✅ ZIP limpio: {cleaned_zip_path}")