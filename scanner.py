import os
from utils import (
    get_supported_files,
    extract_metadata,
    print_file_info,
    show_metadata_details
)

def scan_metadata(path, return_data=False):
    collected = []

    if os.path.isfile(path):
        files = [path] if get_supported_files([path]) else []
    else:
        files = get_supported_files([os.path.join(dp, f) for dp, dn, fn in os.walk(path) for f in fn])

    print(f"\n🧾 Archivos encontrados: {len(files)}")

    for file in files:
        print_file_info(file)
        metadata = extract_metadata(file)
        show_metadata_details(file, metadata)
        collected.append((file, metadata))

    if return_data:
        return collected
