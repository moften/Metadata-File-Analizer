# utils.py

import os
import mimetypes

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