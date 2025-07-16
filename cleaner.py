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
    ensure_clean_dir
)
from docx import Document
from PyPDF2 import PdfReader, PdfWriter
import openpyxl
from PIL import Image

def review_metadata(path):
    files = get_supported_files(path)
    if not files:
        print(" No se encontraron archivos compatibles.")
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

def clean_metadata(path):
    files = get_supported_files(path)
    if not files:
        print("⚠️ No se encontraron archivos compatibles.")
        return

    cleaned_dir = Path(path).parent / "cleaned"
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    for file_path in files:
        print(f"\n🧽 Limpiando: {file_path}")
        ext = Path(file_path).suffix.lower()
        try:
            if ext == ".pdf":
                clean_pdf(file_path, cleaned_dir)
            elif ext == ".docx":
                clean_docx(file_path, cleaned_dir)
            elif ext == ".xlsx":
                clean_xlsx(file_path, cleaned_dir)
            elif ext == ".json":
                clean_json(file_path, cleaned_dir)
            elif ext == ".csv":
                clean_csv(file_path, cleaned_dir)
            elif ext == ".txt":
                clean_txt(file_path, cleaned_dir)
            elif ext == ".zip":
                clean_zip(file_path, cleaned_dir)
            elif ext in [".jpg", ".jpeg", ".png"]:
                clean_image(file_path, cleaned_dir)
            else:
                print(f"   ⚠️ Tipo de archivo no soportado: {ext}")
        except Exception as e:
            print(f"   ⚠️ Error limpiando {Path(file_path).name}: {e}")

def clean_pdf(path, out_dir):
    reader = PdfReader(path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata({})
    output = out_dir / f"{Path(path).stem}_cleaned.pdf"
    with open(output, "wb") as f:
        writer.write(f)
    print(f"   ✅ PDF limpio: {output}")

def clean_docx(path, out_dir):
    doc = Document(path)
    props = doc.core_properties
    props.author = ""
    props.last_modified_by = ""
    props.comments = ""
    try:
        props.revision = str(int(props.revision)) if props.revision and int(props.revision) > 0 else "1"
    except Exception:
        props.revision = "1"
    props.modified = datetime.now()
    props.created = datetime.now()
    output = out_dir / f"{Path(path).stem}_cleaned.docx"
    doc.save(output)
    print(f"   ✅ DOCX limpio: {output}")

def clean_xlsx(path, out_dir):
    wb = openpyxl.load_workbook(path)
    if hasattr(wb, 'properties'):
        wb.properties.creator = ""
        wb.properties.lastModifiedBy = ""
    output = out_dir / f"{Path(path).stem}_cleaned.xlsx"
    wb.save(output)
    print(f"   ✅ XLSX limpio: {output}")

def clean_json(path, out_dir):
    with open(path, "r") as f:
        data = json.load(f)
    output = out_dir / f"{Path(path).stem}_cleaned.json"
    with open(output, "w") as f:
        json.dump(data, f, indent=2)
    print(f"   ✅ JSON limpio: {output}")

def clean_csv(path, out_dir):
    output = out_dir / f"{Path(path).stem}_cleaned.csv"
    with open(path, "r", encoding='utf-8', errors='ignore') as infile, open(output, "w", encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            writer.writerow(row)
    print(f"   ✅ CSV limpio: {output}")

def clean_txt(path, out_dir):
    output = out_dir / f"{Path(path).stem}_cleaned.txt"
    with open(path, "r", encoding='utf-8', errors='ignore') as infile, open(output, "w", encoding='utf-8') as outfile:
        for line in infile:
            outfile.write(line)
    print(f"   ✅ TXT limpio: {output}")

def clean_zip(path, out_dir):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_ref.extractall(temp_dir)
            clean_metadata(temp_dir)
            output = out_dir / f"{Path(path).stem}_cleaned.zip"
            shutil.make_archive(str(output).replace(".zip", ""), 'zip', temp_dir)
            print(f"   ✅ ZIP reempaquetado limpio: {output}")

def clean_image(path, out_dir):
    img = Image.open(path)
    output = out_dir / f"{Path(path).stem}_cleaned{Path(path).suffix}"
    img.save(output)
    print(f"   ✅ Imagen limpia: {output}")
