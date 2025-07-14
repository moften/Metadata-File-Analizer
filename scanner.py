# scanner.py (versión CLI sin interfaz gráfica)

import os
import sys
from utils import get_supported_files, print_file_info

def select_path():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("Introduce la ruta del archivo o carpeta a procesar: ").strip()
    return path

def scan_metadata(path):
    if os.path.isfile(path):
        files = [path]
    elif os.path.isdir(path):
        files = get_supported_files(path)
    else:
        print("❌ Ruta inválida o archivo no encontrado.")
        return

    if not files:
        print("⚠️ No se encontraron archivos compatibles.")
        return

    print(f"\n🧾 Archivos encontrados: {len(files)}")
    for file in files:
        print_file_info(file)