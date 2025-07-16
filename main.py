# main.py

import os
import sys
import readline  # Para autocompletado
from banner import print_banner
from cleaner import review_metadata, clean_metadata

def is_valid_path(path):
    return os.path.exists(path)

def input_path():
    try:
        path = input("Introduce la ruta del archivo o carpeta a procesar: ").strip()
        # Quitar comillas y backslashes escapados
        path = path.replace("\\", "").strip("\"\'")
        return path
    except KeyboardInterrupt:
        print("\n👋 Cancelado por el usuario.")
        sys.exit(0)

def main():
    print_banner()

    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Revisar metadatos")
        print("2. Eliminar metadatos")
        print("3. Salir\n")

        opcion = input("Selecciona una opción (1/2/3): ").strip()

        if opcion == "3":
            print("👋 Saliendo...")
            break

        if opcion not in ["1", "2"]:
            print("❌ Opción inválida.")
            continue

        path = input_path()

        if not is_valid_path(path):
            print("❌ Ruta inválida.")
            continue

        if opcion == "1":
            review_metadata(path)
        elif opcion == "2":
            clean_metadata(path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        path = path.replace("\\", "").strip("\"\'")
        if os.path.exists(path):
            print_banner()
            print("\n🧠 Modo rápido activado desde CLI")
            review_metadata(path)
            clean_metadata(path)
        else:
            print("❌ Ruta inválida proporcionada por CLI.")
    else:
        main()
